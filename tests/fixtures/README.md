# Test Fixtures

Place a PDF named `sample.pdf` here to enable GROBID integration tests.

Any real academic paper PDF works. Suggested: copy from `vault/PDFs/` after
running the pipeline once:

```bash
cp vault/PDFs/arxiv_1706.03762.pdf tests/fixtures/sample.pdf
```

Tests that need this file are marked `@pytest.mark.integration` and will
be skipped automatically if the file is absent.
