# CIANCHOSAINT — memory_bank.state (canonical key prefixes).
#
# Per the cianfhoghlaim `agent-valley-archive/archive/state.py` pattern.
#
# Per the user's selection: `app:` prefix scope (every cianchosaint surface
# shares Farage investigations across all 8 surfaces).
#
# Licence: BUSL-1.1 (per LICENSE.md)

"""cianchosaint.agents.cianchosaint.memory_bank.state — key prefixes.

4 canonical key prefixes:
- `(none)` (this visit only)
- `user:` (this analyst, forever)
- `app:` (everyone, forever) — DEFAULT per the user's selection
- `temp:` (this turn only)

Mirrors cianfhoghlaim's `agent-valley-archive/archive/state.py`:

```
key            scope    written by        read by
─────────────────────────────────────────────────
case           ???      write_down        vesper, the slip, page
recalled       session  recall            vesper, the tower panel
user:visits    user     the service       the tower (floor one)
```
"""

from __future__ import annotations

# The 4 canonical prefixes (per cianfhoghlaim)
KEY_NONE = ""  # no prefix — this visit only (lives for the duration of the session)
KEY_USER = "user:"  # this analyst, forever
KEY_APP = "app:"  # everyone, forever
KEY_TEMP = "temp:"  # this turn only (per cianfhoghlaim's `temp:` prefix)

#: The default prefix for the cianchosaint memory bank (per the user's selection)
DEFAULT_PREFIX = KEY_APP

#: The canonical app scope identifier for the cianchosaint memory bank
APP_SCOPE_KEY = ("cianchosaint", "app")


def prefix_for(name: str) -> str:
    """Return the canonical prefix for a key."""
    if name.startswith(KEY_USER):
        return KEY_USER
    if name.startswith(KEY_APP):
        return KEY_APP
    if name.startswith(KEY_TEMP):
        return KEY_TEMP
    return KEY_NONE


__all__ = [
    "APP_SCOPE_KEY",
    "DEFAULT_PREFIX",
    "KEY_APP",
    "KEY_NONE",
    "KEY_TEMP",
    "KEY_USER",
    "prefix_for",
]
