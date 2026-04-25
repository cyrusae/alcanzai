import pytest
from paper_library.token_utils import estimate_tokens, truncate_to_token_budget

def test_estimate_tokens_reasonable():
    # 1000 common English words should be ~1000-1500 tokens (tiktoken cl100k_base)
    text = 'the quick brown fox jumps over the lazy dog ' * 100  # 900 words roughly
    tokens = estimate_tokens(text)
    assert 500 < tokens < 2000

def test_estimate_tokens_empty():
    assert estimate_tokens('') == 0

def test_truncate_no_truncation_needed():
    text = 'hello world'
    result, n_tokens, was_truncated = truncate_to_token_budget(text, max_tokens=150_000)
    assert result == text
    assert was_truncated is False
    assert n_tokens > 0

def test_truncate_at_paragraph_boundary():
    # Build text that exceeds budget, verify truncation happens and result is shorter
    long_text = ('word ' * 100 + '\n\n') * 50  # ~5000 words with paragraph breaks
    result, n_tokens, was_truncated = truncate_to_token_budget(long_text, max_tokens=100)
    assert was_truncated is True
    assert len(result) < len(long_text)
    # Token count should be reasonably close to the budget (within 20%)
    assert n_tokens <= 120
    # Result should not contain only whitespace
    assert result.strip()

def test_truncate_empty_string():
    result, n_tokens, was_truncated = truncate_to_token_budget('', max_tokens=150_000)
    assert result == ''
    assert was_truncated is False
