# Talk It Out: demo script

Judging is Sunday, Nov 15 at 1:15 PM (table setup 1:00 PM). See
[event schedule](HACKATHON_CONTEXT.md#critical-deadlines). Lines and timings below
are a plan written before the build finished.

<!-- VERIFY after build: rehearse the whole script against the running app and adjust lines, meter numbers and timings -->

## Before judges arrive (1:00 PM setup)

- [ ] Laptop charged, on power, volume up, external speaker if available.
- [ ] Server running using the [platform-appropriate quick start](../README.md#quick-start).
- [ ] Open <http://localhost:8000>. Check `http://localhost:8000/api/health` shows both keys configured.
- [ ] Mic permission already granted in the browser. Do one throwaway round to confirm audio in and out.
- [ ] Pre-recorded backup video open in a second tab or on a phone (see fallbacks).
- [ ] Teammates know who talks: one presenter, one drives the laptop.

## 3-minute table demo

| Time | What you do | What you say |
|---|---|---|
| 0:00-0:20 | Hook. Landing screen with the six characters. | "Pilots practice in simulators. Why do we practice hard conversations for the first time on real people? Talk It Out is a conversation gym: you talk to an AI character by voice and try to calm them down." |
| 0:20-1:10 | Pick Milo (toddler). Let him speak his opening line. Play the calming lines below, one per turn, pointing at the Meltdown meter as it drops. | "Milo is refusing to put his shoes on. Watch the meter. Gemini plays him and moves it based on what I say." |
| 1:10-1:35 | Restart Milo. Say the bad line. Meter spikes. | "Now what most of us do under stress." Then: "It jumped. The app knows the difference between a technique and a reaction." |
| 1:35-2:05 | Finish a round or choose End & score (labeled Ended early), then open the scorecard. | "At the end you get a scorecard: techniques used, your best line, your worst line, and a better thing you could have said." |
| 2:05-2:35 | Switch to Dana, the angry caller. One or two turns only, show the Anger meter. Mention the rest. | "Same engine, real-world use: a customer whose order arrived broken for the third time. This is customer-service de-escalation practice with no real customer at risk. There are six scenarios in all: a teen caught on their phone at 1 AM, a roommate fed up with dishes, a coworker who took credit for your idea, and an upset friend." |
| 2:35-3:00 | Close. | "Built by three people from Grand Valley, mostly first hackathon. Gemini plays and scores the character, ElevenLabs voices it and transcribes you. Next: dementia-care and de-escalation scenarios, custom characters, difficulty levels, and progress tracking, for new parents, babysitters, support teams and nursing students. Thank you." |

### Lines to say to Milo (toddler)

Say them in a calm, low voice. Expect the meter to fall a bit each turn.

1. "You really don't want to put your shoes on. You sound mad." (names the feeling)
2. "I'm sorry I rushed you this morning. That wasn't fair." (sincere apology)
3. "Do you want to wear the red shoes or the blue shoes?" (offers a choice)
4. "Do you want to put them on yourself, or should I help?" (choice, autonomy)
5. "Thank you for helping. You are doing a great job." (praise for cooperation)

### Bad line (for laughs)

"Milo, put your shoes on RIGHT NOW or no TV for a week!" (threat, raised voice)

Expected: the meter spikes. If it does not move much, say a second one:
"Stop crying, you're being ridiculous."

<!-- VERIFY after build: which lines Gemini actually rewards or punishes; replace with lines that reliably work. Confirm technique names shown in the UI match (naming feelings, offering choices, sincere apology, ownership). -->

### Angry caller quick lines

1. "I'm so sorry. Three broken orders is not acceptable, and that's on us."
2. "I can send a replacement today and refund the shipping. Which would you prefer?"

Dana's opening line in the app: "This is the THIRD time my order showed up smashed!
What kind of company are you running?" Tip: the "Try saying" chips under the input
show suggested lines; keep the Hints toggle on for a smoother demo.

### Alternate round: coworker Casey (for a professional-minded judge)

Casey presented your project idea as their own in today's meeting. Meter:
Defensiveness. Opening line: "Look, if this is about the meeting, I really don't have
time for drama right now." Two calm lines:

1. "Thanks for taking a minute. In the meeting, the idea you presented was one I shared with you last week."
2. "I would like to assume this was a mix-up. Can we correct the record together at the next standup?"

Say: "Same engine, workplace stakes: you practice asking for credit without wrecking the relationship."

## Fallbacks

| Problem | Do this |
|---|---|
| Room is noisy or mic is not picked up | Use the typed input box. Typed text takes priority over audio and works the same. Say "we have a typed mode for noisy rooms." |
| Browser blocks the mic | Click the lock icon in the address bar, allow microphone, reload. If it still fails, type. |
| No voice from the character (ElevenLabs down or key limit) | The reply text still appears; read it aloud yourself or just continue. Voice failing does not stop the game. |
| Gemini error or slow reply | Retry once. If it fails again, switch to the backup video immediately. |
| Wi-Fi down | Switch to the backup video. The app needs internet for both APIs. |
| Server crashed | Restart the server using the quick-start instructions. Sessions are in memory, so start a new round. |
| Public site voice limit reached | The live site has a daily voice budget. When it is used up the app tells you to type your reply; typed input remains available. Use the local server for a voiced demo. |
| Anything else | Play the pre-recorded screen video and narrate over it. Do not debug at the table. |

Record the backup video before the final deadline: one clean full run, with audio,
including the scorecard. Keep it on the laptop desktop and a phone.

## 2-minute demo video shot list (for Devpost)

Record the screen plus system audio and a voiceover. Keep it under 2:00.

| Time | Shot | Voiceover |
|---|---|---|
| 0:00-0:10 | Title card "Talk It Out". | "Pilots practice in simulators. Why do we practice hard conversations for the first time on real people?" |
| 0:10-0:20 | Character select screen, hover over the six cards. | "Talk It Out is a conversation gym. Pick a character, talk to them by voice, and try to calm them down." |
| 0:20-0:55 | Milo round, mic visible, meter dropping as the calming lines are spoken. | "Gemini plays a toddler refusing his shoes. ElevenLabs gives him a voice and transcribes me. The meltdown meter moves based on the techniques I use: naming feelings, offering choices, apologizing sincerely." |
| 0:55-1:10 | Bad line, meter spikes. | "Threaten him and the meter jumps." |
| 1:10-1:30 | Scorecard: techniques, best line, worst line with better alternative. | "At the end, a scorecard grades my techniques and suggests a better line." |
| 1:30-1:45 | Dana the angry caller and a quick glimpse of the other characters, a few seconds each. | "Same engine, other situations: an angry customer, a hurt friend, a teenager, a roommate, a coworker." |
| 1:45-2:00 | Closing card with team and "What's next" list. | "Built by three first-time-hackers from Grand Valley State. Next: more scenarios, custom characters, difficulty levels, and progress history." |

Tips: record at 1080p, close other tabs, mute notifications, rehearse once before
recording, and keep the first two lines of dialogue short so the video is not cut off.
