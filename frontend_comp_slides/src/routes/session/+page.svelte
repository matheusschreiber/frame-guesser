<script>
  import Footer from "../../components/footer.svelte";
import Logo from "../../components/logo.svelte";

</script>
<main>
  <header>
    <Logo />
  </header>

  <section>
    <div>
      <h5>NÍVEL DIFÍCIL</h5>
      <h2>De quem é esse slide?</h2>
    </div>

    <img class="w-[400px]" src="messi.jpg" alt="slide"/>

    <div class="flex items-center gap-8">
      <div>icone</div>

      <div>
        <h3>RICARDO CARMINATI</h3>
        <p>SINAIS E SISTEMAS</p>
      </div>

      <div>
        <h3>THIAGO DOS SANTOS</h3>
        <p>SINAIS E SISTEMAS</p>
      </div>
      
      <div>
        <h3>RICARDO CARMINATI</h3>
        <p>SINAIS E SISTEMAS</p>
      </div>

      <div>
        <h3>THIAGO DOS SANTOS</h3>
        <p>SINAIS E SISTEMAS</p>
      </div>
    </div>

    <button>PRÓXIMO</button>
  </section>

  <Footer />
</main>