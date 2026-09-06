const $ = (s, r = document) => r.querySelector(s);
const icons = {
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
  arrow: '<path d="m5 12 14-7-7 14-1-7-6-2Z"/>',
  play: '<path d="m8 5 11 7-11 7Z"/>',
  pause: '<path d="M9 5v14M15 5v14"/>',
  close: '<path d="m6 6 12 12M6 18 18 6"/>',
  left: '<path d="m14 5-7 7 7 7"/>',
  right: '<path d="m10 5 7 7-7 7"/>',
  mesh: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/>',
  reset: '<path d="M4 10a8 8 0 1 1 1 8M4 4v6h6"/>',
  feet: '<ellipse cx="8" cy="8" rx="2.5" ry="5" transform="rotate(12 8 8)"/><ellipse cx="16" cy="14" rx="2.5" ry="5" transform="rotate(-12 16 14)"/><path d="M6 16v3M18 5v3"/>',
};
const icon = (n) =>
  `<svg viewBox="0 0 24 24" aria-hidden="true">${icons[n] || icons.play}</svg>`;
const asset = (n) => `assets/${n}.webp`;
const safe = (s) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
let quote = "Leave a little room for the unexpected.";
try {
  quote = localStorage.getItem("soft-note") || quote;
} catch {}
let selectedDay = 3,
  focusSeconds = 13 * 60 + 40,
  focusRunning = true,
  runnerPlaying = true;
const distances = [4.2, 0.4, 5.6, 3.1, 0.5, 8.2, 3.8],
  days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];
const messages = [
  {
    name: "Research agent",
    time: "2:40 PM",
    text: "Three Bay Area stories, with the key details and sources ready to explore.",
    unread: true,
  },
  {
    name: "Motion agent",
    time: "2:32 PM",
    text: "Content comes and goes independently. Every surface moves at the same pace.",
    unread: false,
  },
  {
    name: "Weather agent",
    time: "2:18 PM",
    text: "Current conditions and the five-day forecast, all in one place.",
    unread: true,
  },
];
const photoNames = {
  poster: "Typography study",
  flower: "Golden chrysanthemum",
  boxes: "Packaging forms",
  butterfly: "Butterfly in glass",
  moss: "Mossy landscape",
  grass: "Grass in motion",
};
function inbox() {
  return `<div class="card-body inbox"><div class="card-head">Inbox <span class="tiny unread-count">${messages.filter((x) => x.unread).length} unread</span><button class="search-button" data-action="search">${icon("search")} Search</button></div><div class="messages">${messages.map((m, i) => `<button class="message ${m.unread ? "unread" : ""}" data-action="message" data-index="${i}"><span class="message-line"><span>${m.name}</span><time class="tiny">${m.time}</time></span><p>${m.text}</p>${i === 1 ? `<img class="thumbs" src="${asset("thumbs")}" alt="Three visual references">` : ""}</button>`).join("")}</div></div>`;
}
const photos = (names, cls = "mood-grid") =>
  `<div class="${cls}">${names.map((n) => `<button class="image-button" data-action="photo" data-photo="${n}" aria-label="Open ${photoNames[n]}"><img src="${asset(n)}" alt="${photoNames[n]}"></button>`).join("")}</div>`;
