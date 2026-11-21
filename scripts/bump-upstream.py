#!/usr/bin/env python3
"""Move each upstream plugin's pin to the newest tag of its series and describe what changed.

Rewrites .claude-plugin/marketplace.json in place and writes the PR body to the
path given as the first argument. Exits 0 with no file written when every pin
is current. Needs GITHUB_TOKEN for the GitHub API.
"""
import json
import os
import re
import sys
import urllib.request

MARKETPLACE = ".claude-plugin/marketplace.json"
# A tag is a prefix and a dotted version: "v1.0.6", "skill-v4.10.0".
VERSION = re.compile(r"^(.*?)(\d+(?:\.\d+)*)$")
# Files that run code or change when the agent acts: the review gate is about these.
EXECUTABLE = re.compile(r"(^|/)(SKILL\.md|hooks/|\.mcp\.json|agents/|scripts/|commands/|plugin\.json)")


def request(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp), resp.headers.get("Link", "")


def api(path):
    return request(f"https://api.github.com/{path}")[0]


def api_list(path):
    """Every item of a list endpoint, following the Link header to the last page."""
    items, url = [], f"https://api.github.com/{path}"
    while url:
        page, link = request(url)
        items += page
        following = re.search(r'<([^>]+)>; rel="next"', link)
        url = following.group(1) if following else None
    return items


def repo_of(source):
    if source["source"] == "github":
        return source["repo"]
    match = re.match(r"https://github\.com/([^/]+/[^/.]+)(\.git)?$", source["url"])
    if not match:
        raise SystemExit(f"cannot track a non-GitHub source: {source['url']}")
    return match.group(1)


def newest_tag(repo, pinned):
    """The highest version among the tags that share the pinned tag's prefix.

    One repository may release several things under prefixed tags
    (skill-v4.10.0 next to engine-v0.1.28), so its latest release can be the
    wrong series. A pin that does not end in a version is left alone.
    """
    match = VERSION.match(pinned)
    if not match:
        return None
    prefix = match.group(1)
    versions = {}
    for ref in api_list(f"repos/{repo}/git/matching-refs/tags/{prefix}"):
        tag = ref["ref"].removeprefix("refs/tags/")
        found = VERSION.match(tag)
        if found and found.group(1) == prefix:
            versions[tuple(int(n) for n in found.group(2).split("."))] = tag
    return versions[max(versions)] if versions else None


def main(body_path):
    with open(MARKETPLACE, encoding="utf-8") as f:
        market = json.load(f)

    sections = []
    for plugin in market["plugins"]:
        source = plugin["source"]
        if isinstance(source, str) or "ref" not in source:
            continue
        repo = repo_of(source)
        tag = newest_tag(repo, source["ref"])
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
