# MathSlime — Point System

## Base Score

Each correct answer awards:

$$S_q = B_d \cdot (1 + \beta \cdot h(t))$$

where:

- $B_d = 10 + 2d$ — base points, determined by difficulty $d$ (speed parameter, 5–10).
- $h(t) = \max\!\left(0,\; 1 - \frac{t}{t_{\max}}\right)$ — speed factor; linear decay from 1 (instant) to 0 (at the time limit).
- $\beta = 2$ — caps the maximum at $3 \times$ the base.

This gives $S_q \in [B_d,\; 3\,B_d]$.

## Hot Streak

Every $c = 5$ consecutive correct answers awards a one-time bonus:

$$S_{\text{streak}} = B_d$$

Any mistake or miss resets the streak counter to 0.

## Boss Rounds

Clearing a boss round awards the sum of per-question scores plus a flat bonus $C$:

$$S_{\text{boss}} = \sum_q S_q + C$$

| Round Type | $C$ |
|---|---|
| Mini-Boss | 50 |
| Mega-Boss | 100 |

Bonus only awarded if the round is cleared (hearts > 0).

## Penalties

| Event | Effect |
|---|---|
| Slime escapes (missed) | $-1$ heart |
| Wrong answer | $-\tfrac{1}{2}$ heart |

Both reset the streak counter. Game over at 0 hearts (3 hearts per round).
