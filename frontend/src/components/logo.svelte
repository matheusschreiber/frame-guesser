<script lang='ts'>
  interface Props {
    small?: boolean;
  }

  let { small = false }: Props = $props();
</script>

<a href="/"><img class="{small?'w-[300px]':'w-[400px]'}" src="logo.png" alt="logo"/></a>
