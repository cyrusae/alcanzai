"""
pytest configuration and shared fixtures.
"""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: marks tests requiring external services (GROBID, Claude API, arXiv network)",
    )
