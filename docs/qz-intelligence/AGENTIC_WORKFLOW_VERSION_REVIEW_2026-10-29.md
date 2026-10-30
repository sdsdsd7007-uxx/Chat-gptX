# Agentic Workflow Tooling — Version Review
**Review date:** 2026-10-29  
**Decision:** Evaluate in read-only sandbox only; do not activate in production from this review.

The official GitHub Agentic Workflows repository showed v1.0.1 as the latest release checked for this review, published 2026-10-27. GitHub's general availability announcement was published 2026-10-28.

The repository records an earlier retired release range (v0.83.3 through versions below v0.85.4). A separate GHSL-2026-180 security advisory identifies a command-argument handling issue affecting versions below v0.91.12 and identifies v0.91.12 as fixed. These represent separate historical release/advisory points, so version string alone is not the acceptance criterion.

Before testing:
- Verify the exact release artifact and current upstream advisories.
- Start with read-only tasks in an isolated environment.
- Minimize connector permissions and keep network/data access bounded.
- Require independent pull-request review and normal CI checks for generated changes.
- Stop evaluation if the tool exceeds its assigned scope.

No Agentic Workflow has been installed or activated by this note.

Sources:
- GitHub GA announcement: https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/
- v1.0.1 release: https://github.com/github/gh-aw/releases/tag/v1.0.1
- GHSL-2026-180 advisory: https://github.com/github/gh-aw/security/advisories/GHSA-f7r8-5pqp-q5p4
- Official repository: https://github.com/github/gh-aw