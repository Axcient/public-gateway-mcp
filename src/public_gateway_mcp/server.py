from mcp.server.fastmcp import FastMCP
import httpx
import pydantic_settings
import datetime
from typing import Any


class Configs(pydantic_settings.BaseSettings):
    API_KEY: str

mcp = FastMCP("Axcient Public APIs")
configs = Configs()

@mcp.tool()
async def get_billable_usage(start_date: datetime.date | None = None, end_date: datetime.date | None = None) -> dict[str, Any]:
    """
    Get billable usage report for specified date range
    If not provided, it'll return current month's usage data
    It returns list of client usage in the children field
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://axapi.axcient.com/billing/usage/billable", params={"start_date": start_date, "end_date": end_date}, headers={"X-Api-Key": configs.API_KEY})
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_client_info(client_id: int) -> dict[str, Any]:
    """
    Get billable usage report for specified date range
    If not provided, it'll return current month's usage data
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://axapi.axcient.com/x360recover/client/{client_id}", headers={"X-Api-Key": configs.API_KEY})
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def add(a: int, b: int = 1) -> int:
    """Add two numbers Axcient way"""
    return (a + b)**2

def main() -> int:
    """Entry point for the direct execution server."""
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
