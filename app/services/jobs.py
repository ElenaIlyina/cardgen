"""Repository-слой: таблица jobs в Postgres.

Единственный владелец SQL. Статусная машина:
pending → extracting → generating → critiquing → (regenerating) → approved | rejected | failed
"""
import json
import uuid
from datetime import UTC, datetime

import psycopg

from app.schemas import CardDraft


def _now() -> str:
    return datetime.now(UTC).isoformat()


def create_job(conn: psycopg.Connection, payload: dict, idempotency_key: str | None) -> str:
    """INSERT pending. При повторном idempotency_key возвращает существующий id."""
    # TODO(шаг 2): если idempotency_key задан — SELECT id FROM jobs
    #   WHERE idempotency_key = %s; нашли → верни существующий id.
    #   Иначе: сгенерируй uuid4().hex[:12] и INSERT (id, idempotency_key, payload).
    #   payload — json.dumps(...).
    raise NotImplementedError("create_job")


def set_status(
    conn: psycopg.Connection, job_id: str, status: str, *, result: CardDraft | None = None,
    error: str | None = None, bump_attempts: bool = False,
) -> None:
    # TODO(шаг 2): UPDATE jobs SET status, updated_at (и result/error/attempts, если заданы)
    #   WHERE id = %s. result → result.model_dump_json(). bump_attempts → attempts = attempts + 1.
    #   Собирай запрос динамически: sets-список + args-список.
    raise NotImplementedError("set_status")


def get_job(conn: psycopg.Connection, job_id: str) -> dict | None:
    # TODO(шаг 2): SELECT id, status, attempts, result, error FROM jobs WHERE id = %s.
    #   Нет строки → None. result может быть dict (psycopg3 JSONB!) —
    #   CardDraft.model_validate(row) для dict, model_validate_json(row) для строки.
    raise NotImplementedError("get_job")
