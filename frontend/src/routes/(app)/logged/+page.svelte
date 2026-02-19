<script lang="ts">
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";

  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import { deleteCookie, getCookie } from "../../../services/cookies";

  let username:string|undefined=$state(undefined);
  let currentRun:number|undefined=$state(undefined);

  onMount(()=>{
    username = getCookie('username')
    currentRun = parseInt(getCookie("runId"));
    if (!username) goto('/login')
  })

</script>

<main>
  {#if username}
  <section class="my-8 py-12 pt-0 bg-purple lg:mx-64 mx-5 px-5 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={2} />
    <div class="px-16 lg:px-0">
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">
        LET'S GO!
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">All ready! <b>Good luck!</b></h1>
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
      <h4 class="text-pink text-[10pt] font-bold underline">Logout</h4>
    </a>

    {#if currentRun}
      <p class="text-lightgray text-sm mb-5">
        You have an active session! Click below to continue where you left off!
      </p>
    {/if}
    <Button text={currentRun?"CONTINUE":"PLAY"} func={() => goto("/session")} />
  </section>
  {:else}
  <section class="my-8 py-12 pt-0 bg-purple m-64 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <div>
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4 mt-5">
        LOADING...
      </h5>
      <h1 class="mb-16 text-whitish text-3xl">Almost there...</h1>
    </div>
  </section>
  {/if}

</main>
