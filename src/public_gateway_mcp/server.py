import pydantic_settings
from fastmcp import FastMCP


class Configs(pydantic_settings.BaseSettings):
    API_KEY: str


mcp = FastMCP("Axcient Public APIs")
configs = Configs()


def main() -> int:
    """Entry point for the direct execution server."""
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
