<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import Button from "./button.svelte";

  export let playable = false;

  onMount(() => {
    let isLoginPage = window.location.href.includes("login") 
    let isLoggedPage = window.location.href.includes("logged")
    if (isLoginPage || isLoggedPage) {
      playable = true;
    }
  });
</script>

<footer
  class="relative w-full overflow-hidden bg-whitish text-gray"
  aria-label="Site footer"
>
  <div
    aria-hidden="true"
    class="pointer-events-none absolute -top-24 left-6 h-48 w-48 rounded-full bg-amber-300/40 blur-3xl"
  ></div>
  <div
    aria-hidden="true"
    class="pointer-events-none absolute -bottom-24 right-6 h-56 w-56 rounded-full bg-sky-300/30 blur-3xl"
  ></div>

  <div
    class="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-14 md:flex-row md:items-center"
  >
    <div class="flex-1">
      <div
        class="inline-flex items-center gap-3 rounded-full bg-white/70 py-2 text-xs uppercase tracking-[0.2em] text-slate-600"
      >
        Guess. React. Repeat.
      </div>
      <h2 class="mt-4 text-2xl tracking-tight font-bold text-primary">
        FrameGuesser
      </h2>
      <p class="mt-2 max-w-xl text-sm">
        Quick-fire rounds built for popcorn instincts. No spoilers, no pressure,
        just a fast way to flex your movie memory.
      </p>
    </div>

    <div class="flex flex-col items-start gap-4 sm:flex-row sm:items-center">
      {#if playable}
        <Button
          text="PLAY"
          func={() => {
            goto("/login");
          }}
        />
      {/if}
    </div>
  </div>

  <div class="border-t border-lightgray">
    <div
      class="mx-auto flex max-w-6xl flex-col items-start gap-3 px-6 py-6 text-xs text-slate-600 sm:flex-row sm:items-center sm:justify-between"
    >
      <p><b>FrameGuesser</b>・<a href="https://github.com/matheusschreiber/frame-guesser">Github</a>・2026</p>
      <div class="flex flex-wrap gap-4">
        <span class="rounded-full bg-white/80 px-3 py-1"
          >No ads in gameplay</span
        >
        <span class="rounded-full bg-white/80 px-3 py-1">Daily hints</span>
        <span class="rounded-full bg-white/80 px-3 py-1">Built for phones</span>
      </div>
    </div>
  </div>
</footer>
