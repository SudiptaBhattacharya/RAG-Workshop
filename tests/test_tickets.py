import pytest

from rag_workshop.tickets import create_ticket_draft


def test_ticket_is_a_draft_requiring_approval() -> None:
    draft = create_ticket_draft("Review shortfall", "Target exceeded actual", "medium")
    assert draft["status"] == "draft_requires_human_approval"


def test_ticket_rejects_unknown_severity() -> None:
    with pytest.raises(ValueError):
        create_ticket_draft("Review", "Evidence", "critical")
