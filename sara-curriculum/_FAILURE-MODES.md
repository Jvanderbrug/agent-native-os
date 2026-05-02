# Live Workshop Failure Modes

**For:** Tyler (alignment + decision)
**Authored:** 2026-04-30
**Source:** Sara's April 16 live walkthrough of Components 0–9 as a student. The failure modes captured here are real friction points she hit; everything else is extrapolated from the same root patterns.

---

## TL;DR — Why this needs to be addressed before May 3

The Claude Code workshop is a **one-day live install**. We have 6–8 hours to get 30+ non-technical students from zero to a working overnight agent. If a student gets stuck on a silent failure for 30+ minutes, they fall behind a Component, and recovery requires either a TA stopping the room or the student leaving partially built.

Sara's April 16 walkthrough surfaced two failure patterns that **will hit students live**:

1. **The macOS silent-failure pattern.** macOS denies operations (file writes, MCP access, scheduled jobs) without raising an error. Claude reports success because *its own code* finished. Student sees no error. Nothing works. They blame themselves.
2. **The credential-leak pattern.** Claude inspects shell config or env files and pastes raw API keys into the chat. With 30+ students live, this is 30+ simultaneous credential leaks — across Slack screenshots, Zoom recordings, exported transcripts.

Both patterns are workshop-killers. Both are preventable.

---

## The 8 silent failure modes

Ranked by likelihood × severity. "Severity" = how long it takes to unblock a student.

### 1. Full Disk Access (FDA) not granted to Claude.app

**Likelihood:** Very high — every macOS user starts here.
**Severity:** Medium — 30 sec to fix once spotted.

| | |
|---|---|
| **Symptom** | Brief reports "Saved." Student opens Finder. No file. |
| **Real cause** | macOS silently blocks the write. Claude's code completes successfully; macOS just refuses. |
| **Diagnostic** | Ask: did the file appear in Finder? If no → check System Settings → Privacy & Security → Full Disk Access → is Claude.app toggled ON? |
| **Fix** | Add Claude.app to FDA list. Restart Claude. |
| **Pre-work mitigation** | Walk students through granting FDA before workshop day. Provide screenshots for macOS 15 *and* 16 (UI differs). |

---

### 2. Wrong app gets FDA

**Likelihood:** High — the docs/curriculum say "your terminal" and students grant Terminal.app instead of Claude.app.
**Severity:** Medium — same as #1, but harder to spot.

| | |
|---|---|
| **Symptom** | Identical to #1. File not landing despite "Saved." |
| **Real cause** | Student followed instructions referencing "terminal" but is using the Claude desktop app. FDA on Terminal.app does nothing for Claude.app. |
| **Diagnostic** | "Which app are you running Claude inside? Open it from your Dock and tell me what icon you clicked." |
| **Fix** | Grant FDA to the app they're actually running. |
| **Pre-work mitigation** | Curriculum copy must say **"the app you launched Claude from"**, not "your terminal." Sara's CLAUDE.md teaching prep already flags this; needs to propagate to student-facing copy. |

---

### 3. 1Password CLI not signed in

**Likelihood:** High — `op` sessions time out after 30 min by default.
**Severity:** Low — 60 sec to fix.

| | |
|---|---|
| **Symptom** | MCPs that depend on `op read "op://..."` show "Failed to connect" in `/mcp`. |
| **Real cause** | The wrapper script tries to fetch the API key from 1Password, but `op` requires an active session. No session → returns nothing → MCP launches with no API key → fails. |
| **Diagnostic** | Run `op whoami` in a terminal. If it errors → not signed in. |
| **Fix** | `op signin` then restart Claude (so the MCP wrappers run with a fresh `op` session). |
| **Pre-work mitigation** | Configure 1Password CLI session timeout to "until logout" instead of 30 min. Document this as part of the setup guide. |

---

### 4. The launchd "silence = success" wall

**Likelihood:** Universal — every student hits this.
**Severity:** High — students don't know if their job worked, can't self-verify, and won't realize until tomorrow morning when no brief appears.

