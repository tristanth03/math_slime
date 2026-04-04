# MathSlime — Project Instructions

> A dead-simple, ad-free, lightweight math game for kids (ages 4–10).
> Single HTML file. No frameworks. No build step. Pure fun.

---

## 1. Concept

Kids solve mental arithmetic problems to defeat approaching slime blobs.
Correct answer → slime pops. Wrong answer → slime gets closer.
Three slimes reach you → game over.

That's the entire game. No shop, no account, no upsell.

---

## 2. Why This Exists

The inspiration (MathHero on Google Play) is good but bloated: in-app purchases, excessive unlockables, heavy download, and ads. This project strips everything back to the *one thing that matters*: **a child practicing math while having fun**.

**Design pillars:**

| Pillar | Rule |
|---|---|
| **Simple** | A 4-year-old should figure it out in 10 seconds without adult help. |
| **Lightweight** | Single `.html` file, < 200 KB total, runs offline. |
| **Free** | No ads, no IAP, no tracking, no analytics. Period. |
| **Honest** | No dark patterns, no "watch ad to continue", no fake difficulty walls. |

---

## 3. Game Mechanics

### 3.1 Core Loop

```
┌──────────────────────────────────────────┐
│  Slime appears on the right              │
│  ↓                                       │
│  Math problem appears above the slime    │
│  ↓                                       │
│  Child taps/types the answer             │
│  ↓                                       │
│  Correct → slime pops (confetti burst)   │
│  Wrong   → slime hops closer one step    │
│  ↓                                       │
│  Next slime spawns                       │
│  ↓                                       │
│  3 slimes reach the left edge → Game Over│
└──────────────────────────────────────────┘
```

### 3.2 Answer Input

- **Ages 4–6 (Levels 1–3):** Show 3 multiple-choice bubbles. One correct, two distractors.
- **Ages 7+ (Levels 4+):** Show a number pad (0–9, backspace, submit). No keyboard needed — mobile-first.

### 3.3 Slime Behavior

- Slimes are simple CSS circles with two dot-eyes and a wobbly idle animation.
- They spawn on the right edge and drift left at a pace determined by the level timer.
- They don't "attack" — they just arrive. The threat is their presence, not violence.
- When popped: scale-up + opacity fade + 5–8 small colored circles scatter outward (confetti).

### 3.4 Lives

- The child has **3 hearts** (displayed top-left).
- A slime reaching the left edge costs 1 heart.
- 0 hearts → friendly "Game Over" screen with score + "Play Again" button.
- **No punishment language.** Never say "You lost!" — say "Great try! You solved X problems!"

---

## 4. Level Design

Levels are the backbone. Each level is a *math skill*, not a gimmick.

### Level Table

| Level | Name | Operations | Number Range | Input | Slime Speed | Problems to Clear |
|-------|------|-----------|--------------|-------|-------------|-------------------|
| 1 | "Baby Steps" | `a + b` | 1–5 | 3 choices | Very slow (12s) | 5 |
| 2 | "Getting Warmer" | `a + b` | 1–10 | 3 choices | Very slow (12s) | 8 |
| 3 | "Take Away" | `a − b` | results ≥ 0, within 10 | 3 choices | Slow (10s) | 8 |
| 4 | "Mix It Up" | `a + b`, `a − b` | within 10 | Numpad | Slow (10s) | 10 |
| 5 | "Double Digits" | `a + b` | 1–20 | Numpad | Medium (8s) | 10 |
| 6 | "Subtract & Conquer" | `a − b` | within 20, results ≥ 0 | Numpad | Medium (8s) | 10 |
| 7 | "Times Tables ×2 ×5 ×10" | `a × b` | a ∈ {2,5,10}, b ∈ 1–10 | Numpad | Medium (8s) | 12 |
| 8 | "Times Tables ×3 ×4" | `a × b` | a ∈ {3,4}, b ∈ 1–10 | Numpad | Medium-fast (7s) | 12 |
| 9 | "All Times Tables" | `a × b` | a,b ∈ 1–10 | Numpad | Medium-fast (7s) | 15 |
| 10 | "Divide & Rule" | `a ÷ b` | clean division only, within tables | Numpad | Medium-fast (7s) | 12 |
| 11 | "The Big Mix" | `+`, `−`, `×`, `÷` | mixed, age-appropriate | Numpad | Fast (6s) | 15 |
| 12 | "Speed Demon" | `+`, `−`, `×`, `÷` | same as 11 | Numpad | Very fast (5s) | 20 |

### Level Progression Rules

- Completing a level unlocks the next. Progress is saved to `localStorage`.
- A child can **replay any unlocked level** at any time.
- There is **no star rating**. You either clear it or you don't. No anxiety.
- After Level 12, show a simple "You finished all levels! 🎉" screen. Encourage replay for speed.

