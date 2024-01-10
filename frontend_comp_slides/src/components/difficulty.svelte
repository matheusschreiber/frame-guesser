<script lang='ts'>
    export let difficultyLevel: number;
</script>

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