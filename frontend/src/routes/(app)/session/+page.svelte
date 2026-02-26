<script lang="ts">
	import toast, { Toaster } from 'svelte-french-toast';
	import LineBackground from "../../../components/lineBackground.svelte";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { api } from "../../../services/api";
	import Loading from "../../../components/loading.svelte";
	import { deleteCookie, getCookie, setCookie } from "../../../services/cookies";

	let correctAnswerCatchPhrases = [
		"If you keep this up, you might actually look like you pay attention in movies!",
		"Wow, do we have a genius here or was that just pure luck?",
		"Great job! Just need to keep this pace for more than 5 minutes.",
		"Impressive! I'm almost believing you actually know something!",
		"Congratulations! If you keep this up, maybe one day you won't need to guess.",
		"You're amazing! But don't get used to it, there's still a long way to go.",
		"Keep up the good work! Or at least keep faking it well.",
		"If you keep this up, maybe even your mom will start feeling proud.",
		"Very good! Keep it up and maybe I'll stop doubting you.",
		"Unbelievable! I'm starting to suspect you're cheating.",
	];

	let wrongAnswerCatchPhrases = [
		"Someone's been scrolling while watching.",
		"Oops! If being wrong was a sport, you'd already be in the Olympics.",
		"Well, at least you were consistent... in getting it wrong.",
		"Interesting approach! Wrong, but interesting.",
		"Almost! You just forgot to get it right.",
		"The right answer was right there... But you chose to ignore it.",
		"If the goal was to get it wrong, congratulations, mission accomplished!",
		"Maybe the right answer was hiding from you this time.",
		"At least you're keeping the average... way down there.",
		"I could pretend that answer is correct... But even I'm not that generous.",
		"You didn't get it wrong, you just found a different (and incorrect) way to answer.",
		"The right answer was one neuron away. Too bad it was on vacation.",
		"You got it wrong with so much confidence that you made me doubt the right answer.",
	];

	let confirm = $state(false);
	let selected: number | null = $state(null);
	let hintsUsed = $state(0);
	let totalHintsAmount = $state(0);
	let phrase:string = $state("");

	let slidesLeftAmount: number = $state();
	let difficultyLevel: number = $state();

	var loading = $state(true);
	var hasAnswered = $state(false);
	var answer: number | null = $state(null);
	var loadingHint = $state(false);

	var options = $state([
		"Loading... | Loading...",
		"Loading... | Loading...",
		"Loading... | Loading...",
		"Loading... | Loading...",
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
		} catch (err: any) {
			toast.error("Unexpected problem! Try again later.");
			return;
		}

		if (response.data.answer == true) {
			phrase = correctAnswerCatchPhrases[
				Math.floor(Math.random() * correctAnswerCatchPhrases.length)
			]
			toast.success("+" + response.data.points + " pts! Correct answer!");
		} else if (response.data.answer == false) {
			phrase = wrongAnswerCatchPhrases[
				Math.floor(Math.random() * wrongAnswerCatchPhrases.length)
			]
			toast.error("Wrong answer!");
		} else {
			toast.error("Unexpected response from server! Try again later.");
			selected = null;
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
			await handleAnswerSlide();
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
		phrase = "";

		let response;
		let currentRun = getCookie("runId");

		try {
			currentRun = currentRun ? currentRun : "0";
			response = await api.get("slide/" + currentRun);
		} catch (err: any) {
			if (err.response.status === 301) {
				goto(`/results`);
			} else {
				deleteCookie("runId");
				toast.error("Unexpected problem with your session! Redirecting to home...");
				goto(`/`)
			}
			return;
		}
		
		let slideUrl = import.meta.env.VITE_API_URL + "/" + response.data.slide_image_path;
		try{
			await preloadImage(slideUrl);
		} catch (err) {
			slideImage = "error.png";
		}
		slideImage = slideUrl;

		setCookie("runId", response.data.run_id);
		loading = false;
		difficultyLevel = response.data.difficulty_level;
		options = response.data.slide_alternatives;
		hintsUsed = response.data.hints_used;
		slidesLeftAmount = response.data.slides_left_amount;
		totalHintsAmount = response.data.hints_total-1;
		hasAnswered = hintsUsed == totalHintsAmount ? true : false;
	}

	async function fetchNewHint() {
		loadingHint = true;
		let runId = getCookie("runId");
		if (!runId) {
			toast.error("Unexpected problem with your session! Redirecting to home...");
			goto(`/`);
			return;
		}

		try {
			const response = await api.post("slide/hint/" + runId);
			let newUrl = import.meta.env.VITE_API_URL + "/" + response.data.slide_image_path;
			await preloadImage(newUrl);
			slideImage = newUrl
			loadingHint = false;
		} catch (err: any) {
			slideImage = "error.png";
			toast.error("Unexpected problem fetching hint! Try again later.");
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

	function preloadImage(url: string): Promise<void> {
		return new Promise((resolve, reject) => {
			const img = new Image();
			img.src = url;
			img.onload = () => resolve();
			img.onerror = reject;
		});
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
					<span class="text-red">LEVEL HARD</span>
				{:else if difficultyLevel === 4}
					<span class="text-orange">LEVEL SEMI-HARD</span>
				{:else if difficultyLevel === 3}
					<span class="text-yellow">LEVEL NORMAL</span>
				{:else if difficultyLevel === 2}
					<span class="text-green">LEVEL EASY</span>
				{:else if difficultyLevel === 1}
					<span class="text-blue">LEVEL VERY EASY</span>
				{/if}
			</h5>
			<h2 class="text-whitish text-3xl">From which movie is this?</h2>
		</div>

		<div class="flex lg:flex-row flex-col">
			<aside class="lg:w-fit flex flex-col justify-end">
				{#if slideImage != ""}
					<div class="flex w-[90%] mx-auto justify-start mb-[-10px]">
						<h3 class="mt-4 text-whitish bg-terciary w-fit px-2 py-1 pb-3 rounded-lg text-sm">
							{#if typeof(slidesLeftAmount) == "undefined"}
								Loading...
							{:else}
								{10 - slidesLeftAmount + 1}/{10}
							{/if}
						</h3>
					</div>
				{/if}

				{#if slideImage == "" || slideImage == undefined}
					<Loading />
				{:else}
					<img
						class="rounded-lg h-[400px] w-[400px]"
						src={slideImage}
						alt="slide"
					/>
				{/if}
			</aside>

			<aside class="flex flex-col items-center justify-end px-6">
				<div
					class="flex lg:flex-col flex-wrap mt-4 lg:mt-0 gap-4 justify-center lg:justify-between pb-8 items-center ">
					{#each options as item, i}
						<div onclick={() => handleSelection(i)}
							role="button"
							tabindex={2}
							onkeypress={() => {}}
							class="bg-secondary px-4 py-2 rounded-lg shadow-medium border-2 select-none w-[200px] duration-200 hover:scale-90
              				{answer == i
								? 'border-green'
								: selected == i
									? hasAnswered
										? 'border-red'
										: 'border-pink'
									: hasAnswered
										? 'opacity-[.3] border-secondary cursor-not-allowed'
										: 'border-secondary'}">
							<h3 class="text-whitish font-bold text-sm">
								{item.split("|")[0].trim()}
							</h3>
							<p class="text-gray text-sm">
								{item.split("|")[1].trim()}
							</p>
						</div>
					{/each}
				</div>

				<div class="flex justify-around w-full h-[50px]">
					<div class="flex flex-col items-center">
						{#if loadingHint}
							<Loading />
						{:else}
							{#if hintsUsed > 0}
								<p
									class="absolute font-fredoka text-sm text-whitish mt-[-25px]">
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
									duration-200 hover:scale-90
									{confirm ? 'border-yellow' : 'border-secondary'}
									{hintsUsed == totalHintsAmount || hasAnswered
									? 'opacity-20 cursor-not-allowed'
									: 'opacity-100 cursor-pointer'}"
								onkeypress={() => {}}>
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
								<p
									class="absolute font-fredoka text-sm text-whitish mt-16">
									Click again to confirm hint
								</p>
							{/if}
						{/if}
					</div>

					{#if loading}
						<Loading />
					{:else}
						<button
							class="px-4 py-2 h-12 bg-terciary font-bold text-sm rounded-lg border-2 duration-200 hover:scale-90
            					{selected == null
								? 'border-terciary text-whitish'
								: answer == null
									? 'border-pink text-pink'
									: selected == answer
										? 'border-green text-green'
										: 'border-red text-red'}"
							onclick={loading ? null : () => handleNextSlide()}>
							{hasAnswered ? "NEXT" : "CHECK"}
						</button>
					{/if}
				</div>
			</aside>
		</div>
		<p class="mt-4 text-center text-lightgray italic">{phrase}</p>
	</section>
	<p class="text-center text-gray lg:w-[500px] w-full mx-auto mb-16 italic">
		This image has been modified to apply selective blur, pixelation, 
		and negative effects to specific areas. These regions were identified 
		through AI-based analysis that focused on detecting significant 
		features and objects within the image.
	</p>
	<Toaster />
</main>
