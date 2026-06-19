"""
llm.py — the provider seam.

Every model call in the engine goes through one of two primitives here:

- `parse`    — structured output. Returns a validated Pydantic object of
               the caller's `output_format` type (or None on dry_run).
- `generate` — free text. Returns the model's prose/JSON string (or None
               on dry_run).

Provider is chosen by the *model name*, not by a separate flag. A call
that passes `model="grok-4.3"` lands on xAI; `model="claude-opus-4-6"`
(or anything `claude-*`) lands on Anthropic. This keeps the existing
`model=` argument — already threaded through every public function — as
the single selector, so no new parameter has to be plumbed through the
~30 call sites. See `provider_for`.

`DEFAULT_MODEL` resolves once, at import, from `STORY_LLM_MODEL` (falling
back to Claude). The public functions use it as their signature default,
so `STORY_LLM_MODEL=grok-4.3 python …` flips the whole engine to Grok in
one place, while an explicit `model=` argument always wins over the env
(that's how the cross-check harness pins Claude *and* Grok in one run).

Why a seam at all, given everything was Claude-direct: the request shapes
genuinely differ. Anthropic uses `messages.parse`/`messages.create` with
`thinking` + `output_config={"effort": …}` and an ephemeral cache block on
the system prompt; xAI is OpenAI-compatible — `chat.completions.parse`
with `response_format=<PydanticModel>`, system prompt as a plain message,
automatic prompt caching. The per-provider bodies below own those
differences; callers stay shape-agnostic.

Adding Google / OpenAI later is a new `provider_for` prefix plus a
`_<provider>_parse` / `_<provider>_generate` pair — no caller changes.
"""

from __future__ import annotations

import os
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Provider routing
# ---------------------------------------------------------------------------

#: Global default model. Resolved once at import. `STORY_LLM_MODEL` lets an
#: operator point the whole engine at a different model/provider without
#: touching code; an explicit `model=` argument at a call site overrides it.
DEFAULT_MODEL = os.environ.get("STORY_LLM_MODEL") or "claude-opus-4-6"


def provider_for(model: str) -> str:
    """Map a model id to its provider by name prefix.

    `claude-*` (and any unrecognized id) → ``"anthropic"`` — the historical
    default, kept so a bare/unknown model never silently changes vendor.
    `grok-*` → ``"xai"``. `gpt-*`/`o1`/`o3`/`o4` and `gemini-*` are reserved
    for the OpenAI/Google backends (not yet wired — see `_unsupported`)."""
    m = (model or "").lower()
    if m.startswith("grok"):
        return "xai"
    if m.startswith(("gpt", "o1", "o3", "o4")):
        return "openai"
    if m.startswith("gemini"):
        return "google"
    return "anthropic"


# ---------------------------------------------------------------------------
# Lazy, cached SDK clients (one per provider per process)
# ---------------------------------------------------------------------------

_anthropic_client = None
_xai_client = None


def _get_anthropic(client):
    """Honor a caller-supplied Anthropic client (tests inject fakes); else
    build and cache a real one. Import is lazy so the offline spine — gap
    rules, schema builders, encodings — never needs the SDK installed."""
    if client is not None:
        return client
    global _anthropic_client
    if _anthropic_client is None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "Anthropic models require the anthropic SDK. Install via "
                "`pip install -r prototype/requirements.txt`."
            ) from exc
        _anthropic_client = anthropic.Anthropic()
    return _anthropic_client


def _get_xai(client):
    """xAI is OpenAI-wire-compatible, so we drive it with the `openai` SDK
    pointed at `api.x.ai`. Honor a caller-supplied OpenAI-style client (duck:
    has `.chat`); else build and cache one from `XAI_API_KEY`."""
    if client is not None and hasattr(client, "chat"):
        return client
    global _xai_client
    if _xai_client is None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "xAI/Grok models require the openai SDK (xAI is OpenAI-wire-"
                "compatible). Install via `pip install -r prototype/"
                "requirements.txt`."
            ) from exc
        key = os.environ.get("XAI_API_KEY")
        if not key:
            raise RuntimeError(
                "XAI_API_KEY is not set — required to call Grok models."
            )
        _xai_client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")
    return _xai_client


def _unsupported(provider: str, model: str):
    raise NotImplementedError(
        f"Provider {provider!r} (model {model!r}) is reserved but not yet "
        f"wired. Supported today: Anthropic (claude-*) and xAI (grok-*). "
        f"Add a _{provider}_parse / _{provider}_generate pair in llm.py."
    )


# ---------------------------------------------------------------------------
# Dry-run printing (shared, provider-agnostic)
# ---------------------------------------------------------------------------

def _print_dry_run(system_prompt: str, user_prompt: str) -> None:
    print("=" * 76)
    print("SYSTEM PROMPT")
    print("=" * 76)
    print(system_prompt)
    print()
    print("=" * 76)
    print("USER PROMPT")
    print("=" * 76)
    print(user_prompt)


# ---------------------------------------------------------------------------
# Public primitives
# ---------------------------------------------------------------------------

