from nomad_plugins_metadata.extractor.merge import merge_generated_and_manual


def test_manual_override_has_precedence_and_report_is_emitted():
    generated = {
        'name': 'auto-name',
        'deployment': {'on_pypi': False, 'on_example_oasis': True},
        'tags': ['auto'],
    }
    manual = {
        'name': 'manual-name',
        'deployment': {'on_pypi': True},
        'extra_field': 'kept',
    }

    merged, report = merge_generated_and_manual(generated, manual)

    assert merged['name'] == 'manual-name'
    assert merged['deployment']['on_pypi'] is True
    assert merged['deployment']['on_example_oasis'] is True
    assert merged['extra_field'] == 'kept'

    fields = {item['field'] for item in report['overridden_fields']}
    assert 'name' in fields
    assert 'deployment.on_pypi' in fields
    assert report['summary']['manual_precedence'] is True
