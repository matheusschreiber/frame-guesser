<script>
  import { goto } from "$app/navigation";
  import Button from "../components/button.svelte";
  import Footer from "../components/footer.svelte";


  import Logo from "../components/logo.svelte";

</script>
<main>
  <header class="w-full flex justify-center items-center py-8 mt-8">
    <Logo small />
  </header>
  <section class="w-full flex justify-center text-center flex-col gap-16 mb-32">
    <p class="font-bold font-fredoka text-lg text-terciary">ERROR</p>
    <h1 class="text-[100pt] font-bold font-fredoka mb-16 mt-[-2rem] animate-colorWarp">404</h1>

    <p class="italic text-gray">I think you got lost...</p>
    <div class="animate-bounce hover:animate-none w-fit m-auto">
      <Button text="INÍCIO" func={()=>goto('/')} />
    </div>
  </section>

  <Footer />
</main>