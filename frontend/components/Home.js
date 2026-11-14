import { html, React } from "./html.js";
import { api } from "../api.js";

const { useState, useEffect } = React;

export function Home({ onPick }) {
  const [characters, setCharacters] = useState(null);
  const [error, setError] = useState(null);
  const [starting, setStarting] = useState(null); // id of the character being started
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    setError(null);
    setCharacters(null);
    api.getCharacters().then(setCharacters).catch((e) => setError(e.message));
  }, [reloadKey]);

  async function pick(c) {
    setStarting(c.id);
    setError(null);
    try {
      const session = await api.createSession(c.id);
      onPick(session);
    } catch (e) {
      setError(e.message);
      setStarting(null);
    }
  }

  return html`
    <main class="page">
      <header class="hero">
        <h1>Talk It Out <span aria-hidden="true">💬</span></h1>
        <p class="pitch">Practice hard conversations before they happen.</p>
      </header>

      ${error && html`
        <div class="banner error" role="alert">
          <span>${error}</span>
          <button class="btn small" onClick=${() => setReloadKey((k) => k + 1)}>Retry</button>
        </div>`}
      ${!characters && !error && html`<p class="muted center">Loading characters…</p>`}
      ${characters && characters.length === 0 && html`<p class="muted center">No characters available yet.</p>`}

      <div class="cards">
        ${(characters || []).map((c) => html`
          <button key=${c.id} class="card char-card" disabled=${!!starting} onClick=${() => pick(c)}>
            <div class="card-emoji">${c.emoji}</div>
            <h2>${c.name} <small>${c.title}</small></h2>
            <p>${c.scenario}</p>
            <p class="goal"><strong>Goal:</strong> ${c.goal}</p>
            <span class="tag">${c.meter_label}</span>
            <span class="cta">${starting === c.id ? "Starting…" : "Start talking →"}</span>
          </button>`)}
      </div>
    </main>`;
}
