"""
Token estimation and text truncation utilities.

Uses tiktoken (OpenAI's tokenizer) for fast local estimates.
~5-15% off from Anthropic's tokenizer — accurate enough for truncation,
not for billing. Actual billed counts come from response.usage after API call.

Usage:
    from paper_library.token_utils import estimate_tokens, truncate_to_token_budget
    tokens = estimate_tokens(text)
    truncated, n_tokens, was_truncated = truncate_to_token_budget(text, max_tokens=150_000)
"""

import tiktoken
import logging
import structlog
from typing import Optional, Tuple

# Module-level logger (simple until telemetry is init'd)
logger = logging.getLogger(__name__)

# Global encoder cache
_ENCODER: Optional[tiktoken.Encoding] = None

def _get_encoder() -> tiktoken.Encoding:
    """Get or create the tiktoken encoder for gpt-4."""
    global _ENCODER
    if _ENCODER is None:
        try:
            _ENCODER = tiktoken.encoding_for_model("gpt-4")
        except Exception as e:
            logger.warning("Failed to initialize tiktoken encoder: %s. Using fallback.", e)
            # Re-raise if we can't even get a basic encoding
            _ENCODER = tiktoken.get_encoding("cl100k_base")
    return _ENCODER

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a string using tiktoken.
    Fallback: len(text) // 4 if tiktoken fails.
    """
    if not text:
        return 0
    
    try:
        enc = _get_encoder()
        return len(enc.encode(text))
    except Exception as e:
        logger.warning("Token estimation failed: %s. Falling back to char-based estimate.", e)
        return len(text) // 4

def _truncate_at_boundary(text: str, max_chars: int) -> str:
    """
    Cuts at paragraph break (\n\n) → sentence end (. ! ?) → word boundary (space) → hard cut.
    Look back up to 500 chars from cutoff.
    """
    if len(text) <= max_chars:
        return text
    
    # Initial hard cut
    candidate = text[:max_chars]
    lookback_start = max(0, max_chars - 500)
    lookback_zone = candidate[lookback_start:]
    
    # 1. Paragraph break
    idx = lookback_zone.rfind("\n\n")
    if idx != -1:
        return candidate[:lookback_start + idx].strip()
    
    # 2. Sentence end
    for char in [". ", "! ", "? "]:
        idx = lookback_zone.rfind(char)
        if idx != -1:
            return candidate[:lookback_start + idx + 1].strip()
    
    # 3. Word boundary
    idx = lookback_zone.rfind(" ")
    if idx != -1:
        return candidate[:lookback_start + idx].strip()
    
    # 4. Hard cut
    return candidate.strip()

def truncate_to_token_budget(text: str, max_tokens: int = 150_000) -> Tuple[str, int, bool]:
    """
    Returns (truncated_text, estimated_tokens, was_truncated).
    If estimate <= max_tokens, return (text, estimate, False) unchanged.
    """
    if not text:
        return "", 0, False
    
    tokens = estimate_tokens(text)
    if tokens <= max_tokens:
        return text, tokens, False
    
    log = structlog.get_logger(__name__)
    
    log.info("text_truncation_needed", 
             estimated_tokens=tokens, 
             max_tokens=max_tokens, 
             text_chars=len(text))
    
    # Smart truncation: proportional char estimate (ratio * 0.95 conservative)
    ratio = max_tokens / tokens
    target_chars = int(len(text) * ratio * 0.95)
    
    truncated_text = _truncate_at_boundary(text, target_chars)
    new_tokens = estimate_tokens(truncated_text)
    
    # If still over budget, do one more conservative pass
    if new_tokens > max_tokens:
        ratio = max_tokens / new_tokens
        target_chars = int(len(truncated_text) * ratio * 0.95)
        truncated_text = _truncate_at_boundary(truncated_text, target_chars)
        new_tokens = estimate_tokens(truncated_text)
    
    log.info("text_truncated",
             original_tokens=tokens,
             truncated_tokens=new_tokens,
             original_chars=len(text),
             truncated_chars=len(truncated_text))
    
    return truncated_text, new_tokens, True