### Distractor Generation (Multiple Choice)

For choice-based levels, generate wrong answers that are *plausible*:
- One distractor = correct answer ± 1
- One distractor = correct answer ± 2 or ± 3
- Never show negative numbers as choices.
- Shuffle the position of the correct answer.

---

## 5. Visual Design

### 5.1 Aesthetic: "Soft Doodle"

Think: a child's coloring book brought to life with gentle motion. Rounded everything. Hand-drawn feel.

### 5.2 Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Background | Warm cream | `#FFF8F0` |
| Text / UI | Soft charcoal | `#3A3A3A` |
| Slime (default) | Lime green | `#A8E06C` |
| Slime (level 4–7) | Coral pink | `#FF8FA3` |
| Slime (level 8–12) | Lavender | `#B49FDC` |
| Correct flash | Mint | `#6EDBA2` |
| Wrong flash | Soft red | `#FF6B6B` |
| Hearts | Warm red | `#E8453C` |
| Buttons | Sky blue | `#64B5F6` |

### 5.3 Typography

- **Primary font:** `"Patrick Hand"` from Google Fonts — handwritten, childlike, legible.
- **Numbers in problems:** `"Fredoka One"` — chunky, rounded, easy to read at large sizes.
- Fallback: `"Comic Sans MS", cursive, sans-serif` (yes, unironically — kids love it).

### 5.4 Slime Design (Pure CSS)

```
       ╭───────╮
      ╱  ●   ●  ╲      ← two dot-eyes, slightly off-center
     │           │
     ╰───┬─┬─┬──╯      ← wavy bottom edge (border-radius tricks)
         ╵ ╵ ╵         ← 3 small drip circles underneath
```

- Implemented as a single `div` with `border-radius: 50% 50% 45% 55% / 60% 60% 40% 40%`.
- Eyes are `::before` and `::after` pseudo-elements.
- Idle animation: gentle vertical bounce (`translateY` oscillation, 1.5s ease-in-out infinite).
- When approaching: add a slight horizontal wobble.

### 5.5 Layout

```
┌──────────────────────────────────┐
│  ♥ ♥ ♥          Level 3    ⚙    │  ← Top bar: hearts, level name, settings
│                                  │
│                                  │
│         3 + 4 = ?                │  ← Problem floats above the slime
│            🟢                    │  ← Slime (moves left over time)
│                                  │
│                                  │
│  ┌─────┐ ┌─────┐ ┌─────┐        │  ← Answer choices (or numpad)
│  │  5  │ │  7  │ │  6  │        │
│  └─────┘ └─────┘ └─────┘        │
└──────────────────────────────────┘
```

The game area is a single centered container, max-width 500px, so it looks good on phones and doesn't stretch absurdly on desktops.

---

## 6. Screens

### 6.1 Title Screen

- Game title "MathSlime" in `Fredoka One`, big and bouncy.
- A single idle slime with blinking eyes.
- **"Play"** button (large, sky blue, rounded).
- Below: a row of level circles (1–12). Locked ones are greyed out with a tiny lock icon.

### 6.2 Level Select (optional — could also be inline on title)

- Grid of 12 circles.
- Unlocked = colored + tappable.
- Locked = grey + lock icon.
- Current highest = pulsing glow.

### 6.3 Gameplay Screen

- See §5.5 layout.
- Problem text is large (at least 48px).
- Slime drifts from right to left.
- When a slime is popped, the next one spawns after a 1-second pause.

### 6.4 Level Complete Screen

- "Level Clear! 🎉"
- "You solved X out of Y!" (always positive framing)
- "Next Level →" button
- "Back to Levels" link

### 6.5 Game Over Screen

- "Great try!"
- "You solved X problems this round!"
- "Try Again" button (restarts same level)
- "Back to Levels" link

---

## 7. Audio (Optional / Progressive Enhancement)

If we add audio, keep it **tiny** and optional:

| Event | Sound | Implementation |
|-------|-------|----------------|
| Correct answer | Short cheerful "pop" | Web Audio API — synthesized, not a file |
| Wrong answer | Soft low "bonk" | Web Audio API — synthesized |
| Slime reaches edge | Quick descending tone | Web Audio API — synthesized |
| Level complete | 3-note ascending chime | Web Audio API — synthesized |

**All audio must be synthesized via Web Audio API** — no external sound files. This keeps the total size under 200 KB.

A mute toggle (🔊 / 🔇) sits in the top-right corner. Default state: **muted**. Kids in classrooms shouldn't blast sounds unexpectedly.

---

