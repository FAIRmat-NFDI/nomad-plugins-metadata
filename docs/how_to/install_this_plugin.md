# Install This Plugin

Install `nomad-plugins-metadata` as a CLI/tooling dependency in the environment
where you generate plugin metadata.

## Option 1: Install stable pinned Git version (recommended)

Use a tag (example below) or pinned commit:

```bash
pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0"
```

With `uv`:

```bash
uv pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0"
```

## Option 2: Install latest development version (not stable)

```bash
pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@main"
```

With `uv`:

```bash
uv pip install "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@main"
```

## Verify installation

```bash
nomad-plugin-metadata --help
```

## Upgrade to newest version

From a stable pinned Git ref:

```bash
pip uninstall -y nomad-plugins-metadata
pip install --no-cache-dir --force-reinstall "git+https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git@v1.0.0"
```

## TODO

Replace Git install examples with pinned PyPI version examples after first
stable PyPI publication.
