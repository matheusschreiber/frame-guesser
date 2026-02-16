<script lang='ts'>
    interface Props {
        difficultyLevel: number;
    }

    let { difficultyLevel }: Props = $props();
</script>

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