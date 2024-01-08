<script>
  import "../../app.css";
  import Footer from "../../components/footer.svelte";
  import Logo from "../../components/logo.svelte";
</script>

<header class="w-full flex justify-center items-center py-8 mt-8">
  <Logo small />
</header>

<!-- Page content -->
<slot></slot> 

<Footer />