| | |
|---|---|
| **Symptom** | `launchctl bootstrap` runs. Returns nothing. Student stares at the terminal. "Did it work?" |
| **Real cause** | macOS launchctl follows Unix convention: silence on success. Non-technical users read this as failure. |
| **Diagnostic** | Run `launchctl list \| grep <job-label>`. If the job appears → loaded. If empty → didn't load. |
| **Fix** | This is a curriculum-design fix, not a runtime fix: **every launchd command in the curriculum must be paired with a verification command and an expected output.** Don't leave students staring at silence. |
| **Pre-work mitigation** | N/A — this is a curriculum fix. Sara's Component 9 walkthrough captured this as Gotcha #4. |

---

### 5. Shell environment not loaded in launchd

**Likelihood:** High — anyone who skips the wrapper-script step will hit this.
**Severity:** High — the scheduled job will run but every MCP that needs an API key will fail. Student sees "Saved" with no Exa, no 1Password, no Firecrawl. They won't know why until they read the logs.

| | |
|---|---|
| **Symptom** | The 4am scheduled job runs. The brief appears. But the Signal section is empty/sparse and Exa/Firecrawl/etc. all show as failed in the brief output. |
| **Real cause** | launchd runs jobs with a **minimal environment** — it does NOT source `~/.zshrc`. So `EXA_API_KEY`, `FIRECRAWL_API_KEY`, `OP_SERVICE_ACCOUNT_TOKEN`, etc. are all missing at runtime. |
| **Diagnostic** | Read the stderr.log for the launchd job. Look for "API key missing" or "auth failed" patterns. |
| **Fix** | Wrap the `claude` invocation in a shell script that sources `~/.zshrc` first. Sara's `morning-brief-launcher.sh` does exactly this. |
| **Pre-work mitigation** | N/A — this is built into the curriculum already. Risk is only if a student skips the wrapper step. |

---

### 6. OAuth blocked or wrong account selected

**Likelihood:** Medium — depends on student's setup. Higher for B2B accelerator audience (corporate-managed laptops).
**Severity:** Very high — often NOT fixable in 5 minutes. May require stopping the room or moving the student to a personal machine.

| | |
|---|---|
| **Symptom** | "Authorize Claude" browser flow fails, hangs, or completes but MCP still shows "Failed to connect." |
| **Real cause** | Possibilities: (a) corporate Google Workspace blocks third-party OAuth apps by default; (b) student authorized with their personal Gmail but their work calendar is on a different account; (c) 2FA loop, "unusual activity" challenge, or browser cookie issues. |
| **Diagnostic** | "Did the browser show 'Approved' before redirecting back? What email did you authorize?" |
| **Fix** | Often requires admin intervention from student's IT department, or switching to a personal Google account. Not fixable on workshop day. |
| **Pre-work mitigation** | **Mandatory pre-work step: students must successfully authorize Gmail and Calendar MCPs at least 48 hours before workshop day**, on the same machine they'll use during the workshop. If this fails in pre-work, escalate to a 1:1 setup call. |

---

### 7. npx download fails or hangs

**Likelihood:** Medium — depends on network conditions.
**Severity:** Medium — usually fixable with a workaround.

| | |
|---|---|
| **Symptom** | MCP shows "Failed to connect." First-time launches hang for 30+ seconds. |
| **Real cause** | `npx -y exa-mcp-server` (or similar) downloads the package on first run. Slow network, corporate proxy, npm registry issues, or stale npm cache can all break this. |
| **Diagnostic** | Run the wrapper script manually in a terminal. Watch for npx output. Does it hang? Error? Complete but timeout? |
| **Fix** | Pre-install MCP server packages globally: `npm install -g exa-mcp-server`. Then update wrapper to call the installed binary directly instead of `npx -y`. |
| **Pre-work mitigation** | Have students run all MCP wrappers once during pre-work. First-run downloads happen offline-of-the-workshop, so day-of is cache-warm. |

---

### 8. Non-interactive `claude -p` silently skips OAuth-based MCPs

**Likelihood:** Universal — every student who uses launchd or any other unattended scheduling will hit this.
**Severity:** Very high — student's 6am brief runs but is missing entire data sources, and the failure is silent.

*Discovered live 2026-04-30 during Sara's Component 9 walkthrough resumption. Originally not in the April 16 list because that walkthrough never got past the FDA bug to test launchd behavior.*

