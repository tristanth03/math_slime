# MathSlime — Project Instructions

> A dead-simple, ad-free, lightweight math game for kids (ages 4–10).
> Single HTML file. No frameworks. No build step. Pure fun.

---

## 1. Concept

Kids solve mental arithmetic problems to defeat approaching slime blobs.
Correct answer → slime pops. Wrong answer → slime gets closer.
Three slimes reach you → game over.

That's the entire game. No shop, no upsell.

---

## 2. Why This Exists

The inspiration (MathHero on Google Play) is good but bloated: in-app purchases, excessive unlockables, heavy download, and ads. This project strips everything back to the *one thing that matters*: **a child practicing math while having fun**.

**Design pillars:**

| Pillar | Rule |
|---|---|
| **Simple** | A 4-year-old should figure it out in 10 seconds without adult help. |
| **Lightweight** | Single `.html` file, runs offline after first load. |
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

- **Ages 4–6 (Levels 1–2):** Show 3 multiple-choice bubbles. One correct, two distractors.
- **Ages 6+ (Levels 3+):** Show a number pad (0–9, backspace, submit). No keyboard needed — mobile-first.

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

## 4. Authentication

### 4.1 Provider: Firebase Authentication (Google Sign-In)

MathSlime uses **Firebase Authentication** with the **Google Sign-In** provider. This is the only auth method — simple, familiar, and most kids/parents already have a Google account.

### 4.2 Firebase Setup

Include the Firebase SDK via CDN (no npm/build step):

```html
<script src="https://www.gstatic.com/firebasejs/10.x.x/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.x.x/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.x.x/firebase-firestore-compat.js"></script>
```

Firebase config object (replace with real project values):

```js
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "mathslime.firebaseapp.com",
  projectId: "mathslime",
  storageBucket: "mathslime.appspot.com",
  messagingSenderId: "000000000000",
  appId: "YOUR_APP_ID"
};
firebase.initializeApp(firebaseConfig);
```

### 4.3 Auth Flow

```
┌─────────────────────────────────────────────────┐
│  App loads → check firebase.auth().currentUser   │
│  ↓                                               │
│  User signed in?                                 │
│   YES → show title screen (with avatar + name)   │
│   NO  → show title screen with "Sign In" button  │
│         + "Play as Guest" option                 │
│  ↓                                               │
│  Sign In tapped → firebase Google popup/redirect │
│  ↓                                               │
│  On success → store uid, displayName, photoURL   │
│  ↓                                               │
│  Game proceeds normally                          │
└─────────────────────────────────────────────────┘
```

### 4.4 Auth Rules

| Rule | Detail |
|---|---|
| **Guest play is always available** | A child should never be *blocked* from playing. Sign-in is optional. |
| **Guest scores are local only** | Guests use `localStorage` for progress. Scores do not appear on the leaderboard. |
| **Signed-in progress syncs to Firestore** | `unlockedLevels`, best scores per level, and leaderboard entries are persisted in the cloud. |
| **No email/password** | Only Google Sign-In. Keeps it simple and avoids storing sensitive credentials. |
| **Sign-out** | A small "Sign Out" link in the settings/gear menu. Reverts to guest mode. |
| **Display name** | Use `user.displayName` (first name only if possible) on the leaderboard. If blank, fall back to "Slime Hero". |
| **Avatar** | Use `user.photoURL` as a small circular avatar next to the player's name in the HUD and leaderboard. Fall back to a default slime icon. |

### 4.5 Firestore Data Model

```
users/{uid}
  ├── displayName: string
  ├── photoURL: string
  ├── unlockedLevels: number
  └── levels/
        ├── level_1/
        │     ├── bestScore: number
        │     ├── bestTime: number (seconds, fastest completion)
        │     ├── timesCompleted: number
        │     └── lastPlayed: timestamp
        ├── level_2/ ...
        └── ...

leaderboard/{entryId}
  ├── uid: string
  ├── displayName: string
  ├── photoURL: string
  ├── level: number
  ├── score: number
  ├── time: number (seconds)
  ├── createdAt: timestamp
  └── type: "level_clear" | "endless" (future-proofing)
```

### 4.6 Firestore Security Rules (Summary)

- A user may only write to their own `users/{uid}` document.
- Leaderboard entries may only be created (not updated/deleted) and `uid` must match the authenticated user.
- All leaderboard data is publicly readable.
- No anonymous writes to any collection.

---

## 5. Level Design

Levels are the backbone. Each level introduces a new operation while **retaining all previously introduced operations**. This means problems from earlier levels can (and will) appear in later levels to keep skills fresh.

