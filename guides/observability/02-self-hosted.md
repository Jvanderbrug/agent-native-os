# 02 - Self-Host Langfuse On A VPS

**Goal:** Run your own Langfuse instance on a $5-10/month VPS, with a real domain and SSL, that your agents talk to instead of Langfuse Cloud.

This is the graduation path from Cloud. Same dashboard, your hardware.

---

## Why Self-Host

You probably do not need to do this on day one. Cloud is fine to start. Reasons people make the move:

- **Privacy.** Your prompts and responses never leave a server you control.
- **No vendor lock-in.** If Langfuse the company disappears tomorrow, your data and dashboard keep working. Open source.
- **Free at any scale.** Once the box is paid for, every event is free. No per-event pricing as you grow.
- **Runs alongside other services.** If you already have a VPS for n8n, a website, or other tooling, Langfuse is one more docker-compose stack on the same host.
- **Latency.** If your agents run on the same machine or the same network, the round trip drops to milliseconds.

A real-world example: one of the AI Build Lab production fleets runs a self-hosted Langfuse on a Hostinger VPS at a custom subdomain. Multiple machines (Mac Studio, MBP, agent server) all send traces to it through Tailscale or public DNS. It has been stable for months with one shared docker-compose stack.

---

## Step 1: Pick A VPS

Two beginner-friendly providers:

| Provider | Plan | Monthly | Notes |
|---|---|---|---|
| Hostinger VPS | KVM 2 | ~$8 | 2 vCPU, 8 GB RAM, 100 GB NVMe. Plenty for personal Langfuse. |
| DigitalOcean | Basic Droplet 2 GB | $12 | 1 vCPU, 2 GB RAM, 50 GB. Tighter, will work but expect occasional swap. |
| Hetzner Cloud | CPX21 | ~$8 | 3 vCPU, 4 GB RAM, 80 GB. EU-based, great price/performance. |

Minimum spec recommendation: **2 vCPU, 4 GB RAM, 40 GB disk**. Langfuse runs Postgres + ClickHouse + Redis + MinIO, so it needs a bit more than a single-binary app.

Pick Ubuntu 22.04 or 24.04 LTS as the OS. Generate an SSH key during signup and add it to the VPS so you can `ssh root@your-vps-ip` without a password.

---

## Step 2: Install Docker

SSH into the VPS:

```bash
ssh root@your-vps-ip
```

Install Docker and the compose plugin (Ubuntu):

```bash
apt update && apt install -y docker.io docker-compose-plugin
systemctl enable --now docker
docker --version
docker compose version
```

You should see version strings for both.

---

## Windows: Native Git Bash + Docker Desktop

If you are following this from Windows, you do not need to open a WSL terminal for the Docker commands. Native Git Bash plus Docker Desktop works for the local setup path.

Install Docker Desktop, start it, then open Git Bash and confirm Docker is reachable:

```bash
docker --version
docker compose version
```

For a local Windows Langfuse test, clone and run the stack from Git Bash:

```bash
mkdir -p ~/langfuse
cd ~/langfuse
git clone https://github.com/langfuse/langfuse.git .
docker compose up -d
```

Git Bash paths like `~/langfuse` map to `C:\Users\<user>\langfuse`. Keep using forward slashes inside Git Bash commands. If you are installing Langfuse on a VPS, run the `ssh root@your-vps-ip` command from Git Bash and install Docker on the VPS as shown above.

---

## Step 3: Clone Langfuse

```bash
mkdir -p /opt && cd /opt
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

The repo includes a `docker-compose.yml` at the root with everything you need.

---

## Step 4: Configure Secrets

Open `docker-compose.yml` and look for lines marked `# CHANGEME`. There are several. The most important:

- `NEXTAUTH_SECRET`: used to sign session cookies. Generate with `openssl rand -base64 32`.
- `SALT`: used to hash API keys at rest. Generate with `openssl rand -base64 32`.
- `ENCRYPTION_KEY`: used to encrypt sensitive fields. Generate with `openssl rand -hex 32` (must be exactly 64 hex chars).
- `LANGFUSE_INIT_USER_PASSWORD`: your initial admin login. Pick something strong.
- Database passwords (Postgres, ClickHouse, Redis, MinIO): replace each `CHANGEME` with `openssl rand -base64 24`.

**Also set:**

- `NEXTAUTH_URL`: must be the full public URL your instance will live at, e.g. `https://langfuse.yourdomain.com`. This must match exactly or login will fail.

