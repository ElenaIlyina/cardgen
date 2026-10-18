"""LLM-клиент как слой: обёртка над OpenAI Agents SDK с таймаутом и ретраями.

Единственное место в приложении, которое знает про LLM API:
retry-политика, таймаут, различие ошибок 429/5xx/4xx — всё здесь.
Сервисы вызывают run_agent() и не знают про провайдера.
"""
import asyncio
import random

from agents import Agent, Runner
from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI
from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)

_client_configured = False


def setup_llm() -> None:
    """Инициализация OpenAI-compatible клиента (LM Studio / OpenRouter / Z.ai).

    Вызывается один раз на процесс. Идемпотентна.
    Подсказка: см. Занятие 1, практика §2 — те же четыре вызова.
    """
    global _client_configured
    # TODO(шаг 1): создай AsyncOpenAI(base_url, api_key, timeout) и сконфигурируй SDK:
    #   set_default_openai_client(client)
    #   set_default_openai_api("chat_completions")   # LM Studio не знает Responses API
    #   set_tracing_disabled(True)                    # иначе 401 на не-OpenAI ключе
    #   _client_configured = True
    raise NotImplementedError("setup_llm")


def _retryable(exc: Exception) -> bool:
    """Ретраим только транспортные и серверные ошибки: 429, 5xx, таймаут, сеть.

    4xx (кроме 429) — ошибка запроса, повтор бессмыслен.
    """
    # TODO(шаг 1): isinstance-проверки:
    #   APIConnectionError, APITimeoutError -> True
    #   APIStatusError -> status_code == 429 или >= 500
    raise NotImplementedError("_retryable")


async def run_agent(agent: Agent, prompt: str):
    """Запустить агента с ретраями: экспоненциальная задержка + jitter.

    Ретраится только вызов LLM — не вся бизнес-задача (это работа очереди/workflow).
    """
    # TODO(шаг 1): цикл по attempt от 1 до settings.llm_max_retries:
    #   try: return (await asyncio.wait_for(Runner.run(agent, prompt),
    #              timeout=settings.llm_timeout_s)).final_output
    #   except Exception as exc:
    #     - последняя попытка или not _retryable(exc) -> raise
    #     - иначе: delay = min(2**attempt * 0.5, 8.0) * (1 + random.random() * 0.25),
    #       log.warning("llm_call_retry", ...), await asyncio.sleep(delay)
    raise NotImplementedError("run_agent")
