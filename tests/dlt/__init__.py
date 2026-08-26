"""Sister-repo dlt smoke test package (per the cianchosaint init change V.10).

The cianchosaint dlt smoke test mirrors `cianfhoghlaim/tests/dlt/test_imports.py`
and walks every `dlt_sources/<subtree>` via `importlib.import_module` to
verify the standalone bulk-copy imports resolve cleanly.

The 6 cascade contracts (per parent change §15-§19) wire into this smoke
test once the GitHub repo exists.
"""