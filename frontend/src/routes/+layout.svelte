<script lang="ts">
  import "../app.css";
  import { dev } from "$app/environment";
  import { injectAnalytics } from "@vercel/analytics/sveltekit";
  import { onMount } from "svelte";

  onMount(() => {
    injectAnalytics({ mode: dev ? "development" : "production" });
  });

  interface Props {
    children?: import("svelte").Snippet;
  }

  let { children }: Props = $props();
</script>

{@render children?.()}
