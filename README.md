# Z8ter Starter

A starter for **Z8ter**, with server-rendered Jinja templates, **Solid + TypeScript** components, and **Tailwind v4 + DaisyUI** styles.

## Quickstart

### 1) Prerequisites

- **Python 3.10+**
- **Node.js 20.19+ within Node 20, or Node.js 22.12+**, and **npm** (required by Vite 7)
- macOS, Linux, or Windows (PowerShell)

### 2) Clone this template

Use GitHub's **Use this template** button, then clone your new repository:

```bash
git clone https://github.com/<your-username>/<your-new-repo>.git
cd <your-new-repo>
```

### 3) Python setup

This repository stores its Python dependencies in `requirements.txt`. Choose uv or pip and keep the resulting environment active when running the app.

With uv on macOS or Linux:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or with pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, use `python` instead of `python3` and activate the environment with `.venv\Scripts\Activate.ps1` instead of the `source` command.

`requirements.txt` selects Z8ter 0.3.x and lets the framework resolve its supported runtime dependencies. Z8ter 0.3.1 uses Starlette 1.6+ within the 1.x series; remove any stale Starlette 0.x pins when upgrading an older copy of this starter. Activate this environment again when returning to the project in a new terminal.

To update an existing environment, use `uv pip install --upgrade -r requirements.txt` or `python -m pip install --upgrade -r requirements.txt`, then run your app's checks.

### 4) Install frontend tools and build the assets

```bash
npm ci
npm run build
```

The initial build writes the stylesheet, JavaScript bundles, and Vite manifest that the server uses to render a complete page.

### 5) Run the app and asset watchers

```bash
npm run dev
```

Open the [app](http://127.0.0.1:8000/), the [about page](http://127.0.0.1:8000/about), or the [hello API](http://127.0.0.1:8000/api/hello/).

The development command runs three processes:

- Tailwind watches CSS and template/component classes, writing `static/css/output.css`.
- Vite rebuilds the TypeScript/Solid assets and manifest in `static/js/`.
- `z8 run dev` serves the Python app with reload.

Wait for the server and asset watchers to be ready before opening the app. Refresh the browser after frontend changes; the starter uses Vite's build watcher. Running `z8 run dev` alone starts only the Python server.

The home page and sample API do not require a database. Configure authentication, sessions, and any additional security middleware when your app needs them.

## What's inside

```text
main.py                         # AppBuilder configuration
endpoints/
  views/index.py                # Home view
  views/about.py                # About view
  api/hello.py                  # Class-based JSON API
content/index.yaml              # Home-page content
src/
  css/app.css                   # Tailwind and DaisyUI entry
  ts/app.ts                     # Per-page module loader
  ts/pages/index.ts             # Home-page component registration
  ts/pages/about.ts             # About-page initialization
  ts/ui-components/             # Solid custom elements
  ts/utils/                     # Shared browser helpers
templates/
  base.jinja                    # Layout, CSS, and Vite script tag
  pages/                        # Page templates
  server-components/            # Shared Jinja macros
static/
  css/                          # Built stylesheet
  js/                           # Vite bundles, source maps, and manifest
  favicon/
vite.config.ts
package.json
requirements.txt
```

The active Python views live in `endpoints/views/`. The older top-level `views/` directory is unused.

## How pages work

A `View` renders a template such as `pages/index.jinja`. Z8ter supplies `page_id` and any matching YAML content from `content/`. The base template puts the ID in the body's `data-page` attribute and loads the Vite entry with `vite_script_tag("src/ts/app.ts")`.

`src/ts/app.ts` dynamically imports a matching module from `src/ts/pages/`. For example, `index` loads `src/ts/pages/index.ts`; `account.profile` maps to `src/ts/pages/account/profile.ts`. Export a default function to initialize the page. A `common.ts` module can provide site-wide initialization.

## API endpoints

`endpoints/api/hello.py` uses Z8ter's API helper:

```python
from z8ter.endpoints.api import API
from z8ter.requests import Request
from z8ter.responses import JSONResponse


class Hello(API):
    @API.endpoint("GET", "/")
    async def send_hello(self, request: Request) -> JSONResponse:
        return JSONResponse({"message": "Hello from the API!"}, 200)
```

The route is `/api/hello/`:

```bash
curl http://127.0.0.1:8000/api/hello/
# {"message":"Hello from the API!"}
```

## Check and build

```bash
# Check TypeScript once; exits with an error if types are invalid
npm run typecheck
# Watch TypeScript while developing
npm run typecheck:watch

# Build CSS and Vite assets for production
npm run build
# Check installed package compatibility and npm advisories
python -m pip check
npm audit

# Run the server locally without reload
z8 run prod
```

Set `Z8TER_DEBUG=false` in your deployment environment. For a production process with an explicit bind address, use the app factory:

```bash
uvicorn main:app_builder.build --factory --host 0.0.0.0 --port 8000
```

Build assets before starting the production server, and deploy behind your usual ASGI reverse proxy.

## Customize

- **Add a page:** create a view in `endpoints/views/`, a matching template in `templates/pages/`, and optional YAML in `content/` and TypeScript in `src/ts/pages/`.
- **Add shared browser behavior:** create `src/ts/pages/common.ts` with a default initialization function.
- **Add styles:** edit `src/css/app.css`. Its source globs include Jinja templates and TypeScript/Solid components.
- **Add an API:** create another class in `endpoints/api/` using the `Hello` example.
