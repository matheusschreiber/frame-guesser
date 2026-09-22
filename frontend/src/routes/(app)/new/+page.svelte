<script lang="ts">
  import toast, { Toaster } from "svelte-hot-french-toast";
  import Button from "../../../components/button.svelte";
  import LineBackground from "../../../components/lineBackground.svelte";
  import Loading from "../../../components/loading.svelte";
  import { api } from "../../../services/api";
  import { getCookie, setCookie, deleteCookie } from "../../../services/cookies";
  import { jwtDecode, type JwtPayload } from "jwt-decode";
  import { onMount } from "svelte";

  type StaffJwt = JwtPayload & { username: string; is_staff?: boolean };

  const CROP_SIZE = 400;

  // Auth state
  let checkingAuth = $state(true);
  let isStaff = $state(false);
  let username: string | undefined = $state();

  // Login form
  let loginUsername: string | undefined = $state();
  let loginPassword: string | undefined = $state();
  let loggingIn = $state(false);

  // Movie form
  let movieName = $state("");
  let movieYear: number | undefined = $state();
  let movieDirector = $state("");
  let submitting = $state(false);
  let generatingHints = $state(false);
  let generatedHints: string[] = $state([]);
  let zoomedHintIndex: number | null = $state(null);

  // Cropper state
  let fileInput: HTMLInputElement | undefined = $state();
  let imageEl: HTMLImageElement | null = $state(null);
  let imageSrc: string | undefined = $state();
  let imageNaturalW = $state(0);
  let imageNaturalH = $state(0);
  let originalFileName = $state("image.png");

  let scale = $state(1);
  let minScale = $state(1);
  let offsetX = $state(0);
  let offsetY = $state(0);

  let dragging = false;
  let dragStartX = 0;
  let dragStartY = 0;
  let dragStartOffsetX = 0;
  let dragStartOffsetY = 0;

  // Movie list
  type MovieItem = {
    id: number;
    name: string | null;
    year: number | null;
    director: string | null;
    hints_amount: number;
    difficulty_level: number;
    image_path: string | null;
  };
  let movies: MovieItem[] = $state([]);
  let loadingMovies = $state(false);
  let search = $state("");
  let viewMode: "list" | "grid" = $state("list");
  let searchDebounce: ReturnType<typeof setTimeout> | undefined;
  const apiBase = import.meta.env.VITE_API_URL as string;

  onMount(() => {
    hydrateAuth();
    checkingAuth = false;
    if (isStaff) fetchMovies();
  });

  async function fetchMovies(q: string = "") {
    try {
      loadingMovies = true;
      const response = await api.get("movie/list/admin/", { params: q ? { q } : {} });
      movies = response.data;
    } catch {
      // Silent — list is a helper, not the main action.
    } finally {
      loadingMovies = false;
    }
  }

  function onSearchInput(e: Event) {
    search = (e.target as HTMLInputElement).value;
    if (searchDebounce) clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => fetchMovies(search.trim()), 250);
  }

  function hydrateAuth() {
    const rawTokens = getCookie("auth");
    if (!rawTokens) return;
    try {
      const access = JSON.parse(rawTokens).access;
      const decoded = jwtDecode<StaffJwt>(access);
      username = decoded.username;
      isStaff = !!decoded.is_staff;
    } catch {
      isStaff = false;
    }
  }

  async function handleLogin() {
    if (!loginUsername || !loginPassword) {
      toast.error("There are blank fields");
      return;
    }
    try {
      loggingIn = true;
      const response = await api.post("user/token/", {
        username: loginUsername,
        password: loginPassword,
      });
      if (response.status !== 200) {
        toast.error("Invalid Credentials");
        return;
      }
      const decoded = jwtDecode<StaffJwt>(response.data.access);
      if (!decoded.is_staff) {
        toast.error("You must be an admin user.");
        return;
      }
      setCookie("auth", JSON.stringify(response.data));
      setCookie("username", decoded.username);
      username = decoded.username;
      isStaff = true;
      fetchMovies();
    } catch (err: any) {
      if (err?.response?.status === 401) toast.error("Invalid Credentials");
      else toast.error("Unexpected problem!");
    } finally {
      loggingIn = false;
    }
  }

  function handleLogout() {
    deleteCookie("auth");
    deleteCookie("username");
    isStaff = false;
    username = undefined;
  }

  function onFileSelected(e: Event) {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      toast.error("Please select an image file.");
      return;
    }
    originalFileName = file.name;
    generatedHints = [];
    const reader = new FileReader();
    reader.onload = (ev) => {
      imageSrc = ev.target?.result as string;
    };
    reader.readAsDataURL(file);
  }

  function onImageLoad() {
    if (!imageEl) return;
    imageNaturalW = imageEl.naturalWidth;
    imageNaturalH = imageEl.naturalHeight;
    // Minimum scale keeps the image at least covering the crop area.
    minScale = Math.max(CROP_SIZE / imageNaturalW, CROP_SIZE / imageNaturalH);
    scale = minScale;
    centerImage();
  }

  function centerImage() {
    const w = imageNaturalW * scale;
    const h = imageNaturalH * scale;
    offsetX = (CROP_SIZE - w) / 2;
    offsetY = (CROP_SIZE - h) / 2;
    clampOffsets();
  }

  function clampOffsets() {
    const w = imageNaturalW * scale;
    const h = imageNaturalH * scale;
    const minX = CROP_SIZE - w;
    const minY = CROP_SIZE - h;
    if (offsetX > 0) offsetX = 0;
    if (offsetY > 0) offsetY = 0;
    if (offsetX < minX) offsetX = minX;
    if (offsetY < minY) offsetY = minY;
  }

  function onPointerDown(e: PointerEvent) {
    if (!imageSrc) return;
    dragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    dragStartOffsetX = offsetX;
    dragStartOffsetY = offsetY;
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
  }

  function onPointerMove(e: PointerEvent) {
    if (!dragging) return;
    offsetX = dragStartOffsetX + (e.clientX - dragStartX);
    offsetY = dragStartOffsetY + (e.clientY - dragStartY);
    clampOffsets();
    if (generatedHints.length > 0) generatedHints = [];
  }

  function onPointerUp(e: PointerEvent) {
    dragging = false;
    try {
      (e.currentTarget as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {}
  }

  function onScaleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    const newScale = parseFloat(target.value);
    // Keep the crop-area center anchored while zooming.
    const centerRatioX = (CROP_SIZE / 2 - offsetX) / (imageNaturalW * scale);
    const centerRatioY = (CROP_SIZE / 2 - offsetY) / (imageNaturalH * scale);
    scale = newScale;
    offsetX = CROP_SIZE / 2 - centerRatioX * imageNaturalW * scale;
    offsetY = CROP_SIZE / 2 - centerRatioY * imageNaturalH * scale;
    clampOffsets();
    if (generatedHints.length > 0) generatedHints = [];
  }

  function buildCroppedBlob(): Promise<Blob> {
    return new Promise((resolve, reject) => {
      if (!imageEl) return reject(new Error("No image"));

      const canvas = document.createElement("canvas");
      canvas.width = CROP_SIZE;
      canvas.height = CROP_SIZE;
      const ctx = canvas.getContext("2d");
      if (!ctx) return reject(new Error("Canvas not supported"));

      // Map crop-area coords back to source pixels.
      const sx = -offsetX / scale;
      const sy = -offsetY / scale;
      const sSize = CROP_SIZE / scale;

      ctx.drawImage(imageEl, sx, sy, sSize, sSize, 0, 0, CROP_SIZE, CROP_SIZE);

      const ext = (originalFileName.split(".").pop() || "png").toLowerCase();
      const type = ext === "jpg" || ext === "jpeg" ? "image/jpeg" : "image/png";
      canvas.toBlob((blob) => {
        if (!blob) return reject(new Error("Failed to build image"));
        resolve(blob);
      }, type, 0.95);
    });
  }

  function dataUrlToBlob(dataUrl: string): Blob {
    const [meta, base64] = dataUrl.split(",");
    const mime = /data:([^;]+)/.exec(meta)?.[1] || "image/png";
    const bin = atob(base64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new Blob([bytes], { type: mime });
  }

  function resetHints() {
    generatedHints = [];
  }

  function closeZoom() {
    zoomedHintIndex = null;
  }

  function onZoomKeydown(e: KeyboardEvent) {
    if (zoomedHintIndex === null) return;
    if (e.key === "Escape") {
      e.preventDefault();
      closeZoom();
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      zoomedHintIndex = (zoomedHintIndex + 1) % generatedHints.length;
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      zoomedHintIndex = (zoomedHintIndex - 1 + generatedHints.length) % generatedHints.length;
    }
  }

  async function handleGenerateHints() {
    if (!imageSrc) {
      toast.error("Please select an image.");
      return;
    }
    try {
      generatingHints = true;
      const blob = await buildCroppedBlob();
      const ext = (originalFileName.split(".").pop() || "png").toLowerCase();
      const filename = `movie.${ext}`;
      const formData = new FormData();
      formData.append("image", blob, filename);

      const response = await api.post("movie/generate-hints/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (response.status === 200) {
        generatedHints = response.data.hints;
        toast.success(`Generated ${generatedHints.length} hint(s).`);
      }
    } catch (err: any) {
      const msg = err?.response?.data?.error || "Failed to generate hints.";
      toast.error(msg);
    } finally {
      generatingHints = false;
    }
  }

  async function handleSubmit() {
    if (!movieName || !movieDirector || !movieYear) {
      toast.error("All fields are required.");
      return;
    }
    if (generatedHints.length === 0) {
      toast.error("Please generate hints first.");
      return;
    }
    try {
      submitting = true;
      const formData = new FormData();
      formData.append("name", movieName);
      formData.append("year", String(movieYear));
      formData.append("director", movieDirector);
      generatedHints.forEach((dataUrl, idx) => {
        formData.append("images", dataUrlToBlob(dataUrl), `hint${idx}.png`);
      });

      const response = await api.post("movie/new/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (response.status === 201) {
        toast.success("Movie added!");
        movieName = "";
        movieYear = undefined;
        movieDirector = "";
        generatedHints = [];
        imageSrc = undefined;
        if (fileInput) fileInput.value = "";
        fetchMovies(search.trim());
      }
    } catch (err: any) {
      const msg = err?.response?.data?.error || "Failed to save movie.";
      toast.error(msg);
    } finally {
      submitting = false;
    }
  }
</script>

<main>
  <section
    class="my-8 py-12 pt-0 bg-purple lg:m-64 mx-5 mb-32 rounded-xl shadow-medium text-center overflow-hidden flex flex-col items-center justify-center"
  >
    <LineBackground variant={2} />

    <div class="px-2 lg:px-0">
      <h5 class="mx-auto w-fit text-green font-bold text-sm mb-4">ADMIN</h5>
      <h1 class="mb-8 text-whitish text-3xl">Add a new movie</h1>
    </div>

    {#if checkingAuth}
      <Loading />
    {:else if !isStaff}
      <div class="flex flex-col w-87.5 gap-4 px-5 lg:px-0">
        <p class="text-lightgray font-fredoka">Admin login required</p>
        {#if loggingIn}
          <Loading />
        {:else}
          <input
            class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
            type="text"
            placeholder="USERNAME"
            name="username"
            bind:value={loginUsername}
          />
          <input
            class="bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
            type="password"
            placeholder="PASSWORD"
            name="password"
            bind:value={loginPassword}
            onkeypress={(e) => {
              if (e.key === "Enter") handleLogin();
            }}
          />
          <div class="flex justify-center mt-4">
            <Button text="LOGIN" func={handleLogin} />
          </div>
        {/if}
      </div>
    {:else}
      <div class="flex flex-col items-center gap-4 w-full max-w-130 px-5 lg:px-0">
        <p class="text-lightgray font-fredoka">
          Logged in as <b class="text-whitish">{username}</b>
          <button
            type="button"
            class="ml-2 text-pink text-[10pt] font-bold underline cursor-pointer"
            onclick={handleLogout}
          >
            Logout
          </button>
        </p>

        <label class="w-full">
          <span class="block text-left text-lightgray font-fredoka mb-1">Image (400x400)</span>
          <input
            bind:this={fileInput}
            type="file"
            accept="image/*"
            onchange={onFileSelected}
            class="w-full text-whitish file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-terciary file:text-whitish file:font-bold hover:file:cursor-pointer"
          />
        </label>

        {#if imageSrc}
          <div class="flex flex-col items-center gap-2">
            <div
              role="application"
              aria-label="Crop area"
              class="relative overflow-hidden bg-black rounded-lg touch-none select-none cursor-move"
              style="width: {CROP_SIZE}px; height: {CROP_SIZE}px;"
              onpointerdown={onPointerDown}
              onpointermove={onPointerMove}
              onpointerup={onPointerUp}
              onpointercancel={onPointerUp}
            >
              <img
                bind:this={imageEl}
                src={imageSrc}
                alt="preview"
                draggable={false}
                onload={onImageLoad}
                style="position:absolute; left:0; top:0; transform-origin: 0 0; transform: translate({offsetX}px, {offsetY}px) scale({scale}); max-width:none;"
              />
              <div class="absolute inset-0 pointer-events-none border-2 border-whitish/60 rounded-lg"></div>
            </div>
            <div class="w-full flex items-center gap-3">
              <span class="text-lightgray text-xs">Zoom</span>
              <input
                type="range"
                min={minScale}
                max={Math.max(minScale * 4, 4)}
                step="0.01"
                value={scale}
                oninput={onScaleInput}
                class="flex-1"
              />
            </div>
            <p class="text-lightgray text-xs">Drag to reposition. The visible square will be saved at 400×400.</p>
          </div>
        {/if}

        <input
          class="w-full bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="text"
          placeholder="MOVIE NAME"
          bind:value={movieName}
        />
        <input
          class="w-full bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="number"
          placeholder="YEAR"
          bind:value={movieYear}
        />
        <input
          class="w-full bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray"
          type="text"
          placeholder="DIRECTOR"
          bind:value={movieDirector}
        />

        {#if generatedHints.length > 0}
          <div class="w-full">
            <p class="text-lightgray font-fredoka mb-2 text-left">
              Generated hints ({generatedHints.length}) — click a hint to zoom
            </p>
            <div class="flex gap-2 overflow-x-auto pb-2">
              {#each generatedHints as hint, i (i)}
                <div class="shrink-0 flex flex-col items-center gap-1">
                  <button
                    type="button"
                    onclick={() => (zoomedHintIndex = i)}
                    class="p-0 border-0 bg-transparent cursor-zoom-in"
                    aria-label={`Zoom hint ${i}`}
                  >
                    <img
                      src={hint}
                      alt={`hint ${i}`}
                      class="w-24 h-24 rounded-md object-cover bg-black hover:opacity-90 transition-opacity"
                    />
                  </button>
                  <span class="text-gray text-[10px] font-bold">#{i}</span>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        <div class="flex justify-center mt-4 gap-3 flex-wrap">
          {#if submitting || generatingHints}
            <Loading />
          {:else if generatedHints.length === 0}
            <Button text="GENERATE HINTS" func={handleGenerateHints} />
          {:else}
            <Button text="REGENERATE HINTS" func={handleGenerateHints} />
            <Button text="SAVE MOVIE" func={handleSubmit} />
          {/if}
        </div>
      </div>

      <div class="w-full max-w-225 px-5 lg:px-0 mt-16">
        <div class="flex items-center justify-between mb-4 gap-3">
          <h2 class="text-whitish text-2xl">Existing movies</h2>
          <div class="flex bg-terciary rounded-lg overflow-hidden shrink-0">
            <button
              type="button"
              onclick={() => (viewMode = "list")}
              class="px-3 py-2 text-xs font-bold cursor-pointer {viewMode === 'list' ? 'bg-pink text-whitish' : 'text-lightgray hover:text-whitish'}"
              aria-pressed={viewMode === "list"}
            >
              LIST
            </button>
            <button
              type="button"
              onclick={() => (viewMode = "grid")}
              class="px-3 py-2 text-xs font-bold cursor-pointer {viewMode === 'grid' ? 'bg-pink text-whitish' : 'text-lightgray hover:text-whitish'}"
              aria-pressed={viewMode === "grid"}
            >
              GRID
            </button>
          </div>
        </div>
        <input
          type="text"
          placeholder="Search by name, year or director"
          value={search}
          oninput={onSearchInput}
          class="w-full bg-terciary h-12 px-4 rounded-lg text-whitish placeholder:font-bold placeholder:text-gray mb-4"
        />

        <div
          class="bg-secondary rounded-lg p-3 max-h-125 overflow-y-auto text-left"
        >
          {#if loadingMovies}
            <div class="flex justify-center py-6"><Loading /></div>
          {:else if movies.length === 0}
            <p class="text-lightgray text-center py-6">No movies found.</p>
          {:else if viewMode === "list"}
            <ul class="flex flex-col gap-2">
              {#each movies as movie (movie.id)}
                <li
                  class="flex items-center gap-3 bg-terciary rounded-lg p-2"
                >
                  {#if movie.image_path}
                    <img
                      src={apiBase + "/" + movie.image_path}
                      alt={movie.name}
                      class="w-16 h-16 rounded-md object-cover shrink-0 bg-black"
                      loading="lazy"
                    />
                  {:else}
                    <div class="w-16 h-16 rounded-md bg-black shrink-0"></div>
                  {/if}
                  <div class="flex-1 min-w-0">
                    <p class="text-whitish font-bold truncate">
                      {movie.name}
                    </p>
                    <p class="text-lightgray text-sm truncate">
                      {movie.director ?? "—"}{movie.year ? ` · ${movie.year}` : ""}
                    </p>
                    <div class="flex gap-1 mt-1 flex-wrap">
                      <span
                        class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple text-whitish"
                        title="Hints amount"
                      >
                        💡 {movie.hints_amount}
                      </span>
                      <span
                        class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-pink text-whitish"
                        title="Difficulty level"
                      >
                        {"★".repeat(movie.difficulty_level)}{"☆".repeat(Math.max(0, 5 - movie.difficulty_level))}
                      </span>
                    </div>
                  </div>
                  <span class="text-gray text-xs shrink-0">#{movie.id}</span>
                </li>
              {/each}
            </ul>
          {:else}
            <ul class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
              {#each movies as movie (movie.id)}
                <li class="bg-terciary rounded-lg p-2 flex flex-col gap-2 relative">
                  {#if movie.image_path}
                    <img
                      src={apiBase + "/" + movie.image_path}
                      alt={movie.name}
                      class="w-full aspect-square rounded-md object-cover bg-black"
                      loading="lazy"
                    />
                  {:else}
                    <div class="w-full aspect-square rounded-md bg-black"></div>
                  {/if}
                  <div class="absolute top-3 left-3 right-3 flex flex-row items-start gap-1 flex-wrap">
                    <span
                      class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple/90 text-whitish backdrop-blur-sm"
                      title="Hints amount"
                    >
                      💡 {movie.hints_amount}
                    </span>
                    <span
                      class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-pink/90 text-whitish backdrop-blur-sm"
                      title="Difficulty level"
                    >
                      {"★".repeat(movie.difficulty_level)}{"☆".repeat(Math.max(0, 5 - movie.difficulty_level))}
                    </span>
                  </div>
                  <div class="min-w-0">
                    <p class="text-whitish font-bold text-sm truncate">
                      {movie.name}
                    </p>
                    <p class="text-lightgray text-xs truncate">
                      {movie.director ?? "—"}{movie.year ? ` · ${movie.year}` : ""}
                    </p>
                  </div>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
        <p class="text-lightgray text-xs mt-2 text-right">
          {movies.length} movie{movies.length === 1 ? "" : "s"}
        </p>
      </div>
    {/if}
  </section>
  <Toaster />

  {#if zoomedHintIndex !== null && generatedHints[zoomedHintIndex]}
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Zoomed hint preview"
      tabindex="-1"
      class="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4 cursor-zoom-out"
      onclick={closeZoom}
      onkeydown={onZoomKeydown}
    >
      <button
        type="button"
        onclick={(e) => { e.stopPropagation(); closeZoom(); }}
        aria-label="Close zoom"
        class="absolute top-4 right-4 w-10 h-10 rounded-full bg-terciary text-whitish text-lg font-bold cursor-pointer hover:bg-pink"
      >
        ✕
      </button>

      {#if generatedHints.length > 1}
        <button
          type="button"
          onclick={(e) => {
            e.stopPropagation();
            zoomedHintIndex = (zoomedHintIndex! - 1 + generatedHints.length) % generatedHints.length;
          }}
          aria-label="Previous hint"
          class="absolute left-4 w-10 h-10 rounded-full bg-terciary text-whitish text-lg font-bold cursor-pointer hover:bg-pink"
        >
          ‹
        </button>
        <button
          type="button"
          onclick={(e) => {
            e.stopPropagation();
            zoomedHintIndex = (zoomedHintIndex! + 1) % generatedHints.length;
          }}
          aria-label="Next hint"
          class="absolute right-4 w-10 h-10 rounded-full bg-terciary text-whitish text-lg font-bold cursor-pointer hover:bg-pink"
        >
          ›
        </button>
      {/if}

      <div class="flex flex-col items-center gap-3 max-w-full max-h-full" onclick={(e) => e.stopPropagation()} role="presentation">
        <img
          src={generatedHints[zoomedHintIndex]}
          alt={`hint ${zoomedHintIndex}`}
          class="max-w-[90vw] max-h-[85vh] object-contain rounded-lg bg-black shadow-medium"
        />
        <span class="text-whitish font-bold text-sm">
          Hint #{zoomedHintIndex} · {zoomedHintIndex + 1} / {generatedHints.length}
        </span>
      </div>
    </div>
  {/if}
</main>

<svelte:window onkeydown={onZoomKeydown} />
