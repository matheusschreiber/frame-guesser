<script lang="ts">
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";
  import { goto } from "$app/navigation";
</script>

<svelte:head>
  <title>Privacy Policy・FrameGuesser</title>
  <meta
    name="description"
    content="Privacy Policy for FrameGuesser — how we collect, use, and protect your data."
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
      onclick={() => (history.length > 1 ? history.back() : goto("/home"))}
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
      Privacy Policy
    </h1>
    <p class="mt-2 text-sm text-slate-500">Last updated: July 31, 2026</p>

    <section class="mt-10 space-y-8 text-sm leading-relaxed md:text-base">
      <div>
        <h2 class="text-xl font-semibold text-primary">1. Overview</h2>
        <p class="mt-2">
          This Privacy Policy explains what information FrameGuesser collects,
          how we use it, and the choices you have. By using the service you
          agree to the practices described here.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          2. Information We Collect
        </h2>
        <ul class="mt-2 list-disc space-y-1 pl-6">
          <li>
            <b>Account data:</b> the username and credentials you provide when
            registering.
          </li>
          <li>
            <b>Gameplay data:</b> scores, hints used, matches played, and other
            in-game activity needed to run the game and show your history.
          </li>
          <li>
            <b>Session data:</b> authentication cookies used to keep you signed
            in.
          </li>
          <li>
            <b>Technical data:</b> basic request information (such as
            timestamps and error logs) and anonymous analytics collected via
            Vercel Analytics to understand usage patterns.
          </li>
        </ul>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          3. How We Use Information
        </h2>
        <ul class="mt-2 list-disc space-y-1 pl-6">
          <li>To operate the game and keep you signed in.</li>
          <li>To display leaderboards, scores, and your play history.</li>
          <li>To diagnose issues and improve performance.</li>
          <li>To enforce our Terms of Service and prevent abuse.</li>
        </ul>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          4. Cookies and Local Storage
        </h2>
        <p class="mt-2">
          We use cookies and browser storage strictly to keep you signed in and
          remember basic preferences. We do not use advertising or third-party
          tracking cookies.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">5. Sharing</h2>
        <p class="mt-2">
          We do not sell your personal data. We only share information with
          service providers necessary to run the app (such as our hosting and
          analytics providers) and when required by law.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">6. Data Retention</h2>
        <p class="mt-2">
          We keep account and gameplay data for as long as your account is
          active. You may request deletion of your account and associated data
          at any time by contacting us.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">7. Your Rights</h2>
        <p class="mt-2">
          Depending on your jurisdiction, you may have the right to access,
          correct, export, or delete your personal data. Reach out through the
          channel below to exercise these rights.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">8. Children</h2>
        <p class="mt-2">
          FrameGuesser is not directed to children under 13. If you believe a
          child has provided us personal data, please contact us so we can
          remove it.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">
          9. Changes to This Policy
        </h2>
        <p class="mt-2">
          We may update this Privacy Policy from time to time. Continued use of
          the service after changes take effect constitutes acceptance of the
          revised policy.
        </p>
      </div>

      <div>
        <h2 class="text-xl font-semibold text-primary">10. Contact</h2>
        <p class="mt-2">
          Questions about this policy? Reach out via the project's
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
