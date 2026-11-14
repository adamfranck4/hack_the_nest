import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const catalog = JSON.parse(await readFile(new URL("../characters.json", import.meta.url), "utf8"));
globalThis.location = { search: "?mock=1" };
globalThis.fetch = async (url) => new Response(await readFile(url), {
  headers: { "content-type": "application/json" },
});
const { api } = await import("../api.js");

test("mock catalog and openings match the generated live catalog", async () => {
  assert.deepEqual(await api.getCharacters(), catalog.characters.map((entry) => entry.character));
  assert.equal(catalog.characters.length, 6);
  for (const entry of catalog.characters) {
    const session = await api.createSession(entry.character.id);
    assert.deepEqual(session.character, entry.character);
    assert.deepEqual(session.opening, entry.opening);
    assert.equal(session.mood, entry.character.start_mood);
  }
});

test("ending after one turn reports ended and keeps the opening in the transcript", async () => {
  const session = await api.createSession("toddler");
  await api.sendTurn(session.session_id, { text: "I hear you and understand." });
  const card = await api.getScorecard(session.session_id);
  assert.equal(card.outcome, "ended");
  assert.deepEqual(card.transcript[0], { role: "character", text: session.opening.text });
});

test("a terminal mock round keeps its game outcome", async () => {
  const session = await api.createSession("toddler");
  let turn;
  do {
    turn = await api.sendTurn(session.session_id, { text: "Whatever, shut up." });
  } while (turn.status === "active");
  assert.equal(turn.status, "lost");
  assert.equal((await api.getScorecard(session.session_id)).outcome, "lost");
});

test("exhausted-voice demo still accepts typed messages", async () => {
  globalThis.location.search = "?mock=1&novoice=1";
  const { api: muted } = await import("../api.js?novoice-test");
  const session = await muted.createSession("teen");
  assert.equal(session.voice_available, false);
  await assert.rejects(muted.sendTurn(session.session_id, { audio: new Blob(["audio"]) }),
    (error) => error.status === 429);
  assert.equal((await muted.sendTurn(session.session_id, { text: "I hear you." })).turn, 1);
});
