from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from nomad_plugins_metadata.extractor import cli as cli_module
from nomad_plugins_metadata.extractor import extract as extract_module
from nomad_plugins_metadata.extractor import merge as merge_module
from nomad_plugins_metadata.schema_packages.schema_validation import load_schema

ROOT = Path(__file__).resolve().parents[1]
DOCS_REF = ROOT / 'docs' / 'reference'
CLI_REF_PATH = DOCS_REF / 'cli_reference.md'
SCHEMA_REF_PATH = DOCS_REF / 'schema_reference.md'


def _render_cli_reference() -> str:
    parser = cli_module.build_parser()
    extract_cmd = next(
        action
        for action in parser._subparsers._actions  # noqa: SLF001
        if getattr(action, 'dest', None) == 'command'
    ).choices['extract']

    lines: list[str] = [
        '# CLI and API Reference',
        '',
        '## CLI',
        '',
        'Command:',
        '',
        '```bash',
        'nomad-plugin-metadata extract [options]',
        '```',
        '',
        '| Option | Type | Default | Description |',
        '|---|---|---|---|',
    ]

    for action in extract_cmd._actions:  # noqa: SLF001
        if not action.option_strings:
            continue
        if any(flag in ('-h', '--help') for flag in action.option_strings):
            continue
        option = ', '.join(action.option_strings)
        if action.__class__.__name__ == 'BooleanOptionalAction':
            type_name = 'bool flag'
        elif action.type is None:
            type_name = 'str'
        else:
            type_name = getattr(action.type, '__name__', str(action.type))
        default = ''
        if action.default is not None and str(action.default) != '==SUPPRESS==':
            default = str(action.default)
        help_text = (action.help or '').replace('\n', ' ').strip()
        lines.append(f'| `{option}` | `{type_name}` | `{default}` | {help_text} |')

    lines.extend(
        [
            '',
            '## API (Docstrings)',
            '',
            'This section is generated from Python docstrings.',
            '',
        ]
    )

    api_objects = [
        ('`ExtractRunConfig`', cli_module.ExtractRunConfig),
        ('`run_extract`', cli_module.run_extract),
        ('`build_parser`', cli_module.build_parser),
        ('`main`', cli_module.main),
        ('`build_generated_metadata`', extract_module.build_generated_metadata),
        (
            '`build_generated_metadata_with_release_context`',
            extract_module.build_generated_metadata_with_release_context,
        ),
        ('`merge_generated_and_manual`', merge_module.merge_generated_and_manual),
    ]

    for title, obj in api_objects:
        doc = inspect.getdoc(obj) or 'No docstring available.'
        lines.append(f'### {title}')
        lines.append('')
        lines.append(doc)
        lines.append('')

    return '\n'.join(lines).rstrip() + '\n'


def _slot_comment(slot_name: str, slot: dict[str, Any], enums: dict[str, Any]) -> str:
    range_name = slot.get('range', 'string')
    multivalued = bool(slot.get('multivalued', False))
    required = bool(slot.get('required', False))
    bits: list[str] = []
    if multivalued:
        bits.append(f'list[{range_name}]')
    else:
        bits.append(str(range_name))
    if range_name in enums:
        values = ', '.join(enums[range_name]['permissible_values'].keys())
        bits.append(f'enum: {values}')
    bits.append('required' if required else 'optional')
    description = (slot.get('description', '') or '').replace('\n', ' ').strip()
    if description:
        bits.append(description)
    return '; '.join(bits)


def _render_annotated_yaml_for_class(
    class_name: str,
    schema: dict[str, Any],
    indent: int = 0,
    seen: set[str] | None = None,
) -> list[str]:
    if seen is None:
        seen = set()
    if class_name in seen:
        return ['{}']
    seen.add(class_name)

    classes = schema['classes']
    slots = schema['slots']
    enums = schema.get('enums', {})
    cls = classes[class_name]
    lines: list[str] = []
    prefix = ' ' * indent

    for slot_name in cls.get('slots', []):
        slot = slots.get(slot_name, {})
        range_name = slot.get('range', 'string')
        multivalued = bool(slot.get('multivalued', False))

        lines.append(f"{prefix}# {_slot_comment(slot_name, slot, enums)}")
        if range_name in classes:
            if multivalued:
                lines.append(f'{prefix}{slot_name}:')
                lines.append(f'{prefix}  -')
                nested = _render_annotated_yaml_for_class(
                    range_name, schema, indent=indent + 4, seen=seen.copy()
                )
                lines.extend(nested)
            else:
                lines.append(f'{prefix}{slot_name}:')
                nested = _render_annotated_yaml_for_class(
                    range_name, schema, indent=indent + 2, seen=seen.copy()
                )
                lines.extend(nested)
            continue

        if multivalued:
            lines.append(f'{prefix}{slot_name}: []')
        else:
            lines.append(f'{prefix}{slot_name}: null')

    return lines


def _render_schema_reference() -> str:
    schema = load_schema()
    classes = schema.get('classes', {})
    slots = schema.get('slots', {})
    enums = schema.get('enums', {})

    root_class = 'PluginPackage'
    root_slots = classes[root_class].get('slots', [])

    lines: list[str] = [
        '# Schema Reference',
        '',
        'Source of truth:',
        f"- `{(ROOT / 'src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml').relative_to(ROOT)}`",
        '',
        '## Root Fields (`PluginPackage`)',
        '',
        '| Field | Range | Required | Multi | Enum Values | Description |',
        '|---|---|---|---|---|---|',
    ]

    for slot_name in root_slots:
        slot = slots.get(slot_name, {})
        range_name = slot.get('range', 'string')
        required = bool(slot.get('required', False))
        multi = bool(slot.get('multivalued', False))
        enum_values = ''
        if range_name in enums:
            enum_values = ', '.join(enums[range_name]['permissible_values'].keys())
        desc = (slot.get('description', '') or '').replace('\n', ' ').strip()
        lines.append(
            f"| `{slot_name}` | `{range_name}` | `{required}` | `{multi}` | {enum_values} | {desc} |"
        )

    lines.extend(
        [
            '',
            '## Full Schema-Shaped YAML Template',
            '',
            'Generated from the LinkML schema (all fields included), with per-field comments:',
            '',
            '```yaml',
        ]
    )

    annotated_lines = _render_annotated_yaml_for_class(root_class, schema)
    lines.extend(annotated_lines)
    lines.extend(['```', ''])

    lines.append('## Enums')
    lines.append('')
    for enum_name, enum_def in enums.items():
        values = ', '.join(enum_def.get('permissible_values', {}).keys())
        lines.append(f'- `{enum_name}`: {values}')
    lines.append('')

    return '\n'.join(lines).rstrip() + '\n'


def main() -> None:
    DOCS_REF.mkdir(parents=True, exist_ok=True)
    CLI_REF_PATH.write_text(_render_cli_reference(), encoding='utf-8')
    SCHEMA_REF_PATH.write_text(_render_schema_reference(), encoding='utf-8')


if __name__ == '__main__':
    main()
