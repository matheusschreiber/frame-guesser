<script lang="ts">
  import { base } from '$app/paths';
  import Footer from '../../components/footer.svelte';
</script>

<svelte:head>
  <title>Intermission | Frame Guesser</title>
  <meta name="description" content="Frame Guesser is temporarily down for maintenance. We'll be back soon." />
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

<main class="maintenance">
  <header>
    <img class="logo" src={`${base}/logos/logo_dark.png`} alt="Frame Guesser" />
    <span class="status"><span class="status-dot"></span> Maintenance in progress</span>
  </header>

  <section class="intermission" aria-labelledby="maintenance-title">
    <div class="artwork" aria-hidden="true">
      <img class="frame" src={`${base}/icons/frame.svg`} alt="" />
      <img class="popcorn" src={`${base}/icons/popcorn.svg`} alt="" />
    </div>
    <p class="eyebrow">A SHORT INTERMISSION</p>
    <h1 id="maintenance-title">Even great movies<br />need an intermission.</h1>
    <p class="description">We're giving Frame Guesser a little behind-the-scenes care.<br class="desktop-break" /> Your next movie challenge will be back soon.</p>
    <a class="retry" href={`${base}/home`} data-sveltekit-reload>Check again</a>
    <p class="footnote">Thanks for waiting. Save us some popcorn!</p>
  </section>

  <Footer />
</main>

<style>
  .maintenance {
    min-height: 100svh;
    display: flex;
    flex-direction: column;
    color: var(--color-terciary);
    font-family: var(--font-fredoka);
  }
  header {
    width: min(1100px, 100%);
    margin: 0 auto;
    padding: 32px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }
  .logo { width: 190px; height: auto; }
  .status { display: flex; align-items: center; gap: 10px; font-size: 14px; }
  .status-dot { width: 8px; height: 8px; flex-shrink: 0; border-radius: 50%; background: var(--color-orange); }
  .intermission {
    flex: 1;
    padding: 36px 24px 64px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    animation: reveal 600ms ease-out both;
  }
  .artwork { position: relative; width: 220px; height: 160px; margin-bottom: 28px; }
  .frame { position: absolute; width: 164px; height: 140px; left: 12px; top: 4px; transform: rotate(-9deg); }
  .popcorn { position: absolute; width: 88px; height: 112px; right: 0; bottom: 0; transform: rotate(12deg); }
  .eyebrow { font-size: 13px; font-weight: 500; color: var(--color-secondary); margin-bottom: 18px; }
  h1 { font-size: 48px; font-weight: 500; line-height: 1.12; margin-bottom: 22px; }
  .description { max-width: 520px; color: #655a75; font-size: 18px; line-height: 1.6; }
  .retry {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
    padding: 12px 32px;
    margin-top: 30px;
    border-radius: 8px;
    background: var(--color-primary);
    color: var(--color-whitish);
    font-size: 17px;
    font-weight: 500;
    transition: background 150ms ease;
  }
  .retry:hover { background: var(--color-terciary); }
  .retry:focus-visible { outline: 3px solid var(--color-orange); outline-offset: 4px; }
  .footnote { margin-top: 18px; color: #655a75; font-size: 14px; }
  @keyframes reveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  @media (max-width: 600px) {
    header { flex-direction: column; padding: 26px 20px 12px; gap: 16px; }
    .logo { width: 170px; }
    .intermission { padding: 24px 20px 40px; }
    .artwork { margin-bottom: 22px; }
    h1 { font-size: 34px; }
    .description { font-size: 16px; }
    .desktop-break { display: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    .intermission { animation: none; }
    .retry { transition: none; }
  }
</style>