| | |
|---|---|
| **Symptom** | Scheduled morning brief runs at 6am. The brief lands. But Gmail (and possibly Calendar) sections are empty or sparse. Brief output explicitly says "permission not granted this run" for those MCPs. Student wakes up to a half-broken brief with no clear cause. |
| **Real cause** | OAuth-based MCPs (Gmail, Calendar) require Claude to prompt the user for permission to use the integration. In interactive mode, Claude pops a dialog and the user clicks Approve. In non-interactive `claude -p` mode (used by all launchd-fired scheduled runs), there is no human to click Approve, so Claude silently denies the MCP and continues without it. |
| **Diagnostic** | Run the brief twice: once interactively (`/morning-brief` in chat) and once via `launchctl kickstart`. If interactive works and kickstart shows "permission not granted" for some MCPs → this is the gotcha. |
| **Fix** | Add `--permission-mode bypassPermissions` to the `claude -p` invocation in the wrapper script: `claude -p --permission-mode bypassPermissions "/morning-brief"`. This flag is the right named affordance for unattended scheduled runs (cleaner than `--dangerously-skip-permissions`, which is the same effect but named to scare you). |
| **Pre-work mitigation** | Curriculum must include the flag in the wrapper template students copy. A callout box explains why: "Claude is designed for an interactive human-in-the-loop. launchd takes the human out of the loop, so Claude needs to be told the human has pre-authorized everything." |

**Curriculum framing:** This gotcha is **the inverse of the credential-leak pattern.** Gotcha #6 (the credential leak) is "Claude does too much without thinking." Gotcha #8 is "Claude does too little because there's no one to ask." Both come from the same root: Claude's interactive design colliding with unattended scheduling. The curriculum needs a section explicitly framing this tradeoff so students understand both extremes.

---

## The credential-leak pattern (the one that hit Sara live)

**This is the security failure mode and it's separate from the silent-failure category.** It's the *opposite* — Claude succeeds at something it should NOT have done.

### What happened

During Sara's April 16 walkthrough, Claude was troubleshooting why launchd-loaded MCPs weren't getting API keys. Earlier in the session it had used a redacted approach to inspect environment variables. Later in the same session it lost that pattern and ran:

```bash
head -30 ~/.zshrc
```

This pasted Sara's real `OP_SERVICE_ACCOUNT_TOKEN`, `GRAND_CENTRAL_API_KEY`, and `FIRECRAWL_API_KEY` into the visible chat transcript. Tyler had to rotate all three credentials.

### Why this is a workshop catastrophe

