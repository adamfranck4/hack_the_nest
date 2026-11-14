// All calls to the backend live here. Add ?mock=1 to the page URL to use fake data.
export const MOCK = new URLSearchParams(location.search).get("mock") === "1";

async function request(path, options) {
  let res;
  try {
    res = await fetch(path, options);
  } catch (e) {
    throw new Error("Can't reach the server. Is the backend running?");
  }
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body && body.detail) {
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
      }
    } catch (e) { /* keep default message */ }
    throw new Error(detail);
  }
  return res.json();
}

const realApi = {
  async getCharacters() {
    return (await request("/api/characters")).characters;
  },
  createSession(characterId) {
    return request("/api/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ character_id: characterId }),
    });
  },
  // payload is { text } or { audio: Blob }
  sendTurn(sessionId, payload) {
    const form = new FormData();
    if (payload.text) form.append("text", payload.text);
    else if (payload.audio) form.append("audio", payload.audio, "speech." + extFor(payload.audio.type));
    return request(`/api/sessions/${sessionId}/turns`, { method: "POST", body: form });
  },
  getScorecard(sessionId) {
    return request(`/api/sessions/${sessionId}/scorecard`);
  },
};

function extFor(type) {
  if (!type) return "webm";
  if (type.includes("ogg")) return "ogg";
  if (type.includes("mp4")) return "mp4";
  return "webm";
}

// ---------------------------------------------------------------- MOCK MODE
// Contract-shaped fake data so the UI can be built without the backend.
const MOCK_CHARACTERS = [
  { id: "toddler", name: "Milo", emoji: "🧸", title: "Toddler", scenario: "Milo's ice cream just fell on the floor and he is about to lose it.", goal: "Calm Milo down before the meltdown.", meter_label: "Meltdown meter", start_mood: 70 },
  { id: "angry_caller", name: "Dana", emoji: "📞", title: "Angry caller", scenario: "Dana has been on hold for 45 minutes and her order never arrived.", goal: "De-escalate Dana and promise a real fix.", meter_label: "Anger meter", start_mood: 80 },
  { id: "upset_friend", name: "Sam", emoji: "💔", title: "Upset friend", scenario: "Sam's best friend forgot their birthday and Sam is hurt.", goal: "Help Sam feel heard.", meter_label: "Hurt meter", start_mood: 65 },
];
const mockSessions = {};
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const mockApi = {
  async getCharacters() {
    await wait(300);
    return MOCK_CHARACTERS;
  },
  async createSession(characterId) {
    await wait(300);
    const character = MOCK_CHARACTERS.find((c) => c.id === characterId);
    if (!character) throw new Error("Unknown character");
    const id = Math.random().toString(16).slice(2);
    mockSessions[id] = { character, mood: character.start_mood, turn: 0, status: "active", transcript: [] };
    return {
      session_id: id, character, mood: character.start_mood, status: "active", turn: 0, max_turns: 8,
      opening: { text: `*sniffle* ${character.name} here... everything is going wrong today!`, audio_b64: null, suggestions: ["I can tell this is really upsetting. Tell me what happened.", "I'm sorry that happened, and I want to help fix it."] },
    };
  },
  async sendTurn(sessionId, payload) {
    await wait(900);
    const s = mockSessions[sessionId];
    if (!s) throw new Error("Session not found");
    if (s.status !== "active") throw new Error("Session is not active");
    const text = payload.text || "I hear you, that sounds really frustrating. I'm sorry.";
    if (text.toLowerCase().includes("fail")) throw new Error("Mock failure: Gemini did not respond"); // try typing "fail"
    const calm = /sorry|understand|hear|feel|help|calm/i.test(text);
    const rude = /calm down|whatever|stop|shut/i.test(text);
    const delta = rude ? 18 : calm ? -(8 + Math.floor(Math.random() * 12)) : 5;
    s.mood = Math.max(0, Math.min(100, s.mood + delta));
    s.turn += 1;
    s.status = s.mood <= 15 ? "won" : s.mood >= 100 ? "lost" : s.turn >= 8 ? "timeout" : "active";
    const reply = delta < 0 ? "Okay... that makes me feel a bit better." : "You're not listening to me!";
    s.transcript.push({ role: "user", text }, { role: "character", text: reply });
    return {
      turn: s.turn, user_text: text, reply_text: reply, reply_audio_b64: null, mood: s.mood, mood_delta: delta,
      techniques: calm ? ["Validation", "Empathy"] : [],
      note: calm ? "Nice: naming their feeling lowers the temperature." : "Try acknowledging how they feel first.",
      suggestions: s.status === "active" ? (calm
        ? ["What would help you feel better right now?", "Thanks for telling me, I'm here and I'm listening."]
        : ["I hear you, that sounds really frustrating.", "I'm sorry, let me understand what went wrong."]) : [],
      status: s.status, max_turns: 8,
    };
  },
  async getScorecard(sessionId) {
    await wait(700);
    const s = mockSessions[sessionId];
    if (!s || s.turn === 0) throw new Error("Play at least one turn first");
    const score = Math.max(5, Math.min(98, 100 - s.mood));
    return {
      outcome: s.status === "active" ? "timeout" : s.status, final_mood: s.mood, score,
      summary: "You stayed steady and used empathy well, but sometimes jumped to fixing too early.",
      techniques_used: [{ name: "Validation", count: 3 }, { name: "Empathy", count: 2 }],
      best_line: { text: "I hear you, that sounds really frustrating.", why: "It names the feeling without arguing." },
      worst_line: { text: "Just calm down.", why: "Telling someone to calm down usually escalates them.", better: "I can see this is really upsetting. Let's sort it out together." },
      transcript: s.transcript,
    };
  },
};

export const api = MOCK ? mockApi : realApi;
