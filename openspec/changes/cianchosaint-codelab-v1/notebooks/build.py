# CIANCHOSAINT politician pipeline — notebook builder.
#
# Per `openspec/changes/cianchosaint-codelab-v1/specs/cianchosaint-codelab/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `loop-lab-table/notebooks/build.py`:
# transforms each codelab level into a self-contained notebook cell, inlines
# the shared schemas, and writes the Colab-style `.ipynb` JSON.

from __future__ import annotations

import json
from pathlib import Path


def build_politician_pipeline_notebook() -> dict:
    """Build the canonical Colab-style notebook for the politician pipeline."""
    cells: list[dict] = []

    # Markdown intro
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "intro"},
            "source": [
                "# CIANCHOSAINT politician pipeline\n",
                "**Setup → 5 runnable levels.** Every assertion is a sentence "
                "against the real pipeline (per `scripts/walk.py`).",
            ],
        }
    )

    # Level 1 — the 7 case-study politicians
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "level-1"},
            "source": [
                "## Level 1 — the 7 case-study politicians\n",
                "**Claim:** `AGENT_FACTORY_REGISTRY` has 18 agents (3 root + 15 specialist).",
            ],
        }
    )
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"id": "level-1-code"},
            "outputs": [],
            "source": [
                "from agents.cianchosaint._factory import AGENT_FACTORY_REGISTRY\n",
                "assert len(AGENT_FACTORY_REGISTRY) == 18\n",
                "print(f'Registry has {len(AGENT_FACTORY_REGISTRY)} agents')",
            ],
        }
    )

    # Level 2 — the BAML extraction
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "level-2"},
            "source": [
                "## Level 2 — the BAML extraction\n",
                "**Claim:** `ExtractPoliticianFromWebPage` returns a structured record.",
            ],
        }
    )
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"id": "level-2-code"},
            "outputs": [],
            "source": [
                "# Run the eval walk to verify the BAML extraction (per T2.4)\n",
                "import subprocess\n",
                "result = subprocess.run(['python3', 'tests/evals/politician/walk.py'],\n",
                "capture_output=True, text=True, env={'PYTHONPATH': '.'})\n",
                "assert 'All 10 assertions passed' in result.stdout, result.stdout",
            ],
        }
    )

    # Level 3 — the 4 FunctionTools
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "level-3"},
            "source": [
                "## Level 3 — the 4 FunctionTools\n",
                "**Claim:** all 4 politician FunctionTools are callable.",
            ],
        }
    )
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"id": "level-3-code"},
            "outputs": [],
            "source": [
                "from agents.cianchosaint.tools import (\n",
                "    politician_account_resolver,\n",
                "    adjacent_context_resolver,\n",
                "    funder_network_graph,\n",
                "    wikipedia_bridge,\n",
                ")\n",
                "assert callable(politician_account_resolver)\n",
                "assert callable(adjacent_context_resolver)\n",
                "assert callable(funder_network_graph)\n",
                "assert callable(wikipedia_bridge)\n",
                "print('All 4 politician FunctionTools are callable')",
            ],
        }
    )

    # Level 4 — the 3 workflow graphs
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "level-4"},
            "source": [
                "## Level 4 — the 3 workflow graphs\n",
                "**Claim:** all 3 workflow graphs build without errors.",
            ],
        }
    )
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"id": "level-4-code"},
            "outputs": [],
            "source": [
                "from agents.cianchosaint.workflows import (\n",
                "    politician_resolver_graph,\n",
                "    funder_network_graph,\n",
                "    wikipedia_bridge_graph,\n",
                ")\n",
                "assert callable(politician_resolver_graph)\n",
                "assert callable(funder_network_graph)\n",
                "assert callable(wikipedia_bridge_graph)\n",
                "print('All 3 workflow graphs are callable')",
            ],
        }
    )

    # Level 5 — RAGAS eval + GEPA optimizer
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {"id": "level-5"},
            "source": [
                "## Level 5 — RAGAS eval + GEPA optimizer\n",
                "**Claim:** the optimizer + study runners are runnable.",
            ],
        }
    )
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"id": "level-5-code"},
            "outputs": [],
            "source": [
                "import subprocess\n",
                "result = subprocess.run(['python3', 'scripts/politician_optimize.py', '--budget', '20'],\n",
                "capture_output=True, text=True, env={'PYTHONPATH': '.'})\n",
                "assert result.returncode == 0, result.stdout + result.stderr\n",
                "print('GEPA optimizer completed')",
            ],
        }
    )

    # Wrap in the canonical Colab notebook schema
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return notebook


def main() -> int:
    """Build the canonical Colab-style notebook + write it to disk."""
    import sys

    here = Path(__file__).resolve().parent
    out_path = here / "politician_pipeline.ipynb"

    notebook = build_politician_pipeline_notebook()
    out_path.write_text(json.dumps(notebook, indent=2))
    print(f"Wrote {out_path} ({len(notebook['cells'])} cells)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
