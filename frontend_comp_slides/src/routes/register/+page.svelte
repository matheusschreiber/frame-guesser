<script lang="ts">
  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";

  import { goto } from "$app/navigation";
  import { api } from "../../services/api";
  import Swal from "sweetalert2";
  import { setContext } from "svelte";

  let username = "";
  let password = "";
  let confirmPassword = "";

  async function handleRegister() {
    if (confirmPassword != password) return;

    try {
      const response = await api.post("user/create/", {
        username,
        password,
      });

      setContext('username', username)
      setContext('password', password) // TODO: retirar isso
      goto("/logged");
    } catch (err: any) {
      Swal.fire("Vish", err.response.data.error, "warning");
    }
  }
</script>

<main>
  <header class="w-full flex justify-center py-8 mt-8">
    <Logo small />
  </header>

  <section class="my-8 py-12 pt-0 bg-purple m-64 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={2} />
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        VAMOS COMEÇAR
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Escolha um nome e senha...</h1>
    </div>

    <div class="flex flex-col w-[350px] gap-4">
      <p class="text-gray font-fredoka">
        Use seu nome mesmo, ou aproveite para esbanjar a criatividade
      </p>
      <input
        class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
        type="text"
        placeholder="NOME"
        name="username"
        max="30"
        bind:value={username}
      />

      <p class="text-gray font-fredoka mt-4">
        Use sua senha mais segura (ex.: senha123)
      </p>
      <input
        class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
        type="password"
        placeholder="SENHA"
        name="password"
        bind:value={password}
      />
      <input
        class="bg-terciary h-12 px-4 z-10 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
        type="password"
        placeholder="CONFIRME A SENHA"
        name="password"
        bind:value={confirmPassword}
      />
      <span
        class="text-red z-0 transition-all
      {confirmPassword != password && confirmPassword != ''
          ? 'mt-0'
          : 'mt-[-40px]'}">As senhas estao diferentes</span
      >

      <a href="/login" class="mt-16"
        ><h4 class="text-pink text-[10pt] mb-[-10px] font-bold underline">
          Já tenho uma conta
        </h4></a
      >
      <Button text="REGISTRAR" func={handleRegister} />
    </div>
  </section>

  <Footer />
</main>
