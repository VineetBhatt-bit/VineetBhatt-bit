#!/usr/bin/env python3

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OWNER = "VineetBhatt-bit"
API_BASE = f"https://api.github.com/users/{OWNER}/repos"


def fetch_page(page: int) -> list[dict]:
    url = f"{API_BASE}?per_page=100&page={page}&type=owner"

    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "VineetBhatt-bit-profile-telemetry",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)

    except HTTPError as error:
        print(f"GitHub API error: HTTP {error.code}", file=sys.stderr)
        sys.exit(1)

    except URLError as error:
        print(f"Network error: {error.reason}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("GitHub API returned an unexpected response.", file=sys.stderr)
        sys.exit(1)

    return data


def fetch_all_repositories() -> list[dict]:
    repositories = []
    page = 1

    while True:
        batch = fetch_page(page)

        if not batch:
            break

        repositories.extend(batch)
        page += 1

    return repositories


def normalize_repository(repo: dict) -> dict:
    required_fields = [
        "name",
        "description",
        "language",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "created_at",
        "updated_at",
        "pushed_at",
        "html_url",
    ]

    missing = [field for field in required_fields if field not in repo]

    if missing:
        raise ValueError(
            f"Repository {repo.get('name', '<unknown>')} "
            f"is missing fields: {', '.join(missing)}"
        )

    return {
        "name": repo["name"],
        "description": repo["description"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "open_issues": repo["open_issues_count"],
        "created_at": repo["created_at"],
        "updated_at": repo["updated_at"],
        "pushed_at": repo["pushed_at"],
        "html_url": repo["html_url"],
    }


def build_telemetry(repositories: list[dict]) -> dict:
    normalized = [
        normalize_repository(repo)
        for repo in repositories
    ]

    normalized.sort(key=lambda repo: repo["name"].lower())

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "GitHub REST API",
        "owner": OWNER,
        "repository_count": len(normalized),
        "repositories": normalized,
    }


def write_telemetry(telemetry: dict) -> Path:
    output_path = (
        Path(__file__).resolve().parents[2]
        / "assets"
        / "telemetry"
        / "repositories.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(telemetry, indent=2) + "\n",
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    repositories = fetch_all_repositories()
    telemetry = build_telemetry(repositories)
    output_path = write_telemetry(telemetry)

    print(f"Generated: {output_path}")
    print(f"Repositories: {telemetry['repository_count']}")


if __name__ == "__main__":
    main()