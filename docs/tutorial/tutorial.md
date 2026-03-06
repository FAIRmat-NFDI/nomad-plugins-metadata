# Tutorial

This tutorial shows the standard plugin-repo metadata workflow.

## 1. Add manual metadata file

Create `nomad_plugin_metadata.yaml` in repository root.

Minimal example:

```yaml
id: my-plugin
metadata_schema_version: 1.0.0
name: My Plugin
source_repository: https://github.com/example/my-plugin
maturity: alpha
```

## 2. Run extractor locally

```sh
nomad-plugin-metadata extract --repo-path .
```

Generated outputs:

- `.nomad/plugin-metadata.generated.yaml`
- `.nomad/plugin-metadata.effective.yaml`
- `.nomad/plugin-metadata.override-report.yaml`

If the plugin is installed in your environment, extractor output also includes
technical entry-point metadata (e.g., parser `mainfile_*` patterns, compression support).

## 3. Validate schema assets in this package

From this repository:

```sh
uv run pytest -q tests/schema_packages/test_schema_assets.py
```

## 4. Add release workflow in plugin repository

Copy template:

- `docs/templates/update-plugin-metadata.yml`

Place it in plugin repo as:

- `.github/workflows/update-plugin-metadata.yml`

By default it runs on release publication, updates generated/effective/report files,
updates `nomad_plugin_metadata.yaml`, and opens or updates a rolling PR for maintainer review.

## 5. Review overrides

Check `.nomad/plugin-metadata.override-report.yaml` after runs.
If important fields are consistently overridden manually, consider improving extractor rules for that plugin type.
