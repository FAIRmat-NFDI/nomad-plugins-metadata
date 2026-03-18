# Template Files

These templates are ready to copy into a plugin repository.

## Files

- `update-plugin-metadata.yml`
  - Release-driven metadata update workflow.
  - Runs extractor in PR mode and opens/updates a rolling metadata PR.
- `check-plugin-metadata-pr.yml`
  - Pull-request check-only workflow.
  - Fails when metadata artifacts are out of sync.

## Where to copy in plugin repos

- `docs/templates/update-plugin-metadata.yml` -> `.github/workflows/update-plugin-metadata.yml`
- `docs/templates/check-plugin-metadata-pr.yml` -> `.github/workflows/check-plugin-metadata-pr.yml`

## `package_spec` note

Templates are written for pinned, reproducible Git installs:

- `git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0`

TODO: switch templates to pinned PyPI package versions after first stable PyPI publication.
