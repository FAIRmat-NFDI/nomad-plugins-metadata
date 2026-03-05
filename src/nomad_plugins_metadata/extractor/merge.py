from __future__ import annotations

from copy import deepcopy


def _deep_merge(base: dict, override: dict, path: str, overridden: list[dict]) -> dict:
    merged = deepcopy(base)
    for key, override_value in override.items():
        next_path = f'{path}.{key}' if path else key
        if key not in merged:
            merged[key] = deepcopy(override_value)
            continue

        base_value = merged[key]
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = _deep_merge(base_value, override_value, next_path, overridden)
            continue

        if base_value != override_value:
            overridden.append(
                {
                    'field': next_path,
                    'generated_value': base_value,
                    'manual_value': override_value,
                }
            )
        merged[key] = deepcopy(override_value)

    return merged


def merge_generated_and_manual(generated: dict, manual_override: dict) -> tuple[dict, dict]:
    """Merge plugin metadata with deterministic `manual > generated` precedence."""
    overridden: list[dict] = []
    merged = _deep_merge(generated, manual_override, path='', overridden=overridden)

    report = {
        'summary': {
            'overridden_field_count': len(overridden),
            'manual_precedence': True,
        },
        'overridden_fields': overridden,
    }
    return merged, report
