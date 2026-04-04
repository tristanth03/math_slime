# HTML Performance Review

## Critical Optimizations for Speed

### 1. **Firebase Script Loading** (index.html - lines 9-11)
**Issue:** Multiple sequential Firebase CDN loads block page render.
```html
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js"></script>
```
**Fix:** Use `async` + `defer` attributes, or load Firebase only when needed (lazy load auth/firestore after gameplay starts).

---

### 2. **Google Fonts Preload** (index.html - lines 7-8)
**Issue:** Two font families with `display=swap` - swap blocks render briefly.
```html
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Patrick+Hand&display=swap"...>
```
**Fix:** Use `display=optional` for non-critical fonts (Patrick Hand), or self-host font files. Load fonts via `preload` instead of Google API if self-hosted.

---

### 3. **Canvas Resizing on Every Window Resize** (index.html - lines 400-407)
**Issue:** `resizeCanvas()` called without debounce, can fire dozens of times during resize.
```javascript
window.addEventListener('resize', resizeCanvas);
```
**Fix:** Add debounce (150-300ms) to prevent thrashing:
```javascript
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(resizeCanvas, 300);
});
```

---

### 4. **DOM innerHTML in Game Loop** (index.html - lines 1026-1063, 1082)
**Issue:** Repainting entire answer bar on every question, numpad display updated constantly.
```javascript
bar.innerHTML = ''; // Causes layout recalc
numpadValue = numpadValue.slice(0, -1);
document.getElementById('numpad-display').textContent = numpadValue || '_'; // Repeated reflows
```
**Fix:** Cache DOM references, update only changed elements. Batch DOM updates outside frame callbacks.

---

### 5. **Frequent `querySelectorAll()` in Game Loop** (index.html - lines 918, 1060, 1303-1307)
**Issue:** DOM queries happen repeatedly; especially problematic in leaderboard rendering.
**Fix:** Cache selectors, use event delegation, avoid querying inside loops.

---

### 6. **Synchronous Firebase Calls in Loop** (index.html - lines 1330-1332, 1353)
**Issue:** Leaderboard loads execute synchronous await in UI render code.
**Fix:** Load leaderboard data in parallel with game rendering; cache results.

---

### 7. **Star Twinkling in Draw Loop** (index.html - lines 856-865)
**Issue:** 35 stars redrawn every frame with trigonometry calculation.
```javascript
s.twinkle += 0.015;
ctx.globalAlpha = s.alpha * (0.6 + 0.4 * Math.sin(s.twinkle));
```
**Fix:** Pre-calculate twinkle values or use CSS animations instead. Reduce star count (20 vs 35).

---

### 8. **Bezier Curve Drawing Per Slime Per Frame** (index.html - lines 732-738)
**Issue:** Complex bezier paths drawn for every slime every frame - expensive on low-end devices.
**Fix:** Cache slime path as canvas pattern, reuse. Or use `arc()` instead of beziers (v0_0 approach is simpler).

---

### 9. **Leaderboard Avatar Images** (index.html - lines 1372-1374)
**Issue:** External user images loaded without `loading="lazy"` or size constraints.
**Fix:** Add image constraints:
```javascript
`<img class="lb-avatar" src="${d.photoURL}" alt="" loading="lazy" width="24" height="24">`
```

---

### 10. **Particle Spawning Overhead** (index.html - lines 775-790, 791-799)
**Issue:** 12 particles per pop, filter/update every frame:
```javascript
for (let i = 0; i < 12; i++) {
  const colors = [color, '#FFD700', '#FF6B6B', ...]; // Array lookup each particle
  popParticles.push({...});
}
popParticles = popParticles.filter(p => {
  p.x += p.vx * dt * 60;
  p.y += p.vy * dt * 60;
  p.vy += 0.15;
  p.alpha -= dt / p.life;
  return p.alpha > 0;
});
```
**Fix:** Pre-allocate particle pool (object reuse pattern), reduce particles to 8, use built-in array methods sparingly.

---

## Quick Wins (Easy Fixes)

- **Remove unused Google Analytics** (if `measurementId` not used)
- **Minify inline CSS** (save ~2KB)
- **Use `will-change: transform`** on canvas for GPU acceleration
- **Cache `cW()` / `cH()` calls** - they call `getBoundingClientRect()` repeatedly
- **Consolidate setTimeout calls** - batch callbacks into single requestAnimationFrame

---

## v0_0 vs Main: Performance Comparison

- **v0_0:** Simpler slime graphics (circles), no Firebase, faster rendering ✅
- **Main:** More complex visuals (beziers, more particles), Firebase overhead, but better features

**Recommendation:** Keep v0_0 approach for rendering (simpler shapes), add Firebase selectively.
