import importlib.metadata
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import urlparse

import httpx
import pydantic_settings
import yaml
from fastmcp import FastMCP

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Sequence


class Settings(pydantic_settings.BaseSettings):
    api_key: str
    openapi_timeout_seconds: float = 3.0
    http_timeout_seconds: float = 45.0


def server_namespace_from_spec(spec: dict[str, Any]) -> str:
    url: str = spec["servers"][0]["url"]
    return urlparse(url).path.strip("/")


def _load_openapi_spec(
    url: str,
    client: httpx.Client,
) -> dict[str, Any]:
    response = client.get(url)
    response.raise_for_status()
    return cast("dict[str, Any]", yaml.safe_load(response.text))


def load_openapi_specs(
    urls: "Sequence[str]",
    timeout: float,
) -> list[dict[str, Any]]:
    with httpx.Client(timeout=timeout) as client:
        return [_load_openapi_spec(url, client) for url in urls]


@asynccontextmanager
async def lifespan(_app: FastMCP[Any]) -> "AsyncGenerator[None]":
    try:
        yield
    finally:
        await transport.aclose()


__version__ = importlib.metadata.version(__package__)
OPENAPI_SPEC_URLS = (
    "https://developer.axcient.com/specs/x360Recover.yaml",
    "https://developer.axcient.com/specs/x360Cloud.yaml",
    "https://developer.axcient.com/specs/x360Sync.yaml",
    "https://developer.axcient.com/specs/Billing.yaml",
)
settings = Settings()
spec_dict = {
    server_namespace_from_spec(spec): spec
    for spec in load_openapi_specs(
        OPENAPI_SPEC_URLS,
        settings.openapi_timeout_seconds,
    )
}
transport = httpx.AsyncHTTPTransport(
    verify=True,
    trust_env=True,
    http1=False,
    http2=True,
)
mcp: FastMCP[Any] = FastMCP("Axcient Public APIs", lifespan=lifespan)
for namespace, spec in spec_dict.items():
    child = FastMCP.from_openapi(
        openapi_spec=spec,
        client=httpx.AsyncClient(
            base_url=spec["servers"][0]["url"],
            headers={
                "X-Api-Key": settings.api_key,
                "User-Agent": f"public-gateway-mcp/{__version__}",
            },
            timeout=settings.http_timeout_seconds,
            transport=transport,
        ),
        name=namespace,
        mcp_names={
            "get_device_vault_restore_point_by_asio_endpoint_id_org_level": "get_device_vault_restort_point_by_asio"
        },
    )
    mcp.mount(child, namespace=namespace)


def main() -> int:
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
