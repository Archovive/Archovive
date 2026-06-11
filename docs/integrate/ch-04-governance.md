# Governance — Governance

**Integrate** · [README](../../README.md) · [Docs](../README.md) · [Evaluate](../evaluate/decision-hub.md) · [← 03-ci](ch-03-ci.md) · [Next → 05-evidence](ch-05-evidence.md)

---

## Who is this chapter for?

**Tech leads, compliance engineers, and architects** who need to understand how Archovive goes from "code graph" to **regulatory verdict** — and what lives in `attestation.json` and `compliance_report.json`.

---

## Governance in one sentence

Archovive translates **architecture state** into **regulatory statements** — with rules that are reproducible, versioned, and signable.

---

## Policy packs

Policy packs are **not Excel checklists**. They are machine-readable rule sets operating on graph metrics:

| Pack | Framework | Example rule |
|------|-----------|--------------|
| `GLOBAL_BASE` | Architecture baseline | Coupling ≤ threshold |
| `DORA_2026` | DORA | Layer boundary crossings = 0 |
| `NIS2_MINIMAL_V1` | NIS2 | Critical domain instability |
| `CRA_MINIMAL_V1` | CRA | Security reachability, SBOM stubs |
| `SOX_2026` | SOX ITGC | Coupling / boundary for finance IT |

The OSS demo evaluates three rules live. Enterprise bundle: all packs including Ed25519 `.json.sig` signatures.

**Why this is the moat:** SAST tools do not know DORA articles. GRC tools do not compile a repository into a graph. Archovive connects both.

---

## Drift matrix

The drift matrix describes **deviation from a stored baseline** (enterprise bundle):

```text
$ archovive diff baseline/ HEAD
  boundary_crossing ... api→payments.ledger
  drift_score ......... 0.42
Exit Code: 1
```

| Field | Meaning |
|-------|---------|
| `drift_status: unmeasured` | First run — **no risk signal**, neutral only |
| `drift_status: measured` | Baseline exists — deviation computed |
| `drift_score: null` | No numeric score without baseline |
| `drift_score: 0.0–1.0` | With baseline — higher = more structural drift |

**Important:** `unmeasured` or `null` does **not** mean "medium risk". Drift scores become meaningful only after `archovive init` / baseline storage.

Structural classes (enterprise): topological, semantic, behavioral — in `drift_matrix.json`.

**Surface:** CLI `archovive diff` (enterprise bundle) · CI artifact `drift_matrix.json` · MCP via `archovive-mcp` (enterprise bundle).

---

## Verdicts

| Verdict | Meaning | Typical CI reaction |
|---------|---------|---------------------|
| `APPROVED` | All policies passed | Allow merge / release |
| `POLICY_VIOLATION` | Regulatory rule violated | Exit 2 — block |
| `DRIFT_VIOLATION` | Architecture deviates from baseline | Exit 1 — block |
| `OVERRIDE_REQUIRED` | Human decision needed | Workflow / ticket |

In enterprise, `archovive gate` materializes the verdict as a **decision contract** — signed JSON with `decision_id`, `lookup_key`, timestamp.

---

## Attestation schema (overview)

Governance produces an **evidence set** — machine-readable, linked, hash-chained:

```
Repository
    → Graph (graph_hash)
    → Policy results (compliance_report.json)
    → Verdict (attestation.json)
    → Replay pin (repro.json / replay_hash)
```

Three **cameras** (perspectives on the same result):

| Camera | Buyer | Main artifact |
|--------|-------|---------------|
| **Operator** | Humans | `ARCHOVIVE_OUTPUT.md` |
| **Machine** | CI/CD | `repro.json`, `drift_matrix.json` |
| **Evidence** | Auditors | `attestation.json`, SBOM, verify chain |

Details → [Evidence](../integrate/ch-05-evidence.md)

---

## Truth surfaces (enterprise)

These three commands **must give identical answers** — parity guarantee:

```bash
archovive ask "why blocked?"
archovive chat "why blocked?"
archovive governance decide --json
```

No separate "chat knowledge". One kernel truth, multiple surfaces (CLI, MCP, CI).

---
