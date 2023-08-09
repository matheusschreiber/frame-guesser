<script lang="ts">
  import ButtonLineBackground from "./buttonLineBackground.svelte";

  export let text: string;
  export let func: Function;
</script>

<div on:click={() => func()} role="button" tabindex={1} on:keypress={() => {}}>
  <button
    class="group bg-terciary px-2 py-4 rounded-xl text-whitish text-sm font-bold overflow-hidden hover:scale-105 transition hover:shadow-heavy"
  >
    <ButtonLineBackground />
    {text}
  </button>
</div>
