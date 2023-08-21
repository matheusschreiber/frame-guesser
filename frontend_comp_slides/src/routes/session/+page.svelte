<script lang="ts">
  import Swal from "sweetalert2";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";
  import { goto } from "$app/navigation";
  import { getContext, onMount, setContext } from "svelte";
  import { api } from "../../services/api";
  import Loading from "../../components/loading.svelte";
  import { getCookie, setCookie } from "../../services/cookies";

  let confirm = false;
  let selected: number | null = null;
  let hintsAmount = 0;
  let hintsUsed = 0;

  let currentSlide = 1;
  let slidesAmount = 5;

  var loading = true;
  var hasAnswered = false;
  var answer: number | null = null;
  var loadingHint = false;

  var username: string = getContext("username");
  var password: string = getContext("password"); //TODO: remove this when AUTH2.0 is added

  var options = [
    "Nome Professor | Estrutura de Dados I",
    "Nome Professor | Estrutura de Dados II",
    "Nome Professor | Estrutura de Dados III",
    "Nome Professor | Estrutura de Dados IV",
  ];
  var slideImage = "";

  function handleConfirm() {
    if (confirm) {
      fetchNewHint();
      if (hintsUsed + 1 <= hintsAmount) hintsUsed++;
      confirm = false;
    } else confirm = true;
  }

  function handleSelection(pos: number) {
    if (hasAnswered) return;

    if (selected == pos) selected = null;
    else selected = pos;
  }

  async function handleAnswerSlide() {
    let runId = getCookie("runId");
    if (!runId) return;
    const response = await api.put(
      "slide/answer/" + runId,
      {
        answer: options[selected ? selected : 0],
      },
      {
        auth: { username: "matheus", password: "123123abc" },
      }
    );

    if (response.data.answer == true) {
      Swal.fire({
        title: "<strong>BOA! RESOSTA CERTA!</strong>",
        icon: "success",
        html: "Sabe muito!",
        showConfirmButton: false,
      });
    } else if (response.data.answer == false) {
      Swal.fire({
        title: "<strong>OPS! MAIS SORTE NA PRÓXIMA</strong>",
        icon: "error",
        html: "Alguém andou faltando algumas aulas",
        showConfirmButton: false,
      });
    } else {
      Swal.fire("uai", "Houve algum problema com os servidores", "error").then(
        () => {
          selected = null;
        }
      );
    }

    slideImage = import.meta.env.VITE_API_URL + response.data.slide_image_path;

    options.map((option: string, idx: number) => {
      if (option.toLowerCase() == response.data.slide.toLowerCase())
        answer = idx;
    });

    loading = false;
    hasAnswered = true;
  }

  async function handleNextSlide() {
    loading = true;

    if (!hasAnswered) handleAnswerSlide()
    else {
      await fetchSlide()
      currentSlide++;
    }
  }

  async function fetchSlide() {
    // if (!username || !password) return; //FIXME: chango to auth2
    if (currentSlide == slidesAmount) goto(`/results`, { replaceState: false });

    hasAnswered = false;
    loading = true;
    answer = null;
    selected = null;
    hintsUsed = 0;
    // TODO: add error catching
    const response = await api.get("slide/random", {
      auth: { username: "matheus", password: "123123abc" },
    });
    slideImage = import.meta.env.VITE_API_URL + response.data.slide_image_path;
    hintsAmount = response.data.hints_amount - 1;
    setCookie("runId", response.data.run_id);
    loading = false;
  }

  async function fetchNewHint() {
    loadingHint = true
    let runId = getCookie("runId");
    if (!runId) return; // TODO: add better error catching...

    const response = await api.post(
      "slide/hint/" + runId,
      {},
      {
        auth: { username: "matheus", password: "123123abc" },
      }
    );

    slideImage = import.meta.env.VITE_API_URL + response.data.slide_image_path;
    loadingHint = false
  }

  onMount(() => {
    fetchSlide();
  });
</script>

<main>
  <header class="w-full flex justify-center items-center py-8 mt-8">
    <Logo small />
  </header>

  <section class="my-8 py-12 pb-24 bg-purple w-fit px-32 m-auto rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={3} />
    <div class="flex flex-col items-center justify-center">
      <h5 class="mx-auto w-fit text-red font-bold text-sm mb-4">
        NÍVEL DIFÍCIL
        <!-- TODO: get this from backend -->
      </h5>
      <h2 class="text-whitish text-3xl">De quem é esse slide?</h2>
      <h3 class="mb-8 mt-4 text-whitish bg-terciary w-fit rounded-lg p-4">
        {currentSlide}/{slidesAmount}
      </h3>
    </div>

    {#if slideImage == ""}
      <Loading />
    {:else}
      <img class="w-[400px]" src={slideImage} alt="slide" />
    {/if}
    
    <!-- TODO: REFACTOR THIS PAGE, THE UX/UI IS TRASH!!! -->

    <!-- <div class="grid grid-cols-2 gap-2 mt-16"> -->
    <div class="flex gap-2 mt-16">
      {#each options as item, i}
        <div
          on:click={() => handleSelection(i)}
          role="button"
          tabindex={2}
          on:keypress={() => {}}
          class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 select-none
          {answer == i
            ? 'border-green'
            : selected == i
            ? hasAnswered
              ? 'border-red'
              : 'border-pink'
            : 'border-secondary'}">
          <h3 class="text-whitish font-bold text-sm">
            {item.split("|")[0].trim()}
          </h3>
          <p class="text-gray text-sm">{item.split("|")[1].trim()}</p>
        </div>
      {/each}
    </div>

    <div class="flex justify-center mt-16">
      <div class="flex flex-col items-center">
        {#if loadingHint}
          <Loading />
        {:else}
          {#if hintsUsed > 0}
            <p class="absolute font-fredoka text-sm text-whitish w-32 mt-2">
              {hintsUsed}/{hintsAmount}
            </p>
          {/if}
          <div
            on:click={hintsUsed != hintsAmount ? () => handleConfirm() : null}
            role="button"
            tabindex={1}
            class="bg-secondary p-4 rounded-3xl shadow-medium scale-[.4] h-28 w-28 flex
            justify-center items-center border-4 select-none
            {confirm ? 'border-yellow' : 'border-secondary'}
            {hintsUsed == hintsAmount
              ? 'opacity-20 cursor-not-allowed'
              : 'opacity-100 cursor-pointer'}"
            on:keypress={() => {}}>
            <img
              src="icons/lamp.svg"
              alt="icon lamp"
              class={confirm ? "hidden" : "flex"}
            />
            <img
              src="icons/tip.svg"
              alt="confirm icon"
              class={confirm ? "flex" : "hidden"}
            />
          </div>
          {#if confirm}
            <p class="absolute font-fredoka text-sm text-whitish mt-24 w-32 ml-[-10px]">
              Clique novamente para confirmar a sua dica
            </p>
          {/if}
        {/if}

      </div>

      {#if loading}
        <Loading />
      {:else}
        <button
          class="px-4 py-2 my-8 bg-terciary font-bold text-sm rounded-lg border-2
        {selected == null
            ? 'border-terciary text-whitish'
            : answer == null ? 'border-pink text-pink' 
            : selected == answer ? 'border-green text-green' : 'border-red text-red'}"
          on:click={loading ? null : () => handleNextSlide()}
        >
          {hasAnswered ? "AVANÇAR" : "VERIFICAR"}
        </button>
      {/if}
    </div>
  </section>

  <Footer />
</main>
