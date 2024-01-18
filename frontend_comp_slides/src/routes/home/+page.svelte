<script lang="ts">
  import Button from "../../components/button.svelte";
  import Footer from "../../components/footer.svelte";
  import LineBackground from "../../components/lineBackground.svelte";
  import Logo from "../../components/logo.svelte";
  import { onMount } from "svelte";
  import FancyDisciplines from "../../components/fancyDisciplines.svelte";
  import { goto } from "$app/navigation";
  import { api } from "../../services/api";

  type User = {
    username?: string;
    total_points?: number;
  };

  type Message = {
    username?: string;
    text?: string;
  };

  let users: User[] = [{}];
  let messages: Message[] = [{}];
  let fetchingMessages = true;

  function loadHorizontalCarousel(id: number) {
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
    let direction = 1; // 1=left -1=right
    let speedLimit = 1;
    let framerate = 20;

    let diffTotaSizeAndActualSize = 0;

    if (id == 1) speedLimit = 2;

    slider.scrollLeft += 10;

    function loop(){
      setTimeout(()=>{
        let messageCard = document.getElementsByClassName('message-card')[0]
        if (!messageCard) return
        
        diffTotaSizeAndActualSize = ((messages.length+1) * messageCard.clientWidth) - slider.clientWidth

        // finds the limit at the right border
        if (Math.abs(slider.scrollLeft - diffTotaSizeAndActualSize) < 130) {
          speed = 0;
          direction = -1;
        }

        // finds the limit at the left border
        if (slider.scrollLeft == 0 && speed < 0) {
          speed = 0.95;
          direction = 1;
        }

        // motor direction control
        if (Math.abs(speed)<speedLimit) speed += (direction * acceleration);
        else speed = speedLimit * direction

        // motor
        slider.scrollLeft += speed;


        loop()
      }, framerate)
    }
    setInterval(() => {

      

    }, framerate);
  }

  async function fetchUsers() {
    const response = await api.get("user/list/");
    users = response.data;
  }

  async function fetchMessages() {
    const response = await api.get("user/message/list/");
    messages = response.data;
    fetchingMessages = false;
  }

  onMount(() => {
    fetchUsers();

    fetchMessages();

    loadHorizontalCarousel(1);
    loadHorizontalCarousel(2);
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

    <div class="animate-bounce hover:animate-none w-fit m-auto">
      <Button
        text="JOGAR"
        func={() => {
          goto("/login");
        }}
      />
    </div>
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
              <td class="font-bold text-terciary">{user.total_points} pts</td>
              <td class="{i != 0 ? 'invisible' : 'visible'} w-8"
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
        {#if fetchingMessages}
          {#each [1, 2, 3, 4, 5, 6, 7] as message}
          <div
            class="animate-skeletonEffectCard px-8 py-4 bg-whitish shadow-medium rounded-xl gap-4 my-4 flex message-card"
          >
            <div
              class="h-16 w-16 animate-skeletonEffectItem rounded-full"
            ></div>
            <div class="w-[300px]">
              <h3
                class="animate-skeletonEffectItem w-full text-sm font-bold text-terciary h-4 w-32 rounded-lg"
              ></h3>
              <p
                class="animate-skeletonEffectItem w-full font-fredoka text-gray h-8 w-32 mt-3 rounded-lg"
              ></p>
            </div>
          </div>
          {/each}
        {:else}
          {#each row == 1 ? messages : messages.reverse() as message}
            <div
              class="px-8 py-4 bg-[#FFF] shadow-medium rounded-xl gap-4 my-4 message-card {message ==
              null
                ? 'hidden'
                : 'flex'}"
            >
              <img src="icons/user.svg" alt="user icon" />
              <div class="w-[300px]">
                <h3 class="w-full text-sm font-bold text-terciary">
                  {message.username}
                </h3>
                <p class="w-full font-fredoka text-gray">
                  {message.text}
                </p>
              </div>
            </div>
          {/each}
        {/if}
      </div>
    {/each}
  </section>

  <Footer />
</main>
