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

<div class="fixed bottom-10 right-10">
    <a href="https://ko-fi.com/frameguesser" 
      target="_blank" 
      rel="noopener noreferrer" 
      class="inline-flex items-center gap-2.5 bg-[#FF5E5B] 
      hover:bg-[#e04f4c] text-whitish font-semibold py-2.5 px-5 rounded-full 
      shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5">
      
      <svg class="w-5 h-5 fill-whitish" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M23.881 8.948c-.773-4.085-4.859-5.005-4.859-5.005s-.087-.023-.248-.044c-.79-.1-1.838-.17-3.13-.213C13.242 3.6 9.873 3.6 7.42 3.68c-1.282.043-2.317.113-3.097.213-.158.02-.245.044-.245.044S.013 4.863.001 8.948c-.012 4.085 3.394 7.214 3.394 7.214s.09.072.261.18c.841.536 2.036 1.053 3.633 1.411 2.064.462 4.796.476 6.953.037 1.587-.323 2.783-.807 3.63-1.325.178-.109.273-.183.273-.183s3.51-3.251 2.737-7.334zm-5.753 5.485c-.014.015-.027.03-.042.045-.583.583-1.638.991-3.153 1.22-1.748.264-3.963.252-5.698-.027-1.428-.23-2.404-.61-2.952-1.155-.015-.015-.028-.03-.041-.045-.63-.675-.989-1.722-.989-2.88 0-1.161.359-2.208.989-2.883.013-.015.026-.03.041-.045.548-.545 1.524-.926 2.952-1.156 1.735-.279 3.95-.291 5.698-.027 1.515.228 2.57.636 3.153 1.22.015.015.028.03.042.045.63.675.989 1.722.989 2.883 0 1.158-.359 2.205-.989 2.88zm4.354-2.732c-.144.757-.492 1.343-.961 1.742a7.18 7.18 0 0 1-.222-.243c.4-.416.666-.948.775-1.558.175-.98-.073-1.797-.698-2.298a4.131 4.131 0 0 1 .15-.023c.691.037 1.127.623.956 1.58z"/>
      </svg>
      
      <span>Buy me a coffee</span>
    </a>
  </div>
