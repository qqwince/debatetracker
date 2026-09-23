import "./styles.css";
import { createGame, createUser, getMe } from "./api.js";

const STORAGE_KEY = "debatetracker.login";
const SESSION_GAMES_KEY = "debatetracker.sessionGames";

const MOTION_TYPES = [
  ["unknown", "Unknown"],
  ["this_house_believes_that", "THBT"],
  ["this_house_opposes", "THO"],
  ["this_house_prefer", "THP"],
  ["this_house_regrets", "THR"],
  ["this_house_supports", "THS"],
  ["this_house_would", "THW"],
];

const MOTION_THEMES = [
  "unknown",
  "international_relationship",
  "economics",
  "politics",
  "science_medicine",
  "AI_technologies",
  "philosophy_religion",
  "law_crime",
  "education",
  "art",
  "feminism",
  "sport",
  "conflict",
  "urbanism",
  "media",
  "LGBTQ",
  "europe",
  "asia",
  "central_asia",
  "kazakhstan",
  "social",
  "prefers_world",
];

const POSITIONS = ["OG", "OO", "CG", "CO"];

const app = document.querySelector("#app");

function labelTheme(value) {
  return value.replaceAll("_", " ");
}

function typeOptions(selected = "unknown") {
  return MOTION_TYPES.map(
    ([value, label]) =>
      `<option value="${value}" ${value === selected ? "selected" : ""}>${label}</option>`
  ).join("");
}

function themeOptions(selected = "unknown") {
  return MOTION_THEMES.map(
    (value) =>
      `<option value="${value}" ${value === selected ? "selected" : ""}>${labelTheme(value)}</option>`
  ).join("");
}

function positionOptions(selected = "OG") {
  return POSITIONS.map(
    (value) =>
      `<option value="${value}" ${value === selected ? "selected" : ""}>${value}</option>`
  ).join("");
}

function todayInputValue() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

function loadSessionGames() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_GAMES_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveSessionGames(games) {
  localStorage.setItem(SESSION_GAMES_KEY, JSON.stringify(games.slice(0, 20)));
}

function renderAuth(mode = "login", message = "", loginValue = "") {
  app.innerHTML = `
    <section class="auth">
      <div class="card">
        <h2>Debate Tracker</h2>
        <p class="hint">Логин — это доступ: пароля нет.</p>
        <div class="tabs">
          <button class="tab ${mode === "login" ? "active" : ""}" data-mode="login">Войти</button>
          <button class="tab ${mode === "register" ? "active" : ""}" data-mode="register">Регистрация</button>
        </div>
        <form class="stack" id="auth-form">
          <label>
            Login
            <input name="login" maxlength="127" required autocomplete="username" placeholder="например, speaker_og" value="${loginValue}" />
          </label>
          <button class="primary" type="submit">${mode === "login" ? "Продолжить" : "Создать пользователя"}</button>
        </form>
        ${message ? `<p class="flash ${message.ok ? "ok" : "bad"}">${message.text}</p>` : ""}
      </div>
    </section>
  `;

  app.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const login = app.querySelector('input[name="login"]')?.value || "";
      renderAuth(tab.dataset.mode, "", login);
    });
  });

  app.querySelector("#auth-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const login = new FormData(event.target).get("login").trim();
    const button = event.target.querySelector("button");
    button.disabled = true;
    try {
      if (mode === "register") {
        await createUser(login);
      }
      const me = await getMe(login);
      localStorage.setItem(STORAGE_KEY, me.login);
      renderApp(me);
    } catch (err) {
      renderAuth(mode, { ok: false, text: err.message }, login);
    }
  });
}

function renderApp(user, notice = "") {
  const games = loadSessionGames().filter((game) => game.owner === user.login);
  app.innerHTML = `
    <div class="shell">
      <header class="topbar">
        <div class="brand">
          <h1>Debate Tracker</h1>
          <p>Журнал раундов</p>
        </div>
        <div class="who">
          <span>${user.login}</span>
          <button class="danger" id="logout" type="button">Выйти</button>
        </div>
      </header>
      <div class="layout">
        <section class="composer">
          <h2>Новая запись</h2>
          <form id="game-form" class="stack">
            <div class="grid">
              <label>
                Турнир
                <input name="tournament_name" required placeholder="WUDC Open" />
              </label>
              <label>
                Дата турнира
                <input name="tournament_date" type="date" required value="${todayInputValue()}" />
              </label>
              <label>
                Тиммейт
                <input name="teammate" required placeholder="партнёр" />
              </label>
              <label>
                Позиция
                <select name="position">${positionOptions()}</select>
              </label>
              <label>
                Спикерпоинты
                <input name="speaker_points" type="number" required min="0" max="100" value="75" />
              </label>
              <label>
                Раунд
                <input name="round_points" type="number" required min="1" max="9" value="1" />
              </label>
              <label>
                Тип моушена
                <select name="motion_type">${typeOptions()}</select>
              </label>
              <label>
                Тема
                <select name="motion_theme">${themeOptions()}</select>
              </label>
            </div>
            <div class="actions">
              <button class="primary" type="submit">Сохранить</button>
            </div>
          </form>
          ${notice ? `<p class="flash ${notice.ok ? "ok" : "bad"}">${notice.text}</p>` : ""}
        </section>
        <section class="records">
          <h2>Записи <span>${games.length}</span></h2>
          ${
            games.length
              ? `<ul class="session-list">${games
                  .map(
                    (game) => `
                <li>
                  <strong>${game.tournament_name}</strong>
                  <em>R${game.round_points} · ${game.position} · ${game.speaker_points} sp</em>
                  <p class="meta">${game.teammate} · ${labelTheme(game.motion_theme)}</p>
                </li>`
                  )
                  .join("")}</ul>`
              : `<p class="empty">Пока пусто — сохраните первый раунд.</p>`
          }
        </section>
      </div>
    </div>
  `;

  app.querySelector("#logout").addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    renderAuth("login");
  });

  app.querySelector("#game-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form).entries());
    const button = form.querySelector("button");
    button.disabled = true;
    const payload = {
      entry_creation_date: new Date().toISOString(),
      tournament_date: new Date(`${data.tournament_date}T12:00:00`).toISOString(),
      tournament_name: data.tournament_name.trim(),
      teammate: data.teammate.trim(),
      position: data.position,
      speaker_points: Number(data.speaker_points),
      round_points: Number(data.round_points),
      motion_type: data.motion_type,
      motion_theme: data.motion_theme,
    };
    try {
      const game = await createGame(user.login, payload);
      const next = [{ ...game, owner: user.login }, ...loadSessionGames()];
      saveSessionGames(next);
      renderApp(user, { ok: true, text: `Игра #${game.id} сохранена.` });
    } catch (err) {
      renderApp(user, { ok: false, text: err.message });
      button.disabled = false;
    }
  });
}

async function boot() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    renderAuth("login");
    return;
  }
  try {
    const me = await getMe(saved);
    renderApp(me);
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    renderAuth("login", { ok: false, text: "Сессия слетела — войдите снова." });
  }
}

boot();
