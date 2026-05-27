import re


INJECTION_PATTERNS = (
	"ignore previous instructions",
	"you are now",
	"system:",
	"assistant:",
)

ABUSE_PATTERNS = (
	"fuck",
	"shit",
	"bitch",
	"idiot",
	"kill yourself",
)


def limit_description(description: str, max_length: int = 500) -> str:
	return (description or "")[:max_length].strip()


def sanitize_description(description: str) -> str:
	text = limit_description(description)
	lowered = text.lower()

	for pattern in INJECTION_PATTERNS:
		lowered = lowered.replace(pattern, " ")

	cleaned = re.sub(r"\s+", " ", lowered).strip()
	return cleaned[:500]


def looks_abusive_or_gibberish(description: str) -> bool:
	text = (description or "").lower().strip()
	if not text:
		return True

	if any(pattern in text for pattern in ABUSE_PATTERNS):
		return True

	alpha_chars = sum(1 for char in text if char.isalpha())
	total_chars = len(text)
	if total_chars == 0:
		return True

	alpha_ratio = alpha_chars / total_chars
	repeated_noise = re.search(r"(.)\1{6,}", text) is not None
	too_many_symbols = sum(1 for char in text if not char.isalnum() and not char.isspace()) > max(12, total_chars // 3)

	return alpha_ratio < 0.25 or repeated_noise or too_many_symbols
