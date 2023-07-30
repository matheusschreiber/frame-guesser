<script>

  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";

</script>

<main>
  <header class="w-full flex justify-center py-8 mt-8">
    <Logo small />
  </header>

  <section class="my-8 py-12 bg-purple m-16 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={2} />
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">VAMOS COMEÇAR</h5>
      <h1 class="mb-16 text-whitish text-3xl">Escolha um nome e senha...</h1>
    </div>

    <div class="flex flex-col w-[350px] gap-4">
      <p class="text-gray font-fredoka">Use seu nome mesmo, ou aproveite para esbanjar a criatividade</p>
      <input class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray" type="text" placeholder="NOME" name="username" max="30"/>
      <input class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray" type="password" placeholder="SENHA" name="password"/>
      <p class="text-gray font-fredoka mb-16">Use sua senha mais segura (ex.: senha123)</p>
      <Button text="COMEÇAR" link="/session"/>
    </div>
  </section>


  <Footer />
</main>