### 5.1 Operation Accumulation Rule

> **From Level 3 onward, every level's problem pool includes all operations from all previous levels *plus* the new operation for that level.**

For example, Level 5 (multiplication) will generate problems using `+`, `−`, and `×` — not just `×`. The *ratio* favors the new operation (~50% new, ~50% review) so the child gets practice on the new skill while reinforcing earlier ones.

### 5.2 Level Table

| Level | Name | New Operation | Number Range | Accumulated Ops | Input | Slime Speed | Problems to Clear |
|-------|------|--------------|--------------|-----------------|-------|-------------|-------------------|
| 1 | "Baby Steps" | `a + b` | 1–9 (single digit) | `+` | 3 choices | Very slow (12 s) | 5 |
| 2 | "Take Away" | `a − b` | 1–9, result ≥ 0 | `+`, `−` | 3 choices | Very slow (12 s) | 8 |
| 3 | "Double Digits" | `a + b` (range expands) | 0–20 | `+`, `−` | Numpad | Slow (10 s) | 8 |
| 4 | "Subtract & Stretch" | `a − b` (range expands) | 0–20, result ≥ 0 | `+`, `−` | Numpad | Slow (10 s) | 10 |
| 5 | "First Times" | `a × b` | a, b ∈ 0–5 | `+`, `−`, `×` | Numpad | Medium (8 s) | 10 |
| 6 | "Fair Shares" | `a ÷ b` | clean division only (e.g. 4÷2, 12÷3, 25÷5) | `+`, `−`, `×`, `÷` | Numpad | Medium (8 s) | 10 |
| 7 | *TBD — see §5.4* | *TBD* | *TBD* | all prior + new | Numpad | Medium-fast (7 s) | 12 |
| 8 | *TBD* | *TBD* | *TBD* | all prior + new | Numpad | Medium-fast (7 s) | 12 |
| 9 | *TBD* | *TBD* | *TBD* | all prior + new | Numpad | Fast (6 s) | 15 |
| 10 | *TBD* | *TBD* | *TBD* | all prior + new | Numpad | Fast (6 s) | 15 |
| 11 | *TBD* | *TBD* | *TBD* | all prior + new | Numpad | Very fast (5 s) | 18 |
| 12 | "Speed Demon" | all ops, full range | mixed, age-appropriate | all | Numpad | Very fast (5 s) | 20 |

### 5.3 Detailed Operation Specs (Levels 1–6)

**Level 1 — Addition (single digit)**
- `a + b` where `a, b ∈ {1, 2, …, 9}`
- Answers range from 2 to 18
- Input: 3 multiple-choice bubbles

**Level 2 — Subtraction (single digit)**
- New: `a − b` where `a ≥ b`, both single digit, result ≥ 0
- Pool: ~50% subtraction, ~50% addition (Level 1 style)
- Input: 3 multiple-choice bubbles

**Level 3 — Addition (0–20)**
- New: `a + b` where `a, b ∈ {0, 1, …, 20}`, answer ≤ 40
- Pool: ~50% double-digit addition, ~50% review (L1–L2 style problems)
- Input: Numpad (first numpad level)

**Level 4 — Subtraction (0–20)**
- New: `a − b` where `a, b ∈ {0, 1, …, 20}`, `a ≥ b`, result ≥ 0
- Pool: ~50% double-digit subtraction, ~50% review (L1–L3 style)
- Input: Numpad

**Level 5 — Multiplication (simple)**
- New: `a × b` where `a, b ∈ {0, 1, 2, 3, 4, 5}`
- Answers range from 0 to 25
- Pool: ~50% multiplication, ~50% review (L1–L4 style)
- Input: Numpad

**Level 6 — Division (whole results only)**
- New: `a ÷ b` where `b ≠ 0` and `a / b` is a whole number
- Generated by picking `b ∈ {2, 3, 4, 5}` and `result ∈ {1, 2, …, 10}`, then computing `a = b × result`
- Example problems: `4 ÷ 2 = 2`, `12 ÷ 3 = 4`, `25 ÷ 5 = 5`
- Pool: ~50% division, ~50% review (L1–L5 style)
- Input: Numpad

### 5.4 Levels 7–12: TBD Placeholder

These levels are reserved for future design. Candidate ideas include:

- **Larger multiplication** (full times tables up to 10×10)
- **Larger division** (dividends up to 100)
- **Mixed two-step problems** (e.g. `3 + 4 × 2` — order of operations intro)
- **Missing operand** (e.g. `_ + 5 = 12`)
- **Negative number introduction** (for older kids)
- **Speed rounds** — same ops, but faster slimes and tighter timing

