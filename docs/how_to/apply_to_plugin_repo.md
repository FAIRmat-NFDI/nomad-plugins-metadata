# Apply to a Plugin Repo

Use this guide to onboard any NOMAD plugin repository to the metadata pipeline.

## 1. Copy workflow templates

Copy these files from this repository:

- `docs/templates/update-plugin-metadata.yml`
- `docs/templates/check-plugin-metadata-pr.yml`

Into the target plugin repository:

- `.github/workflows/update-plugin-metadata.yml`
- `.github/workflows/check-plugin-metadata-pr.yml`

## 2. Verify workflow package source

Templates currently default to Git installation of this package:

- `package_spec: git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@main`

When a PyPI release is available, switch to a pinned PyPI version:

- `package_spec: nomad-plugins-metadata==<PINNED_VERSION>`

## 3. Create feature branch in plugin repo

```bash
git checkout -b test/metadata-pipeline
```

## 4. Local dry run in plugin repo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@main"
pip install -e .
nomad-plugin-metadata extract --repo-path .
```

Expected outputs:

- `.metadata/nomad_plugin_metadata.manual.yaml`
- `.metadata/nomad_plugin_metadata.auto.yaml`
- `.metadata/plugin-metadata.override-report.yaml`
- `nomad_plugin_metadata.yaml`

## 5. One-time migration from legacy root files (if needed)

If the plugin repo still has old root-level files:

- `nomad_plugin_metadata.manual.yaml`
- `nomad_plugin_metadata.auto.yaml`

Migrate with:

```bash
mkdir -p .metadata
[ -f nomad_plugin_metadata.manual.yaml ] && mv nomad_plugin_metadata.manual.yaml .metadata/
[ -f nomad_plugin_metadata.auto.yaml ] && mv nomad_plugin_metadata.auto.yaml .metadata/
nomad-plugin-metadata extract --repo-path .
```

## 6. Maintainer edit cycle

1. Edit `.metadata/nomad_plugin_metadata.manual.yaml` only.
2. Re-run `nomad-plugin-metadata extract --repo-path .`.
3. Check `.metadata/plugin-metadata.override-report.yaml` for conflicts.

## 7. Commit and open PR

```bash
git add \
  .github/workflows/update-plugin-metadata.yml \
  .github/workflows/check-plugin-metadata-pr.yml \
  .metadata/nomad_plugin_metadata.manual.yaml \
  .metadata/nomad_plugin_metadata.auto.yaml \
  .metadata/plugin-metadata.override-report.yaml \
  .metadata/README.md \
  nomad_plugin_metadata.yaml
git commit -m "chore: enable plugin metadata pipeline"
git push -u origin test/metadata-pipeline
```

Then open a PR to `main` for maintainer review.

## 8. CI behavior after merge

- On release publish, workflow updates metadata artifacts and opens/updates a rolling PR.
- On normal PRs, check-only workflow enforces that metadata artifacts are in sync.
