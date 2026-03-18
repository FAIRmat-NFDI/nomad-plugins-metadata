# Apply to a Plugin Repo

Use this guide to set up and operate release-driven metadata automation for a
plugin repository.
For local/manual editing flow, use `how_to/use_this_plugin.md`.

## 1. Create a feature branch in target plugin repo

```bash
git checkout -b test/metadata-pipeline
```

## 2. Copy workflow templates

Copy these files from this repository:

- `docs/templates/update-plugin-metadata.yml`
- `docs/templates/check-plugin-metadata-pr.yml`

Into the target plugin repository:

- `.github/workflows/update-plugin-metadata.yml`
- `.github/workflows/check-plugin-metadata-pr.yml`

## 3. Verify workflow package source

Use a pinned Git ref for reproducible workflow behavior (example tag):

- `package_spec: git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0`

## 4. Run a local dry run once

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0"
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

## 6. Commit setup and open onboarding PR

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

## 7. Operational behavior after merge

- On release publish, workflow updates metadata artifacts and opens/updates a rolling PR.
- On normal PRs, check-only workflow enforces that metadata artifacts are in sync.

## 8. Maintainer handling of release-generated metadata PRs

When a release creates or updates a metadata PR (typically `chore: update plugin metadata`):

1. Inspect generated changes in the PR.
2. If manual edits are needed, check out the PR branch locally.
3. Follow local flow from `how_to/use_this_plugin.md`:
   - run extract
   - edit `.metadata/nomad_plugin_metadata.manual.yaml`
   - run extract again
4. Commit and push to the same PR branch.
5. Re-review and merge.

## TODO

Replace pinned Git `package_spec` with pinned PyPI version once package is
published on PyPI.