const cards = [
  { id: "inbox", name: "Inbox", html: inbox },
  {
    id: "note",
    name: "Quick note",
    html: () =>
      `<div class="card-body note"><div class="card-head">Quick note<button class="end tiny" data-action="edit-note" aria-label="Edit note">Edit</button></div><p class="quote">${safe(quote)}</p><span class="note-tag">Draft · This session</span></div>`,
  },
  {
    id: "mood",
    name: "Mood board",
    html: () =>
      `<div class="card-body">${photos(["poster", "flower", "boxes", "butterfly"])}<div class="card-foot"><div><h2 class="card-title">Mood board</h2><p class="muted">Collected inspiration</p></div><span class="tiny">4 references</span></div></div>`,
  },
  {
    id: "event",
    name: "Up next",
    html: () =>
      `<div class="card-body event"><div class="card-head">Up next<span class="end">${icon("clock")}</span></div><div class="time">7:30<small>PM</small></div><p class="event-title">Omakase Dinner</p><p class="muted">2 Hours · with Hamna</p><div class="event-bottom"><img class="avatars" src="${asset("avatars")}" alt="Three dinner guests"><button class="pill" data-action="directions">${icon("arrow")} Show directions</button></div></div>`,
  },
  {
    id: "runner",
    name: "Nike running",
    html: () =>
      `<div class="runner ${runnerPlaying ? "" : "paused"}" aria-label="Nike running, animated photo study"><img class="runner-photo" src="${asset("runner")}" alt="Runner on a misty mountain trail"><div class="runner-bottom"><span>Nike running</span><button data-action="runner" aria-label="${runnerPlaying ? "Pause" : "Play"} photo animation">${icon(runnerPlaying ? "pause" : "play")}</button><button data-action="runner-restart" aria-label="Restart photo animation">${icon("play")}</button></div><div class="runner-progress"></div></div>`,
  },
  {
    id: "activity",
    name: "Activity",
    html: () =>
      `<div class="card-body activity"><div class="card-head">Activity<span class="end">${icon("feet")}</span></div><div class="distance"><span class="distance-value">${distances[selectedDay].toFixed(1)}</span><small>km</small></div><div class="bars">${distances.map((v, i) => `<button class="bar-button ${i === selectedDay ? "active" : ""}" data-action="day" data-day="${i}" aria-label="${days[i]}: ${v} kilometers" aria-pressed="${i === selectedDay}"><span class="bar" style="--bar:${v * 6.5}px"></span><small>${days[i][0]}</small></button>`).join("")}</div></div>`,
  },
  {
    id: "shader",
    name: "Shader Experiments",
    html: () =>
      `<div class="card-body">${photos(["moss", "grass", "grass"], "grass-grid")}<div class="card-foot"><div><h2 class="card-title">Shader Experiments</h2><p class="muted">Grass in motion</p></div><span class="tiny">3 studies</span></div></div>`,
  },
  {
    id: "focus",
    name: "Focus",
    html: () =>
      `<div class="card-body focus"><div class="card-head">Focus<span class="end tiny">${focusRunning ? "In progress" : "Paused"}</span></div><div class="clock"><div class="clock-ring"></div><div class="clock-time">${timeString()}</div></div><div class="focus-actions"><button class="pill reset" data-action="focus-reset" aria-label="Reset focus timer">${icon("reset")}</button><button class="pill" data-action="focus">${icon(focusRunning ? "pause" : "play")} ${focusRunning ? "Pause" : "Resume"}</button></div></div>`,
  },
];
function timeString() {
  return `${Math.floor(focusSeconds / 60)}:${String(focusSeconds % 60).padStart(2, "0")}`;
}
function renderGallery() {
  $("#gallery").innerHTML = cards
    .slice(0, 7)
    .map(
      (c, i) =>
        `<section class="tile" style="--i:${i}"><h2 class="tile-label">${c.name}</h2><article class="card" data-card="${i}" tabindex="0" aria-label="${c.name}, open motion study">${c.html()}</article></section>`,
    )
    .join("");
}
renderGallery();
const stage = $("#stage"),
  surface = $("#surface"),
  mesh = $("#mesh"),
  toolbar = $(".toolbar");
let active = 0,
  playing = false,
  slow = false,
  showMesh = false,
  interval = null,
  closeTimer = null,
  transitionId = 0,
  lastOrigin = null,
  measureFrame = null;
const reduced = matchMedia("(prefers-reduced-motion: reduce)");
const duration = () => (reduced.matches ? 0 : slow ? 1400 : 700);
$("#close").innerHTML = icon("close");
$("#previous").innerHTML = icon("left");
$("#next").innerHTML = icon("right");
$("#mesh-button").innerHTML = icon("mesh");
$("#dots").innerHTML = cards
  .map(
    (c, i) =>
      `<button aria-label="Show ${c.name}" data-target="${i}"></button>`,
  )
  .join("");
