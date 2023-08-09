<script lang="ts">
  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";

  import { goto } from "$app/navigation";
  import { api } from "../../services/api";
  import Swal from "sweetalert2";

  let username = "";
  let password = "";
</script>

<main>
  <header class="w-full flex justify-center py-8 mt-8">
    <Logo small />
  </header>

  <section
    class="my-8 py-12 pt-0 bg-purple m-32 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center"
  >
    <LineBackground variant={2} />
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        VAMOS COMEÇAR
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Tudo pronto! Boa Sorte!</h1>
    </div>

    <div class="bg-secondary p-4 px-8 rounded-lg text-whitish">
      <h2>JOAOZINHO gameplay</h2>
    </div>
    <a
      href="/"
      class="mb-16 mt-2"
      on:click={() => {
        localStorage.clear();
      }}
      role="button"
      tabindex={1}
      on:keypress={() => {}}
    >
      <h4 class="text-pink text-[10pt] font-bold underline">Deslogar</h4>
    </a>

    <Button text="COMEÇAR" func={() => goto("/session")} />
  </section>

  <Footer />
</main>
