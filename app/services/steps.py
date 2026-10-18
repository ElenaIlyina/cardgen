"""Стадии пайплайна: extract → generate → critique.

Каждая функция — один агент-шаг. Один и тот же код работает в трёх runtime:
- FastAPI-эндпоинт (шаг 1 практики),
- Celery-воркер (шаги 2-3),
- Temporal activity (шаг 4).
Это и есть выигрыш слоистой архитектуры.
"""
from app.agents.prompts import critic_agent, extractor_agent, generator_agent
from app.core.logging import get_logger
from app.llm.client import run_agent
from app.schemas import CardDraft, CritiqueReport, SupplierFacts

log = get_logger(__name__)


async def extract(supplier_text: str) -> SupplierFacts:
    log.info("step_extract_start")
    # TODO(шаг 1): out = await run_agent(extractor_agent, supplier_text)
    #   если out уже SupplierFacts — верни; иначе SupplierFacts.model_validate_json(_ensure_json(out))
    raise NotImplementedError("extract")


async def generate(facts: SupplierFacts, feedback: list[str] | None = None) -> CardDraft:
    # TODO(шаг 1): собери prompt: "Факты о товаре:\n" + facts.model_dump_json(indent=2)
    #   + если feedback: "\n\nЗамечания критика, учти:\n" + "- {i}" построчно
    #   вызови generator_agent, приведи к CardDraft как в extract
    raise NotImplementedError("generate")


async def critique(facts: SupplierFacts, draft: CardDraft) -> CritiqueReport:
    # TODO(шаг 1): prompt = факты + "\n\nЧерновик карточки для проверки:\n" + черновик
    #   вызови critic_agent, приведи к CritiqueReport
    raise NotImplementedError("critique")


def _ensure_json(text) -> str:
    """Локальные модели иногда оборачивают JSON в ```json ... ``` — срезаем."""
    s = str(text).strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else s
        s = s.rsplit("```", 1)[0]
    return s.strip()


async def run_pipeline(supplier_text: str, max_attempts: int = 3):
    """Полный цикл: extract → (generate → critique → feedback)* → итог.

    Возвращает (итоговый черновик, число генераций, вердикт).
    """
    # TODO(шаг 1): extract один раз; затем цикл до max_attempts:
    #   generate (первый раз без feedback, дальше с issues критика) → critique;
    #   approve → verdict="approved", break; иначе feedback = report.issues
    #   и лог pipeline_regenerate. Если цикл кончился — verdict="rejected".
    raise NotImplementedError("run_pipeline")
