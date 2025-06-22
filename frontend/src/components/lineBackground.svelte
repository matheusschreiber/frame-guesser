<script lang='ts'>
  interface Props {
    variant?: number;
  }

  let { variant = 1 }: Props = $props();
</script>

{#if variant==1}
<div class="mb-[-600px] mt-[-50px] mx-[-15%] flex w-fill justify-center">
  <svg xmlns="http://www.w3.org/2000/svg" width="1586" height="597" viewBox="0 0 1586 597" fill="none">
    <path d="M1584 1.49976C1541.39 59.0148 1457.88 114.622 1357 160.286C1337.9 168.931 1318.18 177.219 1298 185.097C1240.05 207.715 1178.29 226.946 1116.5 241.5C1067.61 253.015 1006.97 263.304 938.5 269.597" stroke="#DD58D6" stroke-width="3" stroke-linecap="round"/>
    <path d="M1116.5 241.5C1178.29 226.946 1240.05 207.715 1298 185.097" stroke="#EAD83A" stroke-width="3" stroke-linecap="round"/>
    <path d="M483.15 241.499C650.379 280.194 816.661 281.876 951 268.396" stroke="#EF4343" stroke-width="3" stroke-linecap="round"/>
    <path d="M200.5 394.5C227.296 318.003 318.058 203.298 483.15 241.499C510.336 247.79 537.497 253.102 564.499 257.53" stroke="#43EF4A" stroke-width="3" stroke-linecap="round"/>
    <path d="M1.49976 595C43.9418 594.551 169.092 537.59 200.5 394.5" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
  </svg>
</div>
{/if}

{#if variant==2}
<div class="flex w-fill justify-center mb-[-500px] mt-[-50px]">
  <svg xmlns="http://www.w3.org/2000/svg" width="1645" height="621" viewBox="0 0 1645 621" fill="none">
    <path d="M1.99988 619.463C44.6071 561.948 128.123 506.341 229 460.677C248.097 452.032 267.817 443.743 288 435.866C345.948 413.247 407.708 394.016 469.5 379.463C516.237 368.455 573.715 358.567 638.5 352.22" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
    <path d="M469.5 379.463C407.708 394.016 345.948 413.247 288 435.866" stroke="#EAD83A" stroke-width="3" stroke-linecap="round"/>
    <path d="M1102.85 379.464C935.62 340.768 769.338 339.087 635 352.567" stroke="#EF4343" stroke-width="3" stroke-linecap="round"/>
    <path d="M1385.5 226.463C1358.7 302.959 1267.94 417.664 1102.85 379.464C1075.66 373.173 1048.5 367.861 1021.5 363.433" stroke="#43EF4A" stroke-width="3" stroke-linecap="round"/>
    <path d="M1643 2.5C1545 -5.50002 1447.94 48.2033 1385.5 226.463" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
  </svg>
</div>
{/if}

{#if variant==3}
<div class="flex w-fill justify-center mb-[-1000px] mt-[-50px] ml-[-800px]">
  <svg xmlns="http://www.w3.org/2000/svg" width="281" height="1077" viewBox="0 0 281 1077" fill="none">
    <path d="M205.667 1075.5C231.411 1020.98 260.236 934.405 272.62 836" stroke="#EF4343" stroke-width="3" stroke-linecap="round"/>
    <path d="M171.167 404.5C275.87 535.26 290.463 700.297 272.041 840.5" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
    <path d="M171.167 404.5C114.052 333.172 74.9503 270.324 48.8574 216.5" stroke="#EAD83A" stroke-width="3" stroke-linecap="round"/>
    <path d="M51.5536 222C24.6352 167.689 10.8356 122.343 5.18602 86.5" stroke="#DD58D6" stroke-width="3" stroke-linecap="round"/>
    <path d="M10.1671 2C2.26996 18.6498 -1.85411 50.4802 6.9308 96.5" stroke="#43EF4A" stroke-width="3" stroke-linecap="round"/>
  </svg>
</div>
{/if}

{#if variant==4}
<div class="flex w-fill justify-center mb-[-1600px] mt-[-50px] ml-[-1000px]">
  <svg xmlns="http://www.w3.org/2000/svg" width="325" height="1667" viewBox="0 0 325 1667" fill="none">
    <path d="M8.09766 1330.5C19.3344 1395.5 70.9998 1540 22.9998 1665.5" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
    <path d="M83.5985 938.5C83.5985 938.5 -24.4023 1142.5 8.09782 1330.5" stroke="#DD58D6" stroke-width="3" stroke-linecap="round"/>
    <path d="M322.599 2C309.429 49.0258 298.465 92.1678 289.24 132" stroke="#DD58D6" stroke-width="3" stroke-linecap="round"/>
    <path d="M291.812 121C269.647 214.896 257.086 290.667 248.281 355.5" stroke="#2BEFFC" stroke-width="3" stroke-linecap="round"/>
    <path d="M248.966 350.5C235.057 451.555 230.477 526.051 213.654 600.5" stroke="#EAD83A" stroke-width="3" stroke-linecap="round"/>
    <path d="M183.099 699.5C197.183 664.001 206.949 630.791 214.325 597.5" stroke="#EF4343" stroke-width="3" stroke-linecap="round"/>
    <path d="M183.099 699.5C124.699 846.7 92.432 920.167 83.5986 938.5" stroke="#43EF4A" stroke-width="3" stroke-linecap="round"/>
    </svg>
</div>
{/if}






