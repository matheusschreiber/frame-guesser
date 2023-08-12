<script lang='ts'>
  import Swal from "sweetalert2"
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";
  import { goto } from '$app/navigation';
  import { getContext, onMount } from "svelte";
  import { api } from "../../services/api";

  let confirm = false
  let selected:number|null= null
  let tipsAmount = 5
  let tipsUsed = 0
  
  let currentSlide = 1
  let slidesAmount = 5

  var username:string = getContext('username')
  var password:string = getContext('password')

  function handleConfirm() {
    if (confirm) {
      console.log('confirm!')
      if (tipsUsed+1<=tipsAmount) tipsUsed++
      confirm = false
    } else confirm = true
  }

  function handleSelection(pos:number) {
    if (selected==pos) selected = null
    else selected=pos
  }

  function handleNextSlide() {
    if (currentSlide==slidesAmount) goto(`/results`, { replaceState:false }) 

    if (Math.random()>.5) {
      Swal.fire({
        title: '<strong>BOA! RESOSTA CERTA!</strong>',
        icon: 'success',
        html: 'Sabe muito!',
        showConfirmButton: false,
      }).then(()=>{
        selected=null          
      })
    } else {
      Swal.fire({
        title: '<strong>OPS! MAIS SORTE NA PRÓXIMA</strong>',
        icon: 'error',
        html: 'Alguém andou faltando algumas aulas',
        showConfirmButton: false,
      }).then(()=>{
        selected=null        
      })
    }

    currentSlide++
  }

  async function fetchSlide() {
    // if (!username || !password) return;

    // const response = await api.get('slide/random', {auth: {username, password}})

    // console.log(response.data)
  }

  onMount(()=>{
    fetchSlide()
  })

</script>
<main>
  <header class="w-full flex justify-center items-center py-8 mt-8">
    <Logo small/>
  </header>

  <section class="my-8 py-12 bg-purple m-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={3} />
    <div class="flex flex-col items-center justify-center">
      <h5 class="mx-auto w-fit text-red font-bold text-sm mb-4">NÍVEL DIFÍCIL</h5>
      <h2 class="text-whitish text-3xl">De quem é esse slide?</h2>
      <h3 class="mb-8 mt-4 text-whitish bg-terciary w-fit rounded-lg p-4">{currentSlide}/{slidesAmount}</h3>
    </div>

    <!-- TODO: adicionar um placeholder (uma imagem default enquanto carrega) -->
    <img class="w-[400px]" src="messi.jpg" alt="slide"/>

    <div class="flex items-center gap-8 mt-4">
      {#if tipsUsed>0} <p class="absolute font-fredoka text-sm text-whitish mt-[-100px] w-32 ml-[-10px]">{tipsUsed}/{tipsAmount}</p> {/if}
      <div
        on:click={handleConfirm} role="button" tabindex={1} 
        class="bg-secondary p-4 rounded-3xl shadow-medium scale-[.4] h-28 w-28 flex 
        justify-center items-center cursor-pointer border-4 select-none
        {confirm?'border-yellow':'border-secondary'}" on:keypress={()=>{}}>

        <img src="icons/lamp.svg" alt="icon lamp" class="{confirm?'hidden':'flex'}"/>
        <img src="icons/tip.svg" alt="confirm icon" class="{confirm?'flex':'hidden'}"/>
      </div>
      {#if confirm} <p class="absolute font-fredoka text-sm text-whitish mt-32 w-32 ml-[-10px]">Clique novamente para confirmar a sua dica</p> {/if}
      
      {#each [1,2,3,4] as item, i}
        <div on:click={()=>handleSelection(i)} role="button" tabindex={2} on:keypress={()=>{}}
          class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 select-none {selected==i?'border-pink':'border-secondary'}">
          <h3 class="text-whitish font-bold text-sm">PROFESSOR DA SILVA</h3>
          <p class="text-gray text-sm">SINAIS E SISTEMAS</p>
        </div>
      {/each}
    </div>

    <button class="px-4 py-2 my-8 bg-terciary font-bold text-sm rounded-lg border-2 
      {selected!=null?'border-green text-green':'border-terciary text-whitish'}"
      on:click={()=>{handleNextSlide()}}>

      AVANÇAR
    </button>
  </section>

  <Footer />
</main>