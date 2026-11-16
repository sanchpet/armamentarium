#!/usr/bin/env python3
"""Move each upstream plugin's pin to its newest tag and describe what changed.

Rewrites .claude-plugin/marketplace.json in place and writes the PR body to the
path given as the first argument. Exits 0 with no file written when every pin
is current. Needs GITHUB_TOKEN for the GitHub API.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

MARKETPLACE = ".claude-plugin/marketplace.json"
# Files that run code or change when the agent acts: the review gate is about these.
EXECUTABLE = re.compile(r"(^|/)(SKILL\.md|hooks/|\.mcp\.json|agents/|scripts/|commands/|plugin\.json)")


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def repo_of(source):
    if source["source"] == "github":
        return source["repo"]
    match = re.match(r"https://github\.com/([^/]+/[^/.]+)(\.git)?$", source["url"])
    if not match:
        raise SystemExit(f"cannot track a non-GitHub source: {source['url']}")
    return match.group(1)


def newest_tag(repo):
    try:
        return api(f"repos/{repo}/releases/latest")["tag_name"]
    except urllib.error.HTTPError as err:
        if err.code != 404:
            raise
    tags = api(f"repos/{repo}/tags?per_page=1")
    return tags[0]["name"] if tags else None


def main(body_path):
    with open(MARKETPLACE, encoding="utf-8") as f:
        market = json.load(f)

    sections = []
    for plugin in market["plugins"]:
        source = plugin["source"]
        if isinstance(source, str) or "ref" not in source:
            continue
        repo = repo_of(source)
        tag = newest_tag(repo)
        if tag is None or tag == source["ref"]:
            continue
        sha = api(f"repos/{repo}/commits/{tag}")["sha"]
        compare = api(f"repos/{repo}/compare/{source['sha']}...{sha}")
        prefix = source.get("path", "").strip("/")
        files = [
            f["filename"][len(prefix) + 1:] if prefix else f["filename"]
            for f in compare.get("files", [])
            if not prefix or f["filename"].startswith(prefix + "/")
        ]
        gated = [f for f in files if EXECUTABLE.search(f)]

        lines = [
            f"### `{plugin['name']}`: {source['ref']} → {tag}",
            "",
            f"[Compare](https://github.com/{repo}/compare/{source['ref']}...{tag}) · "
            f"[Release](https://github.com/{repo}/releases/tag/{tag}) · "
            f"{len(files)} files changed in the plugin",
        ]
        if compare.get("files") is not None and len(compare["files"]) >= 300:
            lines.append("")
            lines.append("The compare API caps the list at 300 files; read the compare page in full.")
        if gated:
            lines += ["", "Changed files that run code or steer the agent:", ""]
            lines += [f"- `{f}`" for f in gated]
        sections.append("\n".join(lines))

        source["ref"], source["sha"] = tag, sha

    if not sections:
        print("all upstream pins are current")
        return

    with open(MARKETPLACE, "w", encoding="utf-8") as f:
        json.dump(market, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(body_path, "w", encoding="utf-8") as f:
        f.write(
            "Upstream plugins have new tags. The pin covers the plugin's files; "
            "anything a plugin fetches at run time is outside it (see the README).\n\n"
        )
        f.write("\n\n".join(sections) + "\n")
    print(f"bumped {len(sections)} plugin(s)")


if __name__ == "__main__":
    main(sys.argv[1])
