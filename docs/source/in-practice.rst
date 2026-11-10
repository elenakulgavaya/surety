In Practice: Migrating from E2E to Contract Tests
===================================================

This page walks through a real migration using Surety: 20 full-stack Playwright
tests replaced — step by step — with a contract layer that catches
frontend/backend boundary breaks before anything is deployed.

The demo app is `talkvote <https://github.com/elenakulgavaya/talkvote>`_ — a
conference talk submission and voting tool with a React frontend and a
Node/Express backend. All six pull requests are in the repo. The full narrative
and companion code PDF are at `qaexplained.com
<https://elenakulgavaya.github.io/from-e2e-to-contract-tests-practical-migration-path/>`_.

The boundary problem
--------------------

Every passing E2E test makes a silent assertion about the backend. When a test
navigates to a detail page and asserts that a title is visible, it's asserting
that the backend returns a ``title`` field the frontend reads and renders. That
dependency is a contract — it's just not captured anywhere.

The result: when the backend changes, the E2E suite catches it after deploy,
with a stack trace pointing at a timeout or a missing element, not at the
field that actually changed.

The migration makes those implicit contracts explicit, as a shared Python file
both sides import. When the contract changes, both pipelines re-run. When a
symbol disappears, every test that referenced it breaks immediately — before
anything ships.

The shared contract
--------------------

Everything in this migration flows from one file: ``api.py``. It defines the
API's request and response shapes as Surety types. Both the mock setup on the
consumer side and the real HTTP calls on the provider side import from it.

.. code-block:: python

   # api.py — the shared contract both sides import
   from surety import Dictionary, String, Int, Enum
   from surety.api import ApiContract, HttpMethod

   class Track(str, Enum):
       Frontend = 'frontend'
       Backend = 'backend'
       QA = 'qa'
       DevOps = 'devops'

   class Status(str, Enum):
       Submitted = 'submitted'
       Approved = 'approved'
       Rejected = 'rejected'

   class Talk(Dictionary):
       Id = String(name='id', required=False)
       Title = String(name='title')
       SpeakerName = String(name='speakerName')
       Track = String(name='track', default=Track.QA)
       Status = String(name='status', default=Status.Submitted, required=False)
       Votes = Int(name='votes', default=0, required=False)

   class GetTalksResponse(Dictionary):
       Talks = Array(Talk, name='talks', min_len=1, max_len=20)

   class GetTalks(ApiContract):
       method = HttpMethod.GET
       url = '/api/talks'
       resp_body = GetTalksResponse

The contract isn't a document or a team convention — it's a shared import.
When ``Status.Submitted`` is renamed to ``Status.Pending``, every file that
referenced the old name breaks at import time, in both pipelines, before
anything is merged.

Step 1 — Rewrite in Python
--------------------------

The TypeScript E2E suite was ported one-for-one to Python and Playwright. Same
files, same coverage, new language. The goal was architectural: Python's
ecosystem handles direct database access, queue draining, and service mocking
better than TypeScript. Doing the language change while the tests were still
pure browser automation — a 1:1 match with the original — decoupled the
language decision from the later architectural ones.

Step 2 — Isolate the frontend
------------------------------

The frontend tests moved off the real backend onto a mock server. Every mocked
response was built from the shared ``api.py`` types — not hand-written JSON.

.. code-block:: python

   # test_02_filtering.py
   from api import GetTalks, GetTalksResponse, Talk

   def test_filters_by_track(page: Page):
       GetTalks.reply(reset=True, times=2, body=GetTalksResponse().with_values([
           Talk() for _ in range(8)
       ]))
       page.goto("./")

       with page.expect_response(
           lambda r: "/api/talks" in r.url and r.status == 200
       ):
           GetTalks.reply(reset=True, body=GetTalksResponse().with_values([
               Talk().with_values({Talk.Track.name: 'qa'})
           ]), params={'track': 'qa'})
           page.select_option('[data-testid="filter-track"]', "qa")

       cards = page.locator("article")
       assert cards.count() > 0

``Talk()`` generates a complete, valid talk with randomised defaults.
``.with_values()`` overrides only the fields this test cares about — the rest
stay auto-generated. ``GetTalks.reply()`` registers the mock on MockServer
using the contract's own schema, so the response always matches what the
consumer contract says.

The original TypeScript suite kept running alongside the new one. Nothing was
deleted yet. The two coexisted until the new suite earned its place.

Step 3 — Prove the backend contract
-------------------------------------

Step 2 proved the frontend renders correctly when fed a conforming response.
Step 3 proved that response was actually true: real HTTP calls against the live
backend, verified against the same shared types.

.. code-block:: python

   # test_submit_talk.py
   from api import Talk, Track, Level, SubmitTalk, SubmitTalkRequest

   def test_submit_talk():
       talk = Talk().with_values({
           Talk.Track.name: Track.QA,
           Talk.Level.name: Level.Beginner,
       })
       SubmitTalk(
           req_body=SubmitTalkRequest().with_values(talk.value)
       ).request().verify()

The same ``Talk`` object Step 2 used to build mocked responses now builds a
real request body. ``.request()`` sends it; ``.verify()`` checks the response
against the contract. For fields the server controls — a generated ID, a
timestamp — rules replace exact values:

.. code-block:: python

   # calls.py — SubmitTalk.verify()
   def verify(self, **kwargs):
       super().verify_response(
           error_code=201,
           resp_body=api.SubmitTalkResponse().with_values(
               self.req_body.value
           ).with_values({
               api.SubmitTalkResponse.Status.name: api.Status.Submitted,
               api.SubmitTalkResponse.Votes.name: 0,
           }),
           rules={
               api.SubmitTalkResponse.Id.name: is_valid_uuid,
               api.SubmitTalkResponse.CreatedAt.name: precise_dates_equal_with_delta,
           }
       )

