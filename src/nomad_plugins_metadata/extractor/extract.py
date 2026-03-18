from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import tomllib
from packaging.version import InvalidVersion, Version

from nomad_plugins_metadata.schema_packages.schema_validation import load_schema

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None


def _read_pyproject(pyproject_path: Path) -> dict:
    if not pyproject_path.exists():
        return {}
    with pyproject_path.open('rb') as f:
        return tomllib.load(f)


def _schema_version() -> str:
    schema = load_schema()
    return str(schema.get('version', '1.0.0'))


def _owners_to_maintainers(project: dict) -> list[dict]:
    maintainers = []
    for item in project.get('maintainers', []) or []:
        name = item.get('name')
        email = item.get('email')
        if not name and not email:
            continue
        maintainers.append({'name': name or '', 'email': email or ''})
    # preserve order, deduplicate exact dicts
    deduped = []
    seen = set()
    for entry in maintainers:
        marker = (entry.get('name', ''), entry.get('email', ''))
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(entry)
    return deduped


def _pyproject_authors(project: dict) -> list[dict]:
    authors = []
    for item in project.get('authors', []) or []:
        name = item.get('name')
        email = item.get('email')
        if not name and not email:
            continue
        authors.append({'name': name or '', 'email': email or ''})
    deduped = []
    seen = set()
    for entry in authors:
        marker = (entry.get('name', ''), entry.get('email', ''))
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(entry)
    return deduped


