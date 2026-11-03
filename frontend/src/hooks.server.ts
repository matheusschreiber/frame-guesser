import { env } from '$env/dynamic/private';
import { base } from '$app/paths';
import { redirect, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const maintenancePath = `${base}/maintenance`;

  if (env.MAINTENANCE_MODE === 'true') {
    event.setHeaders({ 'cache-control': 'no-store' });

    if (event.url.pathname !== maintenancePath) {
      redirect(307, maintenancePath);
    }

    const response = await resolve(event);
    response.headers.set('retry-after', '300');
    return new Response(response.body, {
      status: 503,
      headers: response.headers
    });
  }

  if (event.url.pathname === maintenancePath) {
    event.setHeaders({ 'cache-control': 'no-store' });
    redirect(307, `${base}/home`);
  }

  return resolve(event);
};