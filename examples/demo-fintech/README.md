# Demo fintech microservice (OSS simulate fixture)

Small multi-service Python layout with **intentional** architecture violations:

- API layer imports `payments.ledger` directly (DORA boundary crossing)
- High coupling between `api`, `payments`, and `notifications`
- Use with: `archovive simulate` or `archovive ci check --repo examples/demo-fintech`

This is not production code — it exists so you see a real verdict in 30 seconds.
