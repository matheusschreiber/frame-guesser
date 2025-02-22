<script lang="ts">
  import { onMount } from "svelte";

  
  onMount(()=>{
    Array.from(document.getElementsByClassName('year-dynamic')).forEach((element: Element) => {
      if (element) {
        element.textContent = (new Date().getFullYear()).toString()
      }
    });
  })
</script>

<div class="lg:flex hidden h-[200px] pt-20 w-full bg-lightgray items-end pb-8 justify-center">
  <div class="flex w-full justify-center items-center text-gray text-sm">
    <p class="text-center w-fit text-sm"><span class="year-dynamic"></span>・<span class="font-bold">Comp Slides</span>・Engenharia da Computação・UFES</p>
  </div>
</div>

<div class="flex lg:hidden pt-20 w-full bg-lightgray pb-8">
  <div class="flex w-full items-start px-5 text-gray text-sm lg:flex-row flex-col">
    <span class="font-bold mb-4">CompSlides</span>
    <span>UFES・<span class="year-dynamic"></span></span>
    <span>Engenharia da Computação</span>
  </div>
</div>