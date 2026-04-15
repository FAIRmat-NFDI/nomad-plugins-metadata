from nomad_plugins_metadata.extractor.cli import build_parser
from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def test_all_exported_slots_have_descriptions():
    schema = load_schema()
    slots = schema.get('slots', {})
    missing = [
        slot_name
        for slot_name, slot in slots.items()
        if not str(slot.get('description', '') or '').strip()
    ]
    assert missing == [], f'Missing slot descriptions: {missing}'


def test_primary_extract_cli_options_have_help_text():
    parser = build_parser()
    extract_cmd = next(
        action
        for action in parser._subparsers._actions  # noqa: SLF001
        if getattr(action, 'dest', None) == 'command'
    ).choices['extract']

    help_by_option = {}
    for action in extract_cmd._actions:  # noqa: SLF001
        for option in action.option_strings:
            help_by_option[option] = (action.help or '').strip()

    required_help_options = [
        '--repo-path',
        '--manual-path',
        '--auto-path',
        '--effective-path',
        '--report-path',
        '--release-tag',
        '--release-sha',
        '--plugins-index-path',
    ]
    missing = [
        option
        for option in required_help_options
        if not help_by_option.get(option, '').strip()
    ]
    assert missing == [], f'Missing CLI help descriptions: {missing}'
