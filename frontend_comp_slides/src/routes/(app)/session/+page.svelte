<script lang="ts">
  import Swal from "sweetalert2";
  import LineBackground from "../../../components/lineBackground.svelte";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { api } from "../../../services/api";
  import Loading from "../../../components/loading.svelte";
  import { getCookie, setCookie } from "../../../services/cookies";

  let confirm = false;
  let selected: number | null = null;
  let hintsAmount = 0;
  let hintsUsed = 0;

  let currentSlide = 1;
  let slidesAmount = 5;
  let difficultyLevel: number;

  var loading = true;
  var hasAnswered = false;
  var answer: number | null = null; 
  var loadingHint = false;

  var options = [
    "Nome Professor | Estrutura de Dados I",
    "Nome Professor | Estrutura de Dados II",
    "Nome Professor | Estrutura de Dados III",
    "Nome Professor | Estrutura de Dados IV",
  ];
  var slideImage = "";

  function handleConfirm() {
    if (hasAnswered) return;

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
    const response = await api.put("slide/answer/" + runId, { answer: options[selected ? selected : 0], });

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
      Swal.fire("Uai", "Houve algum problema com os servidores", "error").then(
        () => {
          selected = null;
        }
      );
    }

    slideImage = import.meta.env.VITE_API_URL + '/' + response.data.slide_image_path;

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
    if (currentSlide == slidesAmount) goto(`/results`, { replaceState: false });

    hasAnswered = false;
    loading = true;
    answer = null;
    selected = null;
    hintsUsed = 0;
    
    let response;
    let currentRun = getCookie("runId");

    try {
      if (currentRun && currentRun!="undefined"){
        response = await api.get("slide/random/"+currentRun);
      } else {
        response = await api.get("slide/random");
      }
    } catch(err) {
      Swal.fire("Uai", "Houve algum problema com os servidores", "error")
      return;
    }

    slideImage = import.meta.env.VITE_API_URL + '/' +response.data.slide_image_path;
    hintsAmount = response.data.hints_amount - 1;
    setCookie("runId", response.data.run_id);
    slidesAmount = response.data.slides_left_amount
    loading = false;
    difficultyLevel = response.data.difficulty_level
  }

  async function fetchNewHint() {
    loadingHint = true
    let runId = getCookie("runId");
    if (!runId) {
      Swal.fire("Uai", "Houve algum problema com a sua sessão, redirecionando...", "error")
      return;
    }

    const response = await api.post("slide/hint/" + runId);

    slideImage = import.meta.env.VITE_API_URL + '/' +response.data.slide_image_path;
    loadingHint = false
  }

  function clickOutside(element:any, callbackFunction:Function) {
		function onClickBody(event:Event) {
			if (!element.contains(event.target)) {
				callbackFunction();
			}
		}
		document.body.addEventListener('click', onClickBody);
		return {
			update(newCallbackFunction:Function) {callbackFunction = newCallbackFunction;},
			destroy() {document.body.removeEventListener('click', onClickBody);}
		}
	}

  onMount(() => {
    fetchSlide();

    // script to automatically scroll to the main content of the page
    let d = document.getElementById('div-scroll-main')
    if (d){
      window.scrollTo({
        top: d.offsetTop-25,
        left: 0,
        behavior: "smooth",
      })
    }
  });
</script>

<main>
  <section class="my-8 pt-12 pb-24 bg-purple w-fit px-32 m-auto rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center">
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

    <div class="flex">
      <aside class="w-[600px] flex flex-col justify-end">
        {#if slideImage != ""}
          <div class="flex w-[90%] mx-auto justify-start mb-[-10px]">
            <h3 class="mt-4 text-whitish bg-terciary w-fit px-2 py-1 pb-3 rounded-lg text-sm">
              {currentSlide}/{slidesAmount}
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
        <div class="flex flex-col gap-4 justify-between pb-8 items-center h-[350px]">
          {#each options as item, i}
            <div
              on:click={() => handleSelection(i)}
              role="button"
              tabindex={2}
              on:keypress={() => {}}
              class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 select-none w-[200px]
              {answer == i
                ? 'border-green'
                : selected == i
                ? hasAnswered
                  ? 'border-red'
                  : 'border-pink'
                : hasAnswered ? 'opacity-[.3] border-secondary cursor-not-allowed':'border-secondary'}">
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
                  {hintsUsed}/{hintsAmount}
                </p>
              {/if}
              <div
                use:clickOutside={() => confirm = false}
                on:click={hintsUsed != hintsAmount ? () => handleConfirm() : null}
                role="button"
                tabindex={1}
                class="bg-secondary rounded-3xl shadow-medium h-12 w-12 flex
                justify-center items-center border-2 select-none
                {confirm ? 'border-yellow' : 'border-secondary'}
                {hintsUsed == hintsAmount || hasAnswered
                  ? 'opacity-20 cursor-not-allowed'
                  : 'opacity-100 cursor-pointer'}"
                on:keypress={() => {}}>
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
                : answer == null ? 'border-pink text-pink' 
                : selected == answer ? 'border-green text-green' : 'border-red text-red'}"
              on:click={loading ? null : () => handleNextSlide()}
            >
              {hasAnswered ? "AVANÇAR" : "VERIFICAR"}
            </button>
          {/if}
        </div>
      </aside>
    </div>

  </section>
</main>
