<script lang="ts">
    import { onMount } from "svelte";

    onMount(() => {
        const borderColorsArray: any[] = [
            { borderColor: "#00EC09" },
            { borderColor: "#EAD83A" },
            { borderColor: "#EF4343" },
            { borderColor: "#DD58D6" },
            { borderColor: "#4369EF" },
            { borderColor: "#00DEEC" },
            { borderColor: "#ffb224" },
        ];

        const spinner = document.getElementById("arc-loading-spinner");
        spinner?.animate([{ transform: "rotate(360deg)" }], {
            duration: 300,
            iterations: Infinity,
        });

        spinner?.animate(borderColorsArray, {
            duration: 10000,
            iterations: Infinity,
        });

        const spinnerBackgroundExternal = document.getElementById("bg-external-loading-spinner");
        spinnerBackgroundExternal?.animate(borderColorsArray.reverse(), {
            duration: 10000,
            iterations: Infinity,
        });

        spinnerBackgroundExternal?.animate([{ transform: "rotate(-360deg)" }], {
            duration: 600,
            iterations: Infinity,
        });

        const spinnerBackgroundInternal = document.getElementById("bg-internal-loading-spinner");
        spinnerBackgroundInternal?.animate(borderColorsArray, {
            duration: 10000,
            iterations: Infinity,
        });
    });
</script>

<div class="w-full flex justify-center">
    <div
        id="bg-external-loading-spinner"
        class="border-0 border-t-1"
        style="border-radius:100%; height: 40px; width:40px; border-bottom-width: 3px; border-right-width: 3px; padding-left: 4px; padding-top: 4px;"
    >
        <div
            id="bg-internal-loading-spinner"
            style="border-radius:100%; height: 30px; width:30px; border-width:7px"
        >
            <div
                id="arc-loading-spinner"
                class="border-t-0 border-l-0"
                style="border-bottom-width:  7px; border-right-width:  7px; border-radius:50%; width:30px; height:30px; margin-left: -7px; margin-top: -7px;"
            ></div>
        </div>
    </div>
</div>
