#!/usr/bin/env python3
"""Run OSV-Scanner v2 and normalize dependency findings for Hermes lineage.

This wrapper is intentionally read-only. It never invokes OSV remediation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import pathlib
import shutil
import subprocess
import sys
import uuid
from typing import Any

ACCEPTED_SCAN_EXIT_CODES = {0, 1}
SCHEMA_VERSION = "0.1.0"


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _severity_vector(vulnerability: dict[str, Any]) -> str | None:
    severity = vulnerability.get("severity")
    if not isinstance(severity, list):
        return None

    for item in severity:
        if not isinstance(item, dict):
            continue
        score = _safe_text(item.get("score"))
        if score and score.startswith(("CVSS:3.0/", "CVSS:3.1/")):
            return score

    return None


def _round_up_tenth(value: float) -> float:
    return math.ceil(value * 10.0) / 10.0


def _cvss_v3_base_score(vector: str) -> float | None:
    try:
        parts = vector.split("/")
        if parts[0] not in {"CVSS:3.0", "CVSS:3.1"}:
            return None

        metrics = dict(part.split(":", 1) for part in parts[1:])

        attack_vector = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}[
            metrics["AV"]
        ]
        attack_complexity = {"L": 0.77, "H": 0.44}[metrics["AC"]]
        scope = metrics["S"]
        privileges_required = {
            "U": {"N": 0.85, "L": 0.62, "H": 0.27},
            "C": {"N": 0.85, "L": 0.68, "H": 0.50},
        }[scope][metrics["PR"]]
        user_interaction = {"N": 0.85, "R": 0.62}[metrics["UI"]]
        impact_values = {"H": 0.56, "L": 0.22, "N": 0.0}

        confidentiality = impact_values[metrics["C"]]
        integrity = impact_values[metrics["I"]]
        availability = impact_values[metrics["A"]]

        impact_subscore = 1 - (
            (1 - confidentiality) * (1 - integrity) * (1 - availability)
        )

        if scope == "U":
            impact = 6.42 * impact_subscore
        else:
            impact = (
                7.52 * (impact_subscore - 0.029)
                - 3.25 * (impact_subscore - 0.02) ** 15
            )

        if impact <= 0:
            return 0.0

        exploitability = (
            8.22
            * attack_vector
            * attack_complexity
            * privileges_required
            * user_interaction
        )

        if scope == "U":
            return _round_up_tenth(min(impact + exploitability, 10.0))

        return _round_up_tenth(min(1.08 * (impact + exploitability), 10.0))
    except (KeyError, ValueError):
        return None


def _severity_label(vulnerability: dict[str, Any]) -> str:
    database_specific = vulnerability.get("database_specific")
    if isinstance(database_specific, dict):
        label = _safe_text(database_specific.get("severity"))
        if label:
            normalized = label.lower()
            if normalized == "medium":
                return "moderate"
            if normalized in {"critical", "high", "moderate", "low"}:
                return normalized

    vector = _severity_vector(vulnerability)
    if vector:
        score = _cvss_v3_base_score(vector)
        if score is not None:
            if score == 0:
                return "none"
            if score <= 3.9:
                return "low"
            if score <= 6.9:
                return "moderate"
            if score <= 8.9:
                return "high"
            return "critical"

    return "unknown"


def _fixed_versions(vulnerability: dict[str, Any]) -> list[str]:
    versions: set[str] = set()
    affected = vulnerability.get("affected")
    if not isinstance(affected, list):
        return []

    for item in affected:
        if not isinstance(item, dict):
            continue
        ranges = item.get("ranges")
        if not isinstance(ranges, list):
            continue
        for range_item in ranges:
            if not isinstance(range_item, dict):
                continue
            events = range_item.get("events")
            if not isinstance(events, list):
                continue
            for event in events:
                if not isinstance(event, dict):
                    continue
                fixed = _safe_text(event.get("fixed"))
                if fixed:
                    versions.add(fixed)

    return sorted(versions)


def _canonical_groups(package_result: dict[str, Any]) -> list[list[str]]:
    groups = package_result.get("groups")
    canonical: list[list[str]] = []
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, dict):
                continue
            ids = group.get("ids")
            if isinstance(ids, list):
                cleaned = sorted({str(item) for item in ids if _safe_text(item)})
                if cleaned:
                    canonical.append(cleaned)
    return canonical


def normalize_report(
    raw: dict[str, Any],
    *,
    run_id: str,
    target: pathlib.Path,
    scanner_version: str | None,
    started_at: str,
    finished_at: str,
    exit_code: int,
) -> dict[str, Any]:
    """Normalize OSV JSON without claiming exploitability."""

    findings: list[dict[str, Any]] = []
    ordinal = 0

    results = raw.get("results")
    if not isinstance(results, list):
        results = []

    for result in results:
        if not isinstance(result, dict):
            continue
        source = result.get("source")
        if not isinstance(source, dict):
            source = {}
        source_path = _safe_text(source.get("path"))
        source_type = _safe_text(source.get("type"))

        packages = result.get("packages")
        if not isinstance(packages, list):
            continue

        for package_result in packages:
            if not isinstance(package_result, dict):
                continue
            package = package_result.get("package")
            if not isinstance(package, dict):
                package = {}

            vulnerabilities = package_result.get("vulnerabilities")
            if not isinstance(vulnerabilities, list):
                vulnerabilities = []
            vulnerability_by_id = {
                str(vulnerability.get("id")): vulnerability
                for vulnerability in vulnerabilities
                if isinstance(vulnerability, dict)
                and _safe_text(vulnerability.get("id"))
            }

            groups = _canonical_groups(package_result)
            grouped_ids = {item for group in groups for item in group}
            groups.extend(
                [[vuln_id] for vuln_id in vulnerability_by_id if vuln_id not in grouped_ids]
            )

            for advisory_ids in groups:
                ordinal += 1
                primary_id = advisory_ids[0]
                advisory = vulnerability_by_id.get(primary_id, {})
                if not advisory:
                    advisory = next(
                        (
                            vulnerability_by_id[item]
                            for item in advisory_ids
                            if item in vulnerability_by_id
                        ),
                        {},
                    )

                aliases: set[str] = set(advisory_ids)
                for advisory_id in advisory_ids:
                    item = vulnerability_by_id.get(advisory_id)
                    if not isinstance(item, dict):
                        continue
                    item_aliases = item.get("aliases")
                    if isinstance(item_aliases, list):
                        aliases.update(
                            str(alias) for alias in item_aliases if _safe_text(alias)
                        )

                findings.append(
                    {
                        "finding_id": f"SEC-OSV-{run_id[-8:].upper()}-{ordinal:04d}",
                        "run_id": run_id,
                        "type": "known-vulnerable-dependency",
                        "state": "candidate",
                        "confidence": "unreviewed",
                        "severity": _severity_label(advisory),
                        "severity_vector": _severity_vector(advisory),
                        "primary_advisory_id": primary_id,
                        "advisory_ids": sorted(aliases),
                        "summary": _safe_text(advisory.get("summary")),
                        "details": _safe_text(advisory.get("details")),
                        "fixed_versions": _fixed_versions(advisory),
                        "package": {
                            "name": _safe_text(package.get("name")),
                            "version": _safe_text(package.get("version")),
                            "ecosystem": _safe_text(package.get("ecosystem")),
                        },
                        "source": {
                            "path": source_path,
                            "type": source_type,
                        },
                        "review": {
                            "scope": "unknown",
                            "reachability": "not-assessed",
                            "disposition": "unresolved",
                            "reason": None,
                        },
                    }
                )

    return {
        "schema_version": SCHEMA_VERSION,
        "run": {
            "run_id": run_id,
            "scanner": "osv-scanner",
            "scanner_version": scanner_version,
            "target": str(target.resolve()),
            "started_at": started_at,
            "finished_at": finished_at,
            "scan_exit_code": exit_code,
            "finding_count": len(findings),
        },
        "findings": findings,
    }


def _scanner_version(scanner: str) -> str | None:
    completed = subprocess.run(
        [scanner, "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    return _safe_text(completed.stdout) or _safe_text(completed.stderr)


def _write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--output", type=pathlib.Path, help="Normalized JSON output path")
    parser.add_argument("--raw-output", type=pathlib.Path, help="Original OSV JSON output path")
    parser.add_argument("--scanner", default="osv-scanner", help="OSV-Scanner executable")
    parser.add_argument("--run-id", help="Externally assigned lineage run ID")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    target = args.target.resolve()
    if not target.exists():
        print(f"error: target does not exist: {target}", file=sys.stderr)
        return 2

    scanner = shutil.which(args.scanner)
    if scanner is None:
        print(f"error: OSV-Scanner executable not found: {args.scanner}", file=sys.stderr)
        return 2

    run_id = args.run_id or f"OSV-{uuid.uuid4().hex[:16].upper()}"
    started_at = _utc_now()
    command = [scanner, "scan", "source", "-r", str(target), "--format", "json"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    finished_at = _utc_now()

    if completed.returncode not in ACCEPTED_SCAN_EXIT_CODES:
        print(completed.stderr.rstrip(), file=sys.stderr)
        print(
            f"error: OSV-Scanner failed with exit code {completed.returncode}",
            file=sys.stderr,
        )
        return completed.returncode or 2

    try:
        raw = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError as exc:
        digest = hashlib.sha256((completed.stdout or "").encode("utf-8")).hexdigest()[:12]
        print(f"error: invalid OSV JSON output ({digest}): {exc}", file=sys.stderr)
        return 2

    if not isinstance(raw, dict):
        print("error: OSV JSON root must be an object", file=sys.stderr)
        return 2

    normalized = normalize_report(
        raw,
        run_id=run_id,
        target=target,
        scanner_version=_scanner_version(scanner),
        started_at=started_at,
        finished_at=finished_at,
        exit_code=completed.returncode,
    )

    if args.raw_output:
        _write_json(args.raw_output, raw)
    if args.output:
        _write_json(args.output, normalized)
    else:
        json.dump(normalized, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")

    if completed.stderr.strip():
        print(completed.stderr.rstrip(), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
