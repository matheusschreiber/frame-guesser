<script lang="ts">
	import { onMount } from "svelte";
	import { api } from "../services/api";

	let movies: string[] = [];

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

	async function fetchMovies() {
		try {
			const response = await api.get("movie/list/");
			response.data.map((movie: { name: string, year: number }) => {
				movies.push(`${movie.name} (${movie.year})`);
			});
		} catch (err) {
			console.error("Error fetching movies:", err);
		}
	}

	onMount(async () => {
		fetchMovies();

		while (true) {
			if (movies.length) {
				let index = Math.floor(Math.random() * movies.length);

				await addTyping(movies[index]);
				await sleep(duration * 0.45);
				await eraseTyping(movies[index]);
			}

			await sleep(0.01);
		}
	});

	let blink = $state(true);
	setInterval(() => {
		blink = !blink;
	}, 200);
</script>

<h1
	id="title-typing-effect"
	class="text-5xl font-bold text-terciary lg:w-100
  text-center md:text-left"
>
	{text}<span class="text-green {blink ? 'invisible' : 'visible'}">_</span>
</h1>
