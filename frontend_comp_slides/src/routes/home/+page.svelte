<script>
  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";
</script>

<main>
  <header>
    <h1 class="text-4xl font-bold">Estrutura de Dados II</h1>
    <Logo />
  </header>

  <section class="my-8">
    <h5 >COMO JOGAR</h5>
    <h1>Adivinhe apenas olhando um slide</h1>
    <div class="flex gap-8">
      <div>
        <h1>1</h1>
        <img src="" alt="icone slide" />
        <p>Olhe para todos os detlahes de um slide</p>
      </div>

      <div>
        <h1>2</h1>
        <img src="" alt="icone lampada" />
        <p>use as dicas para ter mais chances de acertar</p>
      </div>

      <div>
        <h1>3</h1>
        <img src="" alt="icone trofeu" />
        <p>Quanto menos dicas, maior a sua pontuação</p>
      </div>
    </div>

    <Button text="COMEÇAR" link="/register" />
  </section>

  <section class="my-8">
    <div>
      <h5>DESTAQUE-SE</h5>
      <h1>Ranking</h1>
      <p>
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
