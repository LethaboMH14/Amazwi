# Local LAN demo runbook

Detected host LAN address: `192.168.0.169`.

Backend laptop (`starter/backend`):

```powershell
$env:AMAZWI_DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/DB?sslmode=require"
& "<bundled-python>\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend laptop (`starter/frontend`):

```powershell
$env:API_PROXY_TARGET="http://192.168.0.169:8000"
& "<bundled-node>\node.exe" node_modules/vite/bin/vite.js --host 0.0.0.0 --port 5173
```

Phone and second laptop: open `http://192.168.0.169:5173/`.
Backend health probe: `http://192.168.0.169:8000/health`.

Neon/Supabase URLs should include `sslmode=require` when their provider
requires TLS. The seed uses one short-lived SQLAlchemy session and does not
open a separate connection per row; run it before the frontend starts making
database-backed requests.

This environment confirmed uvicorn on the LAN address. Vite could not be
started here because esbuild was denied access while traversing the workspace
parent path; run the command above on the event laptop where the repository is
not subject to that sandbox restriction.
