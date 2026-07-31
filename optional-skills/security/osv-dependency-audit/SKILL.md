---
name: osv-dependency-audit
description: Use when auditing project dependencies for known vulnerabilities with OSV-Scanner.
version: 0.1.0
author: Harness Cognitivo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, dependencies, osv, vulnerabilities, supply-chain]
    related_skills: [oss-forensics]
---

# OSV Dependency Audit

## Overview

Use OSV-Scanner as a deterministic dependency scanner, then treat every result as a **candidate finding** until reachability and project context are reviewed. This skill does not authorize package upgrades or automatic remediation.

The workflow keeps the Hermes core narrow: OSV-Scanner remains an external CLI, while this skill controls invocation, normalization, evidence capture, and handoff to later review stages.

## When to Use

Use this skill when:

- a repository contains package manifests or lockfiles;
- dependencies changed in a pull request;
- a release or security review needs a supply-chain check;
- a known vulnerability must be located in the dependency graph;
- a container or source tree needs an OSV-backed vulnerability inventory.

Do not use it as proof that an application is exploitable. A vulnerable package may be unreachable, test-only, development-only, or blocked by project controls.

## Preconditions

1. Confirm `osv-scanner` is installed and print its version:

   ```bash
   osv-scanner --version
   ```

2. Prefer a pinned major version. The wrapper expects the OSV-Scanner v2 command surface.

3. Run from a clean or intentionally dirty working tree and record the current commit:

   ```bash
   git rev-parse HEAD
   git status --short
   ```

Completion criterion: scanner version, target repository, commit, and working-tree state are known before the scan starts.

## Standard Scan

Run the bundled wrapper from the repository root:

```bash
python optional-skills/security/osv-dependency-audit/scripts/run_osv_scan.py \
  --target . \
  --output .hermes/artifacts/security/osv/latest.normalized.json \
  --raw-output .hermes/artifacts/security/osv/latest.raw.json
```

The wrapper:

- executes `osv-scanner scan source -r <target> --format json`;
- accepts exit code `0` for no findings and `1` for findings;
- rejects scanner execution failures;
- preserves the original JSON when `--raw-output` is provided;
- emits normalized candidate findings with lineage-friendly IDs;
- never runs `osv-scanner fix`.

Completion criterion: both the scanner execution status and normalized report are available, or the wrapper exits with a clear failure.

## Direct Commands

Human-readable recursive source scan:

```bash
osv-scanner scan source -r .
```

Machine-readable recursive source scan:

```bash
osv-scanner scan source -r . --format json > osv-results.json
```

Single lockfile scan:

```bash
osv-scanner scan -L path/to/lockfile --format json > osv-lockfile-results.json
```

Do not hide stderr when diagnosing failures; OSV-Scanner sends non-JSON operational output there.

## Finding Lifecycle

Every normalized OSV result begins as:

```text
candidate -> confirmed | rejected -> fixed -> verified
```

For each candidate:

1. **Locate** the manifest or lockfile and affected package.
2. **Classify scope** as runtime, development, test, build, optional, or unknown.
3. **Check reachability** when supported by the ecosystem or by code inspection.
4. **Review controls** that may block practical exploitation.
5. **Deduplicate aliases** such as CVE, GHSA, and ecosystem advisory IDs.
6. **Assign confidence** only after evidence review.
7. **Propose remediation** without changing dependencies unless explicitly authorized.
8. **Re-scan after remediation** and preserve both before and after reports.

Completion criterion: each reported candidate has an explicit disposition or remains visibly unresolved; silence is not rejection.

## Severity and Confidence

Keep severity and confidence separate:

- **Severity** describes potential impact from advisory data.
- **Confidence** describes how strongly the project evidence supports the finding.

Never increase severity because a title sounds alarming. Never mark a finding as confirmed solely because OSV-Scanner returned it.

## Required Evidence

A reviewed finding should retain:

- normalized finding ID;
- scan run ID;
- scanner version;
- repository commit;
- source manifest or lockfile;
- package, version, and ecosystem;
- primary advisory ID and aliases;
- advisory severity data when present;
- dependency scope;
- reachability evidence or reason it is unavailable;
- decision: confirmed, rejected, or unresolved;
- reviewer identity or agent role;
- remediation and verification links when applicable.

## Safety Rules

- Do not execute remediation automatically.
- Do not edit lockfiles merely to make the report green.
- Do not suppress a finding without a written reason.
- Do not treat absence of a fixed version as permission to ignore the issue.
- Do not expose private dependency names or repository paths in public reports.
- Prefer read-only scans in the first pass.

## Common Pitfalls

1. **Treating exit code 1 as a tool failure.** OSV-Scanner uses a non-zero code when vulnerabilities are found. The wrapper accepts 0 and 1.
2. **Counting aliases as separate vulnerabilities.** CVE, GHSA, and ecosystem IDs can describe the same issue. Use grouped IDs when available.
3. **Confusing package presence with exploitability.** Add reachability and usage evidence before confirmation.
4. **Scanning only manifests without lockfiles.** Prefer lockfiles because they represent resolved versions.
5. **Using experimental remediation unattended.** Keep dependency changes under explicit authorization and normal review.
6. **Losing the raw report.** Preserve raw JSON for auditability when the result matters.
7. **Sending the entire report to every agent.** Route only the candidate and evidence relevant to that specialist.

## Verification Checklist

- [ ] OSV-Scanner version recorded
- [ ] Repository commit and working-tree state recorded
- [ ] Correct source tree or lockfile scanned
- [ ] Raw JSON preserved for consequential scans
- [ ] Normalized candidate IDs generated
- [ ] Aliases deduplicated where grouping data exists
- [ ] No automatic fix executed
- [ ] Every candidate has an explicit review state
- [ ] Re-scan performed after any authorized remediation
- [ ] Before/after artifacts linked in operational lineage
