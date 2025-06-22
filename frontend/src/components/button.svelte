<script lang="ts">
  import ButtonLineBackground from "./buttonLineBackground.svelte";

  interface Props {
    text: string;
    func: Function;
  }

  let { text, func }: Props = $props();
</script>

<div onclick={() => func()} role="button" tabindex={1} onkeypress={() => {}}>
  <button
    class="group w-32 h-16 p-0 flex justify-center items-center lg:w-fit lg:h-fit lg:block
     bg-terciary lg:px-2 lg:py-4 rounded-xl text-whitish text-sm font-bold overflow-hidden hover:scale-105 transition hover:shadow-heavy"
  >
    <div class="hidden lg:flex">
      <ButtonLineBackground />
    </div>
    {text}
  </button>
</div>
