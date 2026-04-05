# MathSlime — To Do

## Architecture

* Separate engine from data
   * `index.html` — game engine (rendering, scoring, animation, auth, leaderboard)
   * `levels.json` — level definitions (pure data, no logic)
   * Engine fetches `levels.json` on load, generates no problems itself
* Each level entry is a tuple $L(n) = \big(\mathcal{O}_n, D_n, s_n, p_n, c_n, \mathcal{R}_n\big)$
   * $\mathcal{O}_n$ — operator pool (e.g. `["+", "-"]`)
   * $D_n$ — domain / input range per operator
   * $s_n$ — slime speed (seconds to cross canvas)
   * $p_n$ — problems to clear
   * $c_n$ — number of answer choices
   * $\mathcal{R}_n$ — constraints (e.g. no negative results, clean division)
* File structure:
   ```
   mathslime/
   ├── index.html
   ├── levels.json
   ├── instructions_h.md
   └── to_do.md
   ```
* Served via GitHub Pages — multi-file is fine, no CORS issues

## Level Design

* Design 100 levels (appended progressively)
   * **[01] Levels 1–5:** $T_1 : X \times X \to Y_1$ with $X \in \{0,\dots,5\}$, $T_1(x_1, x_2) \in \{0,\dots,10\} = Y_1$
   * **[02] Levels 6–10:** New $T_2 : X \times X \to Y_2$ with $X \in \{0,\dots,5\}$, $T_2(x_1, x_2) \in \{-5,\dots,0,\dots,5\} = Y_2$
   * **[03] Levels 11–15:** $X$ extends to $\{0,\dots,10\}$, hence $T_1 : Y_1 = \{0,\dots,20\}$ and $T_2 : Y_2 = \{-10,\dots,0,\dots,10\}$
   * **[04] Levels 16–20:** Same operators and ranges as [03], increased problem count
   * **[05] Levels 21–25:** New $M_1 : Z \times Z \to Y_3$ with $Z \in \{0,\dots,5\}$, $M_1(z_1, z_2) \in \{0,\dots,25\} = Y_3$
   * **[06] Levels 26–30:** New $D_1 : Y_3 \times Z \to Z$ with results in $\{0,1,2,3,4,5\}$, clean division from smallest combinations of $M_1$
   * **[07] Levels 31–35:** $T_1$ domain extends to $\{0,\dots,100\}$, all prior operators retained
   * **[TBD] Levels 36–100**

## Bugs

* Fix leaderboard
   * Fastest tab not working
   * Levels tab not working

## Gameplay

* Make the game window larger
* $-\frac{1}{2}$ heart penalty on wrong answer
* Design a decay pattern as a function of time
   * Normalize scores accordingly

## Visual / Audio

* Make the level map pull from different themes
* Make sounds more appealing
