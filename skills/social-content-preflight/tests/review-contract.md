# Review contract test

## Intent

The Skill must never convert incomplete evidence or a detector result into a
guarantee that content is safe or will pass platform review.

## Scenario

Given a draft containing an unsupported absolute claim and no source, while the
optional `content-compliance-checker` is unavailable:

1. The review continues without the optional detector.
2. The missing detector is disclosed.
3. The unsupported claim is flagged and rewritten with a bounded statement.
4. The verdict is not `PASS` while the evidence gap remains.
5. `human_confirmation_required` remains `true`.
6. No publication action is performed.
