<script lang="ts">
  import Button from "../components/button.svelte";
  import Footer from "../components/footer.svelte";
  import LineBackground from "../components/lineBackground.svelte";
  import Logo from "../components/logo.svelte";
  import { onMount } from "svelte";
  import FancyDisciplines from "../components/fancyDisciplines.svelte";
  import { goto } from "$app/navigation";
  import { api } from "../services/api";

  type User = {
    username?: string;
    points?: number;
    message?: string;
  };

  let users: User[] = [{}];

  function loadHorizontlDrag(id: number) {
    const slider = document.getElementById(`horizontal-scroll-${id}`) as any;
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;

    slider?.addEventListener("mousedown", (e: any) => {
      isDown = true;
      startX = e.pageX - slider?.offsetLeft;
      scrollLeft = slider?.scrollLeft;
    });
    slider?.addEventListener("mouseleave", () => {
      isDown = false;
    });
    slider?.addEventListener("mouseup", () => {
      isDown = false;
    });
    slider?.addEventListener("mousemove", (e: any) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - slider?.offsetLeft;
      const walk = x - startX; //scroll-fast
      slider.scrollLeft = scrollLeft - walk;
    });

    let speed = 0;
    let acceleration = 0.05;
    let speedLimit = 1;
    let offset = slider.clientWidth * 0.05;
    let framerate = 20;

    if (id == 1) speedLimit = 2;

    setInterval(() => {
      if (slider.scrollLeft < offset && speed < speedLimit)
        speed += acceleration;
      else if (
        (slider.scrollLeft > slider.clientWidth - offset * 10 || speed < 0) &&
        speed > -speedLimit
      )
        speed -= acceleration;

      slider.scrollLeft += speed;

      // console.log({
      //   width: slider.clientWidth,
      //   scroll: slider.scrollLeft,
      //   speed: speed,
      // });
    }, framerate);
  }

  async function fetchUsers() {
    const response = await api.get("user/list");
    users = response.data;
  }

  onMount(() => {
    fetchUsers();

    loadHorizontlDrag(1);
    loadHorizontlDrag(2);
  });
</script>

<main>
  <header class="flex w-full justify-around items-center my-32">
    <FancyDisciplines />
    <Logo />
  </header>
  <p class="text-gray font-fredoka w-fit mx-auto text-lg">
    Você conhece mesmo os slides dos seus professores?
  </p>
  <section
    class="my-8 p-16 pt-32 bg-purple m-32 rounded-xl shadow-medium text-center overflow-hidden"
  >
    <LineBackground />
    <h5 class="mx-auto w-fit text-cyan font-bold text-sm mb-4">COMO JOGAR</h5>
    <h1 class="mb-16 text-whitish text-3xl">
      Adivinhe apenas olhando um slide
    </h1>
    <div class="flex justify-around mb-16">
      <div
        class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all"
      >
        <div
          class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy"
        >
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">
            1
          </h1>
          <img src="icons/slide.svg" alt="icon slide" />
        </div>
        <p class="text-whitish">Olhe para todos os detalhes de um slide</p>
      </div>

      <div
        class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all"
      >
        <div
          class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy"
        >
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">
            2
          </h1>
          <img src="icons/lamp.svg" alt="icon lamp" />
        </div>
        <p class="text-whitish">
          Use as dicas para ter mais chances de acertar
        </p>
      </div>

      <div
        class="flex flex-col items-center gap-4 w-[150px] hover:scale-105 transition-all"
      >
        <div
          class="bg-quaternary h-[150px] w-full text-whitish rounded-lg p-4 flex flex-col items-center justify-center shadow-heavy"
        >
          <h1 class="bg-terciary rounded-full px-3 py-1 mb-4 text-sm font-bold">
            3
          </h1>
          <img src="icons/trophy.svg" alt="icon trophy" />
        </div>
        <p class="text-whitish">Quanto menos dicas, maior a sua pontuação</p>
      </div>
    </div>

    <Button
      text="JOGAR"
      func={() => {
        goto("/login");
      }}
    />
  </section>

  <section class="my-8 flex items-center py-10 px-32 w-full justify-around">
    <div>
      <h5 class="w-fit text-blue font-bold text-sm">DESTAQUE-SE</h5>
      <h1 class="font-bold text-terciary text-5xl mb-4">Ranking</h1>
      <p class="font-fredoka text-gray w-[300px]">
        Reza a lenda que quem acertar mais slides consegue passar o resto da
        faculade <u>sem fazer finais...</u>
      </p>
    </div>
    <div
      class="bg-rankings bg-center bg-contain bg-no-repeat py-12 px-8 w-[600px] h-[450px] flex justify-center items-center"
    >
      <table
        id="new-scroll"
        class="w-[80%] text-center ml-8 h-[200px] table-cell overflow-scroll overflow-x-hidden"
      >
        <tbody>
          {#each users as user, i}
            <tr class="h-10">
              <td class="{i != 0 ? 'invisible' : 'visible'} w-8"
                ><img
                  class="mx-auto"
                  src="icons/crown.svg"
                  alt="crown icon"
                /></td
              >
              <td class="font-bold text-gray text-[8pt]"
                >{(i + "").padStart(2, "0")}</td
              >
              <td class="font-bold text-terciary text-left pl-2 w-64"
                >{user.username}</td
              >
              <td class="font-bold text-terciary">{user.points} pts</td>
              <td class="{user.points != 0 ? 'invisible' : 'visible'} w-8"
                ><img
                  class="mx-auto"
                  src="icons/crown.svg"
                  alt="crown icon"
                /></td
              >
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </section>

  <section class="my-8">
    <h5 class="mx-auto w-fit text-red font-bold text-sm mb-4">
      DEIXE SEU RECADO
    </h5>
    {#each [1, 2] as row}
      <div
        id="horizontal-scroll-{row}"
        class="flex overflow-scroll overflow-x-scroll overflow-y-hidden gap-8 cursor-move"
      >
        {#each row == 1 ? users : users.reverse() as user}
          <div
            class="px-8 py-4 bg-[#FFF] shadow-medium rounded-xl gap-4 my-4 {user.message ==
            null
              ? 'hidden'
              : 'flex'}"
          >
            <img src="icons/user.svg" alt="user icon" />
            <div class="w-[300px]">
              <h3 class="w-full text-sm font-bold text-terciary">
                {user.username}
              </h3>
              <p class="w-full font-fredoka text-gray">
                {user.message}
              </p>
            </div>
          </div>
        {/each}
      </div>
    {/each}
  </section>

  <Footer />
</main>
