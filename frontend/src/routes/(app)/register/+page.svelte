<script lang="ts">
  import toast, { Toaster } from 'svelte-french-toast';
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";
  import { goto } from "$app/navigation";
  import { api } from "../../../services/api";
  import { jwtDecode, type JwtPayload } from "jwt-decode";
  import { deleteCookie, setCookie } from "../../../services/cookies";
  import { onMount } from "svelte";
  import Loading from "../../../components/loading.svelte";

  let username: string = $state();
  let password: string = $state();
  let confirmPassword: string = $state();
  let loading: boolean = $state(false);

  async function handleRegister() {
    loading = true;
    if (confirmPassword != password) return;

    try {
      const responseFromUserCreation = await api.post("user/create/", {
        username,
        password,
      });

      const responseFromTokenAcquisition = await api.post("user/token/", {
        username,
        password,
      });

      let userAccessData: JwtPayload & { username: string } = jwtDecode(
        responseFromTokenAcquisition.data.access,
      );
      username = userAccessData.username;
      setCookie("auth", JSON.stringify(responseFromTokenAcquisition.data));
      setCookie("username", username);
      goto("/logged");
    } catch (err: any) {
      toast.error(err.response.data.error);
    }

    loading = false;
  }

  onMount(() => {
    deleteCookie("auth");
    deleteCookie("username");
  });
</script>

<main>
  <section
    class="my-8 py-12 pt-0 bg-purple lg:m-64 mx-5 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center"
  >
    <LineBackground variant={2} />
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        LET'S START
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Choose a username and password...</h1>
    </div>

    {#if loading}
      <Loading />
    {:else}
      <div class="flex flex-col w-[350px] gap-4 px-5 lg:px-0">
        <p class="text-lightgray font-fredoka">
          Pick a creative username
        </p>
        <input
          class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="text"
          placeholder="USERNAME"
          name="username"
          max="30"
          bind:value={username}
        />

        <p class="text-lightgray font-fredoka mt-4">
          Pick a strong password, and don't forget it!
        </p>
        <input
          class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="password"
          placeholder="PASSWORD"
          name="password"
          bind:value={password}
        />
        <input
          class="bg-terciary h-12 px-4 z-10 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="password"
          placeholder="CONFIRM PASSWORD"
          name="password"
          bind:value={confirmPassword}
        />
        <span
          class="text-red z-0 transition-all
        {confirmPassword != password && confirmPassword != ''
            ? 'mt-0'
            : 'mt-[-40px]'}">Passwords don't match</span
        >

        <a href="/login" class="mt-16"
          ><h4 class="text-pink text-[10pt] mb-[-10px] font-bold underline">
            I already have an account
          </h4></a
        >
        <div class="flex justify-center">
          <Button text="REGISTER" func={handleRegister} />
        </div>
      </div>
    {/if}
  </section>
  <Toaster />
</main>
