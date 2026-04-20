"""
reader_model_client_base.py — shared infrastructure for the three
reader-model clients (substrate, dramatic, aristotelian).

Factored out per state-of-play-10 production-track item G after the
pattern was stable across three invocations. Same discipline as the
`conformance.py` extraction: narrow interface, zero behavior change,
each client imports what it needs and keeps its dialect-specific
helpers in place.

Three primitives:

- `DroppedOutput` — uniform drop-shape across all clients. Prior
  to the extraction, each client defined a near-identical version
  (same field names, near-identical docstring). Shared here with
  the union of the prior docstring content.
- `SYSTEM_PROMPT_OPENING` — the literal two-sentence opener shared
  across all three clients' SYSTEM_PROMPTs. Each client composes
  its own full prompt from this opener + dialect-specific body +
  closing directives.
- `invoke_parse_helper` — the claude-api `client.messages.parse`
  call shape the three clients repeat, together with the dry-run
  print block and client construction. Returns the raw parsed
  Pydantic output. Each client's `invoke_*_reader_model` function
  calls this and then applies its own classify/translate
  post-processing.

Not factored out (intentional):

- Record-to-dict helpers. Each dialect has different records.
- Pydantic output schemas. Each dialect has different content types.
- `build_user_prompt` functions. Each dialect has different section
  composition.
- `_classify_*` / `_translate_*` helpers. Per-content-type scope
  validation and translation are dialect-specific.
- Result dataclasses (`ReaderModelResult`, `DramaticReaderModel-
  Result`, `AristotelianReaderModelResult`). Each carries
  different fields.

The extracted surface is the API-boundary boilerplate plus the
shared DroppedOutput shape. Dialect semantics stay dialect-local.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

try:
    import anthropic
except ImportError as exc:
    raise ImportError(
        "The reader-model client base requires the anthropic SDK. "
        "Install dependencies via "
        "`pip install -r prototype/requirements.txt`."
    ) from exc


@dataclass(frozen=True)
class DroppedOutput:
    """A raw LLM output record that failed scope or structural
    validation at ingest or translation time. `reason` is a short
    human-readable explanation; `raw` is the Pydantic record so a
    reviewing author can see exactly what was dropped and why.

    R5 enforcement (reader-model-sketch-01). The prompt tells the
    LLM what's in scope, but the translation layer verifies in
    code. A review that targets a description / lowering / record
    id not shown, an out-of-scope (target_kind, field) pair, or a
    reference (observation id, verification-review synthetic id)
    that doesn't resolve lands here — never in the accepted
    translated lists.

    Same shape across all three reader-model clients. Previously
    each client defined its own near-identical class; sharing here
    keeps the translation contract consistent.
    """
    reason: str
    raw: object


# The shared opening of all three clients' SYSTEM_PROMPTs. The rest
# of each prompt is dialect-specific and stays in the respective
# client module. Do NOT append a trailing newline here — callers
# compose with their own formatting.
SYSTEM_PROMPT_OPENING = (
    "You are a reader-model — an interpretive peer to a structured "
    "story-telling engine. Your role is specified by "
    "reader-model-sketch-01 in the project's design/ directory."
)


def invoke_parse_helper(
    *,
    system_prompt: str,
    user_prompt: str,
    output_format: Any,
    model: str,
    max_tokens: int,
    effort: str,
    dry_run: bool,
    client: Optional["anthropic.Anthropic"] = None,
) -> Optional[Any]:
    """Execute the shared Anthropic `messages.parse` call. Handles:

    - Dry-run printing (prints system + user prompts; returns None).
    - Lazy client construction from env if `client is None`.
    - The `parse()` request shape each client shares:
      `thinking={"type": "adaptive"}`, effort-controlled output,
      cache-controlled system message (ephemeral), single-user-
      message composition, per-caller output_format.

    Returns the `response.parsed_output` (of whatever Pydantic type
    the caller's `output_format` names). On `dry_run=True`, returns
    `None` — the caller synthesizes an empty result of its own
    type. This keeps the helper free of dialect-specific result
    shapes.

    The `parse()` API does not accept top-level `cache_control`.
    The directive goes on the system block to cache the frozen
    system prompt across calls per the claude-api skill's silent-
    invalidator audit.
    """
    if dry_run:
        print("=" * 76)
        print("SYSTEM PROMPT")
        print("=" * 76)
        print(system_prompt)
        print()
        print("=" * 76)
        print("USER PROMPT")
        print("=" * 76)
        print(user_prompt)
        return None

    if client is None:
        client = anthropic.Anthropic()

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
