import { html, React } from "./html.js";
import { api } from "../api.js";

const { useState, useEffect } = React;

const OUTCOMES = {
  won: "🎉 You calmed them down",
  lost: "🌋 Full meltdown",
  timeout: "⏱️ Out of turns",
  ended: "🏁 Ended early",
};

export function Scorecard({ sessionId, character, onRetry, onPickAnother }) {
  const [card, setCard] = useState(null);
  const [error, setError] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [showTranscript, setShowTranscript] = useState(false);

  useEffect(() => {
    setError(null);
    setCard(null);
    api.getScorecard(sessionId).then(setCard).catch((e) => setError(e.message));
  }, [sessionId, reloadKey]);

  if (error) {
    return html`
      <main class="page narrow">
        <div class="banner error" role="alert"><span>${error}</span>
          <button class="btn small" onClick=${() => setReloadKey((k) => k + 1)}>Retry</button></div>
        <div class="row"><button class="btn secondary" onClick=${onPickAnother}>Pick another</button></div>
      </main>`;
  }
  if (!card) {
    return html`<main class="page narrow"><p class="muted center big-loading">Grading your conversation…</p></main>`;
  }

  const scoreColor = card.score >= 70 ? "var(--good)" : card.score >= 40 ? "var(--warn)" : "var(--bad)";
  return html`
    <main class="page narrow">
      <section class="card score-hero">
        <div class="score-num" style=${{ color: scoreColor }}>${card.score}<span>/100</span></div>
        <div class="outcome">${OUTCOMES[card.outcome] || card.outcome}</div>
        <p class="summary">${card.summary}</p>
      </section>

      <section class="card">
        <h3>Techniques you used</h3>
        ${card.techniques_used.length === 0
          ? html`<p class="muted">No calming techniques detected this time.</p>`
          : html`<div class="chips">${card.techniques_used.map((t) =>
              html`<span key=${t.name} class="chip">${t.name} <b>×${t.count}</b></span>`)}</div>`}
      </section>

      ${card.best_line && html`
        <section class="card line best">
          <h3>⭐ Best line</h3>
          <blockquote>“${card.best_line.text}”</blockquote>
          <p><strong>Why it worked:</strong> ${card.best_line.why}</p>
        </section>`}

      ${card.worst_line && html`
        <section class="card line worst">
          <h3>⚠️ Line to rethink</h3>
          <blockquote>“${card.worst_line.text}”</blockquote>
          <p><strong>Why:</strong> ${card.worst_line.why}</p>
          <p><strong>Try instead:</strong> ${card.worst_line.better}</p>
        </section>`}

      <section class="card">
        <button class="link-btn" onClick=${() => setShowTranscript(!showTranscript)} aria-expanded=${showTranscript}>
          ${showTranscript ? "▼" : "▶"} Transcript
        </button>
        ${showTranscript && html`
          <div class="transcript">
            ${card.transcript.map((m, i) => html`
              <p key=${i} class=${m.role}><b>${m.role === "user" ? "You" : character.name}:</b> ${m.text}</p>`)}
          </div>`}
      </section>

      <div class="row">
        <button class="btn" onClick=${onRetry}>Try again with ${character.name}</button>
        <button class="btn secondary" onClick=${onPickAnother}>Pick another</button>
      </div>
    </main>`;
}
