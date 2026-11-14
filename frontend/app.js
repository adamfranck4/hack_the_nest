// Entry point: decides which screen to show (home -> conversation -> scorecard).
import { html, React } from "./components/html.js";
import { createRoot } from "react-dom/client";
import { Home } from "./components/Home.js";
import { Conversation } from "./components/Conversation.js";
import { Scorecard } from "./components/Scorecard.js";
import { api, MOCK } from "./api.js";

const { useState } = React;

function App() {
  const [screen, setScreen] = useState("home"); // "home" | "conversation" | "scorecard"
  const [session, setSession] = useState(null);
  const [starting, setStarting] = useState(false);
  const [retryError, setRetryError] = useState(null);

  function start(s) {
    setSession(s);
    setScreen("conversation");
  }

  async function tryAgain() {
    setStarting(true);
    setRetryError(null);
    try {
      start(await api.createSession(session.character.id));
    } catch (e) {
      setRetryError(e.message);
    }
    setStarting(false);
  }

  return html`
    <div>
      ${MOCK && html`<div class="mock-badge">MOCK MODE</div>`}
      ${screen === "home" && html`<${Home} onPick=${start} />`}
      ${screen === "conversation" && html`
        <${Conversation} key=${session.session_id} session=${session}
          onFinish=${() => setScreen("scorecard")} onQuit=${() => setScreen("home")} />`}
      ${screen === "scorecard" && html`
        <${Scorecard} sessionId=${session.session_id} character=${session.character}
          onRetry=${tryAgain} onPickAnother=${() => setScreen("home")} />`}
      ${starting && html`<div class="toast">Starting a new conversation…</div>`}
      ${retryError && html`<div class="toast error">${retryError}</div>`}
    </div>`;
}

createRoot(document.getElementById("root")).render(html`<${App} />`);
