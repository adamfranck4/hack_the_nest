import { html, React } from "./html.js";
import { api } from "../api.js";
import { playBase64, stopAudio } from "../audio.js";
import { MoodMeter } from "./MoodMeter.js";

const { useState, useEffect, useRef } = React;

const END_BANNERS = {
  won: { cls: "won", text: "🎉 You did it! They're calm." },
  lost: { cls: "lost", text: "🌋 Full meltdown!" },
  timeout: { cls: "timeout", text: "⏱️ Out of turns. Let's see how you did." },
};

export function Conversation({ session, onFinish, onQuit }) {
  const { character } = session;
  const [mood, setMood] = useState(session.mood);
  const [turn, setTurn] = useState(session.turn);
  const [status, setStatus] = useState(session.status);
  const [messages, setMessages] = useState([
    { role: "character", text: session.opening.text },
  ]);
  const [delta, setDelta] = useState(null);
  const [busy, setBusy] = useState(false);
  const [pendingText, setPendingText] = useState(null);
  const [error, setError] = useState(null);
  const [lastPayload, setLastPayload] = useState(null);
  const [recording, setRecording] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [draft, setDraft] = useState("");
  const recorderRef = useRef(null);
  const chunksRef = useRef([]);
  const endRef = useRef(null);
  const active = status === "active";

  // Speak the opening line, and stop audio when leaving the screen.
  useEffect(() => {
    speak(session.opening.audio_b64);
    return () => {
      stopAudio();
      stopRecorder(true);
    };
  }, []);

  // Keep the newest message in view.
  useEffect(() => {
    if (endRef.current && endRef.current.scrollIntoView) {
      endRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, [messages, busy, error]);

  function speak(b64) {
    if (!b64) return;
    setSpeaking(true);
    playBase64(b64).then(() => setSpeaking(false));
  }

  async function submit(payload) {
    setBusy(true);
    setError(null);
    setLastPayload(payload);
    setPendingText(payload.text || "🎤 …");
    try {
      const r = await api.sendTurn(session.session_id, payload);
      setMessages((m) => [
        ...m,
        { role: "user", text: r.user_text },
        { role: "character", text: r.reply_text, note: r.note, techniques: r.techniques },
      ]);
      setMood(r.mood);
      setTurn(r.turn);
      setStatus(r.status);
      setDelta({ value: r.mood_delta, key: r.turn });
      setLastPayload(null);
      speak(r.reply_audio_b64);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
      setPendingText(null);
    }
  }

  function sendText(e) {
    e.preventDefault();
    const text = draft.trim();
    if (!text || busy || !active) return;
    setDraft("");
    submit({ text });
  }

  async function toggleMic() {
    if (recording) return stopRecorder(false);
    stopAudio();
    setSpeaking(false);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunksRef.current = [];
      rec.ondataavailable = (ev) => ev.data.size && chunksRef.current.push(ev.data);
      rec.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        if (rec.discard) return;
        const blob = new Blob(chunksRef.current, { type: rec.mimeType || "audio/webm" });
        if (blob.size > 0) submit({ audio: blob });
      };
      rec.start();
      recorderRef.current = rec;
      setRecording(true);
      setError(null);
    } catch (e) {
      setError("Couldn't use the microphone (" + (e.message || e.name) + "). Type your message instead.");
    }
  }

  function stopRecorder(discard) {
    const rec = recorderRef.current;
    if (rec && rec.state !== "inactive") {
      rec.discard = discard;
      rec.stop();
    }
    recorderRef.current = null;
    setRecording(false);
  }

  const inputsOff = busy || !active;
  const end = END_BANNERS[status];
  return html`
    <main class="page convo">
      <div class="convo-top">
        <button class="link-btn" onClick=${onQuit}>← Back</button>
        <span class="turns">Turn ${Math.min(turn + (active ? 1 : 0), session.max_turns)} / ${session.max_turns}</span>
      </div>

      <section class="stage">
        <div class=${"avatar" + (speaking ? " speaking" : "")} aria-hidden="true">${character.emoji}</div>
        <div class="stage-info">
          <h2>${character.name} <small>${character.title}</small></h2>
          <p class="goal">🎯 ${character.goal}</p>
        </div>
      </section>

      <${MoodMeter} label=${character.meter_label} mood=${mood} delta=${delta} />

      <section class="chat" aria-live="polite">
        ${messages.map((m, i) => html`
          <div key=${i} class=${"bubble-row " + m.role}>
            <div class="bubble">${m.text}</div>
            ${(m.note || (m.techniques && m.techniques.length > 0)) && html`
              <div class="coach">
                ${m.techniques && m.techniques.map((t) => html`<span key=${t} class="chip">${t}</span>`)}
                ${m.note && html`<span class="note">💡 ${m.note}</span>`}
              </div>`}
          </div>`)}
        ${pendingText && html`<div class="bubble-row user"><div class="bubble pending">${pendingText}</div></div>`}
        ${busy && html`<div class="bubble-row character"><div class="bubble thinking">${character.name} is thinking<span class="dots"></span></div></div>`}
        <div ref=${endRef}></div>
      </section>

      ${error && html`
        <div class="banner error" role="alert">
          <span>${error}</span>
          ${lastPayload && html`<button class="btn small" onClick=${() => submit(lastPayload)} disabled=${busy}>Retry</button>`}
        </div>`}

      ${end && html`
        <div class=${"banner end " + end.cls}>
          <strong>${end.text}</strong>
          <button class="btn" onClick=${onFinish}>See my scorecard</button>
        </div>`}

      ${active && html`
        <section class="controls">
          <button class=${"mic" + (recording ? " recording" : "")} onClick=${toggleMic} disabled=${busy}
            aria-label=${recording ? "Stop recording and send" : "Start recording"}>
            ${recording ? "⏹ Stop & send" : "🎤 Tap to talk"}
          </button>
          ${recording && html`<span class="rec-note"><span class="rec-dot"></span> Recording… tap again to send</span>`}
          <form class="typed" onSubmit=${sendText}>
            <input type="text" value=${draft} onInput=${(e) => setDraft(e.target.value)} disabled=${inputsOff || recording}
              placeholder="…or type what you would say" aria-label="Type your message" />
            <button class="btn" type="submit" disabled=${inputsOff || recording || !draft.trim()}>Send</button>
          </form>
          ${turn >= 1 && html`<button class="link-btn" onClick=${onFinish} disabled=${busy}>End & score</button>`}
        </section>`}
    </main>`;
}
