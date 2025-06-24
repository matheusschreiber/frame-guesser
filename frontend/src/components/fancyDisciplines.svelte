<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../services/api";
  import Swal from "sweetalert2";

  let disciplines: string[] = [];

  let text = $state("");

  let duration = 3000;

  function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function addTyping(string: string) {
    if (!string || string.length == 0) return;
    let i = 0;
    let timePerLetter = (duration * 0.45) / string.length; // this is to ensure 2sec for all words
    while (i < string.length) {
      text += string[i++];
      await sleep(timePerLetter);
    }
  }

  async function eraseTyping(string: string) {
    if (!string || string.length == 0) return;
    let i = string.length;
    let timePerLetter = (duration * 0.1) / string.length; // this is to ensure 2sec for all words
    while (i-- > 0) {
      text = text.slice(0, -1);
      await sleep(timePerLetter);
    }
  }

  async function fetchDisciplines() {
    try{
      const response = await api.get("disciplines/");
      response.data.map((discipline: string) =>
        disciplines.push(discipline.split("|")[1])
      );
    } catch (err) {
      console.error("Error fetching disciplines:", err);
    }
  }

  onMount(async () => {
    fetchDisciplines();

    while (true) {
      if (disciplines.length) {
        let index = Math.floor(Math.random() * disciplines.length);
        
        await addTyping(disciplines[index]);
        await sleep(duration * 0.45);
        await eraseTyping(disciplines[index]);
      }

        await sleep(0.01);
    }
  });

  let blink = $state(true);
  setInterval(() => {
    blink = !blink;
  }, 200);
</script>

<h1 id="title-typing-effect" class="text-5xl font-bold text-terciary lg:w-[400px] 
  text-center md:text-left">
  {text}<span class="text-green {blink ? 'invisible' : 'visible'}">_</span>
</h1>