Each TBD level must follow the accumulation rule: it adds its new operation/range to the existing pool.

### 5.5 Level Progression Rules

- Completing a level unlocks the next. Progress is saved to `localStorage` (guest) or Firestore (signed-in).
- A child can **replay any unlocked level** at any time.
- There is **no star rating**. You either clear it or you don't. No anxiety.
- After the final level, show a simple "You finished all levels! 🎉" screen. Encourage replay for speed.

### 5.6 Distractor Generation (Multiple Choice — Levels 1–2)

For choice-based levels, generate wrong answers that are *plausible*:
- One distractor = correct answer ± 1
- One distractor = correct answer ± 2 or ± 3
- Never show negative numbers as choices.
- Never show duplicate choices.
- Shuffle the position of the correct answer.

### 5.7 Problem Generation Logic

```js
function generateProblem(level) {
  // 1. Build the operation pool based on level (accumulation rule)
  // 2. Pick an operation — 50% chance of new op, 50% chance of review op
  // 3. Generate operands within the range for that op + level
  // 4. Return { text: "3 + 4", answer: 7, choices: [5, 7, 6] | null }
  //    choices is null for numpad levels (3+)
  //    Division: always generate via (b * result) ÷ b to ensure clean answers
  //    Subtraction: always ensure a ≥ b (no negatives)
}
```

---

## 6. Leaderboard

### 6.1 Philosophy

The leaderboard exists to give kids a *personal goal* and a *social spark* — not to breed anxiety. It is designed to celebrate variety (fastest, highest score, most levels) rather than a single ranking that creates winners and losers.

### 6.2 Leaderboard Categories

The leaderboard has **three tabs/views**, each highlighting a different kind of achievement:

| Tab | Title | What it Ranks | Columns Shown |
|---|---|---|---|
| 🏆 **High Score** | "Top Slime Poppers" | Highest single-game score across any level | Rank · Avatar · Name · Score · Level reached |
| ⚡ **Fastest Clear** | "Speed Demons" | Fastest time to clear a specific level (dropdown to pick level) | Rank · Avatar · Name · Time · Level |
| 🌟 **Most Levels** | "Slime Scholars" | Highest level unlocked | Rank · Avatar · Name · Highest Level · Total Problems Solved |

### 6.3 Leaderboard UX

- Accessible from the **title screen** via a trophy icon (🏆) in the top-right corner.
- Requires sign-in to appear on the board. Guest players see the board but with a gentle prompt: *"Sign in to see your name here!"*
- Shows the **top 20** entries per category.
- The current player's row is always highlighted (even if outside top 20, anchor it at the bottom with their rank).
- Each row shows: rank number, circular avatar (from Google), display name (first name only), and the relevant stat.
- A small **"Your Best"** card appears above the table showing the player's personal best for the selected category.

### 6.4 Leaderboard Data Flow

```
Game Over / Level Clear
  ↓
  If signed in:
    → Write score + time + level to Firestore leaderboard collection
    → Update user's personal best in users/{uid}/levels/{level_n}
  ↓
  Leaderboard screen queries Firestore:
    → High Score: order by score DESC, limit 20
    → Fastest Clear: filter by level, order by time ASC, limit 20
    → Most Levels: order by unlockedLevels DESC, limit 20
```

### 6.5 Anti-Cheat (Lightweight)

This is a kids' game, not a competitive esport. Keep it simple:

- Server-side (Firestore Security Rules): reject scores above a sane maximum (e.g. score > 10,000 in a single level is suspicious).
- Rate-limit writes: a user can only submit one leaderboard entry per level per minute.
- No client-trust for critical data — the score structure is simple enough that basic validation suffices.

### 6.6 Leaderboard Design

- Same "Soft Doodle" aesthetic as the rest of the game.
- Rows alternate in subtle warm tones (cream / slightly darker cream).
- Top 3 entries have small medal emojis: 🥇 🥈 🥉.
- Transitions: rows slide in gently when the board loads.
- On mobile, the table scrolls vertically within the game container. No horizontal scroll.

---

## 7. Visual Design

### 7.1 Aesthetic: "Soft Doodle"

Think: a child's coloring book brought to life with gentle motion. Rounded everything. Hand-drawn feel.

### 7.2 Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Background | Warm cream | `#FFF8F0` |
| Text / UI | Soft charcoal | `#3A3A3A` |
| Slime (default) | Lime green | `#A8E06C` |
| Slime (level 3–4) | Coral pink | `#FF8FA3` |
| Slime (level 5–6) | Lavender | `#B49FDC` |
| Slime (level 7+) | Cycle through all slime colors | — |
| Correct flash | Mint | `#6EDBA2` |
| Wrong flash | Soft red | `#FF6B6B` |
| Hearts | Warm red | `#E8453C` |
| Buttons | Sky blue | `#64B5F6` |

