<script lang="ts">
  import "../../app.css";
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<header class="w-full flex justify-center items-center py-8 mt-8">
  <Logo small />
</header>

<!-- Page content -->
{@render children?.()} 

<Footer />