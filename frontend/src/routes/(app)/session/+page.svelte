<script lang="ts">
  import Swal from "sweetalert2";
  import LineBackground from "../../../components/lineBackground.svelte";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { api } from "../../../services/api";
  import Loading from "../../../components/loading.svelte";
  import { getCookie, setCookie } from "../../../services/cookies";
  
  let correctAnswerCatchPhrases = [
    "Se continuar assim vai até parecer que presta atenção nas aulas!",
    "Uau, será que temos um gênio aqui ou foi pura sorte?",
    "Ótimo trabalho! Só falta manter esse ritmo por mais de 5 minutos.",
    "Impressionante! Estou quase acreditando que você estudou!",,
    "Parabéns! Se continuar assim, talvez um dia nem precise chutar.",
    "Você é incrível! Mas não se acostuma, ainda tem muito pela frente.",
    "Continue com o bom trabalho! Ou pelo menos continue enganando bem.",
    "Se continuar assim, talvez até sua mãe comece a se orgulhar.",
    "Muito bem! Continue assim e talvez eu pare de duvidar de você.",
    "Inacreditável! Estou começando a desconfiar que você está trapaceando.",
  ]

  let wrongAnswerCatchPhrases = [
    "Alguém andou faltando algumas aulas",
    "Eita! Se errar fosse um esporte, você já estaria nas Olimpíadas.",
    "Bom, pelo menos você foi consistente... em errar.",
    "Interessante abordagem! Errada, mas interessante.",
    "Quase! Só faltou acertar.",
    "A resposta certa estava logo ali... Mas você escolheu ignorá-la.",
    "Se o objetivo era errar, parabéns, missão cumprida!",
    "Talvez a resposta certa estivesse se escondendo de você dessa vez.",
    "Pelo menos você está mantendo a média... lá embaixo.",
    "Eu poderia fingir que essa resposta está certa... Mas nem eu sou tão generoso.",
    "Você não errou, apenas encontrou um jeito diferente (e incorreto) de responder.",
    "A resposta certa estava a um neurônio de distância. Pena que ele estava de folga.",
    "Você errou com tanta confiança que até me fez duvidar da resposta certa.",
  ]

  let confirm = $state(false);
  let selected: number | null = $state(null);
  let hintsUsed = $state(0);
  let totalHintsAmount = $state(0);

  let slidesLeftAmount: number = $state();
  let difficultyLevel: number = $state();

  var loading = $state(true);
  var hasAnswered = $state(false);
  var answer: number | null = $state(null);
  var loadingHint = $state(false);

  var options = $state([
    "Carregando... | Carregando...",
    "Carregando... | Carregando...",
    "Carregando... | Carregando...",
    "Carregando... | Carregando...",
  ]);
  var slideImage: string | undefined = $state();

  function handleConfirm() {
    if (hasAnswered) return;

    if (confirm) {
      fetchNewHint();
      if (hintsUsed < totalHintsAmount) hintsUsed++;
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

    let response;
    try {
      response = await api.put("slide/answer/" + runId, {
        answer: options[selected ? selected : 0],
      });
    } catch (err:any) {
      await Swal.fire("Vish", "Problema inesperado! Tente novamente mais tarde.", "warning");
      return
    }

    if (response.data.answer == true) {
      Swal.fire({
        title: "<strong>BOA! RESOSTA CERTA!</strong>",
        icon: "success",
        html: correctAnswerCatchPhrases[Math.floor(Math.random() * correctAnswerCatchPhrases.length)],
        showConfirmButton: false,
        showCloseButton: true,
      });
    } else if (response.data.answer == false) {
      Swal.fire({
        title: "<strong>OPS! MAIS SORTE NA PRÓXIMA</strong>",
        icon: "error",
        html: wrongAnswerCatchPhrases[Math.floor(Math.random() * wrongAnswerCatchPhrases.length)],
        showConfirmButton: false,
        showCloseButton: true,
      });
    } else {
      Swal.fire("Uai", "Houve algum problema com os servidores", "error").then(
        () => {
          selected = null;
        },
      );
    }

    slideImage =
      import.meta.env.VITE_API_URL + "/" + response.data.slide_image_path;

    options.map((option: string, idx: number) => {
      if (option.toLowerCase() == response.data.slide.toLowerCase())
        answer = idx;
    });

    loading = false;
    hasAnswered = true;
  }

  async function handleNextSlide() {
    loading = true;

    if (!hasAnswered) {
      handleAnswerSlide();
    } else {
      await fetchSlide();
    }

    loading = false;
  }

  async function fetchSlide() {
    hasAnswered = false;
    loading = true;
    answer = null;
    selected = null;
    hintsUsed = 0;

    let response;
    let currentRun = getCookie("runId");

    try {
      if (currentRun && currentRun != "undefined") {
        response = await api.get("slide/random/" + currentRun);
      } else {
        response = await api.get("slide/random");
      }
    } catch (err:any) {
      if (err.response.status === 301) {
        goto(`/results`);
      } else {
        await Swal.fire("Uai", "Houve algum problema com os servidores", "error");
      }
      
      return;
    }

    slideImage =
      import.meta.env.VITE_API_URL + "/" + response.data.slide_image_path;

    setCookie("runId", response.data.run_id);
    loading = false;
    difficultyLevel = response.data.difficulty_level;
    options = response.data.slide_alternatives;
    hintsUsed = response.data.hints_used;
    slidesLeftAmount = response.data.slides_left_amount;
    totalHintsAmount = response.data.hints_total;
    hasAnswered = hintsUsed == totalHintsAmount ? true : false;
  }

  async function fetchNewHint() {
    loadingHint = true;
    let runId = getCookie("runId");
    if (!runId) {
      Swal.fire(
        "Uai",
        "Houve algum problema com a sua sessão, redirecionando...",
        "error",
      );
      return;
    }

    try {
      const response = await api.post("slide/hint/" + runId);
      slideImage = import.meta.env.VITE_API_URL + "/" + response.data.slide_image_path;
      loadingHint = false;
    } catch (err:any) {
      await Swal.fire("Vish", "Problema inesperado! Tente novamente mais tarde.", "warning");
    }
  }

  function clickOutside(element: any, callbackFunction: Function) {
    function onClickBody(event: Event) {
      if (!element.contains(event.target)) {
        callbackFunction();
      }
    }
    document.body.addEventListener("click", onClickBody);
    return {
      update(newCallbackFunction: Function) {
        callbackFunction = newCallbackFunction;
      },
      destroy() {
        document.body.removeEventListener("click", onClickBody);
      },
    };
  }

  onMount(() => {
    fetchSlide();

    // script to automatically scroll to the main content of the page
    let d = document.getElementById("div-scroll-main");
    if (d) {
      window.scrollTo({
        top: d.offsetTop - 25,
        left: 0,
        behavior: "smooth",
      });
    }
  });
</script>

<main>
  <section class="my-8 pt-12 pb-24 bg-purple lg:w-fit w-full lg:px-32 px-3 m-auto rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
    <LineBackground variant={3} />

    <div id="div-scroll-main">
      <h5 class="mx-auto w-fit font-bold text-sm mb-0">
        {#if difficultyLevel === 5}
          <span class="text-red">NÍVEL DIFÍCIL</span>
        {:else if difficultyLevel === 4}
          <span class="text-orange">NÍVEL QUASE DIFÍCIL</span>
        {:else if difficultyLevel === 3}
          <span class="text-yellow">NÍVEL NORMAL</span>
        {:else if difficultyLevel === 2}
          <span class="text-green">NÍVEL FÁCIL</span>
        {:else if difficultyLevel === 1}
          <span class="text-blue">NÍVEL MUITO FÁCIL</span>
        {/if}
      </h5>
      <h2 class="text-whitish text-3xl">De quem é esse slide?</h2>
    </div>

    <div class="flex lg:flex-row flex-col">
      <aside class="lg:w-[600px] flex flex-col justify-end">
        {#if slideImage != ""}
          <div class="flex w-[90%] mx-auto justify-start mb-[-10px]">
            <h3 class="mt-4 text-whitish bg-terciary w-fit px-2 py-1 pb-3 rounded-lg text-sm">
              {10-slidesLeftAmount+1}/{10}
            </h3>
          </div>
        {/if}

        {#if slideImage == ""}
          <Loading />
        {:else}
          <img class="rounded-lg h-[400px]" src={slideImage} alt="slide" />
        {/if}
      </aside>

      <aside class="flex flex-col items-center justify-end px-6">
        <div class="flex lg:flex-col flex-wrap mt-4 lg:mt-0 gap-4 justify-center lg:justify-between pb-8 items-center lg:h-[350px]">
          {#each options as item, i}
            <div
              onclick={() => handleSelection(i)}
              role="button"
              tabindex={2}
              onkeypress={() => {}}
              class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 select-none w-[200px]
              {answer == i
                ? 'border-green'
                : selected == i
                  ? hasAnswered
                    ? 'border-red'
                    : 'border-pink'
                  : hasAnswered
                    ? 'opacity-[.3] border-secondary cursor-not-allowed'
                    : 'border-secondary'}"
            >
              <h3 class="text-whitish font-bold text-sm">
                {item.split("|")[0].trim()}
              </h3>
              <p class="text-gray text-sm">{item.split("|")[1].trim()}</p>
            </div>
          {/each}
        </div>

        <div class="flex justify-around w-full h-[50px]">
          <div class="flex flex-col items-center">
            {#if loadingHint}
              <Loading />
            {:else}
              {#if hintsUsed > 0}
                <p class="absolute font-fredoka text-sm text-whitish mt-[-25px]">
                  {hintsUsed}/{totalHintsAmount}
                </p>
              {/if}
              <div
                use:clickOutside={() => (confirm = false)}
                onclick={hintsUsed != totalHintsAmount
                  ? () => handleConfirm()
                  : null}
                role="button"
                tabindex={1}
                class="bg-secondary rounded-3xl shadow-medium h-12 w-12 flex
                justify-center items-center border-2 select-none
                {confirm ? 'border-yellow' : 'border-secondary'}
                {hintsUsed == totalHintsAmount || hasAnswered
                  ? 'opacity-20 cursor-not-allowed'
                  : 'opacity-100 cursor-pointer'}"
                onkeypress={() => {}}
              >
                <img
                  src="icons/lamp.svg"
                  alt="icon lamp"
                  style="height:20px"
                  class={confirm ? "hidden" : "flex"}
                />
                <img
                  src="icons/tip.svg"
                  alt="confirm icon"
                  style="height:20px"
                  class={confirm ? "flex" : "hidden"}
                />
              </div>
              {#if confirm}
                <p class="absolute font-fredoka text-sm text-whitish mt-16">
                  Clique novamente para confirmar a sua dica
                </p>
              {/if}
            {/if}
          </div>

          {#if loading}
            <Loading />
          {:else}
            <button
              class="px-4 py-2 h-12 bg-terciary font-bold text-sm rounded-lg border-2
            {selected == null
                ? 'border-terciary text-whitish'
                : answer == null
                  ? 'border-pink text-pink'
                  : selected == answer
                    ? 'border-green text-green'
                    : 'border-red text-red'}"
              onclick={loading ? null : () => handleNextSlide()}
            >
              {hasAnswered ? "AVANÇAR" : "VERIFICAR"}
            </button>
          {/if}
        </div>
      </aside>
    </div>
  </section>
</main>
