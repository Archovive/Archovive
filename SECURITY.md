# Security Policy — Archovive (public)

## Supported versions

| Version | Supported |
|---------|-----------|
| **1.0.x** | Yes |
| **< 1.0** | No |

## Reporting a vulnerability

**Public repository (`archovive`):**  
Report security issues in the **MIT-licensed product surface** (CLI, docs, packaging) to:

**security@archovive.com**

Please include:

- Affected version (`archovive` / `archovive-cli` tag)
- Reproduction steps (commands, minimal target, expected vs actual)
- Impact assessment (confidentiality, integrity, availability)

We aim to acknowledge reports within **5 business days**.

## archovive-core (commercial engine)

The deterministic engine (`archovive-core`) is **not** distributed in this repository.  
Vulnerabilities in the engine, hypergraph compiler, policy evaluator, proof pipeline, or golden fixtures are handled **under commercial license** with licensed customers.

- **Core access / security:** security@archovive.com  
- **Licensing:** core@archovive.com

Do **not** open public GitHub issues for unfixed core vulnerabilities before coordinated disclosure.

## Safe harbor

Good-faith security research on the **public CLI surface** is welcome when:

- You do not access customer private registries or keys without authorization
- You do not exfiltrate real tenant attestations or sovereign kits
- You follow responsible disclosure

## Artifacts never to commit

See `.gitignore`: `attest.json`, `sovereign-kit/`, `*.pem`, `ledger.jsonl`, production keys.
