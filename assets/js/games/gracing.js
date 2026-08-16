/* Racing — dodge oncoming cars. Pure canvas mini-game. */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  var canvas = document.getElementById("game-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var W = canvas.width, H = canvas.height, laneCount = 4, laneW = W / laneCount;
  var player = { lane: 1, w: 34, h: 56, y: H - 70 };
  var cars = [], score = 0, speed = 2.6, spawn = 0, running = false, raf = 0, over = false, t0 = 0;

  function setHud(v) { var e = document.getElementById("score"); if (e) e.textContent = v; }
  function toast(m) { var t = document.getElementById("toast"); if (t) { t.textContent = m; t.classList.add("show"); setTimeout(function () { t.classList.remove("show"); }, 1600); } }
  function reset() { player.lane = Math.floor(laneCount / 2); cars = []; score = 0; speed = 2.6; spawn = 0; over = false; setHud(0); }
  function drawRoad() {
    ctx.fillStyle = "#2b2b3a"; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = "#f5f5f5"; ctx.lineWidth = 3; ctx.setLineDash([18, 22]);
    for (var i = 1; i < laneCount; i++) { ctx.beginPath(); ctx.moveTo(i * laneW, 0); ctx.lineTo(i * laneW, H); ctx.stroke(); }
    ctx.setLineDash([]);
  }
  function car(x, y, w, h, color) {
    ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.fillRect(x + 4, y + 8, w - 8, 10);
    ctx.fillStyle = "rgba(0,0,0,.3)"; ctx.fillRect(x + 4, y + h - 16, w - 8, 10);
  }
  function loop(ts) {
    if (!running) return;
    if (!t0) t0 = ts;
    drawRoad();
    spawn += 1;
    if (spawn > 46) {
      spawn = 0; var l = Math.floor(Math.random() * laneCount);
      cars.push({ lane: l, y: -60, w: 32, h: 52, color: ["#ff5d5d", "#5dd6ff", "#ffd35d", "#9d7bff"][Math.floor(Math.random() * 4)] });
      speed += 0.02;
    }
    var px = player.lane * laneW + (laneW - player.w) / 2;
    for (var i = cars.length - 1; i >= 0; i--) {
      var c = cars[i]; c.y += speed;
      car(c.lane * laneW + (laneW - c.w) / 2, c.y, c.w, c.h, c.color);
      if (c.lane === player.lane && c.y + c.h > player.y && c.y < player.y + player.h) { end(); return; }
      if (c.y > H) { cars.splice(i, 1); score += 1; setHud(score); }
    }
    car(px, player.y, player.w, player.h, "#36e07a");
    raf = requestAnimationFrame(loop);
  }
  function end() { running = false; over = true; cancelAnimationFrame(raf); toast((I18N.gameOver || "Crash! Score: {score}").replace("{score}", score)); }
  function go() { if (over) reset(); if (running) return; running = true; t0 = 0; raf = requestAnimationFrame(loop); }
  function pauseGame() { if (!running) return; running = false; cancelAnimationFrame(raf); toast(I18N.paused || "Paused"); }
  function move(dir) { if (!running) return; player.lane = Math.max(0, Math.min(laneCount - 1, player.lane + dir)); }

  drawRoad(); reset();
  var bStart = document.getElementById("btn-start"), bPause = document.getElementById("btn-pause"), bRestart = document.getElementById("btn-restart");
  if (bStart) bStart.addEventListener("click", go);
  if (bPause) bPause.addEventListener("click", pauseGame);
  if (bRestart) bRestart.addEventListener("click", function () { reset(); go(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") move(-1);
    else if (e.key === "ArrowRight") move(1);
    else if (e.key === " ") { e.preventDefault(); running ? pauseGame() : go(); }
  });
  var pad = document.querySelector(".pad");
  if (pad) {
    pad.querySelectorAll('[data-dir="left"]').forEach(function (b) { b.addEventListener("click", function () { move(-1); }); });
    pad.querySelectorAll('[data-dir="right"]').forEach(function (b) { b.addEventListener("click", function () { move(1); }); });
  }
})();
