"""Endpoint to endpoint messages."""
from __future__ import annotations

import sys
from dataclasses import dataclass

if sys.version_info >= (3, 8):  # pragma: >=3.8 cover
    from typing import Literal
else:  # pragma: <3.8 cover
    from typing_extensions import Literal


@dataclass
class EndpointRequest:
    """Message type for requests between endpoints."""

    kind: Literal['request', 'response']
    op: Literal['evict', 'exists', 'get', 'set']
    uuid: str
    key: str
    data: bytes | None = None
    exists: bool | None = None
    error: Exception | None = None
