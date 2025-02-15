<script lang="ts">
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";
  import { goto } from "$app/navigation";
  import { api } from "../../../services/api";
  import Swal from "sweetalert2";
  import { onMount, setContext } from "svelte";
  import Loading from "../../../components/loading.svelte";
  import { getCookie, setCookie } from "../../../services/cookies";
  import { jwtDecode, type JwtPayload } from "jwt-decode";

  let username:string|undefined;
  let password:string|undefined;

  let loading = false;

  onMount(() => {
    
    // adding 'form' submition with 'enter'
    let inputPassword = document.getElementsByName("password")[0];
    inputPassword.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        handleLogin();
      }
    });

    const rawTokens = getCookie('auth')
    username = getCookie('username')
    if (rawTokens && username) goto('/logged')

  });

  async function handleLogin() {
    if (!username || !password) {
      Swal.fire("Uai", "Ainda tem campos não preenchidos ", "warning");
      return;
    }

    try {
      loading = true;
      const response = await api.post(
        "user/token/",
        {
          username,
          password
        },
      );

      if (response.status === 200) {
        let userAccessData:JwtPayload & {username:string} = jwtDecode(response.data.access)
        username = userAccessData.username
        setCookie("auth", JSON.stringify(response.data));
        setCookie("username", username);
        goto("/logged");

      } else {
        await Swal.fire("Vish", "Credenciais inválidas ", "warning");
      }

    } catch (err: any) {
      
      if (err.response.status === 401) {
        await Swal.fire("Uai", "Credenciais inválidas!", "warning");
      } else {
        await Swal.fire("Vish", "Problema inesperado!", "warning");
      }
    }

    loading = false;
  }
</script>

<main>
  <section class="my-8 py-12 pt-0 bg-purple m-64 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
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
      {#if loading}
        <Loading />
      {:else}
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
        <a href="/register" class="mt-16">
          <h4 class="text-pink text-[10pt] font-bold mb-[-10px] underline">
            Ainda não tenho uma conta
          </h4>
        </a>
        <div class="flex justify-center">
          <Button text="LOGIN" func={handleLogin} />
        </div>
      {/if}
    </div>
  </section>
</main>
