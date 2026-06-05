# Enterprise — honest product contract

This appendix is for CISO, procurement, and platform teams. It states what Archovive **guarantees**, what requires **configuration**, and what is **not** provided.

## Tier model

| Axis | Values | Meaning |
|------|--------|---------|
| **Product tier** | `personal` / `team` / `enterprise` | Capabilities, gates, dispatch depth |
| **Pipeline tier** | `core` / `ci` / `gov` | Artifact and attestation depth (`archovive_license.json` → `pipeline_tier`) |

Doctor shows both: **Tier** (product) and **Pipeline tier** (license depth).

## Integration matrix (live vs planned)

| Integration | Code status | Live when | Deal-blocker E2E |
|-------------|---------------|-----------|------------------|
| **PagerDuty** | HTTP adapter | `PAGERDUTY_ROUTING_KEY` set | Manual / staging |
| **Slack** | HTTP adapter | `SLACK_BOT_TOKEN` or webhook | Manual / staging |
| **Jira** | HTTP adapter | `JIRA_BASE_URL` + token + project | Manual / staging |
| **ServiceNow** | HTTP adapter | Instance URL + credentials | Manual / staging |
| **GitHub** | HTTP adapter | `GITHUB_TOKEN` or App key | Manual / staging |
| **SIEM export** | Batch JSONL/CEF API + real-time HEC/webhook | `ARCHOVIVE_SIEM_REALTIME=1` + endpoint | Smoke in deal-blocker |
| **OIDC** | JWT validation | `ARCHOVIVE_OIDC_ISSUER` set | Not in default compose |
| **K8s admission** | Policy bundle + REST | Customer applies Kyverno manifest | CLI stub for apply |

**Dispatch truth:** `archovive gate` shows `Dispatch: sent …`, `dry_run`, or `failed` on stderr. Without vendor credentials, enterprise runs **dry_run** unless `ARCHOVIVE_STAGING_DEMO_LIVE=1` (demo only — not for production).

## Guaranteed (enterprise deploy)

- Single-writer / database-strong CAS when `ARCHOVIVE_STORE_BACKEND=sql` + Postgres
- Ed25519 **signed** `archovive_license.json` (fail-closed without valid signature)
- Decision contract chain: schema → verify → RBAC → authoritative upload gate
- CGE dispatch persistence (SQL backend; Postgres in production compose)

## Explicit non-guarantees

- Multi-process linearizable CAS without external consensus
- Active-active distributed store
- In-cluster admission enforcement without customer ops
- Runtime hooks as enforced product surface (env flag only today)
- Regulatory certification (roadmap)

## Production checklist

```bash
archovive setup --enterprise
archovive ops runtime doctor   # Tier, Pipeline tier, License signature, Vendor keys
cp deploy/profiles/.env.enterprise.example .env
# OIDC mandatory — set ARCHOVIVE_OIDC_ISSUER; static bearer = break-glass only
export ARCHOVIVE_BREAK_GLASS_TOKEN=…
export ARCHOVIVE_SIGNING_KEY_PATH=…
export ARCHOVIVE_MTLS_REQUIRED=1   # requires ARCHOVIVE_TLS_* paths
export ARCHOVIVE_SECURITY_AUDIT_LOG=/var/log/archovive/security_audit.jsonl
docker compose -f deploy/profiles/enterprise.yml up -d
```

Server startup **blocks** enterprise/production when:

- `ARCHOVIVE_API_AUTH_DISABLED=1`
- OIDC issuer missing (`ARCHOVIVE_OIDC_ISSUER`)
- Static `ARCHOVIVE_API_TOKEN` used without break-glass equivalence
- Default API/break-glass token or default CLI signing seed
- `ARCHOVIVE_RBAC_ENFORCE=0` or `ARCHOVIVE_ENTITLEMENT_TEST_STUB=1`
- `ARCHOVIVE_MTLS_REQUIRED=1` without readable TLS cert/key/CA files

Override for local dev only: `ARCHOVIVE_ALLOW_INSECURE_DEFAULTS=1`

## Hardening artifacts

| Artifact | Path |
|----------|------|
| Enterprise env template | `deploy/profiles/.env.enterprise.example` |
| Helm (NetworkPolicy + mTLS Ingress) | `deploy/helm/archovive/` |
| Terraform skeleton (RDS + KMS) | `deploy/terraform/main.tf` |
| Kyverno admission | `deploy/k8s/admission/kyverno-policy.yaml` |
| SBOM generator | `scripts/generate_sbom.sh` |
| Reproducible build (SLSA L2) | `scripts/reproducible_build.sh` |
| cosign sign/verify | `scripts/cosign_sign_artifacts.sh`, `scripts/cosign_verify_artifacts.sh` |
| SLSA provenance | `scripts/generate_slsa_provenance.sh` |
| Supply-chain CI | `.github/workflows/archovive-supply-chain.yml` |
| Hardening gate | `scripts/run_enterprise_hardening_gate.sh` |
| SRE runbooks | `deploy/runbooks/*.md` |

## Procurement artifacts

```bash
archovive spec procurement-pdf --out evidence/procurement/
archovive bundle export --tier enterprise --out dist/
archovive audit export --bundle
```

Internal engineering backlog: `story/docs/OPEN_POINTS.md`  
Full gap analysis: `story/docs/ENTERPRISE_GAPS.md`