def parse(
    *,
    system_prompt: str,
    user_prompt: str,
    output_format: Any,
    model: str,
    max_tokens: int,
    effort: str,
    dry_run: bool = False,
    client: Optional[Any] = None,
) -> Optional[Any]:
    """Structured-output call. Returns a validated instance of
    `output_format` (a Pydantic model), or None on dry_run. Routes to the
    provider named by `model`."""
    if dry_run:
        _print_dry_run(system_prompt, user_prompt)
        return None
    provider = provider_for(model)
    if provider == "anthropic":
        return _anthropic_parse(
            system_prompt, user_prompt, output_format,
            model, max_tokens, effort, client,
        )
    if provider == "xai":
        return _xai_parse(
            system_prompt, user_prompt, output_format,
            model, max_tokens, effort, client,
        )
    _unsupported(provider, model)


def generate(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    max_tokens: int,
    effort: str,
    dry_run: bool = False,
    client: Optional[Any] = None,
) -> Optional[str]:
    """Free-text call. Returns the model's text output (stripped), or None
    on dry_run. Routes to the provider named by `model`."""
    if dry_run:
        _print_dry_run(system_prompt, user_prompt)
        return None
    provider = provider_for(model)
    if provider == "anthropic":
        return _anthropic_generate(
            system_prompt, user_prompt, model, max_tokens, effort, client,
        )
    if provider == "xai":
        return _xai_generate(
            system_prompt, user_prompt, model, max_tokens, effort, client,
        )
    _unsupported(provider, model)


# ---------------------------------------------------------------------------
# Anthropic backend — the original call shapes, unchanged
# ---------------------------------------------------------------------------

def _anthropic_parse(system_prompt, user_prompt, output_format,
                     model, max_tokens, effort, client):
    client = _get_anthropic(client)
    response = client.messages.parse(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
        output_format=output_format,
    )
    return response.parsed_output


def _anthropic_generate(system_prompt, user_prompt,
                        model, max_tokens, effort, client):
    client = _get_anthropic(client)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
    )
    out = []
    for block in getattr(response, "content", []) or []:
        if getattr(block, "type", None) == "text":
            out.append(block.text)
    return "".join(out).strip()


# ---------------------------------------------------------------------------
# xAI / Grok backend — OpenAI-wire-compatible
# ---------------------------------------------------------------------------
#
# Differences from Anthropic that the wire forces here:
#   * system prompt is an ordinary {"role":"system"} message, not a
#     top-level cache-controlled block (xAI caches the prefix automatically);
#   * structured output is `response_format=<PydanticModel>` on
#     `chat.completions.parse`, returning `.choices[0].message.parsed`;
#   * the effort knob is `reasoning_effort` (low/medium/high), NOT
#     Anthropic's `output_config={"effort": …}`. See `_xai_reasoning_effort`.

#: Engine effort levels → xAI `reasoning_effort`. xAI has no "max" tier, so
#: it clamps to "high" (the most thinking xAI exposes). Anything unmapped
#: yields None and the param is simply omitted (model uses its own default).
_XAI_EFFORT = {"low": "low", "medium": "medium", "high": "high", "max": "high"}

#: Models observed at runtime to reject `reasoning_effort` (e.g. the
#: grok-4.20-*-reasoning / -non-reasoning slugs 400 on it). Populated lazily
#: on the first rejection so the no-effort retry happens at most once per
#: model per process — thereafter we skip the param up front.
_xai_no_effort: set = set()


def _xai_messages(system_prompt, user_prompt):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _xai_reasoning_effort(model: str, effort: str):
    """The `reasoning_effort` value to send for this (model, effort), or None
    to omit it — None when the level is unmapped or the model is known to
    reject the parameter."""
    if model in _xai_no_effort:
        return None
    return _XAI_EFFORT.get((effort or "").lower())


def _is_unsupported_effort_error(exc) -> bool:
    """True if `exc` is xAI's 'model does not support parameter
    reasoningEffort' 400 — matched on text so we needn't import the SDK's
    exception type (and it survives minor wording changes)."""
    s = str(exc).lower()
    return "reasoningeffort" in s or "reasoning_effort" in s or (
        "does not support parameter" in s and "reasoning" in s
    )


def _xai_invoke(method, *, model, effort, **base_kwargs):
    """Call `method` (a chat.completions .parse/.create), forwarding
    `reasoning_effort` when this model accepts it. If the model rejects the
    parameter, remember that and retry once without it — so an effort-less
    model degrades to its default thinking instead of erroring."""
    eff = _xai_reasoning_effort(model, effort)
    kwargs = dict(base_kwargs, model=model)
    if eff:
        kwargs["reasoning_effort"] = eff
    try:
        return method(**kwargs)
    except Exception as exc:  # noqa: BLE001 - narrowed by the guard below
        if eff and _is_unsupported_effort_error(exc):
            _xai_no_effort.add(model)
            kwargs.pop("reasoning_effort", None)
            return method(**kwargs)
        raise


def _xai_parse(system_prompt, user_prompt, output_format,
               model, max_tokens, effort, client):
    client = _get_xai(client)
    completion = _xai_invoke(
        client.chat.completions.parse,
        model=model, effort=effort, max_tokens=max_tokens,
        messages=_xai_messages(system_prompt, user_prompt),
        response_format=output_format,
    )
    return completion.choices[0].message.parsed


def _xai_generate(system_prompt, user_prompt,
                  model, max_tokens, effort, client):
    client = _get_xai(client)
    completion = _xai_invoke(
        client.chat.completions.create,
        model=model, effort=effort, max_tokens=max_tokens,
        messages=_xai_messages(system_prompt, user_prompt),
    )
    content = completion.choices[0].message.content or ""
    return content.strip()
