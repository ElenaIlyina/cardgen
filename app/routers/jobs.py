"""Фоновый вариант: job в RabbitMQ → Celery-воркер (шаги 2-3 практики)."""
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from app.core.db import connect
from app.schemas import JobIn
from app.services import jobs as jobs_repo
from app.workers.celery_app import celery_app

router = APIRouter(tags=["jobs"])


@router.post("/jobs", status_code=202)
async def create_job(
    body: JobIn,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    # TODO(шаг 2): create_job(conn, {"supplier_text": ...}, idempotency_key) → job_id;
    #   celery_app.send_task("app.workers.tasks.generate_card",
    #       kwargs={"job_id": ..., "supplier_text": ...}, queue="card.generate");
    #   вернуть JSONResponse({"id": job_id, "status": "pending"}, status_code=202)
    raise NotImplementedError("create_job")


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    # TODO(шаг 2): jobs_repo.get_job(conn, job_id); нет → HTTPException(404)
    raise NotImplementedError("get_job")