### 7.3 Typography

- **Primary font:** `"Patrick Hand"` from Google Fonts — handwritten, childlike, legible.
- **Numbers in problems:** `"Fredoka One"` — chunky, rounded, easy to read at large sizes.
- Fallback: `"Comic Sans MS", cursive, sans-serif` (yes, unironically — kids love it).

### 7.4 Slime Design (Pure CSS)

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

### 7.5 Layout

```
┌──────────────────────────────────┐
│  ♥ ♥ ♥          Level 3    ⚙ 🏆 │  ← Top bar: hearts, level name, settings, leaderboard
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

## 8. Screens

### 8.1 Title Screen

- Game title "MathSlime" in `Fredoka One`, big and bouncy.
- A single idle slime with blinking eyes.
- If signed in: circular avatar + "Hi, [first name]!" greeting. Small "Sign Out" link.
- If guest: **"Sign In with Google"** button (Google-branded, compact) + **"Play as Guest"** text link.
- **"Play"** button (large, sky blue, rounded).
- Below: a row of level circles (1–12). Locked ones are greyed out with a tiny lock icon.
- Trophy icon (🏆) in the top-right opens the leaderboard.

### 8.2 Level Select (optional — could also be inline on title)

- Grid of 12 circles.
- Unlocked = colored + tappable.
- Locked = grey + lock icon.
- Current highest = pulsing glow.

### 8.3 Gameplay Screen

- See §7.5 layout.
- Problem text is large (at least 48px).
- Slime drifts from right to left.
- When a slime is popped, the next one spawns after a 1-second pause.
- An internal (hidden) timer tracks total time for the level attempt — used for "Fastest Clear" leaderboard.

### 8.4 Level Complete Screen

- "Level Clear! 🎉"
- "You solved X out of Y!" (always positive framing)
- If signed in: "Score submitted to leaderboard!" (small text)
- "Next Level →" button
- "Back to Levels" link

### 8.5 Game Over Screen

- "Great try!"
- "You solved X problems this round!"
- "Try Again" button (restarts same level)
- "Back to Levels" link

### 8.6 Leaderboard Screen

- Overlay within the game container (same style as game-over overlay).
- Three tabs at the top: 🏆 High Score · ⚡ Fastest · 🌟 Levels.
- Scrollable table of top 20 entries.
- "Your Best" personal stats card above the table.
- Close button (✕) returns to title screen.

---

## 9. Audio (Optional / Progressive Enhancement)

If we add audio, keep it **tiny** and optional:

| Event | Sound | Implementation |
|-------|-------|----------------|
| Correct answer | Short cheerful "pop" | Web Audio API — synthesized, not a file |
| Wrong answer | Soft low "bonk" | Web Audio API — synthesized |
| Slime reaches edge | Quick descending tone | Web Audio API — synthesized |
| Level complete | 3-note ascending chime | Web Audio API — synthesized |

**All audio must be synthesized via Web Audio API** — no external sound files.

A mute toggle (🔊 / 🔇) sits in the top-right corner. Default state: **muted**. Kids in classrooms shouldn't blast sounds unexpectedly.

---

## 10. Technical Spec

### 10.1 Stack

- **One file:** `index.html` containing all HTML, CSS, and JS.
- **External dependencies (CDN only):**
  - Google Fonts (`Patrick Hand`, `Fredoka One`)
  - Firebase JS SDK (compat build — auth + Firestore)
- **No build step.** Open the file in a browser, done.
- **Offline-capable:** After first load, core game works without internet (fonts fall back, auth/leaderboard degrade gracefully).

### 10.2 State Management

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
  screen: 'title',    // 'title' | 'play' | 'levelComplete' | 'gameOver' | 'leaderboard'
  levelStartTime: null, // Date.now() when level begins — for fastest-clear tracking
  user: null            // null (guest) or { uid, displayName, photoURL }
};
```

Persist `unlockedLevels` to `localStorage` (guest) or Firestore (signed-in). On sign-in, merge: take the higher of local vs. cloud `unlockedLevels`.

### 10.3 Problem Generator

```js
function generateProblem(level) {
  // Returns { text: "3 + 4", answer: 7, choices: [5, 7, 6] | null }
  // choices is null for numpad levels (3+)
  // Follows accumulation rule: all ops from levels ≤ current
  // ~50% new op, ~50% review ops
  // Division: always clean integer results
  // Subtraction: never negative results
  // No duplicate choices
}
```

