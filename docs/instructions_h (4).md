# MathSlime — Project Instructions

> A simple, ad-free math game for kids (ages 4–10).
> Single HTML file. Canvas-rendered. Firebase-backed.

---

## 1. Concept

Kids solve arithmetic to pop falling slime blobs before they reach the bottom. Correct answer → slime pops with particles. Miss a slime → lose a heart. Lose all 3 hearts → game over.

---

## 2. Game Mechanics

### Core Loop

- Slimes spawn at the top of a canvas (800×520) and fall downward.
- Each slime carries a math problem displayed beneath it.
- The child taps a multiple-choice button to answer.
- Correct → slime pops, particles burst, score increases.
- Wrong → button shakes, combo resets. Slime keeps falling.
- Slime reaches the bottom → lose 1 heart.
- 0 hearts → "Great Try!" screen with score and retry option.

### Answer Input

All levels use **multiple-choice buttons** below the canvas. Choice count scales with level:

| Levels | Choices |
|--------|---------|
| 1–2    | 3       |
| 3–4    | 4       |
| 5–6    | 5       |

**Answer lock:** On tap, all buttons are immediately disabled until the next question renders. Prevents rapid-tap exploits.

### Scoring

- Base: 10 points per correct answer.
- Combo bonus: `(combo - 1) × 5` for consecutive correct answers.
- Level bonus: `level × 2` added per correct answer.
- Float text shows points earned and combo streak (🔥).

### Lives

- 3 hearts displayed in the HUD.
- Game-over screen says "Great Try!" — never punishing language.

---

## 3. Level Design

6 levels. Each introduces one new operation while retaining all prior operations (~50% new, ~50% review).

| Lvl | Name               | New Op | Range   | Speed (s) | Problems | Choices |
|-----|--------------------|--------|---------|-----------|----------|---------|
| 1   | Baby Steps         | `+`    | 1–9     | 12        | 5        | 3       |
| 2   | Take Away          | `−`    | 1–9     | 12        | 8        | 3       |
| 3   | Double Digits      | `+`    | 0–20    | 10        | 8        | 4       |
| 4   | Subtract & Stretch | `−`    | 0–20    | 10        | 10       | 4       |
| 5   | First Times        | `×`    | 0–5     | 8         | 10       | 5       |
| 6   | Fair Shares        | `÷`    | 2–5     | 8         | 10       | 5       |

- Subtraction never produces negative results.
- Division always yields clean integers (`b ∈ 2–5`, `a = b × rand(1,10)`).
- Distractor choices include near-misses (±1, ±2–3, ±4–6).

---

## 4. Rendering

Canvas-based (`requestAnimationFrame` loop). Slimes are drawn programmatically:

- Circular body with shade, shine highlight, dot eyes, and a smile arc.
- Wobble animation via oscillating scale.
- Pop animation: scale up + fade out + 14 scatter particles.
- Starfield background with twinkling dots.
- Level badge ("LEVEL N") shown briefly at level start.

Max 3 active (non-popping) slimes on screen at once.

---

## 5. Authentication

### Firebase Auth — Google Sign-In only

- Sign-in is optional. Guests can play all unlocked levels; progress saves to `localStorage`.
- Signed-in users sync progress to Firestore and appear on the leaderboard.
- User bar shows avatar (circular), first name, and a "Sign Out" link.
- Display name falls back to "Slime Hero" if blank.

### Firestore Data Model

```
users/{uid}
  ├── displayName
  ├── photoURL
  ├── unlockedLevels
  └── levels/level_{n}
        ├── bestScore
        ├── bestTime
        ├── timesCompleted
        └── lastPlayed

leaderboard/{entryId}
  ├── uid, displayName, photoURL
  ├── level, score, time
  ├── createdAt
  └── type: "level_clear"
```

On sign-in, local and cloud `unlockedLevels` are merged (take higher value).

---

## 6. Leaderboard

Three tabs:

| Tab         | Sort             | Scope        |
|-------------|------------------|--------------|
| 🏆 Score    | `score` desc     | All levels   |
| ⚡ Fastest  | `time` asc       | Per level    |
| 🌟 Levels   | `unlockedLevels` desc | All users |

- Top 20 entries per view.
- Current user's row highlighted.
- Medal emojis (🥇🥈🥉) for ranks 1–3.
- "Fastest" tab has a level dropdown filter.
- Accessible without sign-in (read-only); sign-in required to submit.

---

## 7. Audio

All sounds synthesized via **Web Audio API** (no external files):

| Event          | Sound                        |
|----------------|------------------------------|
| Correct answer | Two-tone pop (800 Hz → 1200 Hz) |
| Wrong answer   | Low triangle wave (200 Hz)   |
| Lose heart     | Descending three-tone        |
| Level complete | Ascending three-note chime   |

Mute toggle (🔇/🔊) in HUD. **Default: muted.**

---

## 8. Technical Spec

- **Single file:** `index.html` — all HTML, CSS, JS inline.
- **External deps (CDN):** Firebase SDK (app + auth + firestore), compat build v10.12.2.
- **Fonts:** System stack (`Segoe UI`, `system-ui`, `sans-serif`).
- **Responsive:** `max-width: 800px`, canvas shrinks to 360px height on mobile. Buttons have ≥48px tap targets.
- **`prefers-reduced-motion`:** Disables all animations/transitions.
- **State:** Simple JS variables (`score`, `lives`, `level`, `slimes[]`, etc.). No framework.

---

## 9. What We Don't Build

- ❌ Email/password auth
- ❌ Visible countdown timers (the slime *is* the timer)
- ❌ Ads, analytics, tracking
- ❌ In-app purchases
- ❌ Character customization
- ❌ Public chat or social features
- ❌ Comparison language ("you beat X!")

---

## 10. File Structure

```
mathslime/
├── index.html        ← The entire game
└── instructions_h.md ← This file
```
