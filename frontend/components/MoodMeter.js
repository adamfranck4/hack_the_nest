// The star of the show: a big bar from 0 (calm) to 100 (meltdown).
import { html, React } from "./html.js";

export function moodColor(mood) {
  // 0 -> green (hue 130), 50 -> yellow (hue 60), 100 -> red (hue 0)
  const hue = Math.round(130 - (Math.max(0, Math.min(100, mood)) / 100) * 130);
  return `hsl(${hue} 80% 45%)`;
}

// `delta` is { value, key } so the floating number re-animates on every turn.
export function MoodMeter({ label, mood, delta }) {
  const color = moodColor(mood);
  // For this game, a negative delta (calmer) is good.
  const good = delta && delta.value < 0;
  return html`
    <div class="meter">
      <div class="meter-head">
        <span class="meter-label">${label}</span>
        <span class="meter-value" style=${{ color }}>${mood}</span>
      </div>
      <div class="meter-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow=${mood} aria-label=${label}>
        <div class="meter-fill" style=${{ width: mood + "%", background: color }}></div>
        <div class="meter-win-zone" title="Get below 15 to win"></div>
        ${delta && delta.value !== 0 && html`
          <span key=${delta.key} class=${"meter-delta " + (good ? "good" : "bad")} style=${{ left: mood + "%" }}>
            ${delta.value > 0 ? "+" : ""}${delta.value}
          </span>`}
      </div>
      <div class="meter-ends"><span>😌 Calm</span><span>Meltdown 🌋</span></div>
    </div>`;
}