### 10.4 Slime Timer

Each slime has a countdown. Use `requestAnimationFrame` for smooth movement, not `setInterval`.

```js
// Slime moves from 100% (right) to 0% (left) over `levelSpeed` seconds.
// Position = 100 - (elapsed / levelSpeed) * 100
```

When position ≤ 0: slime reached the edge, remove 1 heart, spawn next slime.

### 10.5 Animations (CSS)

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

### 10.6 Responsive Design

- `max-width: 500px; margin: 0 auto;` for the game container.
- All sizes in `rem` or `vw` units.
- Numpad buttons: minimum `48px × 48px` tap targets (WCAG compliant).
- Test at 320px width (small phones) and 1024px (tablets).

### 10.7 Firebase Integration Points

| Action | Trigger | Firestore Operation |
|---|---|---|
| Sign in | User taps "Sign In with Google" | Read `users/{uid}` → merge with local state |
| Level clear | Level complete screen shown | Write to `leaderboard/`, update `users/{uid}/levels/{n}` |
| Game over | Game over screen shown | Write to `leaderboard/` (if score > 0) |
| View leaderboard | Leaderboard screen opened | Read `leaderboard/` (ordered query, limit 20) |
| Sign out | User taps "Sign Out" | Clear `state.user`, revert to localStorage |

---

## 11. Accessibility

- All buttons have clear text labels (no icon-only buttons).
- Color is never the *only* indicator of state (hearts use both color + icon).
- Tap targets ≥ 48px.
- High contrast between text and background (cream + charcoal = ~10:1 ratio).
- `prefers-reduced-motion`: disable slime bounce and confetti if set.
- Screen reader: problem text is in an `aria-live="polite"` region.
- Google Sign-In button follows Google's accessibility guidelines.

---

## 12. What We DON'T Build

This is as important as what we build:

- ❌ Email/password auth (Google only — simple and safe)
- ❌ Star ratings per level (anxiety-inducing)
- ❌ Timers visible to the child (the slime *is* the timer — no numbers ticking down)
- ❌ Ads, analytics, tracking (Firebase Auth + Firestore only — no Analytics SDK)
- ❌ In-app purchases or "premium" tiers
- ❌ Character customization (scope creep — ship v1 first)
- ❌ Backend / server beyond Firebase
- ❌ Multiple game modes in v1
- ❌ Public chat or social features (child safety)
- ❌ Comparison language on leaderboard (no "you beat X!" notifications)

---

## 13. File Structure

```
mathslime/
├── index.html         ← The entire game. Ship this.
└── instructions_h.md  ← This file.
```

That's it. That's the repo. (Firebase is configured entirely via the client SDK — no server files.)

---

## 14. Development Phases

### Phase 1 — Core (MVP)

1. Title screen with level select.
2. Problem generator for levels 1–6 (with accumulation rule).
3. Slime movement + pop mechanic.
4. Multiple choice input (levels 1–2).
5. Numpad input (levels 3+).
6. Hearts / game over / level complete flow.
7. `localStorage` progress save.

### Phase 2 — Auth & Leaderboard

8. Firebase Auth (Google Sign-In) integration.
9. Firestore data model setup.
10. Leaderboard UI (three tabs: High Score, Fastest Clear, Most Levels).
11. Score submission on level clear / game over.
12. Merge local ↔ cloud progress on sign-in.

### Phase 3 — Polish

13. CSS slime design with idle animation.
14. Pop + confetti animations.
15. Web Audio API sounds (synthesized).
16. `prefers-reduced-motion` support.
17. Responsive testing on real devices.

### Phase 4 — Expand Levels (after v1 ships)

18. Design and implement Levels 7–12 (TBD operations).
19. Practice / endless mode.
20. Parent dashboard (local-only stats).
21. PWA manifest for "Add to Home Screen".

---

## 15. Success Criteria

The game is done when:

- [ ] A 5-year-old can start playing within 10 seconds of opening the page.
- [ ] A 9-year-old finds Level 6 satisfying and wants to unlock Level 7.
- [ ] Guest mode works fully offline with no sign-in prompt blocking play.
- [ ] Signed-in players see their name on the leaderboard after clearing a level.
- [ ] The leaderboard loads in under 2 seconds.
- [ ] It runs smoothly on a 2019 budget Android phone.
- [ ] No adult needs to explain how to play.
- [ ] It makes a kid smile.

---

*Built with zero unnecessary dependencies and maximum care.*
