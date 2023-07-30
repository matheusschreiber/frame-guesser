<script>

  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";

</script>

<main>
  <header>
    <Logo />
  </header>

  <section>
    <div>
      <h5>VAMOS COMEÇAR</h5>
      <h1>Escolha um nome e senha...</h1>
    </div>

    <div>
      <p>Use seu nome mesmo, ou aproveite para esbanjar a criatividade</p>
      <input type="text" placeholder="NOME" name="username" max="30"/>
      <input type="password" placeholder="SENHA" name="password"/>
      <p>Use sua senha mais segura (ex.: senha123)</p>
      <Button text="COMEÇAR" link="/session"/>
    </div>
  </section>


  <Footer />
</main>