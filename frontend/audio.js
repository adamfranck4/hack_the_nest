// Tiny audio helper: plays the character's mp3 (base64) and lets us stop it.
let current = null;

export function stopAudio() {
  if (current) {
    current.pause();
    current = null;
  }
}

// Returns a promise that resolves when playback ends (or immediately if it fails).
export function playBase64(b64) {
  stopAudio();
  if (!b64) return Promise.resolve();
  return new Promise((resolve) => {
    const audio = new Audio("data:audio/mpeg;base64," + b64);
    current = audio;
    const done = () => {
      if (current === audio) current = null;
      resolve();
    };
    audio.addEventListener("ended", done);
    audio.addEventListener("error", done);
    // Autoplay may be blocked by the browser: that's fine, text is still shown.
    audio.play().catch(done);
  });
}