This step also surfaces coverage the original E2E suite never had. A
duplicate-vote rejection (HTTP 409) requires two browser sessions in a full E2E
test — in a contract test it's three lines, no browser:

.. code-block:: python

   def test_vote_twice_forbidden():
       talk = Talk()
       SubmitTalk(req_body=SubmitTalkRequest().with_values(talk.value)).request()
       path = TalkPathParams().with_values({TalkPathParams.Id.name: talk.Id.value})
       voter = {'X-Voter-Id': [fake.uuid4()]}
       Vote(path_params=path, headers=voter).request().verify()
       Vote(path_params=path, headers=voter).request().verify(error_code=409)

Step 4 — Verify outgoing requests
------------------------------------

Steps 2 and 3 together prove the two halves of the contract: the backend accepts
a properly-shaped request; the frontend renders correctly when fed a conforming
response. Step 4 closes the loop: does the frontend actually send a
properly-shaped request?

.. code-block:: python

   # test_04_submit_talk.py
   def test_submit_request(page: Page, talk, submit):
       api.SubmitTalk.verify_called(
           expected=api.SubmitTalkRequest().with_values({
               api.SubmitTalkRequest.Title.name: talk.Title.value,
               api.SubmitTalkRequest.SpeakerName.name: talk.SpeakerName.value,
               api.SubmitTalkRequest.Track.name: talk.Track.value,
               api.SubmitTalkRequest.Level.name: talk.Level.value,
           })
       )

``verify_called()`` inspects MockServer's request log and checks what the
frontend actually sent against the contract type. Without it, a passing frontend
test only proves the app renders correctly when given the right answer. With it,
it also proves the app asked the right question.

For requests with generated values, rules work the same way as for responses:

.. code-block:: python

   api.Vote.verify_called(
       path_params=api.TalkPathParams().with_values({
           api.TalkPathParams.Id.name: load_talk.Id.value
       }),
       headers={'X-Voter-Id': [fake.uuid4()]},
       header_rules={'X-Voter-Id': [is_valid_uuid]},
   )

Step 5 — CI trigger chain
--------------------------

Five workflows, each spinning up only the infrastructure it needs:

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Workflow
     - Triggers on PR when
     - Spins up
   * - ``contract-backend.yml``
     - ``backend_tests/**``, ``api.py``, ``src/backend/**``
     - real backend, in-job
   * - ``contract-frontend.yml``
     - ``frontend_tests/**``, ``api.py``, ``src/frontend/**``
     - MockServer + real FE build
   * - ``e2e.yml``
     - ``tests/e2e/**``
     - nothing (points at a deployed env)

``api.py`` sits in both contract pipelines' trigger paths. The chain:

1. A backend change lands → ``contract-backend.yml`` runs
2. If the backend drifts from ``api.py``, the test fails and names the exact field
3. Fixing it means updating ``api.py``
4. Updating ``api.py`` triggers ``contract-frontend.yml`` — checking whether the frontend still agrees with the updated contract

The E2E pipelines can't gate a pull request: they need a deployed application,
which only exists after merge. The contract pipelines carry no such dependency —
they gate PRs that E2E structurally cannot.

Step 6 — Remove the safety net
--------------------------------

As contract coverage solidified at the layer that owned each piece of behavior,
the redundant copy at the E2E layer was removed. Not in one big-bang deletion —
one local decision at a time: *this check is now covered by this lower-layer
test*, repeated until there wasn't much left worth keeping at the old layer.

What the contract catches
--------------------------

**Field rename.** The backend renames ``speakerName`` to ``speaker``. Without
contracts: four E2E failures across three files after deploy, all pointing at
URL timeouts. With contracts: one failure before merge, naming the exact field.
After ``api.py`` was updated, the frontend pipeline ran and ``verify_called()``
caught the outgoing request still using the old name — the half E2E would
never have seen before deploy.

**Enum rename.** ``Status.Submitted`` becomes ``Status.Pending`` in the backend.
Without contracts: the admin queue goes quietly empty; the error never mentions
a status value. With contracts: an exact ``value_changed`` diff — ``actual
'pending'``, ``expected 'submitted'`` — before merge. Updating ``api.py``
propagated to the frontend pipeline, which failed differently: four
``AttributeError`` setup failures across two files, all naming
``Status.Submitted`` as the missing symbol. The fix and the frontend update
landed in a single PR.

The difference in both cases: without contracts, the feedback arrived after
deploy, pointing at a symptom. With contracts, it arrived before merge, pointing
at the cause.

Further reading
----------------

- `Full walkthrough with CI screenshots
  <https://elenakulgavaya.github.io/from-e2e-to-contract-tests-practical-migration-path/>`_
  — the complete migration narrative at QA Explained
- `Companion PDF
  <https://elenakulgavaya.github.io/assets/files/from-e2e-to-contract-tests-companion-guide.pdf>`_
  — all eight E2E spec files and full code for every step, printable
- `talkvote repo <https://github.com/elenakulgavaya/talkvote>`_ — all six PRs,
  the full ``api.py`` contract, and the CI workflows
- :doc:`api` — full ``surety-api`` reference (``ApiContract``, ``ApiCaller``,
  ``verify_called``, ``reply``)
- :doc:`contracts` — schemas, ``with_values``, generation modes
