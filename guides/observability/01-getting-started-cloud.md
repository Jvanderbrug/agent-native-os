# 01 — Langfuse Cloud Quickstart

**Goal:** In ten minutes, have a working Langfuse account, two API keys stored safely, and your first trace visible in the dashboard.

This is the fastest possible "hello world" for agent observability.

---

## Step 1: Sign Up

Go to [cloud.langfuse.com/auth/sign-up](https://cloud.langfuse.com/auth/sign-up) and create an account. You can use email + password, or sign in with Google or GitHub.

The free tier is real — no credit card needed to start, and the included monthly event volume is enough for serious individual use.

### Pick a Region

Langfuse Cloud has multiple regions. The signup flow asks you to pick one.

| Region | Host | Best for |
|---|---|---|
| EU | `https://cloud.langfuse.com` | EU residents, GDPR concerns |
| US | `https://us.cloud.langfuse.com` | North America |
| Japan | `https://jp.cloud.langfuse.com` | APAC |
| HIPAA | `https://hipaa.cloud.langfuse.com` | US healthcare |

Pick the one closest to where you and your agents run. You cannot easily move regions later, so think for thirty seconds before choosing. If you have no opinion and you're in North America, use US.

---

## Step 2: Create A Project

Once you're logged in, you'll be prompted to create an organization, then a project inside it.

**Naming convention we recommend:**
- Organization: your handle or company (e.g., `tyler-aibl`)
- Project: the agent fleet or use case (e.g., `personal-agents`, `client-work`, `experiments`)

You can have multiple projects under one org. Use them to keep distinct workloads separate. For example, the AI Build Lab production fleet uses one project for the agent fleet itself and a separate project for financial pipelines, so traces don't intermingle in dashboards or alerts.

---

## Step 3: Generate API Keys

Inside your project, go to **Settings → API Keys → Create new API keys**.

You'll get three values:

```
LANGFUSE_PUBLIC_KEY = pk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_SECRET_KEY = sk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_HOST       = https://us.cloud.langfuse.com   # or your region
```

**Copy them now.** The secret key is shown only once. If you lose it, you have to rotate.

> Note: the official docs sometimes call this `LANGFUSE_BASE_URL`. The Python SDK accepts both `LANGFUSE_HOST` and `LANGFUSE_BASE_URL`. We'll use `LANGFUSE_HOST` throughout this module because it's what the Claude Code hook ecosystem standardized on.

---

## Step 4: Store The Keys Safely

Do not paste these into a config file you might commit to git.

**The right way (1Password):** If you've worked through Guide 05 already, create a 1Password item:

- Vault: your personal vault
- Item type: API Credential
- Title: `Langfuse Cloud — Personal`
- Fields: `public_key`, `secret_key`, `host`

Right-click each field and copy the secret reference. You'll get `op://` paths like `op://Personal/Langfuse Cloud — Personal/secret_key`.

**The fallback (.env file):** If you don't have 1Password yet, create `~/.langfuse.env` with permissions locked down:

```bash
cat > ~/.langfuse.env <<'EOF'
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://us.cloud.langfuse.com"
EOF

chmod 600 ~/.langfuse.env
```

Then add `source ~/.langfuse.env` to your `~/.zshrc` or `~/.bashrc` so the env vars load on every new shell.

**Verify it loaded:**

```bash
echo $LANGFUSE_PUBLIC_KEY
# Should print pk-lf-... (not blank)
```

If blank, you forgot to source the file. Open a new terminal and try again.

---

## Step 5: Send A Test Trace

Install the Python SDK:

```bash
pip install langfuse
```

Create a quick test script — `/tmp/langfuse_hello.py`:

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span", name="hello-world"
) as span:
    span.update(
        input={"prompt": "say hi"},
        output={"response": "hi from langfuse"},
    )

langfuse.flush()
print("Trace sent. Check your dashboard.")
```

Run it:

```bash
python3 /tmp/langfuse_hello.py
```

If you see `Trace sent.` and no errors, success.

---

## Step 6: See It In The Dashboard

Go back to [cloud.langfuse.com](https://cloud.langfuse.com), open your project, and click **Tracing → Traces** in the left sidebar.

You should see one trace with a single span called `hello-world`, with input and output visible.

That's the loop. Send a trace from anywhere in the world that has your two keys, see it appear in the dashboard within a few seconds.

---

## The Aha Moment

The point of this module isn't the hello-world trace. It's what comes next.

Once Claude Code is wired up (see `03-claude-code-integration.md`), every session you run sends traces automatically. You'll open the Langfuse dashboard and see:

- Your last 50 sessions, sorted by time
- Each session expanded into individual turns (user message → assistant response)
- Every tool call as its own span, with input/output and duration
- Every LLM call with the model name, token counts, and dollar cost
- Tags showing which machine ran it, which agent kicked it off, which project it was for

The first time you wake up and look at last night's traces in the dashboard instead of digging through `~/.claude/projects/`, you'll understand why this matters.

---

## Next

Now that Cloud is working, your options are:
- **Stay on Cloud and wire up Claude Code:** Skip to `03-claude-code-integration.md`.
- **Move to self-hosted first:** Read `02-self-hosted.md` and migrate before you start sending real traffic.

Most people start on Cloud, get the hooks working, then graduate to self-hosting once they understand what they want.
