<script lang='ts'>
  import { onMount } from "svelte";

  let disciplines = ['Estrutura de Dados II', 'Eletromagnetismo I', 'Circuitos Elétricos I', 'Circuitos Lógicos', 'Programação II', 'Fisica III']
  
  let text = ""

  let duration = 3000

  function sleep(ms:number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function addTyping(string: string){
    let i=0
    let timePerLetter = (duration*.45)/string.length // this is to ensure 2sec for all words
    while(i<string.length) {
      text += string[i++]
      await sleep(timePerLetter)
    }
  }

  async function eraseTyping(string: string){
    let i=string.length
    let timePerLetter = duration*.10/string.length // this is to ensure 2sec for all words
    while(i-->0) {
      text = text.slice(0,-1)
      await sleep(timePerLetter)
    }
  }

  onMount(async()=>{
    while(true){
      let index = Math.round(Math.random()*(disciplines.length-1))
      console.log(index)
      await addTyping(disciplines[index])
      await sleep(duration*.45)
      await eraseTyping(disciplines[index])
    }
  })

  let blink = true
  setInterval(()=>{
    blink=!blink
  }, 200)


</script>


<h1 id="title-typing-effect" class="text-6xl font-bold text-terciary w-[400px]">
  {text}<span class="text-green {blink?"invisible":"visible"}">_</span>
</h1>