from __future__ import annotations

import importlib.util
import pathlib


SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[2]
    / "optional-skills"
    / "security"
    / "osv-dependency-audit"
    / "scripts"
    / "run_osv_scan.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("run_osv_scan", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_normalize_report_groups_aliases_as_one_candidate(tmp_path: pathlib.Path) -> None:
    module = _load_module()
    raw = {
        "results": [
            {
                "source": {"path": "uv.lock", "type": "lockfile"},
                "packages": [
                    {
                        "package": {
                            "name": "example-package",
                            "version": "1.0.0",
                            "ecosystem": "PyPI",
                        },
                        "vulnerabilities": [
                            {
                                "id": "GHSA-AAAA-BBBB-CCCC",
                                "aliases": ["CVE-2026-0001"],
                                "summary": "Example issue",
                                "database_specific": {"severity": "HIGH"},
                                "affected": [
                                    {
                                        "ranges": [
                                            {
                                                "events": [
                                                    {"introduced": "0"},
                                                    {"fixed": "1.0.1"},
                                                ]
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                "id": "PYSEC-2026-1",
                                "aliases": ["CVE-2026-0001"],
                            },
                        ],
                        "groups": [
                            {"ids": ["GHSA-AAAA-BBBB-CCCC", "PYSEC-2026-1"]}
                        ],
                    }
                ],
            }
        ]
    }

    normalized = module.normalize_report(
        raw,
        run_id="OSV-1234567890ABCDEF",
        target=tmp_path,
        scanner_version="osv-scanner version 2.x",
        started_at="2026-07-30T20:00:00Z",
        finished_at="2026-07-30T20:00:01Z",
        exit_code=1,
    )

    assert normalized["run"]["finding_count"] == 1
    finding = normalized["findings"][0]
    assert finding["finding_id"] == "SEC-OSV-90ABCDEF-0001"
    assert finding["state"] == "candidate"
    assert finding["confidence"] == "unreviewed"
    assert finding["severity"] == "high"
    assert finding["severity_vector"] is None
    assert finding["package"] == {
        "name": "example-package",
        "version": "1.0.0",
        "ecosystem": "PyPI",
    }
    assert finding["fixed_versions"] == ["1.0.1"]
    assert finding["advisory_ids"] == [
        "CVE-2026-0001",
        "GHSA-AAAA-BBBB-CCCC",
        "PYSEC-2026-1",
    ]
    assert finding["review"]["disposition"] == "unresolved"


def test_normalize_report_handles_empty_results(tmp_path: pathlib.Path) -> None:
    module = _load_module()

    normalized = module.normalize_report(
        {},
        run_id="OSV-EMPTY0000000000",
        target=tmp_path,
        scanner_version=None,
        started_at="2026-07-30T20:00:00Z",
        finished_at="2026-07-30T20:00:00Z",
        exit_code=0,
    )

    assert normalized["run"]["finding_count"] == 0
    assert normalized["findings"] == []


def test_normalize_report_converts_cvss_vector_to_category(
    tmp_path: pathlib.Path,
) -> None:
    module = _load_module()
    vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
    raw = {
        "results": [
            {
                "source": {"path": "uv.lock", "type": "lockfile"},
                "packages": [
                    {
                        "package": {
                            "name": "pyasn1",
                            "version": "0.6.3",
                            "ecosystem": "PyPI",
                        },
                        "vulnerabilities": [
                            {
                                "id": "PYSEC-2026-3455",
                                "severity": [
                                    {
                                        "type": "CVSS_V3",
                                        "score": vector,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }

    normalized = module.normalize_report(
        raw,
        run_id="OSV-CVSS00000000001",
        target=tmp_path,
        scanner_version="osv-scanner version 2.3.8",
        started_at="2026-07-30T20:00:00Z",
        finished_at="2026-07-30T20:00:01Z",
        exit_code=1,
    )

    finding = normalized["findings"][0]
    assert finding["severity"] == "high"
    assert finding["severity_vector"] == vector
    assert module._cvss_v3_base_score(vector) == 7.5
