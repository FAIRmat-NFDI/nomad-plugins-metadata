from __future__ import annotations

import importlib.metadata as importlib_metadata
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _is_local_nomad_plugin_entry_point(entry_point: Any) -> bool:
    dist = getattr(entry_point, 'dist', None)
    dist_name = str(getattr(dist, 'name', '') or '').replace('_', '-').lower()
    value = str(getattr(entry_point, 'value', '') or '')
    return dist_name == 'nomad-plugins-metadata' or value.startswith(
        'nomad_plugins_metadata.'
    )


def _patch_entry_points_module(module: Any) -> None:
    original_entry_points = module.entry_points

    def filtered_entry_points(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
        result = original_entry_points(*args, **kwargs)
        group = kwargs.get('group')
        if group != 'nomad.plugin':
            return result
        return [
            entry_point
            for entry_point in result
            if _is_local_nomad_plugin_entry_point(entry_point)
        ]

    module.entry_points = filtered_entry_points


_patch_entry_points_module(importlib_metadata)

try:  # pragma: no cover - only relevant on py310 environments
    import importlib_metadata as importlib_metadata_backport
except Exception:  # pragma: no cover
    importlib_metadata_backport = None

if importlib_metadata_backport is not None:
    _patch_entry_points_module(importlib_metadata_backport)
