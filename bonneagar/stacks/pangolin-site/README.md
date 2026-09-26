# Pangolin Site — v1.23+ canonical new-site pattern

> **For:** Operators creating a NEW Pangolin site (tunnel agent) on a workload host.
> **Status:** NEW 2026-09-26 (per the v1.23 "Newt → Pangolin Site" rename + the v1.23 self-service HA/clustering release).
> **Replaces:** the standalone Newt binary pattern (the canonical pattern from Pangolin <v1.23).
> **Backward compat:** `bonneagar/stacks/pangolin/newt.yaml` is kept for existing deployments — existing Newt deployments continue to work (per v1.23 docs).

## Why this exists

Per the [Pangolin 1.23 release blog](https://pangolin.net/news/1-23-release) (Sep 15, 2026):

> Newt is the tunnel connector that runs on the remote private network. It handles the intelligent networking and NAT traversal Pangolin uses to make your resources available securely to users anywhere. **1.23 integrates Newt directly into the Pangolin CLI**, so you can start a site with the same tool you already use for SSH, client connections, and the rest of the product:
>
> ```shell
> pangolin up site --id <id> --secret <secret> --endpoint https://app.pangolin.net
> ```
>
> ... the create site wizard in the dashboard now treats the CLI method as the preferred, default way to install a new site, **and Newt is renamed to Pangolin Site** in that flow.

## How to deploy

### Option 1 — Docker Compose (the canonical pattern)

```bash
cd bonneagar/stacks/pangolin-site
# Provision SITE_ID + SITE_SECRET in Infisical vault (dev-baile)
locket inject -- docker compose up -d
```

The `compose.yaml` reads `SITE_ID_FILE` + `SITE_SECRET_FILE` from `/run/secrets/locket/` (the Locket sidecar resolves these from the Infisical vault at startup).

### Option 2 — Pangolin CLI (the recommended pattern)

Per the v1.23 docs, the recommended deployment uses the Pangolin CLI directly on the workload host:

```bash
# Install the CLI
curl -fsSL https://static.pangolin.net/get-cli.sh | bash   # installs to /usr/local/bin

# Login + start the site
pangolin login                                            # browser-based user auth
pangolin up site --id <id> --secret <secret> --endpoint https://pangolin.cianchosaint.ie

# Install as a persistent system service (cross-platform)
sudo pangolin service install site \
  --id <id> \
  --secret <secret> \
  --endpoint https://pangolin.cianchosaint.ie

# Check service status
sudo pangolin service status site

# View logs
sudo pangolin service logs site
```

## Migrating from `newt.yaml` → `pangolin-site.yaml`

If you have an existing Newt deployment (per the legacy `bonneagar/stacks/pangolin/newt.yaml` pattern):

1. Create a NEW site in the Pangolin dashboard using the v1.23 wizard (it defaults to the CLI method now).
2. Get the new `SITE_ID` + `SITE_SECRET` from the dashboard.
3. Provision them in the Infisical vault at `dev-baile/pangolin/newt-<hostname>/{id,secret}` (per the secrets.env template).
4. Deploy the new container with `docker compose up -d` from this directory.
5. Once the new site connects (verify in the dashboard), you can safely `docker compose down` the old Newt container.

**The old Newt binary keeps working during the transition** (per v1.23 docs: *"Existing Newt deployments keep working. Leave them as they are, or switch to the CLI when you want to."*).

## The 6-file GOLD_STANDARD pattern

This directory follows the canonical 6-file pattern (per `bonneagar/GOLD_STANDARD.md`):

| File | Purpose |
|---|---|
| `compose.yaml` | The `pangolin-site` + `locket` services |
| `sidecar.yaml` | Locket secret injection override |
| `secrets.env` | The credentials template (SITE_ID + SITE_SECRET via Infisical) |
| `README.md` | This file (the migration guide) |
| `pangolin.yaml` | TBD (the pangolin private-resource target — currently the pangolin-site uses the same network as `pangolin/`; per Stage 7 we may add a dedicated resource target) |
| `blueprint.yaml` | TBD (per Stage 7 — currently the resource targets are managed by the IaC's `iac:sync:resources` command via the umbrella `pangolin/blueprint.yaml`) |

## Upstream

- **Pangolin CLI**: <https://github.com/fosrl/pangolin-cli>
- **Pangolin 1.23 release blog**: <https://pangolin.net/news/1-23-release>
- **Install a site docs**: <https://docs.pangolin.net/manage/sites/install-site>