With 30+ students live:
- If Claude does this for one student, that student's transcript is leaked to the Zoom recording, Slack screenshots, exported logs, and any other participants watching their screen.
- If Claude does this for multiple students simultaneously (likely — they're all running the same curriculum on the same patterns), we have **30 simultaneous credential leaks** with multiple distribution surfaces.
- We can't post-hoc redact a Zoom recording or pre-recorded transcript.

### What must change before May 3

**1. Workshop CLAUDE.md template (the one each student installs in Component 1) must include a redaction Standing Rule that applies to the agent, not just the human:**

> **Standing Rule — Never inspect raw secrets.** Before reading any environment file (`.zshrc`, `.bashrc`, `.env`, `.envrc`, etc.) or running commands that output environment variables, redact any line matching: `*_KEY=`, `*_TOKEN=`, `*_SECRET=`, `*_PASSWORD=`, `op://*` references, AWS access patterns (`AKIA*`), or anything that looks structurally like a credential. Never paste raw env contents into chat. If diagnosing a credential issue, use `grep -c` (count only) or `wc -l` (line count) instead of `head`/`cat`. If a real value must be inspected, ask the user to read it from a private terminal and paste only the part needed.

**2. Pre-work hardening:**
- Every student rotates pre-existing API keys after the workshop (in case Claude leaks during the day despite the rule).
- 1Password references (`op://...`) are taught from day one. Inline keys in `.zshrc` should be discouraged in pre-work.
- The pre-work setup guide explicitly tells students NOT to put real API keys in shell config files; use 1Password instead.

**3. Live monitoring:**
- TAs are briefed to scan visible chat windows during the day for any obvious credential strings.
- A "If you see a leaked key, raise hand silently" instruction at the start of the day so students don't loudly broadcast a leak in chat.

**4. Post-workshop:**
- Sweep all Slack threads, Zoom recordings, and exported transcripts before publishing anything.
- Provide students a "rotate your keys after this workshop" instruction in the wrap-up.

---

## Other day-of risks worth flagging

These are lower-likelihood than the seven above, but each one has bitten at least one Foundations student in past cohorts.

- **macOS version variation (15 vs 16).** Privacy & Security UI is different. TAs need screenshots for both.
- **Apple Silicon vs Intel.** Older Macs lag on MCP startup; first-run npx downloads are slower.
- **Corporate-managed laptops.** Some students will have IT-locked machines that block OAuth, npx, or Full Disk Access changes. **Pre-work must flag this:** *"If your work laptop is managed by an IT department, use a personal machine for the workshop or expect failure."*
- **Existing Claude Code installs.** Students with stale `~/.claude.json`, conflicting MCP configs, or old skill folders may have ghosts. Pre-work should include a "clean reset" option.
- **Anthropic API rate limits.** 30 students hitting Claude simultaneously during the same exercise — confirm the workshop is run on plans with sufficient throughput. (Max 5x/Max 20x mix?)
- **Time-of-day for OAuth.** Google's OAuth occasionally hits friction (CAPTCHAs, "unusual activity" challenges). Aim for non-peak hours if scheduling allows.
- **Internet dropouts.** A student who loses connectivity mid-MCP-install leaves the install half-done. Pre-work should include "ensure stable connection."

---

## Recommended next steps (Sara → Tyler decision needed)

Two artifacts come out of this:

### Artifact 1 — Pre-work hardening checklist

A "before workshop day" checklist students must complete and verify. Each item maps to one of the 7 failure modes above. If a student can't pass the checklist, they get individual help BEFORE the day, not during it.

Proposed items:
- [ ] Granted Full Disk Access to Claude.app (with screenshot proof)
- [ ] 1Password CLI signed in with extended session timeout
- [ ] Gmail + Calendar MCPs successfully authorized on workshop machine
- [ ] All MCP server packages pre-installed globally (warm npm cache)
- [ ] On macOS 15 or 16; on Apple Silicon (or flag if Intel)
- [ ] Personal laptop (or IT-cleared work laptop with FDA permission already granted)
- [ ] Stable internet connection confirmed
- [ ] Existing Claude Code config cleaned (or fresh install)
- [ ] Read the redaction Standing Rule and confirmed it's in their CLAUDE.md template

### Artifact 2 — TA live-day triage card

A one-page reference TAs use during workshop day. Each row = one failure mode. Each row has:
- The failure name
- The 30-second diagnostic question to ask
- The fix
- The escalation trigger (when to stop the room vs. unblock individually)

Pinned in the workshop Slack. Possibly laminated for in-person events.

### Artifact 3 — Standing Rule update for the workshop CLAUDE.md template

Add the redaction rule (above) to the template students install in Component 1. This is the **single highest-leverage fix** because it prevents the credential-leak pattern at its root.

---

## Status & open questions for Tyler

- [ ] Approve writing up Artifact 1 (Pre-work hardening checklist) — Sara to draft?
- [ ] Approve writing up Artifact 2 (TA live-day triage card) — Sara to draft?
- [ ] Approve adding the redaction Standing Rule to the workshop CLAUDE.md template — Sara to propose exact wording?
- [ ] Decide: do we add a 1:1 pre-workshop setup call requirement for any student who fails the checklist? (Adds support overhead but prevents day-of meltdowns.)
- [ ] Decide: do we add a "rotate your keys after this workshop" instruction in the close-out, regardless of whether anything visible leaked? (Defense in depth.)

---

## Source material

- `workshop/sara-teaching-prep/TYLER-ALIGNMENT-scheduling.md` — Component 9 alignment doc with the original 6 gotchas Sara captured live
- `workshop/sara-teaching-prep/SESSION-HANDOVER-2026-04-16.md` — full session context from the day the security incident happened
- `workshop/sara-teaching-prep/SESSION-HANDOVER-2026-04-30.md` — recovery session, with both bugs verified fixed
- `workshop/student-guide/09-scheduling.md` — provisional Component 9 student guide (banner-marked PROVISIONAL pending Sara's full walkthrough)

---

### 9. iMessage SQLite polling fails when iCloud Messages sync is enabled

**Likelihood:** High — iCloud Messages sync is the default and most students will have it on.
**Severity:** High — Component 11 (Remote Control) can't use iMessage polling on these setups.

| | |
|---|---|
| **Symptom** | Messages appear in the Messages app on Mac, but never show up in `~/Library/Messages/chat.db` (or appear very late). The poller script finds nothing to process. |
| **Real cause** | When `CloudKitSyncingEnabled = 1` in Messages preferences, incoming messages are stored in iCloud rather than written to the local SQLite database immediately. The local database becomes a partial cache — not a reliable trigger source. |
| **Diagnostic** | Run: `defaults read com.apple.madrid | grep CloudKitSyncingEnabled` — if result is `1`, the SQLite polling approach won't work reliably. |
| **Fix** | Don't use iMessage SQLite polling as the Remote Control trigger. Use native Claude Code Remote Control first. Use Claude Code Channels for iMessage/Telegram/Discord if you need app-based messaging. Treat the old iOS Shortcut + queue pattern as fallback. |
| **Pre-work mitigation** | N/A — this is a design decision, not a student error. The Component 11 curriculum must use the SSH queue approach (works regardless of iCloud sync setting). |

**Note discovered during Sara's April 30 student walkthrough:** The first self-message DID appear in the database (creating the conversation entry), but all subsequent messages in the same conversation were iCloud-only. This is consistent with iCloud handling conversation creation locally but keeping message content in the cloud.


---

### 10. Remote Control (Component 11) breaks on multi-turn conversations

**Likelihood:** Very high — most real-world tasks require at least one clarifying question.
**Severity:** High — students spend 10-15 minutes on a task that should take 30 seconds.

| | |
|---|---|
| **Symptom** | Student sends a command. Claude replies asking a clarifying question. Student replies. Nothing happens. Student sends another message. Eventually gives up or comes back to the TA. |
| **Real cause** | The iMessage poller processes each incoming message in isolation with zero conversation context. When Claude asks "which meeting?" and the student replies "today's," Claude receives just the word "today's" with no idea what question was asked. Every turn is a fresh conversation. |
| **Diagnostic** | Ask: did Claude reply asking a clarifying question? If yes → this is the failure mode. |
| **Fix** | Two options: (1) Constrain Component 11 to one-shot commands only — teach students to write complete, unambiguous commands that don't require follow-up. (2) Replace iMessage with Slack — Slack threads maintain context across turns. |
| **Pre-work mitigation** | If keeping iMessage: the student guide must explicitly say "Write complete commands. If Claude asks a follow-up, start a new Shortcut invocation with the full request rewritten, not a reply." |

**Sara's April 30 experience:** Tried to decline a recurring team meeting via iMessage remote control. Claude asked "which meeting?" four times across the conversation because each reply arrived with no context. The meeting was never declined via remote control — had to be declined manually via Calendar MCP. Total time: ~20 minutes for a 30-second task.

**Curriculum recommendation for Tyler:** Component 11 must either (a) demo ONLY one-shot commands in the workshop (e.g. "What's on my calendar today?" — no clarification needed), or (b) be redesigned around Slack which supports threaded conversation context.

---

### 11. Native iMessage Channels can collapse into self-chat

**Likelihood:** Medium for Mac students testing iMessage with their own Apple ID.
**Severity:** Medium - it works technically, but the experience can feel confusing or unserious.

| | |
|---|---|
| **Symptom** | Student texts the native iMessage Channel and gets replies in the same self-message thread, as if they are talking to themselves. Messages can look doubled or hard to distinguish from the user's own texts. |
| **Real cause** | The native iMessage Channel is using the same Apple Messages identity and local Messages surface as the user. That is convenient for setup, but it does not create a separate agent persona or separate contact. |
| **Diagnostic** | Ask: does the thread show the student messaging themselves, or does it show a separate agent contact? If it is the self-thread, this is expected for the simple native setup. |
| **Fix** | For workshop demos, use native Remote Control, Telegram, fakechat, or native iMessage only as a quick demo. For production, use the dedicated agent identity pattern: a separate Apple ID/iMessage identity on a dedicated host machine, like Gigawatt on the M1 Max. |
| **Pre-work mitigation** | Tell students the self-chat behavior is normal for the simple path. Frame dedicated-agent iMessage as an 8D/Lab upgrade, not a required Sunday setup. |

**Tyler's setup note:** The original native iMessage Channel felt wonky because it replied in the same self-thread. The better AI Build Lab pattern is Gigawatt as its own agent entity with its own iCloud/iMessage identity, so Tyler sees messages from Gigawatt as a separate contact.
