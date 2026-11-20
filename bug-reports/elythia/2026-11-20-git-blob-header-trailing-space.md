# Git blob hash helper adds a stray space, so pinned-source checks always fail

- **Repo / files:**
  - `Elythia/research/ELY-0411/test_all.cjs` (line 5)
  - `Elythia/research/ELY-0404/test_dormant_order_fixed.cjs` (line 7)
  - @ `2bebcbcecb1cfe31f9f657fc83322e3ef870b174`
- **Severity:** wrong-result (the test can never pass, on any runtime)
- **Status:** confirmed, fix verified locally, issue-filed (Elythia#1)
- **Found:** 2026-11-20 by Claude (Opus 5.5)

## What happens

Both tests compute a Git blob SHA-1 of a pinned engine file and compare it to the committed hash. They always report drift:

```
AssertionError: Pinned original changed
  actual:   'a819059ff8cf421fd4b607223ca56aebb4e2506e'
  expected: '00f34db583e02a5d26b10cd526d78c40abf91025'
```

The pinned file has **not** changed. `git hash-object research/ELY-0407/engine.js` gives exactly `00f34db5…`.

## Why it happens

Git hashes `"blob " + <byte length> + "\0" + <content>`. Both helpers emit an extra space before the NUL:

```js
// ELY-0411
update(Buffer.from("blob "+b.length+" ","ascii")).update(Buffer.from([0]))
// ELY-0404 _fixed
update("blob "+Buffer.byteLength(source)+" ").update(Buffer.from([0]))
```

That hashes `"blob 10998 \0…"` instead of `"blob 10998\0…"`.

Related history: the original `ELY-0404/test_dormant_order.cjs`, `ELY-0405/test_rotation.cjs` and `ELY-0407/test_all.cjs` had a different header bug, a literal `"\\0"` (backslash, zero) from double escaping. Their `_fixed` siblings for 0405 and 0407 are correct and pass. The 0404 `_fixed` file swapped one header bug for another, and ELY-0411 appears to have copied that pattern.

## How to reproduce

From the repo root on any Node 18+:

```sh
node --test research/ELY-0411/test_all.cjs
node --test research/ELY-0404/test_dormant_order_fixed.cjs
```

## Suggested fix

Drop the trailing space. With that single change, both tests **pass** natively on Node 22.23.5 (checked in a scratch copy):

```js
Buffer.from("blob "+b.length,"ascii")            // ELY-0411
"blob "+Buffer.byteLength(source)                 // ELY-0404 _fixed
```

Elythia's preservation rules say historical files shouldn't be silently replaced, so the right home for the fix is probably new `_fixed` / `_v2` test files rather than edits. That's why this went out as an issue, not a PR.
