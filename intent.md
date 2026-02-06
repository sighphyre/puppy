# Intent: Puppy Test Framework

## Summary
Pivot Puppy from an evaluation tool into a test framework that verifies publicly observable SDK behaviors. Puppy acts as a shim layer that can drive SDKs into specific states and then validate their externally visible behavior through normal operation (polling, metrics, registration, etc.).

## Goals
- Provide a repeatable, cross-SDK test framework focused on public, observable behavior.
- Use Puppy Server as a controllable shim to drive SDKs into known states.
- Collect evidence from standard SDK operation, not internal instrumentation.
- Support two modes:
  - Standalone mode with local hydration (existing `hydrate.sh` flow).
  - Proxy mode that sits in front of Unleash for hard validation; if Unleash rejects what we send, we fail.
- Provide a long-lived report ingestion API for scaffolded test results.

## Non-Goals (for now)
- Deep unit test coverage inside SDKs.
- Replacing existing SDK unit/integration suites.
- Mandating internal SDK APIs or private instrumentation.

## Proposed Approach
- **Shim-driven state control**
  - Puppy Server exposes controlled feature payloads and environment context.
  - It can run C&C against SDK scaffolds to move them into required states.
- **Observable behavior capture**
  - Capture HTTP interactions such as metrics posts, polling cadence, registrations, and feature evaluation outcomes.
  - Derive assertions from these captured behaviors.
- **Validation modes**
  - **Standalone**: Puppy serves features from local hydration files.
  - **Proxy**: Puppy forwards to Unleash and enforces compliance; if Unleash rejects, the test fails.

## Why This Matters
- Standardizes behavioral expectations across SDKs and versions.
- Enables regression detection for polling, metrics, and evaluation behaviors.
- Validates end-to-end behavior without relying on SDK internals.

## Open Questions
- What is the minimum common “public behavior contract” across SDKs?
- How strict should proxy validation be (e.g., fail on any Unleash rejection vs allow warnings)?
- How do we express C&C for scaffolds in a uniform way across languages?
- What data model should captured observations use to make assertions and reports?

## Next Steps
- Define the observable behavior contract (metrics schema, polling behavior, registration flow, evaluation results).
- Specify the C&C interface for driving SDK state.
- Draft a test case format that describes:
  - Desired SDK state
  - Expected observable behaviors
  - Assertion rules
- Identify MVP scope: one SDK, one test suite, one report.
