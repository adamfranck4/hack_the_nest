"""Real-call smoke test. Run from repo root:
    PYTHONPATH=backend backend/.venv/Scripts/python backend/scripts/smoke_integrations.py [out_dir]
Writes the generated mp3 to out_dir (default: system temp dir), never into the repo.
"""
import sys
import tempfile
from pathlib import Path

from app.characters import get_character
from app.integrations import elevenlabs, gemini

out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.gettempdir())
c = get_character("toddler")
hist = [{"role": "character", "text": c.opening_line}]

good = "Oh Milo, you sound really upset. Do you want to wear the red shoes or the blue shoes?"
bad = "Put your shoes on RIGHT NOW or no dessert for a week! Because I said so!"
for label, line in (("good", good), ("bad", bad)):
    r = gemini.character_reply(c, hist, line, c.start_mood)
    print(f"[{label}] delta={r['mood_delta']} techniques={r['techniques']}\n  reply={r['reply']}\n  note={r['note']}")

hist2 = hist + [
    {"role": "user", "text": good},
    {"role": "character", "text": "Me want... blue. Sniff."},
    {"role": "user", "text": "Great choice! When shoes are on, then we get to go see the cake."},
    {"role": "character", "text": "Okay. Cake! Shoes on."},
]
print("score:", gemini.score_session(c, hist2, 20, "won"))

mp3 = elevenlabs.text_to_speech("No shoes! Me no want shoes! Waaah!", c.voice_id)
path = out_dir / "smoke_tts.mp3"
path.write_bytes(mp3)
print("tts bytes:", len(mp3), "->", path)
print("stt:", repr(elevenlabs.speech_to_text(mp3, "smoke_tts.mp3", "audio/mpeg")))