Save the file. Do not commit it to git anywhere.

---

## Step 5: Start The Stack

```bash
docker compose up -d
```

First run takes a few minutes because it pulls images and runs database migrations. Watch the logs:

```bash
docker compose logs -f langfuse-web
```

When you see `Ready` and the worker starts polling, the stack is up. Ctrl-C out of the log tail (the containers keep running in the background).

Test locally on the VPS:

```bash
curl http://localhost:3000
# Should return HTML for the Langfuse login page.
```

---

## Step 6: Wire DNS

In your DNS provider (Cloudflare, Namecheap, Route53, wherever your domain lives):

- Create an `A` record: `langfuse.yourdomain.com` to your VPS IP
- TTL 300 is fine

Wait a minute, then verify:

```bash
dig langfuse.yourdomain.com +short
# Should return your VPS IP.
```

---

## Step 7: Reverse Proxy + SSL With Caddy

Caddy is the easiest reverse proxy with automatic SSL. Install it on the VPS:

```bash
apt install -y caddy
```

Edit `/etc/caddy/Caddyfile`:

```
langfuse.yourdomain.com {
    reverse_proxy localhost:3000
}
```

Reload:

```bash
systemctl reload caddy
```

Caddy will automatically request a Let's Encrypt cert the first time someone hits the URL. Open `https://langfuse.yourdomain.com` in your browser. You should see the Langfuse login page over HTTPS.

Log in with the email + password you set in `LANGFUSE_INIT_USER_PASSWORD` (the email defaults to `LANGFUSE_INIT_USER_EMAIL` if set, otherwise `admin@example.com`). Create your first project, generate API keys.

---

## Step 8: Point Claude Code At Your Self-Hosted Instance

Same env vars as the cloud setup, just a different host:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."   # from your self-hosted project
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://langfuse.yourdomain.com"
```

Run the same hello-world test from `01-getting-started-cloud.md`. The trace should appear in your self-hosted dashboard.

---

## Step 9: Daily Operations

**Update Langfuse:**

```bash
cd /opt/langfuse
git pull
docker compose pull
docker compose up -d
```

The data lives in named Docker volumes, so updates do not lose anything.

**Back up the data:**

The two databases that matter are Postgres (config, users, projects) and ClickHouse (the traces themselves).

A simple nightly backup:

```bash
# Add to crontab: 0 3 * * * /opt/langfuse-backup.sh
docker compose -f /opt/langfuse/docker-compose.yml exec -T postgres pg_dumpall -U postgres | gzip > /backups/postgres-$(date +%F).sql.gz
docker compose -f /opt/langfuse/docker-compose.yml exec -T clickhouse clickhouse-backup create
```

Pipe `/backups/` to S3 or rsync it to another machine. Don't trust a single-host backup.

**Watch resource usage:**

```bash
docker stats
```

If ClickHouse memory creeps up over time, give the VPS more RAM or tune ClickHouse's `max_memory_usage` setting in the compose file.

---

## Common Gotchas

- **Login fails immediately after install:** Almost always `NEXTAUTH_URL` doesn't match the URL you typed in the browser. Edit, restart `langfuse-web`, retry.
- **Caddy says certificate failed:** DNS hasn't propagated yet. Wait two minutes and try again. Check `journalctl -u caddy` for the actual error.
- **All traces show wrong timestamps:** The Langfuse docs are explicit about this: every container in the stack must run in UTC, otherwise queries return wrong or empty results. Verify with `docker compose exec langfuse-web date`.
- **Out of disk:** ClickHouse compresses well but does grow. Watch `df -h` on the VPS, especially under `/var/lib/docker/`.
- **VPS reboot loses everything:** It shouldn't if you used named volumes (the default), but verify with `docker volume ls` and `docker volume inspect`. If you used bind mounts to ephemeral disk you'll lose data on reboot.

---

## When To Move Off Self-Hosted Back To Cloud

Rare but real reasons:

- You stopped wanting to maintain the VPS
- Your team grew and you need SSO, role-based access, audit logs (paid tier features)
- Compliance requires Langfuse-the-company to be the data processor

Migration is one-way friendly: Langfuse has an export endpoint you can use to dump your traces and re-import them on Cloud, but most people just leave history behind and start fresh on the new instance.

---

## Next

Now that you have a running instance (Cloud or self-hosted), wire it into Claude Code so every session traces automatically.

Continue to `03-claude-code-integration.md`.
