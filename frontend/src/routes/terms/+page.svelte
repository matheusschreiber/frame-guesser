<script lang="ts">
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";
  import { goto } from "$app/navigation";
</script>

<svelte:head>
  <title>Terms of Service・FrameGuesser</title>
  <meta
    name="description"
    content="Terms of Service for FrameGuesser — the rules for playing our movie-frame guessing game."
  />
</svelte:head>

<main class="min-h-screen w-full bg-whitish text-gray">
  <header class="mx-auto flex max-w-4xl items-center justify-between px-6 pt-8">
    <button
      onclick={() => goto("/home")}
      class="cursor-pointer"
      aria-label="Back to home"
    >
      <Logo />
    </button>
    <button
      onclick={() => history.length > 1 ? history.back() : goto("/home")}
      class="text-sm text-slate-600 hover:text-primary transition-colors"
    >
      ← Back
    </button>
  </header>

  <article class="mx-auto max-w-4xl px-6 py-12">
    <div
      class="inline-flex items-center gap-3 rounded-full bg-white/70 px-5 py-2 text-xs uppercase tracking-[0.2em] text-slate-600"
    >
      Legal
    </div>
    <h1 class="mt-4 text-3xl md:text-4xl font-bold tracking-tight text-primary">
      Terms of Service
    </h1>
    <p class="mt-2 text-sm text-slate-500">Last updated: July 31, 2026</p>

    <section class="mt-10 space-y-8 text-sm leading-relaxed md:text-base">
      <div>
        <h2 class="text-xl font-semibold text-primary">1. Acceptance of Terms</h2>
        <p class="mt-2">
          By accessing or using FrameGuesser, you agree to be bound by these
          Terms of Service. If you do not agree with any part of these terms,
          please do not use the service.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">2. The Service</h2>
        <p class="mt-2">
          FrameGuesser is a casual movie-frame guessing game provided for
          entertainment purposes. The service is offered "as is" without
          warranties of any kind, and may change or become unavailable at any
          time.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">3. User Accounts</h2>
        <p class="mt-2">
          You are responsible for maintaining the confidentiality of your
          account credentials and for all activity that occurs under your
          account. Please choose a username that is respectful and does not
          impersonate others.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">4. Acceptable Use</h2>
        <p class="mt-2">You agree not to:</p>
        <ul class="mt-2 list-disc space-y-1 pl-6">
          <li>Use the service for any unlawful purpose.</li>
          <li>
            Attempt to disrupt, reverse-engineer, or gain unauthorized access
            to the service or its underlying systems.
          </li>
          <li>
            Use bots, scrapers, or automated tools to play the game or extract
            data.
          </li>
          <li>Post abusive, offensive, or infringing content.</li>
        </ul>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          5. Intellectual Property
        </h2>
        <p class="mt-2">
          Movie frames and related media shown in the game are the property of
          their respective rights holders and are displayed here for the sole
          purpose of gameplay commentary and identification. FrameGuesser
          branding, code, and original content remain the property of the
          project maintainers.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">6. Privacy</h2>
        <p class="mt-2">
          Your use of FrameGuesser is also governed by our
          <a class="text-primary underline hover:opacity-80" href="/privacy"
            >Privacy Policy</a
          >, which describes how we collect and handle your data.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          7. Limitation of Liability
        </h2>
        <p class="mt-2">
          FrameGuesser and its maintainers shall not be liable for any
          indirect, incidental, or consequential damages arising from your use
          of, or inability to use, the service.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">8. Changes to Terms</h2>
        <p class="mt-2">
          We may update these Terms of Service from time to time. Continued use
          of the service after changes take effect constitutes acceptance of
          the revised terms.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">9. Contact</h2>
        <p class="mt-2">
          Questions about these terms? Reach out via the project's
          <a
            class="text-primary underline hover:opacity-80"
            href="https://github.com/matheusschreiber/frame-guesser"
            target="_blank"
            rel="noopener noreferrer">GitHub repository</a
          >.
        </p>
      </div>
    </section>
  </article>

  <Footer />
</main>
