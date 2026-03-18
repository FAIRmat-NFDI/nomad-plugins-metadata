# How to Use This Plugin

This package is used to generate and maintain metadata files for other NOMAD
plugin repositories.

Use this page for the local/manual metadata workflow only.
For CI/release automation setup, use `how_to/apply_to_plugin_repo.md`.

## Direct local workflow

### Step 1: Generate metadata files

From the target plugin repo root:

```bash
nomad-plugin-metadata extract --repo-path .
```

This creates/updates:

- `.metadata/nomad_plugin_metadata.manual.yaml`
- `.metadata/nomad_plugin_metadata.auto.yaml`
- `.metadata/plugin-metadata.override-report.yaml`
- `nomad_plugin_metadata.yaml`

### Step 2: Edit manual metadata

Edit:

- `.metadata/nomad_plugin_metadata.manual.yaml`

Use non-empty values for overrides or manual additions.

### Step 3: Re-run to merge

```bash
nomad-plugin-metadata extract --repo-path .
```

This refreshes generated artifacts and updates the effective root file:

- `nomad_plugin_metadata.yaml`

## Reset options

- Reset manual/auto/report artifacts:
  - remove `.metadata/*`
- Regenerate auto/effective/report while keeping manual:
  - remove `.metadata/nomad_plugin_metadata.auto.yaml`, `.metadata/plugin-metadata.override-report.yaml`, and `nomad_plugin_metadata.yaml`
  - run `nomad-plugin-metadata extract --repo-path .`

## Next step

For release-driven automation (workflow templates + maintainer PR cycle), see:

- `docs/how_to/apply_to_plugin_repo.md`
