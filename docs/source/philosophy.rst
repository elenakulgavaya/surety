Philosophy
==========

Surety is built around a single idea: **contracts define behavior.**

But to understand why contracts matter, it helps to understand what goes wrong
without them.

The Problem with Assertions
----------------------------

Traditional automated testing relies on assertions — point-in-time comparisons
scattered across test files.

At first, assertions feel productive. Coverage grows, suites expand, reports
look green. But as the system evolves, cracks appear:

- Assertions are **fragile**. A single field rename breaks dozens of tests.
- Assertions are **scattered**. The expected structure of an API response lives
  in ten different test files, each describing a partial slice.
- Assertions are **implicit**. Reading ``assert response["status"] == "active"``
  tells you nothing about the full contract — only that someone once cared
  about one field.

When assertions break, investigation begins. But only one out of four common
failure causes is an actual product bug — the rest are test code issues, data
problems, or environment instability. Teams start rerunning tests. Every rerun
decreases trust. Eventually:

    *"It's just the tests."*

At that point, automation stops being an asset.

Why Tests Lose Trust
---------------------

Tests become untrusted when they are slow, unstable, or disconnected from the
code they verify.

**Speed.** If the person waiting for results switches to another task, the
feedback loop is broken. The longer the pipeline runs, the fewer people wait
for the result. And once nobody waits — nobody cares.

**Stability.** When pipelines stay red because of "expected" failures, people
stop checking which failures are new. This is the broken window effect: once
one test is allowed to fail, the rest follow quickly. The pipeline becomes
noise.

**Data.** Shared environments accumulate state. Test data interferes with manual
testing. Scripts generate excessive records. Staging is slower and less stable
than production. As a result, tests become flaky — and flaky tests bring no
value.

The real goal is simple:

    A stable green pipeline.

Green means the system is healthy. Red means a real problem. No dashboards, no
flakiness charts, no coverage percentages — just a clear signal.

Contracts Over Assertions
--------------------------

This is where contracts change the game.

Instead of scattering assertions across tests, you **declare** what valid data
looks like — once:

.. code-block:: python

   class OrderContract(Dictionary):
       OrderId = Int(name='order_id')
       Status = String(name='status')
       Total = Decimal(name='total', f_len=2, positive=True)

A contract defines:

- Expected structure
- Allowed types and ranges
- Optional vs required fields
- Comparison rules for dynamic values

Validation becomes **structural and deterministic** — not a sequence of
scattered assertions. When something changes, the contract changes in one
place, and every test that uses it adapts automatically.

Contracts also **generate test data**. Instead of maintaining fixtures or
copying production data (with all its security, anonymization, and maintenance
overhead), contracts produce controlled, purpose-built data per test. The data
is diverse, maintainable, and risk-free.

Deterministic Validation
-------------------------

Surety does not rely on implicit truthiness or side effects.

Every validation produces a structured result:

- Success or failure
- Detailed explanation of what differs
- Precise mismatch location
- Applied and unapplied rules

No hidden behavior. No magic reporting. No implicit test state.

When tests fail, the diff tells you exactly what changed and where — reducing
investigation time from minutes to seconds.

Separation of Concerns
-----------------------

Surety separates three responsibilities:

1. **Contracts** — define expectations
2. **Execution layers** — perform interactions (API, DB, UI)
3. **Diff engine** — verify interactions

This separation makes contracts **transport-agnostic**. The same contract
validates:

- An HTTP API response
- A database record
- A UI state representation

The contract describes *what correct data looks like*, not *how it was
produced*. This means contracts survive infrastructure changes — switching from
REST to GraphQL, from PostgreSQL to DynamoDB, or from server-rendered UI to a
SPA does not invalidate your contracts.

Stable Pipelines by Design
----------------------------

Contracts directly address the root causes of pipeline instability:

**Code changes breaking tests?** Contracts are the single source of truth for
expected behavior. When a field is added, removed, or renamed, the contract
update propagates to all tests automatically. No scattered assertions to hunt
down.

**Flaky data?** Contracts generate isolated test data. No shared staging
environments, no production copies, no data interference between test runs.

**Slow feedback?** Contracts validate structure in milliseconds. Combined with
mocking (``surety-api``) and isolated environments, test suites stay fast
enough that developers remain in context while waiting.

The pipeline stays green — not because problems are hidden, but because
contracts prevent the class of issues that make tests unreliable.

Extensibility
--------------

Surety is designed as a pluggable ecosystem.

The core defines contracts, field types, and data generation. Extensions provide
execution layers and comparison engines:

- **surety-diff** — structured comparison with custom rules
- **surety-api** — HTTP interaction, mocking, and request verification
- **surety-db** — database operations and record validation
- **surety-config** — YAML-based configuration management

Plugins can extend comparison rules, add new field types, and provide new
execution adapters — without modifying the core.

Minimalism
-----------

Surety favors explicitness over convenience.

It does not:

- Generate hidden assertions
- Hide validation behind decorators
- Implicitly bind test state
- Require sophisticated reporting infrastructure

Everything is declared. Everything is verifiable.

Quality is not measured by the number of tests, coverage percentages, or
flakiness charts. It is measured by how many issues reach users — and how many
of those are regressions. Contracts protect against regressions in a way no
report ever can.

Framework, Not Utility
-----------------------

Surety is not a schema validator, a mock framework, an ORM, or a test runner.

It is a **contract-first verification framework**.

It integrates with test runners (pytest). It integrates with CI pipelines. But
it remains focused on one responsibility:

**Verifying interactions against explicit contracts.**
