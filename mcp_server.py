from __future__ import annotations

from pathlib import Path

from mcp.server import MCPServer

from rag_workshop.tickets import create_ticket_draft

PROJECT_ROOT = Path(__file__).resolve().parent
mcp = MCPServer("AI Architecture Workshop")


@mcp.resource("workshop://documents/atlas-memo")
def atlas_memo() -> str:
    """Read the private Project Atlas launch memo."""
    return (PROJECT_ROOT / "data" / "sample" / "atlas_memo.txt").read_text(encoding="utf-8")


@mcp.resource("workshop://documents/sales-report")
def sales_report() -> str:
    """Read the latest sample quarterly sales report."""
    return (PROJECT_ROOT / "data" / "sample" / "sales_report.txt").read_text(encoding="utf-8")


@mcp.tool()
def prepare_ticket_draft(title: str, evidence: str, severity: str = "medium") -> dict[str, str]:
    """Prepare and save a local ticket draft. This does not contact Jira."""
    return create_ticket_draft(title=title, evidence=evidence, severity=severity, save=True)


if __name__ == "__main__":
    mcp.run()
