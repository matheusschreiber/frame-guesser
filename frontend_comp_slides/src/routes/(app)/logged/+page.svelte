<script lang="ts">
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";

  import { goto } from "$app/navigation";
  import { api } from "../../../services/api";
  import Swal from "sweetalert2";
  import { getContext, onMount } from "svelte";

  import { deleteCookie, getCookie } from "../../../services/cookies";

  let username:string|undefined=undefined;

  onMount(()=>{
    deleteCookie("runId");
    username = getCookie('username')
    if (!username) goto('/login')
  })

</script>

<main>
  {#if username}
  <section class="my-8 py-12 pt-0 bg-purple m-64 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={2} />
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        VAMOS COMEÇAR
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Tudo pronto! Boa Sorte!</h1>
    </div>

    <div class="bg-secondary p-4 px-8 rounded-lg text-whitish">
      
        <h2>{username}</h2>
      
    </div>
    <a
      href="/login"
      class="mb-16 mt-2"
      on:click={() => {
        deleteCookie('auth');
      }}
      role="button"
      tabindex={1}
      on:keypress={() => {}}
    >
      <h4 class="text-pink text-[10pt] font-bold underline">Deslogar</h4>
    </a>

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
