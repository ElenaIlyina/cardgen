"""Мульти-агент через брокер: две очереди, две таски, петля регенерации.

generate_card (очередь card.generate):
    extract → generate → UPDATE jobs → отправить critique_card.

critique_card (очередь card.critique):
    critique → approve: финализировать; regenerate и attempts < 3:
    отправить generate_card с feedback; иначе rejected.

Celery-таски sync, а Agents SDK async → мост asyncio.run() в каждой таске.
Стейт между агентами живёт ТОЛЬКО в таблице jobs — не в памяти воркера.
"""
import asyncio

from app.core.db import connect
from app.core.logging import get_logger
from app.schemas import CardDraft, SupplierFacts
from app.services import jobs as jobs_repo
from app.services import steps
from app.workers.celery_app import celery_app

log = get_logger(__name__)

MAX_ATTEMPTS = 3


@celery_app.task(name="app.workers.tasks.generate_card", max_retries=2)
def generate_card(job_id: str, supplier_text: str, feedback: list[str] | None = None):
    conn = connect()
    try:
        # TODO(шаг 2): set_status extracting → asyncio.run(steps.extract(...))
        #   → set_status generating (bump_attempts=True) → asyncio.run(steps.generate(...))
        #   → set_status critiquing → send_task critique_card в очередь card.critique
        #   с kwargs: job_id, supplier_text, facts_json, draft_json (model_dump_json()).
        # TODO(шаг 3): feedback из критика передай в steps.generate.
        raise NotImplementedError("generate_card")
    except Exception as exc:
        jobs_repo.set_status(conn, job_id, "failed", error=repr(exc))
        log.error("generate_failed", job_id=job_id, error=repr(exc))
        raise


@celery_app.task(name="app.workers.tasks.critique_card", max_retries=2)
def critique_card(job_id: str, supplier_text: str, facts_json: str, draft_json: str):
    conn = connect()
    try:
        # TODO(шаг 3): распарси facts/draft (model_validate_json) →
        #   report = asyncio.run(steps.critique(facts, draft))
        #   approve → set_status approved c result=draft, return.
        #   Иначе: row = get_job; row["attempts"] < MAX_ATTEMPTS →
        #     set_status regenerating + send_task generate_card c feedback=report.issues;
        #     иначе set_status rejected c result=draft и error="critic not satisfied...".
        raise NotImplementedError("critique_card")
    except Exception as exc:
        jobs_repo.set_status(conn, job_id, "failed", error=repr(exc))
        log.error("critique_failed", job_id=job_id, error=repr(exc))
        raise
