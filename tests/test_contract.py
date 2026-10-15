"""Every operation is exercised against an HTTP mock, in both client modes."""
from __future__ import annotations

import asyncio
import inspect
import json
import re
from pathlib import Path
from typing import get_type_hints

import httpx
import pytest

from reclaimerforge import AsyncReclaimerForgeClient, ReclaimerForgeClient, RetryConfig, ValidationError, models

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "docs/openapi.json").read_text())
OPERATIONS = json.loads((ROOT / "docs/operations.json").read_text())
NO_RETRY = RetryConfig(max_retries=0)


def sample(schema: dict):
    if "$ref" in schema:
        return sample(SPEC["components"]["schemas"][schema["$ref"].rsplit("/", 1)[1]])
    if "default" in schema:
        return schema["default"]
    if "enum" in schema:
        return schema["enum"][0]
    if "const" in schema:
        return schema["const"]
    if "anyOf" in schema:
        return sample(schema["anyOf"][0])
    kind = schema.get("type")
    if kind == "object":
        return {k: sample(v) for k, v in schema.get("properties", {}).items()}
    if kind == "array":
        return [sample(schema["items"])]
    if kind == "integer":
        return schema.get("minimum", 1)
    if kind == "number":
        return 1.5
    if kind == "boolean":
        return True
    if kind == "null":
        return None
    if schema.get("format") == "date-time":
        return "2026-10-15T12:00:00+01:00"
    return "value"


def case(operation: dict):
    definition = SPEC["paths"][operation["path"]][operation["verb"].lower()]
    kwargs, paths, queries, headers = {}, {}, {}, {}
    for param in definition.get("parameters", []):
        value = sample(param["schema"])
        # Exercise repetition even when a schema has default=[] (tags).
        if param["schema"].get("type") == "array":
            value = ["slayer", "big-team"]
        key = param["name"].replace("-", "_")
        kwargs[key] = value
        {"path": paths, "query": queries, "header": headers}[param["in"]][param["name"]] = value
    body = None
    contents = definition.get("requestBody", {}).get("content", {})
    if contents:
        media, contents_schema = next(iter(contents.items()))
        if contents_schema["schema"].get("format") == "binary":
            kwargs["content"] = b"\x00\xffbinary\r\n"
            body = kwargs["content"]
            kwargs["content_type"] = media
            headers["content-type"] = media
        else:
            kwargs["body"] = body = sample(contents_schema["schema"])
    status = next((int(s) for s in definition["responses"] if s.startswith("2")), 200)
    response_schema = definition["responses"].get(str(status), {}).get("content", {}).get("application/json", {}).get("schema", {})
    expected = None if status == 204 else b"\x00\xffdownload" if operation["kind"] in {"bytes", "redirect"} else "documentation" if operation["kind"] == "text" else sample(response_schema)
    return kwargs, paths, queries, headers, body, status, expected


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("operation", OPERATIONS, ids=lambda o: o["group"] + "." + o["method"])
def test_every_operation_serializes_and_preserves_response(operation, asynchronous):
    kwargs, paths, queries, headers, body, status, expected = case(operation)
    called = []
    def handler(request):
        called.append(request)
        assert request.method == operation["verb"]
        assert request.url.path == operation["path"].format(**paths)
        assert request.headers["authorization"] == "Bearer test-credential"
        for name, value in queries.items():
            if value is None:
                assert name not in request.url.params
            else:
                values = value if isinstance(value, list) else [value]
                assert request.url.params.get_list(name) == [str(v).lower() if isinstance(v, bool) else str(v) for v in values]
        for name, value in headers.items():
            assert request.headers[name] == value
        if isinstance(body, bytes):
            assert request.content == body
            assert int(request.headers["content-length"]) == len(body)
        elif body is not None:
            assert json.loads(request.content) == body
        else:
            assert request.content == b""
        if status == 204:
            return httpx.Response(status)
        if isinstance(expected, (str, bytes)):
            return httpx.Response(status, content=expected)
        return httpx.Response(status, json=expected)
    if asynchronous:
        async def run():
            async with AsyncReclaimerForgeClient("https://forge.test", api_key="test-credential", retries=NO_RETRY, transport=httpx.MockTransport(handler)) as client:
                assert await getattr(getattr(client, operation["group"]), operation["method"])(**kwargs) == expected
            assert client.is_closed
        asyncio.run(run())
    else:
        with ReclaimerForgeClient("https://forge.test", api_key="test-credential", retries=NO_RETRY, transport=httpx.MockTransport(handler)) as client:
            assert getattr(getattr(client, operation["group"]), operation["method"])(**kwargs) == expected
        assert client.is_closed
    assert len(called) == 1


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("operation", OPERATIONS, ids=lambda o: o["group"] + "." + o["method"])
def test_every_operation_maps_validation_errors(operation, asynchronous):
    kwargs = case(operation)[0]
    detail = [{"loc": ["body", "title"], "msg": "invalid", "type": "value_error"}]
    transport = httpx.MockTransport(lambda request: httpx.Response(422, json={"detail": detail}, headers={"x-request-id": "request-1"}))
    if asynchronous:
        async def run():
            async with AsyncReclaimerForgeClient(transport=transport, retries=NO_RETRY) as client:
                with pytest.raises(ValidationError) as raised:
                    await getattr(getattr(client, operation["group"]), operation["method"])(**kwargs)
                assert raised.value.detail == detail
                assert raised.value.request_id == "request-1"
        asyncio.run(run())
    else:
        with ReclaimerForgeClient(transport=transport, retries=NO_RETRY) as client:
            with pytest.raises(ValidationError) as raised:
                getattr(getattr(client, operation["group"]), operation["method"])(**kwargs)
            assert raised.value.detail == detail
            assert raised.value.request_id == "request-1"


def test_no_missing_operations_parameters_schemas_or_docstrings():
    actual = {(o["path"], o["verb"].lower()) for o in OPERATIONS}
    documented = {(p, v) for p, operations in SPEC["paths"].items() for v in operations}
    assert actual == documented
    assert len(actual) == 105
    aliases = {"backend__app__schemas__files__ListingUpdateRequest": "LegacyFileUpdateRequest", "backend__app__schemas__listings__ListingUpdateRequest": "ListingUpdateRequest"}
    for name, schema in SPEC["components"]["schemas"].items():
        model = getattr(models, aliases.get(name, name))
        hints = get_type_hints(model, include_extras=True)
        assert hints.keys() == schema["properties"].keys()
    with ReclaimerForgeClient() as client:
        for operation in OPERATIONS:
            method = getattr(getattr(client, operation["group"]), operation["method"])
            sig = inspect.signature(method)
            definition = SPEC["paths"][operation["path"]][operation["verb"].lower()]
            assert all(p["name"].replace("-", "_") in sig.parameters for p in definition.get("parameters", []))
            assert "options" in sig.parameters
            assert "docs/partner-api.md" in method.__doc__
            get_type_hints(method)
    # All explicit current endpoint mentions in the complete partner contract.
    def normalize(path):
        return re.sub(r"\{[^}]+\}", "{}", path)
    paths = {normalize(p) for p in SPEC["paths"]}
    for verb, path in re.findall(r"\b(GET|POST|PUT|PATCH|DELETE) (/[^`\s?]+)", (ROOT / "docs/partner-api.md").read_text()):
        assert normalize(path.rstrip(".,")) in paths, (verb, path)
