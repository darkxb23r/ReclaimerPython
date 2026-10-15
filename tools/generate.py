"""Export the local Forge contract and generate typed clients; no network or DB access.

Run with Forge's backend virtualenv and --source PATH to refresh the snapshot.
Run without --source to regenerate from the committed snapshot with stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import keyword
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def export(source: Path) -> dict:
    sys.path.insert(0, str(source))
    from backend.app import config

    # Never load the source checkout's .env, start lifespan jobs, or connect to DB.
    settings = config.Settings(_env_file=None, database_url="sqlite://")
    config.get_settings = lambda: settings
    from fastapi import FastAPI
    from fastapi.routing import APIRoute
    from backend.app.routes.api.router import router as api
    from backend.app.routes.public.router import router as public
    from backend.app.functions.auth.api_key_scopes import catalog_key_required, document_api_key_security, required_api_scopes

    app = FastAPI(title="ReclaimerForge", docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(api)
    app.include_router(public)
    schema = app.openapi()
    document_api_key_security(schema)
    # FastAPI omits raw Request streams, manually read headers and docs routes.
    import inspect
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path = route.path
        code = inspect.getsource(route.endpoint)
        for method in route.methods:
            operation = schema["paths"].get(path, {}).get(method.lower())
            if operation is None:
                operation = {"operationId": route.name, "summary": route.name.replace("_", " ").title(), "tags": ["documentation"], "responses": {"200": {"description": "Documentation", "content": {"text/html" if path.endswith("docs") else "application/json": {"schema": {"type": "string"} if path.endswith("docs") else {"type": "object"}}}}}}
                schema["paths"].setdefault(path, {})[method.lower()] = operation
            operation["x-python-name"] = route.name
            operation["x-source"] = str(Path(inspect.getsourcefile(route.endpoint)).relative_to(source)) + ":" + str(inspect.getsourcelines(route.endpoint)[1])
            scopes = required_api_scopes(method, re.sub(r"\{[^}]+\}", "1", path))
            operation["x-api-scopes"] = list(scopes) if scopes is not None else None
            operation["x-key-required"] = catalog_key_required(method, re.sub(r"\{[^}]+\}", "1", path))
            if scopes is None:
                operation.pop("security", None)
            else:
                operation["security"] = [{"ReclaimerForgeKey": []}]
            if method in {"POST", "PUT", "PATCH"} and ("request.stream()" in code or "append_request_chunk(" in code) and "requestBody" not in operation:
                media = "image/jpeg" if any(s in code for s in ("declared_type", "AVATAR_MEDIA_TYPES", "THUMBNAIL_MEDIA_TYPES")) else "application/octet-stream"
                content = {media: {"schema": {"type": "string", "format": "binary"}}}
                if media.startswith("image/"):
                    content.update({m: {"schema": {"type": "string", "format": "binary"}} for m in ("image/png", "image/webp")})
                operation["requestBody"] = {"required": True, "content": content}
            for header in re.findall(r'request.headers.get\("([^"]+)"', code):
                if header == "content-length":  # httpx computes this from buffered bytes.
                    continue
                operation.setdefault("parameters", []).append({"name": header, "in": "header", "required": header == "content-type", "schema": {"type": "string"}})
            if path in {"/api/public/site-visit", "/api/public/listings/{listing_id}/view"}:
                operation.setdefault("parameters", []).extend({"name": header, "in": "header", "required": False, "schema": {"type": "string"}} for header in ("origin", "sec-fetch-site"))
            if route.response_class.__class__.__name__ != "DefaultPlaceholder":
                cls = getattr(route.response_class, "__name__", "")
                operation["x-response-kind"] = {"FileResponse": "bytes", "HTMLResponse": "text", "RedirectResponse": "redirect"}.get(cls, "json")
            if path == "/api/developer/guide":
                operation["x-response-kind"] = "text"
    schema["paths"]["/docs"] = json.loads(json.dumps(schema["paths"]["/api/docs"]))
    schema["paths"]["/docs"]["get"]["x-python-name"] = "swagger_ui_alias"
    # Manually validated JSON body has an inline schema absent from components.
    from backend.app.schemas.announcements import AnnouncementUpdateRequest
    schema["components"]["schemas"]["AnnouncementUpdateRequest"] = AnnouncementUpdateRequest.model_json_schema()
    schema["paths"]["/api/admin/announcement"]["put"]["requestBody"]["content"]["application/json"]["schema"] = {"$ref": "#/components/schemas/AnnouncementUpdateRequest"}
    files = sorted({source / "README.md", source / "AGENTS.md", source / "LICENSE", source / "plan.md", source / ".env.example", *source.glob("docs/*"), *source.glob("backend/app/**/*.py"), source / "frontend/src/features/developer/components/DeveloperDocs.vue"})
    provenance = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs/source-inventory.json").write_text(json.dumps(provenance, indent=2) + "\n")
    (ROOT / "docs/partner-api.md").write_text((source / "docs/partner-api.md").read_text())
    (ROOT / "docs/UPSTREAM-LICENSE.txt").write_text((source / "LICENSE").read_text())
    historical = re.findall(r"^(GET|POST|PUT|PATCH|DELETE)\s+(/api/v1/\S+)", (source / "docs/architecture-plan.md").read_text(), re.M)
    (ROOT / "docs/historical-proposals.json").write_text(json.dumps(historical, indent=2) + "\n")
    return schema


def identifier(name: str) -> str:
    name = {"backend__app__schemas__files__ListingUpdateRequest": "LegacyFileUpdateRequest", "backend__app__schemas__listings__ListingUpdateRequest": "ListingUpdateRequest"}.get(name, name)
    result = re.sub(r"\W", "_", name)
    return result + "_" if keyword.iskeyword(result) else result


def type_of(schema: dict) -> str:
    if "$ref" in schema:
        return "models." + identifier(schema["$ref"].split("/")[-1])
    for union in ("anyOf", "oneOf"):
        if union in schema:
            return " | ".join(dict.fromkeys(type_of(s) for s in schema[union]))
    if "enum" in schema:
        return "Literal[" + ", ".join(repr(v) for v in schema["enum"]) + "]"
    if "const" in schema:
        return f"Literal[{schema['const']!r}]"
    kind = schema.get("type")
    if kind == "array":
        return "list[" + type_of(schema.get("items", {})) + "]"
    if kind == "object":
        additional = schema.get("additionalProperties", {})
        return "dict[str, " + (type_of(additional) if isinstance(additional, dict) else "Any") + "]"
    return {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"}.get(kind, "Any")


def group_for(path: str, operation: dict) -> str:
    if path.startswith("/api/admin/"):
        return "admin_" + path.split("/")[3].replace("-", "_")
    tag = operation.get("tags", ["documentation"])[0]
    return {"public files": "downloads", "health": "health", "ratings": "ratings"}.get(tag, tag.replace(" ", "_"))


def generate(schema: dict) -> None:
    # Source export and reloaded, sorted JSON must produce byte-identical files.
    schema = json.loads(json.dumps(schema, sort_keys=True))
    package = ROOT / "src/reclaimerforge"
    package.mkdir(parents=True, exist_ok=True)
    models = ['"""Generated wire schemas. Strings retain their JSON date/URL representation."""', "from __future__ import annotations", "from typing import Any, Literal", "from typing_extensions import TypedDict, Required, NotRequired", ""]
    for name, spec in sorted(schema["components"]["schemas"].items()):
        schema_name = name
        name = identifier(name)
        if spec.get("type") != "object" or "properties" not in spec:
            models.append(f"{name} = {type_of(spec).replace('models.', '')}\n")
            continue
        models.extend([f"class {name}(TypedDict):", f'    """Wire contract: #/components/schemas/{schema_name}."""'])
        for field, field_schema in spec["properties"].items():
            wrapper = "Required" if field in spec.get("required", []) else "NotRequired"
            models.append(f"    {identifier(field)}: {wrapper}[{type_of(field_schema).replace('models.', '')}]")
        if not spec["properties"]:
            models.append("    pass")
        models.append("")
    (package / "models.py").write_text("\n".join(models) + "\n")
    groups: dict[str, list] = {}
    for path, operations in schema["paths"].items():
        for verb, operation in operations.items():
            if verb in HTTP_METHODS:
                groups.setdefault(group_for(path, operation), []).append((path, verb, operation))
    resources = ['"""Generated endpoint methods; regenerate with tools/generate.py."""', "from __future__ import annotations", "from typing import Any, Literal, TYPE_CHECKING, cast", "import httpx", "from . import models", "from ._types import UNSET, Unset, RequestOptions", "from ._encoding import endpoint_path", "if TYPE_CHECKING:", "    from .client import ReclaimerForgeClient, AsyncReclaimerForgeClient", ""]
    manifest = []
    for group, entries in sorted(groups.items()):
        class_name = "".join(s.title() for s in group.split("_"))
        for asynchronous in (False, True):
            cls = ("Async" if asynchronous else "") + class_name
            client = ("Async" if asynchronous else "") + "ReclaimerForgeClient"
            resources.extend([f"class {cls}:", f"    def __init__(self, client: {client}) -> None:", '        """Bind this resource to its owning client."""', "        self._client = client", ""])
            names = set()
            for path, verb, operation in entries:
                name = identifier(operation["x-python-name"])
                if name in names:
                    raise ValueError(f"Duplicate method {group}.{name}")
                names.add(name)
                parameters = operation.get("parameters", [])
                signature = []
                path_args, query_args, header_args = {}, {}, {}
                for param in parameters:
                    p_name = identifier(param["name"])
                    spec = param.get("schema", {})
                    typ = type_of(spec)
                    if param["in"] == "path":
                        signature.append(f"{p_name}: {typ}")
                        path_args[param["name"]] = p_name
                signature.append("*")
                for param in parameters:
                    if param["in"] == "path":
                        continue
                    p_name = identifier(param["name"].replace("-", "_"))
                    typ = type_of(param.get("schema", {}))
                    signature.append(f"{p_name}: {typ}" + ("" if param.get("required") else " | Unset = UNSET"))
                    (query_args if param["in"] == "query" else header_args)[param["name"]] = p_name
                content = operation.get("requestBody", {}).get("content", {})
                body = None
                if content:
                    media, body_schema = next(iter(content.items()))
                    raw = body_schema.get("schema", {}).get("format") == "binary"
                    body = "content" if raw else "body"
                    typ = "bytes" if raw else type_of(body_schema.get("schema", {}))
                    signature.append(f"{body}: {typ}" + ("" if operation["requestBody"].get("required") else " | Unset = UNSET"))
                    if raw and "content-type" not in header_args:
                        signature.append(f"content_type: str = {media!r}")
                        header_args["content-type"] = "content_type"
                signature.append("options: RequestOptions | None = None")
                kind = operation.get("x-response-kind", "json")
                response_schema = next((r.get("content", {}).get("application/json", {}).get("schema", {}) for status, r in operation["responses"].items() if status.startswith("2")), {})
                result = "bytes" if kind in {"bytes", "redirect"} else "str" if kind == "text" else "None" if "204" in operation["responses"] else type_of(response_schema)
                if path == "/api/openapi.json":
                    result = "dict[str, Any]"
                doc = [operation.get("summary", name) + ".", f"HTTP: {verb.upper()} {path}.", f"Source: {operation['x-source']}; docs/partner-api.md; docs/openapi.json.", "API key scopes: " + (", ".join(operation["x-api-scopes"]) if operation["x-api-scopes"] is not None else "unavailable; use cookie session or anonymous access as documented") + "."]
                if operation.get("description"):
                    doc.append(operation["description"].replace('"""', "'''"))
                for param in parameters:
                    doc.append(f"{param['name']}: " + json.dumps(param.get("schema", {}), sort_keys=True))
                resources.extend([f"    {'async ' if asynchronous else ''}def {name}(self, {', '.join(signature)}) -> {result}:", '        """' + "\n\n        ".join(doc) + '\n        """'])
                kwargs = [f"params={{{', '.join(repr(k)+': '+v for k,v in query_args.items())}}}", f"headers={{{', '.join(repr(k)+': '+v for k,v in header_args.items())}}}", "options=options", f"response_kind={kind!r}"]
                if body:
                    kwargs.append(f"{'content' if body == 'content' else 'json'}={body}")
                mapping = "{" + ", ".join(repr(k) + ": " + v for k, v in path_args.items()) + "}"
                call = f"{'await ' if asynchronous else ''}self._client._call({verb.upper()!r}, endpoint_path({path!r}, {mapping}), {', '.join(kwargs)})"
                resources.extend([f"        return cast({result!r}, {call})", ""])
                if not asynchronous:
                    manifest.append({"group": group, "method": name, "verb": verb.upper(), "path": path, "operation_id": operation["operationId"], "return_type": result, "kind": kind})
    (package / "resources.py").write_text("\n".join(resources) + "\n")
    bindings = ['"""Generated resource bindings for IDE autocomplete."""', 'from __future__ import annotations', 'from typing import cast', 'from . import resources', '']
    for prefix in ("", "Async"):
        bindings += [f'class {prefix}ResourceBindings:', '    def _bind_resources(self) -> None:']
        for group in sorted(groups):
            cls = prefix + "".join(s.title() for s in group.split("_"))
            bindings += [f'        self.{group}: resources.{cls} = resources.{cls}(cast("{prefix}ReclaimerForgeClient", self))']
        bindings += ['']
    bindings[2:2] = ['from typing import TYPE_CHECKING', 'if TYPE_CHECKING:', '    from .client import ReclaimerForgeClient, AsyncReclaimerForgeClient']
    (package / '_bindings.py').write_text('\n'.join(bindings) + '\n')
    (ROOT / "docs/operations.json").write_text(json.dumps(manifest, indent=2) + "\n")
    counts = Counter(m["group"] for m in manifest)
    report = ["# API surface and coverage", "", "The current supported contract is `partner-api.md`, the source README, and the", "FastAPI route/Pydantic schema definitions. `openapi.json` captures that contract", "plus raw streams, headers, documentation routes and response types omitted by", "FastAPI's automatic schema. All operations have concrete sync and async methods.", "", "## Authentication and invariants", "", "- Bearer API keys: catalog:read, assets:download, listings:write, files:upload, listings:publish, listings:delete. Keys never grant membership or staff privileges.", "- Cookie sessions (`reclaimerforge_session`): account, keys, votes, collaborations and staff APIs. Website aliases support anonymous reads. No OAuth contract exists.", "- Key default quota: 120 requests / 60 seconds. Respect Retry-After and X-RateLimit-*; database failures use 503 with Retry-After: 5.", "- IDs are opaque; private content requires accepted membership. Keep null distinct from empty lists. Manifest schema_version is 1; compatibility and published bytes are pinned.", "- PATCH listing metadata requires title and defaults can clear fields; version PATCH is partial. Raw images and chunks are not multipart forms.", "- Server errors carry detail (string or validation array). Errors include 400/401/403/404/409/410/413/415/422/429/503.", "", "## Historical proposals and documentation gaps", "", "`docs/architecture-plan.md` proposes `/api/v1` releases, reports, and uploads.", "Those routes are not implemented and have no complete request/response contracts.", "The current README and partner guide supersede them. They are recorded below", "and remain accessible through request() if a future server implements them;", "the SDK does not claim server support or invent schemas. Webhooks, hosting", "permissions, script uploads and host feedback are explicitly future work.", "", "The automatic schema omits stream bodies, x-filename, Content-Type, and hidden", "documentation routes; this snapshot supplements them from route definitions.", "Source hashes are in source-inventory.json. No .env, uploads, or secrets were read.", "", "## Operations", "", "| Resource | Operations |", "| --- | ---: |"]
    report += [f"| {g} | {n} |" for g, n in sorted(counts.items())]
    report += [f"| **Total** | **{len(manifest)}** |", "", "| Method | Path | Sync/async resource method | Return |", "| --- | --- | --- | --- |"]
    report += [f"| {m['verb']} | `{m['path']}` | `{m['group']}.{m['method']}` | `{m['return_type']}` |" for m in manifest]
    report += ["", "## Historical /api/v1 proposal (not available on current server)", "", "See original docs/architecture-plan.md, section 13: account registration,", "verification, login/logout/password resets/me; listing list/create/detail/edit;", "listing release list/create; release detail/edit/download; upload start/chunk/", "complete/status; listing rating and reports. These are superseded design sketches."]
    historical_path = ROOT / "docs/historical-proposals.json"
    if historical_path.exists():
        report += ["", "| Method | Proposed path |", "| --- | --- |"]
        report += [f"| {verb} | `{path}` |" for verb, path in json.loads(historical_path.read_text())]
    report += ["", "## Conflicts resolved against current schemas and routes", "", "The partner Markdown says script uploads are unsupported, but the current", "developer page, schemas, and validator support `megalo_source` (.rvt) and", "manifest format `megalo_rvt`. Both are included in the SDK. Discovery schemas", "also allow relevance, most_downloads, least_downloads, most_liked, least_liked,", "newest and oldest beyond the original eight sorts. Current code uses an", "anonymous browser identifier with an IP fallback for traffic deduplication,", "while parts of the prose still describe an IP-only rule. The SDK forwards", "cookies and headers and delegates these rules to the server."]
    (ROOT / "docs/API_SURFACE.md").write_text("\n".join(report) + "\n")
    print(json.dumps({"operations": len(manifest), "schemas": len(schema["components"]["schemas"]), "groups": dict(sorted(counts.items()))}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.source:
        contract = export(args.source.resolve())
        (ROOT / "docs/openapi.json").write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n")
    else:
        contract = json.loads((ROOT / "docs/openapi.json").read_text())
    generate(contract)
