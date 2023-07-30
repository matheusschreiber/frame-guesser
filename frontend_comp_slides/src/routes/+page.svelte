<script>
  import Button from "../components/button.svelte";
  import Footer from "../components/footer.svelte";
  import LineBackground from "../components/lineBackground.svelte";
  import Logo from "../components/logo.svelte";
</script>

<main>
  <header class="flex w-full justify-around items-center my-32">
    <h1 class="text-6xl font-bold text-terciary w-[400px]">Estrutura de Dados II<span class="text-green">_</span></h1>
    <Logo />
  </header>
  <p class="text-gray font-fredoka w-fit mx-auto text-lg">Você conhece mesmo os slides dos seus professores?</p>
  <section class="my-8 p-32 bg-purple m-16 rounded-xl shadow-medium text-center overflow-hidden">
    <LineBackground />
    <h5 class="mx-auto w-fit text-cyan font-bold text-sm mb-4">COMO JOGAR</h5>
    <h1 class="mb-16 text-whitish text-3xl">Adivinhe apenas olhando um slide</h1>
    <div class="flex justify-around mb-16">
      <div class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all">
        <div class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy">
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">1</h1>
          <img src="icons/slide.svg" alt="icon slide" />
        </div>
        <p class="text-whitish">Olhe para todos os detalhes de um slide</p>
      </div>

      <div class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all">
        <div class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy">
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">2</h1>
          <img src="icons/lamp.svg" alt="icon lamp" />
        </div>
        <p class="text-whitish">Use as dicas para ter mais chances de acertar</p>
      </div>

      <div class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all">
        <div class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy">
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">3</h1>
          <img src="icons/trophy.svg" alt="icon trophy" />
        </div>
        <p class="text-whitish">Quanto menos dicas, maior a sua pontuação</p>
      </div>
    </div>

    <Button text="COMEÇAR" link="/register" />
  </section>

  <section class="my-8 flex items-center pt-16 w-full justify-around">
    <div>
      <h5 class="w-fit text-blue font-bold text-sm">DESTAQUE-SE</h5>
      <h1 class="font-bold text-terciary text-5xl mb-4">Ranking</h1>
      <p class="font-fredoka text-gray w-[300px]">
        Reza a lenda que quem acertar mais slides consegue passar o resto da
        faculade <u>sem fazer finais...</u>
      </p>
    </div>
    <div>
      <table>
        <tbody>
          <tr>
            <th>#</th>
            <th>Nome</th>
            <th>Pontuação</th>
          </tr>
          {#each [1, 2, 3, 4] as item}
            <tr>
              <td>{item}</td>
              <td>JOAOZINHO GAMEPLAYS</td>
              <td>1200 pts</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>

  <section class="my-8">
    <h5>DEIXE SEU RECADO</h5>
    <div class="flex">
      {#each [1,2,3,4,5] as item}
      <div>
        <h3>JOAZINHO GAMEPLAYS</h3>
        <p>Esquece fio sou muito bom, nem adianta tentar mais</p>
      </div>
      {/each}
    </div>
  </section>

  <Footer />
</main>