def _read_citation_cff(repo_path: Path) -> dict:
    if yaml is None:
        return {}
    for filename in ('CITATION.cff', 'citation.cff'):
        path = repo_path / filename
        if not path.exists():
            continue
        try:
            with path.open('r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            return {}
        if isinstance(data, dict):
            return data
        return {}
    return {}


def _cff_author_to_person(item: dict) -> dict | None:
    if not isinstance(item, dict):
        return None
    given = str(item.get('given-names', '') or '').strip()
    family = str(item.get('family-names', '') or '').strip()
    raw_name = str(item.get('name', '') or '').strip()
    name = raw_name or ' '.join(part for part in (given, family) if part).strip()
    email = str(item.get('email', '') or '').strip()
    affiliation = str(item.get('affiliation', '') or '').strip()
    role = str(item.get('role', '') or '').strip()
    person = {
        'name': name,
        'email': email,
        'affiliation': affiliation,
        'role': role,
    }
    person = {key: value for key, value in person.items() if value}
    if not person:
        return None
    if 'name' not in person and 'email' not in person:
        return None
    return person


def _maintainers_from_cff(cff: dict) -> list[dict]:
    authors = cff.get('authors', [])
    if not isinstance(authors, list):
        return []
    people: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for author in authors:
        person = _cff_author_to_person(author)
        if person is None:
            continue
        marker = (person.get('name', ''), person.get('email', ''))
        if marker in seen:
            continue
        seen.add(marker)
        people.append(person)
    return people


def _cff_string(cff: dict, *keys: str) -> str:
    for key in keys:
        value = cff.get(key)
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                return stripped
    return ''


def _normalize_package_name(name: str) -> str:
    return re.sub(r'[-_.]+', '-', name).lower().strip()


def _guess_capability_type(entry_point_name: str, python_object: str) -> str:
    text = f'{entry_point_name} {python_object}'.lower()
    for marker, capability in (
        ('schema', 'schema'),
        ('parser', 'parser'),
        ('normalizer', 'normalizer'),
        ('app', 'app'),
        ('example', 'example_upload'),
        ('api', 'api'),
        ('north', 'north_tool'),
    ):
        if marker in text:
            return capability
    return 'tool'


def _extract_extensions_from_name_regex(name_regex: str) -> list[str]:
    if not name_regex:
        return []
    # Best-effort parsing of regexes such as .*\\.(csv|xlsx)$ or ^.*\\.h5$
    matches = re.findall(r'\\\.([A-Za-z0-9]+)', name_regex)
    grouped = re.findall(r'\\\.\(([^)]+)\)', name_regex)
    for group in grouped:
        for candidate in group.split('|'):
            ext = candidate.strip()
            if re.fullmatch(r'[A-Za-z0-9]+', ext):
                matches.append(ext)
    seen = set()
    result = []
    for ext in matches:
        normalized = ext.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(f'.{normalized}')
    return result


def _serialize_bytes(value: bytes | str | None) -> str:
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.hex()
    return str(value)


def _mime_pattern_is_specific(mime_pattern: str) -> bool:
    cleaned = (mime_pattern or '').strip()
    if not cleaned or cleaned in ('.*', 'text/.*', '.*/.*'):
        return False
    wildcardy = ('*', '^', '$', '(', ')', '[', ']', '|', '+', '?')
    return not any(token in cleaned for token in wildcardy)


def _extract_auxiliary_patterns_from_table(metadata_dict: dict | None) -> list[str]:
    if not metadata_dict:
        return []
    table = metadata_dict.get('tableOfFiles')
    if not isinstance(table, str) or not table.strip():
        return []
    candidates = re.findall(r'`([^`]+)`', table)
    result = []
    seen = set()
    for candidate in candidates:
        value = candidate.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _extract_extensions_from_auxiliary_patterns(patterns: list[str]) -> list[str]:
    extensions: list[str] = []
    seen: set[str] = set()
    wildcard_tokens = ('*', '?', '[', ']', '(', ')', '{', '}', '$', '^', '|', '\\')
    for pattern in patterns:
        token = (pattern or '').strip()
        if not token:
            continue
        if any(symbol in token for symbol in wildcard_tokens):
            continue
        last_segment = token.split('/')[-1]
        if '.' not in last_segment:
            continue
        ext = last_segment.rsplit('.', 1)[-1].strip().lower()
        if not re.fullmatch(r'[a-z0-9]+', ext):
            continue
        value = f'.{ext}'
        if value in seen:
            continue
        seen.add(value)
        extensions.append(value)
    return extensions


def _extract_schema_dependencies(pyproject: dict) -> list[dict]:
    project = pyproject.get('project', {}) or {}
    dependencies = []

    def add_dependency(dep_string: str, optional: bool) -> None:
        dep = dep_string.strip()
        if not dep:
            return
        match = re.match(r'^\s*([A-Za-z0-9_.-]+)\s*(.*)$', dep)
        if not match:
            return
        name = match.group(1)
        version_range = match.group(2).strip()
        dependencies.append(
            {
                'dependency_type': 'python_package',
                'package_name': name,
                'version_range': version_range or '',
                'optional': optional,
                'purpose': 'runtime' if not optional else 'optional',
            }
        )

    for dep in project.get('dependencies', []) or []:
        add_dependency(str(dep), optional=False)

    for _, deps in (project.get('optional-dependencies', {}) or {}).items():
        for dep in deps or []:
            add_dependency(str(dep), optional=True)

    return dependencies


def _parse_github_owner_repo(repository_url: str) -> tuple[str, str] | None:
    if not repository_url:
        return None
    parsed = urlparse(repository_url)
    if parsed.netloc.lower() not in ('github.com', 'www.github.com'):
        return None
    parts = [part for part in parsed.path.strip('/').split('/') if part]
    if len(parts) < 2:  # noqa: PLR2004
        return None
    owner, repo = parts[0], parts[1]
    if repo.endswith('.git'):
        repo = repo[:-4]
    if not owner or not repo:
        return None
    return owner, repo


def _check_github_pages_exists(repository_url: str) -> str | None:
    owner_repo = _parse_github_owner_repo(repository_url)
    if owner_repo is None:
        return None
    owner, repo = owner_repo
    docs_url = f'https://{owner.lower()}.github.io/{repo}/'
    request = Request(
        docs_url,
        headers={
            'User-Agent': 'nomad-plugins-metadata-extractor',
        },
    )
    try:
        with urlopen(request, timeout=5):  # noqa: S310
            return docs_url
    except (HTTPError, URLError, TimeoutError, ValueError):
        return None


def _fetch_github_repo_metadata(repository_url: str) -> dict | None:
    owner_repo = _parse_github_owner_repo(repository_url)
    if owner_repo is None:
        return None
    owner, repo = owner_repo
    api_url = f'https://api.github.com/repos/{owner}/{repo}'
    request = Request(
        api_url,
        headers={
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'nomad-plugins-metadata-extractor',
        },
    )
    try:
        with urlopen(request, timeout=5) as response:  # noqa: S310
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None
    if isinstance(payload, dict):
        return payload
    return None


def _is_github_repo_archived(repository_url: str) -> bool | None:
    payload = _fetch_github_repo_metadata(repository_url)
    if payload is None:
        return None

    archived = payload.get('archived')
    if isinstance(archived, bool):
        return archived
    return None


def _version_is_at_least_1(version_str: str) -> bool:
    clean = (version_str or '').strip()
    if clean.startswith('v'):
        clean = clean[1:]
    if not clean:
        return False
    try:
        return Version(clean) >= Version('1.0.0')
    except InvalidVersion:
        return False


def _infer_maturity(plugin_version: str, archived: bool | None) -> str | None:
    if archived is True:
        return 'archived'
    if _version_is_at_least_1(plugin_version):
        return 'stable'
    return None


def _github_telemetry(repository_url: str) -> dict:
    payload = _fetch_github_repo_metadata(repository_url)
    if payload is None:
        return {}
    owner_data = payload.get('owner', {}) if isinstance(payload.get('owner'), dict) else {}
    telemetry = {
        'stars': payload.get('stargazers_count'),
        'owner': owner_data.get('login'),
        'owner_type': owner_data.get('type'),
        'created': payload.get('created_at'),
        'last_updated': payload.get('updated_at'),
        'archived': payload.get('archived'),
    }
    cleaned = {}
    for key, value in telemetry.items():
        if key == 'stars' and isinstance(value, int):
            cleaned[key] = value
        elif key == 'archived' and isinstance(value, bool):
            cleaned[key] = value
        elif key in ('owner', 'owner_type', 'created', 'last_updated') and isinstance(
            value, str
        ):
            if value.strip():
                cleaned[key] = value.strip()
    return cleaned


def _infer_documentation_url(
    documentation: str, upstream_repository: str
) -> str | None:
    if (documentation or '').strip():
        return documentation
    return _check_github_pages_exists(upstream_repository)


def _infer_homepage_url(
    homepage: str, cff_homepage: str, upstream_repository: str
) -> str | None:
    if (homepage or '').strip():
        return homepage
    if (cff_homepage or '').strip():
        return cff_homepage
    if (upstream_repository or '').strip():
        return upstream_repository
    return None


def _entry_point_type_to_capability(entry_point_type: str | None) -> str:
    mapping = {
        'schema_package': 'schema',
        'parser': 'parser',
        'normalizer': 'normalizer',
        'app': 'app',
        'example_upload': 'example_upload',
        'api': 'api',
        'north_tool': 'north_tool',
    }
    if entry_point_type is None:
        return 'tool'
    return mapping.get(entry_point_type, entry_point_type)


def _discover_installed_nomad_entry_points(
    target_package_names: set[str],
) -> dict[str, object]:
    discovered: dict[str, object] = {}
    try:
        entry_points = metadata.entry_points(group='nomad.plugin')
    except Exception:
        return discovered

    for entry_point in entry_points:
        dist = getattr(entry_point, 'dist', None)
        dist_name = getattr(dist, 'name', None)
        if not dist_name:
            continue
        if _normalize_package_name(str(dist_name)) not in target_package_names:
            continue
        try:
            loaded = entry_point.load()
        except Exception:
            continue
        discovered[entry_point.name] = loaded

    return discovered


def _build_entry_points_and_capabilities(
    project: dict,
    repo_path: Path,
) -> tuple[list[dict], list[dict], list[str], list[dict]]:
    pyproject_entry_points = (
        (project.get('entry-points', {}) or {}).get('nomad.plugin', {}) or {}
    )
    package_name = str(project.get('name', repo_path.name))
    target_packages = {
        _normalize_package_name(package_name),
        _normalize_package_name(repo_path.name),
    }
    installed_entry_points = _discover_installed_nomad_entry_points(target_packages)

    entry_points: list[dict] = []
    capabilities: list[dict] = []
    supported_filetypes: list[str] = []
    file_format_support: list[dict] = []

    for ep_name, python_object in pyproject_entry_points.items():
        loaded = installed_entry_points.get(ep_name)
        entry_point_type = getattr(loaded, 'entry_point_type', None)
        capability_type = _entry_point_type_to_capability(entry_point_type)
        if capability_type == entry_point_type:
            capability_type = _guess_capability_type(ep_name, str(python_object))

        entry_points.append(
            {
                'id': f'nomad.plugin:{ep_name}',
                'entry_point_group': 'nomad.plugin',
                'entry_point_name': ep_name,
                'python_object': str(python_object),
                'capability_type': capability_type,
            }
        )

        capability = {
            'id': str(getattr(loaded, 'id', ep_name)),
            'capability_type': capability_type,
            'title': str(getattr(loaded, 'name', ep_name)),
            'summary': str(getattr(loaded, 'description', '') or ''),
        }

        if capability_type == 'parser':
            contents_dict = getattr(loaded, 'mainfile_contents_dict', None)
            parser_details = {
                'parser_name': str(getattr(loaded, 'name', ep_name)),
                'parser_level': getattr(loaded, 'level', None),
                'parser_aliases': list(getattr(loaded, 'aliases', []) or []),
                'mainfile_name_re': str(getattr(loaded, 'mainfile_name_re', '') or ''),
                'mainfile_contents_re': str(
                    getattr(loaded, 'mainfile_contents_re', '') or ''
                ),
                'mainfile_contents_dict': (
                    json.dumps(contents_dict) if contents_dict else ''
                ),
                'mainfile_mime_re': str(getattr(loaded, 'mainfile_mime_re', '') or ''),
                'mainfile_binary_header': _serialize_bytes(
                    getattr(loaded, 'mainfile_binary_header', None)
                ),
                'mainfile_binary_header_re': _serialize_bytes(
                    getattr(loaded, 'mainfile_binary_header_re', None)
                ),
                'mainfile_alternative': getattr(loaded, 'mainfile_alternative', None),
                'compression_support': list(
                    getattr(loaded, 'supported_compressions', []) or []
                ),
                'auxiliary_file_patterns': _extract_auxiliary_patterns_from_table(
                    getattr(loaded, 'metadata', None)
                ),
            }
            parser_details = {
                key: value
                for key, value in parser_details.items()
                if value not in ('', [], None)
            }
            if parser_details:
                capability['parser_details'] = parser_details

            extensions = _extract_extensions_from_name_regex(
                str(getattr(loaded, 'mainfile_name_re', '') or '')
            )
            aux_patterns = list(parser_details.get('auxiliary_file_patterns', []))
            extensions.extend(
                _extract_extensions_from_auxiliary_patterns(aux_patterns)
            )
            mime = str(getattr(loaded, 'mainfile_mime_re', '') or '')
            for ext in extensions:
                if ext in supported_filetypes:
                    continue
                supported_filetypes.append(ext)
                file_format_support.append(
                    {
                        'id': ext.lstrip('.'),
                        'label': ext,
                        'extensions': [ext],
                        'mime_types': [mime] if mime else [],
                    }
                )
            # Fallback: if parser has specific mime matcher but no extension regex, emit
            # at least one file-format support item for discoverability.
            if not extensions and _mime_pattern_is_specific(mime):
                format_id = mime.lower().replace('/', '-').replace('+', '-')
                file_format_support.append(
                    {
                        'id': format_id,
                        'label': mime,
                        'extensions': [],
                        'mime_types': [mime],
                    }
                )

        capability = {
            key: value for key, value in capability.items() if value not in ('', [], None)
        }
        capabilities.append(capability)

    return entry_points, capabilities, supported_filetypes, file_format_support


def build_generated_metadata(repo_path: Path) -> dict:
    """Generate baseline metadata from repo-local static sources."""
    return build_generated_metadata_with_release_context(
        repo_path=repo_path, release_tag=None, release_sha=None
    )


def build_generated_metadata_with_release_context(
    repo_path: Path,
    release_tag: str | None,
    release_sha: str | None,
) -> dict:
    """Generate baseline metadata from repo-local and discoverable plugin sources.

    Sources include:
    - `pyproject.toml` project metadata and entry-point declarations
    - installed `nomad.plugin` entry points from the target package
    - optional `CITATION.cff` / `citation.cff`
    - best-effort repository API lookups (GitHub)
    """
    pyproject = _read_pyproject(repo_path / 'pyproject.toml')
    cff = _read_citation_cff(repo_path)
    project = pyproject.get('project', {})
    urls = project.get('urls', {}) or {}
    entry_points, capabilities, supported_filetypes, file_format_support = (
        _build_entry_points_and_capabilities(project, repo_path)
    )
    schema_dependencies = _extract_schema_dependencies(pyproject)

    license_value = ''
    license_data = project.get('license')
    if isinstance(license_data, str):
        license_value = license_data
    elif isinstance(license_data, dict):
        license_value = str(
            license_data.get('text', '')
            or license_data.get('file', '')
            or license_data.get('name', '')
        )

    package_name = project.get('name', repo_path.name)
    plugin_version = project.get('version', '')
    cff_repository = _cff_string(cff, 'repository-code', 'repository_code')
    cff_homepage = _cff_string(cff, 'url')
    upstream_repository = str(urls.get('Repository', '') or cff_repository)
    github_telemetry = _github_telemetry(str(upstream_repository))
    inferred_maturity = _infer_maturity(
        plugin_version=str(plugin_version),
        archived=github_telemetry.get('archived')
        if isinstance(github_telemetry.get('archived'), bool)
        else None,
    )
    inferred_documentation = _infer_documentation_url(
        documentation=str(urls.get('Documentation', '') or ''),
        upstream_repository=str(upstream_repository),
    )
    inferred_homepage = _infer_homepage_url(
        homepage=str(urls.get('Homepage', '') or ''),
        cff_homepage=cff_homepage,
        upstream_repository=str(upstream_repository),
    )
    issue_tracker = ''
    for key in urls:
        if key.lower().replace(' ', '').replace('_', '') in (
            'issuetracker',
            'bugtracker',
        ):
            issue_tracker = str(urls[key])
            break

    cff_authors = _maintainers_from_cff(cff)
    pyproject_authors = _pyproject_authors(project)
    maintainers = _owners_to_maintainers(project)
    authors = cff_authors or pyproject_authors

    metadata = {
        'id': package_name,
        'metadata_schema_version': _schema_version(),
        'name': package_name,
        'description': project.get('description', ''),
        'plugin_version': plugin_version,
        'license': license_value,
        'upstream_repository': upstream_repository,
        'documentation': inferred_documentation or '',
        'homepage': inferred_homepage or '',
        'issue_tracker': issue_tracker,
        'maintainers': maintainers,
        'authors': authors,
        'entry_points': entry_points,
        'capabilities': capabilities,
        'supported_filetypes': supported_filetypes,
        'file_format_support': file_format_support,
        'schema_dependencies': schema_dependencies,
        'metadata_provenance': [
            {
                'source': 'pyproject',
                'extraction_method': 'deterministic',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            },
            {
                'source': 'plugin_entry_points',
                'extraction_method': 'deterministic',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            },
        ],
    }
    metadata.update(github_telemetry)
    cff_used = bool(cff_authors) or (
        (not str(urls.get('Repository', '') or '').strip() and bool(cff_repository))
        or (not str(urls.get('Homepage', '') or '').strip() and bool(cff_homepage))
    )
    if cff_used:
        metadata['metadata_provenance'].append(
            {
                'source': 'citation_cff',
                'extraction_method': 'deterministic',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            }
        )
    clean_release_tag = (release_tag or '').strip()
    clean_release_sha = (release_sha or '').strip()
    if clean_release_tag or clean_release_sha:
        metadata['release_context'] = {
            'release_tag': clean_release_tag,
            'release_commit_sha': clean_release_sha,
        }
    if inferred_maturity:
        metadata['maturity'] = inferred_maturity

    # Drop empty values for cleaner generated files.
    return {k: v for k, v in metadata.items() if v not in ('', [], None)}
