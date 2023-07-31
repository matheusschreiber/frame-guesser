<script>
  import Button from "../../components/button.svelte";
import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";
  let messageSent = false

</script>

<main>
  <header class="w-full flex justify-center py-8 mt-8">
    <Logo small/>
  </header>

  <section class="my-8 py-12 bg-purple m-16 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={4} />
    <h5 class="mx-auto w-fit text-pink font-bold text-sm mb-4">RESULTADOS</h5>
    <p class="text-whitish text-2xl">Sua pontuação</p>
    <div class="flex items-center gap-4 my-4">
      <img src="icons/star.svg" alt="star icon" />
      <h1 class="text-whitish text-5xl font-bold">1250 pts</h1>
      <img src="icons/star.svg" alt="star icon" />
    </div>
    <p class="text-gray font-fredoka text-sm">Wow! Isso tudo?</p>

    <h2 class="text-3xl text-whitish mt-16">
      Você está <u class="text-yellow font-bold">62,2%</u> acima da média dos usuários
    </h2>
    
    <p class="text-gray text-lg my-16 font-fredoka">Você acertou 5 de 10 slides, parabéns!</p>

    <div class="flex flex-wrap justify-center gap-8">
      {#each [1,2,3,4,5, 6, 7, 8, 9, 10] as item}
      <div class="flex flex-col items-center justify-center bg-terciary rounded-xl">
        <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">FÁCIL</h5>
        <img src="messi.jpg" alt="slide-miniature" class="w-[100px]"/>
        <div class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 {item%2?'border-green':'border-red'}">
          <h3 class="text-whitish font-bold text-sm">PROFESSOR DA SILVA</h3>
          <p class="text-gray text-sm">SINAIS E SISTEMAS</p>
        </div>
      </div>
      {/each}
    </div>

      <div class="flex mt-32 flex-col gap-4 mb-32">
        <p class="font-fredoka text-gray text-sm">Deixe seu recado pela vitória, ou seu choro pela derrota :D</p>
        
        {#if !messageSent}
        
        <textarea class="p-8 h-[200px] w-[500px] rounded-lg placeholder:text-opacity-30" placeholder="Escreva uma mensagem"></textarea>
        <div class="flex mt-[-100px] justify-end items-center">
          <p class="text-gray font-bold text-sm">200 caracteres restantes</p>
          <div class="bg-terciary p-4 scale-50 rounded-xl border-4 border-terciary hover:border-cyan cursor-pointer hover:scale-[.55] transition-transform"
            on:click={()=>messageSent=true} role="button" tabindex={1} on:keypress={()=>{}}>
            <img src="icons/send.svg" alt="send icon" class=""/>
          </div>
        </div>

        {:else}
        
          <textarea class="p-8 h-[200px] w-[500px] rounded-lg placeholder:text-opacity-30" placeholder=""></textarea>
          <div class="mt-[-150px] flex justify-center items-center flex-col">
            <p class="text-terciary font-bold text-sm">Mensagem registrada!</p>
            <img src="icons/check.svg" alt="check icon"/>
          </div>
        {/if}

      </div>

     <Button text="INICIO" link="/"/>

  </section>

  <Footer />
</main>
