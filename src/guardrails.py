import re
from dataclasses import dataclass

# Match rm -rf with any target; \b after / fails at end-of-string.
_UNSAFE_SHELL = re.compile(r"\bformat\s+c:|rm\s+-rf\b", re.I)


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    message: str = ""


def check_input(text: str) -> GuardrailResult:
    cleaned = (text or "").strip()
    if not cleaned:
        return GuardrailResult(False, "Please enter a message.")
    if len(cleaned) > 8000:
        return GuardrailResult(False, "Message is too long.")
    lowered = cleaned.lower()
    if any(
        x in lowered
        for x in ("child sexual", "terrorist attack plan", "suicide method")
    ):
        return GuardrailResult(False, "I can't help with that request.")
    if _UNSAFE_SHELL.search(cleaned):
        return GuardrailResult(False, "That request looks unsafe.")
    return GuardrailResult(True)


def check_output(text: str) -> GuardrailResult:
    if not (text or "").strip():
        return GuardrailResult(False, "Empty response. Please try again.")
    return GuardrailResult(True, text.strip())
