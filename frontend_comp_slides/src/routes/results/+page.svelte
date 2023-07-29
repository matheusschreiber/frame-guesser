<script>
  import Footer from "../../components/footer.svelte";
import Logo from "../../components/logo.svelte";

</script>

<main>
  <header>
    <Logo />
  </header>

  <section>
    <h5>RESULTADOS</h5>
    Sua pontuação

    <div>
      <div>icone</div>
      <h1>1250 pts</h1>
      <div>icone</div>
      <p>Wow! Isso tudo?</p>
    </div>

    <h2>
      Você está <u>62,2%</u> acima da média dos usuários
    </h2>
    <p>Você acertou 5 de 10 slides, parabéns!</p>

     <div class="flex flex-wrap">
      {#each [1,2,3,4,5] as item}
      <div>
        <h5>FÁCIL</h5>
        <img src="messi.jpg" alt="slide-miniature" class="w-[100px]"/>
        <div>
          <h1>RICARDO CARMINATI</h1>
          <p>SINAIS E SISTEMAS</p>
        </div>
      </div>
      {/each}
     </div>

     <div class="flex">
      <p>Deixe seu recado pela vitória, ou seu choro pela derrota :D</p>
      <textarea>Escreva uma mensagem</textarea>
      <div>200 caracteres restantes</div><button>icone</button>
     </div>

  </section>

  <Footer />
</main>
