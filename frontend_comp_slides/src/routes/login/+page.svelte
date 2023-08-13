<script lang="ts">
  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";

  import { goto } from "$app/navigation";
  import { api } from "../../services/api";
  import Swal from "sweetalert2";
  import { onMount, setContext } from "svelte";
  import Loading from "../../components/loading.svelte";

  let username = "";
  let password = "";

  let loading = false;

  // adding 'form' submition with 'enter'
  onMount(() => {
    let inputPassword = document.getElementsByName("password")[0];
    inputPassword.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        handleLogin();
      }
    });
  });

  async function handleLogin() {
    try {
      loading = true;
      const response = await api.post(
        "user/login/",
        {},
        {
          auth: {
            username,
            password,
          },
        }
      );
      // setContext("username", username);
      // setContext("password", password); // TODO: retirar isso
      setTimeout(() => goto("/logged"), 3000); //FIXME: remove this timeout (this is because the set context takes time to be executed)
    } catch (err: any) {
      Swal.fire("Vish", "Credenciais inválidas ", "warning");
      loading = false;
    }
  }
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
      <h1 class="mb-16 text-whitish text-3xl">
        Faça seu login, ou crie uma conta
      </h1>
    </div>

    <div class="flex flex-col w-[350px] gap-4">
      <input
        class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
        type="text"
        placeholder="NOME"
        name="username"
        max="30"
        bind:value={username}
      />
      <input
        class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
        type="password"
        placeholder="SENHA"
        name="password"
        bind:value={password}
      />

      {#if loading}
        <Loading />
      {:else}
        <a href="/register" class="mt-16">
          <h4 class="text-pink text-[10pt] font-bold mb-[-10px] underline">
            Ainda não tenho uma conta
          </h4>
        </a>
        <Button text="LOGIN" func={handleLogin} />
      {/if}
    </div>
  </section>

  <Footer />
</main>
