# Cairns Personalization Vault Fixture

This fixture shows the expected day-one output from `/personalize` plus `cairns-init` in 4D mode.

It is intentionally local and markdown-only. It does not include Supabase, Neo4j, Docker, remote sync, credentials, or personal data.

Use it to QA:

- The L1 files exist and stay short.
- The lazy files are absent at init.
- The privacy ignore content is represented by `gitignore.expected`.
- `/log-decision` can add the first decision card and create `my-decisions.md`.
