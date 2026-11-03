# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/master/packages/create-svelte).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npm create svelte@latest

# create a new project in my-app
npm create svelte@latest my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Maintenance Mode

Set `MAINTENANCE_MODE=true` in `frontend/.env` (use `frontend/.env.example`
for a new environment), or set it in your hosting provider's frontend environment
variables. Restart the dev server after changing `.env`; restart or redeploy the
frontend in production so the running server receives the updated value.

While enabled, every frontend page URL redirects to `/maintenance`, including
unknown URLs. The maintenance page returns HTTP 503 with `Retry-After: 300` and
`Cache-Control: no-store`. Static assets remain available, and regular pages do
not load or make backend requests. The backend itself is not put into maintenance.

Set `MAINTENANCE_MODE=false` (or remove it) and restart/redeploy to restore the
normal routes. `/maintenance` then redirects to `/home`. Only the exact value
`true` enables maintenance. This is a server-side variable; no `VITE_` prefix is
needed. Visitors already on an open page will enter maintenance on their next
navigation or reload.

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
