from __future__ import annotations

import asyncio

from mcp import Client

from mcp_server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        resources = await client.list_resources()
        print("Resources:")
        for resource in resources.resources:
            print(f"- {resource.uri}")

        result = await client.call_tool(
            "prepare_ticket_draft",
            {
                "title": "Review quarterly revenue shortfall",
                "evidence": "Target AUD 1,200,000; actual AUD 1,050,000; shortfall AUD 150,000.",
                "severity": "medium",
            },
        )
        print("\nTool result:")
        print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
