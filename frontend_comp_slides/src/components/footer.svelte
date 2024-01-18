<script>
  import { onMount } from "svelte";

  
  onMount(()=>{
    let yearContainer = document.getElementById('year')
    if (yearContainer) {
      yearContainer.textContent = (new Date().getFullYear()).toString()
    }
  })
</script>

<div class="lg:h-[200px] pt-20 w-full bg-lightgray flex items-end pb-8 justify-center">
  <div class="flex w-full justify-center lg:gap-2 items-center text-gray text-sm lg:flex-row flex-col gap-10">
    <a href="https://github.com/matheusschreiber" target="_blank"><img class="lg:w-8 lg:h-8 w-24 h-24 hover:scale-105 transition-transform" src="icons/git.svg" alt="git icon"/></a>
    <a href="https://www.linkedin.com/in/matheus-schreiber-49472321a/" target="_blank"><img class="lg:w-8 lg:h-8 w-24 h-24 hover:scale-105 transition-transform" src="icons/linkedin.svg" alt="linkedin icon"/></a>
    <a href="https://matheus-schreiber.com.br" target="_blank"><img class="lg:w-8 lg:h-8 w-24 h-24 hover:scale-105 transition-transform" src="icons/globe.svg" alt="globe icon"/></a>
    <p class="w-64 text-center text-lg lg:w-fit lg:text-left lg:text-sm"><span id="year"></span>・<span class="font-bold">Comp Slides</span>・Engenharia da Computação・UFES</p>
  </div>
</div>