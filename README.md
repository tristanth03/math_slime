# 🧫 MathSlime

A lightweight, ad-free math game for kids ages 4–10. Solve arithmetic problems to pop falling slime blobs before they reach the bottom. Single HTML file, no frameworks, no build step.

**Play now:** [tristanth03.github.io/math_slime](https://tristanth03.github.io/math_slime/)

## Quick Start

Open `index.html` in a browser. Sign in with Google to save progress and appear on the leaderboard, or play as a guest.

## Features

- 6 levels introducing addition, subtraction, multiplication, and division
- Multiple-choice answers (3–5 buttons scaling with difficulty)
- Canvas-rendered slimes with pop animations and particle effects
- Combo scoring system for consecutive correct answers
- Leaderboard with three tabs: High Score, Fastest Clear, Most Levels
- Synthesized sound effects via Web Audio API (muted by default)
- No ads, tracking, or in-app purchases

## Design Pillars

Simple, lightweight, free, honest. A 4-year-old should figure it out in 10 seconds without help.

## Tech Stack

- Pure HTML/CSS/JavaScript (single file, canvas-based rendering)
- Firebase Auth (Google Sign-In) + Firestore for cloud progress and leaderboards
- localStorage fallback for guest play
- No build step, no dependencies beyond Firebase CDN scripts