function setPlayUI() {
  $("#play-button").innerHTML = icon(playing ? "pause" : "play");
  $("#play-button").setAttribute(
    "aria-label",
    playing ? "Pause motion demo" : "Play motion demo",
  );
  $("#play-button").setAttribute("aria-pressed", String(playing));
}
setPlayUI();
function animateHeightLabel() {
  cancelAnimationFrame(measureFrame);
  const end = performance.now() + duration() + 50;
  function tick() {
    $("#height-value").textContent =
      Math.round(surface.getBoundingClientRect().height) + " PX";
    if (performance.now() < end) measureFrame = requestAnimationFrame(tick);
  }
  tick();
}
function switchCard(index, initial = false) {
  active = (index + cards.length) % cards.length;
  const id = ++transitionId;
  const oldLayers = [...surface.children];
  const layer = document.createElement("div");
  layer.className = "layer";
  layer.innerHTML = cards[active].html();
  surface.append(layer);
  const h = layer.getBoundingClientRect().height;
  surface.style.height = h + "px";
  mesh.style.height = h + "px";
  surface.classList.toggle(
    "dark",
    cards[active].id === "focus" || cards[active].id === "runner",
  );
  const d = initial ? 0 : duration();
  oldLayers.forEach((el) => {
    el.getAnimations().forEach((a) => a.cancel());
    el.style.pointerEvents = "none";
    const a = el.animate(
      [
        {
          opacity: parseFloat(getComputedStyle(el).opacity) || 1,
          filter: "blur(0px)",
          transform: "translateY(0)",
        },
        { opacity: 0, filter: "blur(5px)", transform: "translateY(-6px)" },
      ],
      {
        duration: d * 0.52,
        easing: "cubic-bezier(.4,0,1,1)",
        fill: "forwards",
      },
    );
    a.finished.then(() => el.remove()).catch(() => el.remove());
  });
  layer
    .animate(
      [
        { opacity: 0, filter: "blur(7px)", transform: "translateY(9px)" },
        { opacity: 1, filter: "blur(0)", transform: "translateY(0)" },
      ],
      {
        duration: d * 0.8,
        delay: d * 0.16,
        easing: "cubic-bezier(.22,1,.36,1)",
        fill: "both",
      },
    )
    .finished.then(() => {
      if (id === transitionId) layer.style.opacity = "1";
    })
    .catch(() => {});
  $("#stage-name").textContent = cards[active].name;
  $("#stage-count").textContent =
    `${String(active + 1).padStart(2, "0")} / ${String(cards.length).padStart(2, "0")}`;
  document.querySelectorAll("#dots button").forEach((b, i) => {
    b.classList.toggle("active", i === active);
    b.setAttribute("aria-pressed", String(i === active));
  });
  animateHeightLabel();
}
function openStage(index = active, origin = null) {
  if (stage.open) {
    switchCard(index);
    return;
  }
  clearTimeout(closeTimer);
  lastOrigin = origin || document.activeElement;
  stage.append(toolbar);
  stage.append($("#cursor"));
  stage.showModal();
  document.body.style.overflow = "hidden";
  $("#gallery-button").classList.remove("selected");
  $("#morph-button").classList.add("selected");
  switchCard(index, true);
  stage.classList.add("visible");
  const from = origin?.getBoundingClientRect();
  if (from && !reduced.matches) {
    const to = surface.getBoundingClientRect();
    $(".surface-wrap").animate(
      [
        {
          transform: `translate(${from.x - to.x}px,${from.y - to.y}px) scale(${from.width / to.width})`,
          transformOrigin: "top left",
        },
        { transform: "translate(0,0) scale(1)", transformOrigin: "top left" },
      ],
      { duration: duration(), easing: "cubic-bezier(.22,1,.36,1)" },
    );
  }
}
function closeStage() {
  stopPlay();
  stage.classList.remove("visible");
  clearTimeout(closeTimer);
  closeTimer = setTimeout(
    () => {
      stage.close();
      document.body.append(toolbar);
      document.body.append($("#cursor"));
      document.body.style.overflow = "";
      $("#gallery-button").classList.add("selected");
      $("#morph-button").classList.remove("selected");
      renderGallery();
      const card = lastOrigin?.dataset?.card;
      if (card !== undefined)
        $(`[data-card="${card}"]`)?.focus({ preventScroll: true });
      else $("#morph-button").focus({ preventScroll: true });
    },
    reduced.matches ? 0 : 300,
  );
}
function schedule() {
  clearInterval(interval);
  interval = setInterval(() => switchCard(active + 1), slow ? 4300 : 2700);
}
function stopPlay() {
  playing = false;
  clearInterval(interval);
  setPlayUI();
}
function togglePlay() {
  if (playing) stopPlay();
  else {
    if (!stage.open) openStage(0);
    playing = true;
    setPlayUI();
    schedule();
  }
}
$("#morph-button").onclick = () => openStage(active);
$("#gallery-button").onclick = () => stage.open && closeStage();
$("#close").onclick = closeStage;
stage.addEventListener("cancel", (e) => {
  e.preventDefault();
  closeStage();
});
$("#play-button").onclick = togglePlay;
$("#speed-button").onclick = () => {
  slow = !slow;
  document.documentElement.style.setProperty(
    "--duration",
    slow ? "1400ms" : "700ms",
  );
  $("#speed-button").textContent = slow ? "0.5×" : "1×";
  if (playing) schedule();
};
$("#mesh-button").onclick = () => {
  showMesh = !showMesh;
  $("#inspector").classList.toggle("shown", showMesh);
  $("#inspector").setAttribute("aria-hidden", String(!showMesh));
  $("#mesh-button").setAttribute("aria-pressed", String(showMesh));
  if (!stage.open) openStage(active);
  if (innerWidth <= 640 && showMesh)
    toast("Mesh view is available on a wider screen.");
};
function manualStep(i) {
  stopPlay();
  switchCard(i);
}
$("#previous").onclick = () => manualStep(active - 1);
$("#next").onclick = () => manualStep(active + 1);
$("#dots").onclick = (e) => {
  const b = e.target.closest("[data-target]");
  if (b) manualStep(+b.dataset.target);
};
document.addEventListener("keydown", (e) => {
  if (/INPUT|TEXTAREA/.test(e.target.tagName)) return;
  if (stage.open) {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      manualStep(active + 1);
    }
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      manualStep(active - 1);
    }
    if (e.code === "Space" && e.target === stage) {
      e.preventDefault();
      togglePlay();
    }
  } else if (e.key === "Enter" && e.target.matches("[data-card]"))
    openStage(+e.target.dataset.card, e.target);
});
$("#gallery").addEventListener("click", (e) => {
  if (e.target.closest("[data-action],input,textarea")) return;
  const c = e.target.closest("[data-card]");
  if (c) openStage(+c.dataset.card, c);
});
let toastTimer;
function toast(s) {
  $("#toast").textContent = s;
  const parent = stage.open ? stage : document.body;
  parent.append($("#toast"));
  $("#toast").classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $("#toast").classList.remove("visible"), 2800);
}
function refreshCurrent() {
  if (stage.open) switchCard(active);
  else renderGallery();
}
function resizeLayer(layer) {
  if (stage.open && layer) {
    surface.style.height = layer.getBoundingClientRect().height + "px";
    mesh.style.height = surface.style.height;
    animateHeightLabel();
  }
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-action]");
  if (!b) return;
  e.stopPropagation();
  const action = b.dataset.action,
    body = b.closest(".card-body"),
    layer = b.closest(".layer");
  if (action === "day") {
    selectedDay = +b.dataset.day;
    const value = $(".distance-value", body);
    value.textContent = distances[selectedDay].toFixed(1);
    value.animate(
      [
        { opacity: 0.15, transform: "translateY(5px)" },
        { opacity: 1, transform: "translateY(0)" },
      ],
      { duration: duration() * 0.6, easing: "ease-out" },
    );
    body.querySelectorAll(".bar-button").forEach((x) => {
      x.classList.toggle("active", x === b);
      x.setAttribute("aria-pressed", String(x === b));
    });
  }
  if (action === "search") {
    let input = $("input", body);
    if (input) {
      input.remove();
      body.querySelectorAll(".message").forEach((x) => (x.hidden = false));
      $(".no-results", body)?.remove();
      return;
    }
    input = document.createElement("input");
    input.className = "search-input";
    input.placeholder = "Search messages";
    input.setAttribute("aria-label", "Search messages");
    $(".card-head", body).after(input);
    input.focus();
    input.addEventListener("input", () => {
      let count = 0;
      body.querySelectorAll(".message").forEach((x) => {
        x.hidden = !x.textContent
          .toLowerCase()
          .includes(input.value.toLowerCase());
        if (!x.hidden) count++;
      });
      $(".no-results", body)?.remove();
      if (!count) {
        const p = document.createElement("p");
        p.className = "no-results";
        p.textContent = "No matching messages.";
        body.append(p);
      }
      resizeLayer(layer);
    });
    resizeLayer(layer);
  }
  if (action === "message") {
    const i = +b.dataset.index;
    messages[i].unread = false;
    b.classList.remove("unread");
    $(".unread-count", body).textContent =
      messages.filter((x) => x.unread).length + " unread";
    const detail = document.createElement("div");
    detail.className = "message-detail";
    detail.innerHTML = `<button class="pill" data-action="back-inbox">${icon("left")} Inbox</button><h2>${messages[i].name}</h2><p>${messages[i].text}</p><p style="margin-top:18px">${i === 1 ? "One shared surface. Independent content. A little room for everything to move." : i === 2 ? "Weather preview · Bodega Bay<br>58°F · Cloudy<br>Light wind from the west." : "Demo inbox · Three references collected for your next research session."}</p>`;
    $(".messages", body).replaceWith(detail);
    resizeLayer(layer);
  }
  if (action === "back-inbox") {
    body.outerHTML = inbox();
    if (layer) resizeLayer(layer);
  }
  if (action === "edit-note") {
    const q = $(".quote", body);
    if (!q) {
      const input = $("textarea", body);
      quote = input.value.trim() || "Leave a little room for the unexpected.";
      try {
        localStorage.setItem("soft-note", quote);
      } catch {}
      const p = document.createElement("p");
      p.className = "quote";
      p.textContent = quote;
      input.replaceWith(p);
      b.textContent = "Edit";
      $(".note-tag", body).textContent = "Saved · On this device";
      return;
    }
    const input = document.createElement("textarea");
    input.className = "quote-input";
    input.value = quote;
    input.maxLength = 160;
    input.setAttribute("aria-label", "Quick note");
    q.replaceWith(input);
    input.focus();
    b.textContent = "Done";
  }
  if (action === "directions")
    toast("Demo event — no restaurant address is included in the reference.");
  if (action === "runner" || action === "runner-restart") {
    runnerPlaying = action === "runner-restart" ? true : !runnerPlaying;
    const r = b.closest(".runner");
    r.classList.toggle("paused", !runnerPlaying);
    const play = $('[data-action="runner"]', r);
    play.innerHTML = icon(runnerPlaying ? "pause" : "play");
    play.setAttribute(
      "aria-label",
      `${runnerPlaying ? "Pause" : "Play"} photo animation`,
    );
    if (action === "runner-restart")
      r.getAnimations({ subtree: true }).forEach((a) => (a.currentTime = 0));
  }
  if (action === "focus") {
    focusRunning = !focusRunning;
    refreshCurrent();
  }
  if (action === "focus-reset") {
    focusSeconds = 13 * 60 + 40;
    focusRunning = true;
    refreshCurrent();
  }
  if (action === "photo") {
    const grid = b.parentElement;
    const n = b.dataset.photo;
    grid.outerHTML = `<div class="photo-detail"><img class="photo-view" src="${asset(n)}" alt="${photoNames[n]}"><button class="pill photo-back" data-action="back-photo">${icon("left")} Back to collection</button></div>`;
    resizeLayer(layer);
  }
  if (action === "back-photo") {
    if (layer) switchCard(active);
    else {
      const c = b.closest("[data-card]");
      c.innerHTML = cards[+c.dataset.card].html();
    }
  }
});
setInterval(() => {
  if (focusRunning && focusSeconds > 0) focusSeconds--;
  document
    .querySelectorAll(".clock-time")
    .forEach((x) => (x.textContent = timeString()));
  if (focusSeconds === 0 && focusRunning) {
    focusRunning = false;
    if (stage.open && active === 7) refreshCurrent();
  }
}, 1000);
const cursor = $("#cursor");
let px = -100,
  py = -100,
  cx = -100,
  cy = -100,
  raf = 0;
function moveCursor() {
  cx += (px - cx) * 0.22;
  cy += (py - cy) * 0.22;
  cursor.style.transform = `translate3d(${cx - 26}px,${cy - 26}px,0)`;
  if (Math.abs(px - cx) + Math.abs(py - cy) > 0.1)
    raf = requestAnimationFrame(moveCursor);
  else raf = 0;
}
document.addEventListener("pointermove", (e) => {
  if (e.pointerType !== "mouse" || reduced.matches) return;
  px = e.clientX;
  py = e.clientY;
  cursor.style.opacity = e.target.closest(".card,.morph-surface,.mesh")
    ? "1"
    : "0";
  if (!raf) raf = requestAnimationFrame(moveCursor);
});
document.addEventListener("pointerdown", () => cursor.classList.add("down"));
document.addEventListener("pointerup", () => cursor.classList.remove("down"));
document.addEventListener("pointerleave", () => (cursor.style.opacity = 0));
window.addEventListener("resize", () => {
  if (stage.open) resizeLayer(surface.lastElementChild);
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden && playing) stopPlay();
});
reduced.addEventListener("change", () => {
  if (reduced.matches) stopPlay();
});
