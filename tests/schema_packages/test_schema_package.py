import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.id == 'nomad-plugin-test'
    assert entry_archive.data.name == 'Test Plugin'
    assert entry_archive.data.capabilities[0].capability_type == 'parser'
    assert entry_archive.data.deployment.on_example_oasis is True