## 8. Technical Spec

### 8.1 Stack

- **One file:** `index.html` containing all HTML, CSS, and JS.
- **Zero dependencies** besides Google Fonts (loaded via `<link>`).
- **No build step.** Open the file in a browser, done.
- **Offline-capable:** After first load, works without internet (fonts fall back gracefully).

### 8.2 State Management

All state lives in a simple JS object:

```js
const state = {
  currentLevel: 1,
  unlockedLevels: 1,
  hearts: 3,
  score: 0,
  problemsSolved: 0,
  currentProblem: null,
  slimePosition: 100, // percentage from left
  screen: 'title'     // 'title' | 'play' | 'levelComplete' | 'gameOver'
};
```

Persist `unlockedLevels` to `localStorage`. That's it. Nothing else needs saving.

### 8.3 Problem Generator

```js
function generateProblem(level) {
  // Returns { text: "3 + 4", answer: 7, choices: [5, 7, 6] | null }
  // choices is null for numpad levels (4+)
  // Distractor logic per §4 rules
}
```

- Division problems must always have clean integer results.
- Subtraction must never produce negative results.
- No duplicate choices.

### 8.4 Slime Timer

Each slime has a countdown. Use `requestAnimationFrame` for smooth movement, not `setInterval`.

```js
// Slime moves from 100% (right) to 0% (left) over `levelSpeed` seconds.
// Position = 100 - (elapsed / levelSpeed) * 100
```

When position ≤ 0: slime reached the edge, remove 1 heart, spawn next slime.

### 8.5 Animations (CSS)

```css
@keyframes slime-idle {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-8px); }
}

@keyframes slime-pop {
  0%   { transform: scale(1); opacity: 1; }
  50%  { transform: scale(1.4); opacity: 0.6; }
  100% { transform: scale(0); opacity: 0; }
}

@keyframes confetti-burst {
  0%   { transform: translate(0, 0) scale(1); opacity: 1; }
  100% { transform: translate(var(--dx), var(--dy)) scale(0); opacity: 0; }
}
```

### 8.6 Responsive Design

- `max-width: 500px; margin: 0 auto;` for the game container.
- All sizes in `rem` or `vw` units.
- Numpad buttons: minimum `48px × 48px` tap targets (WCAG compliant).
- Test at 320px width (small phones) and 1024px (tablets).

---

## 9. Accessibility

- All buttons have clear text labels (no icon-only buttons).
- Color is never the *only* indicator of state (hearts use both color + icon).
- Tap targets ≥ 48px.
- High contrast between text and background (cream + charcoal = ~10:1 ratio).
- `prefers-reduced-motion`: disable slime bounce and confetti if set.
- Screen reader: problem text is in an `aria-live="polite"` region.

---

## 10. What We DON'T Build

This is as important as what we build:

- ❌ User accounts or login
- ❌ Leaderboards (comparison kills intrinsic motivation in young kids)
- ❌ Star ratings per level (anxiety-inducing)
- ❌ Timers visible to the child (the slime *is* the timer — no numbers ticking down)
- ❌ Ads, analytics, tracking
- ❌ In-app purchases or "premium" tiers
- ❌ Character customization (scope creep — ship v1 first)
- ❌ Backend / server of any kind
- ❌ Multiple game modes in v1

---

## 11. File Structure

```
mathslime/
├── index.html      ← The entire game. Ship this.
└── instructions_h.md  ← This file.
```

That's it. That's the repo.

---

## 12. Development Phases

### Phase 1 — Core (MVP)

1. Title screen with level select.
2. Problem generator for all 12 levels.
3. Slime movement + pop mechanic.
4. Multiple choice input (levels 1–3).
5. Numpad input (levels 4–12).
6. Hearts / game over / level complete flow.
7. `localStorage` progress save.

### Phase 2 — Polish

8. CSS slime design with idle animation.
9. Pop + confetti animations.
10. Web Audio API sounds (synthesized).
11. `prefers-reduced-motion` support.
12. Responsive testing on real devices.

### Phase 3 — Future (only if v1 ships and gets feedback)

13. Practice / endless mode.
14. Parent dashboard (local-only stats).
15. Additional level packs (fractions, etc.).
16. PWA manifest for "Add to Home Screen".

---

## 13. Success Criteria

The game is done when:

- [ ] A 5-year-old can start playing within 10 seconds of opening the page.
- [ ] A 9-year-old finds Level 12 challenging but fair.
- [ ] The HTML file is under 200 KB.
- [ ] It runs smoothly on a 2019 budget Android phone.
- [ ] No adult needs to explain how to play.
- [ ] It makes a kid smile.

---

*Built with zero dependencies and maximum care.*
