<script lang="ts">
  import { onMount } from "svelte";
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";
  import { getCookie } from "../../../services/cookies";
  import { api } from "../../../services/api";
  import Swal from "sweetalert2";
  import { goto } from "$app/navigation";
  import Difficulty from "../../../components/difficulty.svelte";
  let messageSent = false;

  type SlideReportType = {
    has_hit: number;
    prof_discipline: string;
    slide_image_path: string;
    difficulty_level: number;
  };

  let runId: string | undefined;
  let totalPoints: number;
  let slidesReportsList: SlideReportType[] = [];
  let aboveAveragePercentage: string;
  let belowAveragePercentage: string;
  let slidesHitsCount: number;

  onMount(() => {
    runId = getCookie("runId");
    if (runId) {
      fetchResults();
    } else {
      goto("/");
    }
  });

  async function fetchResults() {
    try {
      const response = await api.get("/history/" + runId);
      if (response.data) {
        totalPoints = response.data.total_points;
        slidesReportsList = response.data.slides_reports_list;
        aboveAveragePercentage = (response.data.above_average_percentage * 100).toFixed(2)
        belowAveragePercentage = (response.data.below_average_percentage * 100).toFixed(2)
        slidesHitsCount = response.data.slides_hits_count;
      } else {
        throw Error()
      }

    } catch (err) {
      Swal.fire("Vish", "Problema inesperado!", "warning");
    }
  }
</script>

<main>
  <section
    class="my-8 py-12 bg-purple m-16 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center"
  >
    <LineBackground variant={4} />
    <h5 class="mx-auto w-fit text-pink font-bold text-sm mb-4">RESULTADOS</h5>
    <p class="text-whitish text-2xl">Sua pontuação</p>
    <div class="flex items-center gap-4 my-4">
      <img src="icons/star.svg" alt="star icon" />
      <h1 class="text-whitish text-5xl font-bold">{totalPoints} pts</h1>
      <img src="icons/star.svg" alt="star icon" />
    </div>
    {#if totalPoints > 25}
      <p class="text-gray font-fredoka text-sm">Wow! Isso tudo?</p>
    {:else}
      <p class="text-gray font-fredoka text-sm">
        Alguém tá há muito tempo longe do classroom...
      </p>
    {/if}

    <h2 class="text-3xl text-whitish mt-16">
      {#if aboveAveragePercentage}
        Você está <u class="text-yellow font-bold">{aboveAveragePercentage}%</u>
        acima da média dos usuários
      {:else}
        Você está <u class="text-yellow font-bold">{belowAveragePercentage}%</u>
        abaixo da média dos usuários
      {/if}
    </h2>

    <p class="text-gray text-lg my-16 font-fredoka">
      Você acertou {slidesHitsCount} de {slidesReportsList.length} slides,
      {#if slidesHitsCount / slidesReportsList.length > 0.7}
        parabéns!
      {:else if slidesHitsCount / slidesReportsList.length > 0.4}
        tá bom né?
      {:else}
        fazer o que né...
      {/if}
    </p>

    <div class="flex flex-wrap justify-center gap-8">
      {#each slidesReportsList as slide}
        <div
          class="flex flex-col items-center justify-center bg-terciary rounded-xl"
        >
          <!-- <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">FÁCIL</h5> -->
          <span class="font-bold my-2"><Difficulty difficultyLevel={slide.difficulty_level} /></span>

          <div
            style="background-image: url({import.meta.env.VITE_API_URL + "/" + slide.slide_image_path})"
            class="w-[150px] h-[50px] bg-cover bg-top"
          />
          <div
            class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 {slide.has_hit
              ? 'border-green'
              : 'border-red'}"
          >
            <h3 class="text-whitish font-bold text-sm">{slide.prof_discipline.split('|')[0].trim().toUpperCase()}</h3>
            <p class="text-gray text-sm">{slide.prof_discipline.split('|')[1].trim().toUpperCase()}</p>
          </div>
        </div>
      {/each}
    </div>

    <div class="flex mt-32 flex-col gap-4 mb-32">
      <p class="font-fredoka text-gray text-sm">
        Deixe seu recado pela vitória, ou seu choro pela derrota :D
      </p>

      {#if !messageSent}
        <textarea
          class="p-8 h-[200px] w-[500px] rounded-lg placeholder:text-opacity-30"
          placeholder="Escreva uma mensagem"
        />
        <div class="flex mt-[-100px] justify-end items-center">
          <p class="text-gray font-bold text-sm">200 caracteres restantes</p>
          <div
            class="bg-terciary p-4 scale-50 rounded-xl border-4 border-terciary hover:border-cyan cursor-pointer hover:scale-[.55] transition-transform"
            on:click={() => (messageSent = true)}
            role="button"
            tabindex={1}
            on:keypress={() => {}}
          >
            <img src="icons/send.svg" alt="send icon" class="" />
          </div>
        </div>
      {:else}
        <textarea
          class="p-8 h-[200px] w-[500px] rounded-lg placeholder:text-opacity-30"
          placeholder=""
        />
        <div class="mt-[-150px] flex justify-center items-center flex-col">
          <p class="text-terciary font-bold text-sm">Mensagem registrada!</p>
          <img src="icons/check.svg" alt="check icon" />
        </div>
      {/if}
    </div>

    <Button text="INICIO" func={() => {goto('/')}} />
  </section>
</main>
