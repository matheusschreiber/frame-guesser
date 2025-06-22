<script lang="ts">
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";

  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import { deleteCookie, getCookie } from "../../../services/cookies";

  let username:string|undefined=$state(undefined);

  onMount(()=>{
    deleteCookie("runId");
    username = getCookie('username')
    if (!username) goto('/login')
  })

</script>

<main>
  {#if username}
  <section class="my-8 py-12 pt-0 bg-purple lg:m-64 mx-5 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={2} />
    <div class="px-16 lg:px-0">
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        VAMOS COMEÇAR
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Tudo pronto! <b>Boa Sorte!</b></h1>
    </div>

    <div class="bg-secondary p-4 px-8 rounded-lg text-whitish">
        <h2>{username}</h2>
    </div>
    <a
      href="/login"
      class="mb-16 mt-2"
      onclick={() => {
        deleteCookie('auth');
      }}
      role="button"
      tabindex={1}
      onkeypress={() => {}}
    >
      <h4 class="text-pink text-[10pt] font-bold underline">Deslogar</h4>
    </a>

    <div class="my-5 lg:hidden flex w-full items-center gap-3 p-5 bg-terciary">
      <img src="icons/rotate_phone.svg" class="w-10" alt="rotate phone icon" />
      <p class="text-lightgray text-sm text-left">Obs.: Para quem estiver no celular, recomendamos que <b>jogue na horizontal</b>.</p>
    </div>

    <Button text="COMEÇAR" func={() => goto("/session")} />
  </section>
  {:else}
  <section class="my-8 py-12 pt-0 bg-purple m-64 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4 mt-5">
        CARREGANDO...
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Quase lá...</h1>
    </div>
  </section>
  {/if}

</main>
