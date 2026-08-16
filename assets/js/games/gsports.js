/* Sports — basketball free-throw. Drag to aim, release to shoot. */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  var canvas = document.getElementById("game-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var W = canvas.width, H = canvas.height;
  var hoop = { x: W - 70, y: 95, r: 26 };
  var ball = { x: 80, y: H - 60, r: 14, vx: 0, vy: 0, flying: false };
  var score = 0, attempts = 0, running = false, raf = 0, over = false, dragStart = null;

  function setHud(v) { var e = document.getElementById("score"); if (e) e.textContent = v; }
  function setHud2(v) { var e = document.getElementById("attempts"); if (e) e.textContent = v; }
  function toast(m) { var t = document.getElementById("toast"); if (t) { t.textContent = m; t.classList.add("show"); setTimeout(function () { t.classList.remove("show"); }, 1600); } }
  function reset() { ball.x = 80; ball.y = H - 60; ball.vx = 0; ball.vy = 0; ball.flying = false; over = false; }

  function draw() {
    ctx.fillStyle = "#9ad0ff"; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#c98a3c"; ctx.fillRect(0, H - 40, W, 40);
    ctx.fillStyle = "#fff"; ctx.strokeStyle = "#e03b3b"; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(hoop.x, hoop.y, hoop.r, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(hoop.x - hoop.r, hoop.y + hoop.r); ctx.lineTo(hoop.x - hoop.r - 6, hoop.y + hoop.r + 26); ctx.lineTo(hoop.x + 2, hoop.y + hoop.r + 26); ctx.lineTo(hoop.x + 2, hoop.y + hoop.r); ctx.closePath(); ctx.strokeStyle = "#ff7a3b"; ctx.stroke();
    ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
    ctx.fillStyle = "#ff8c2b"; ctx.fill();
    ctx.strokeStyle = "#7a3b00"; ctx.lineWidth = 2; ctx.stroke();
  }
  function loop() {
    if (!running) return;
    draw();
    if (ball.flying) {
      ball.vy += 0.35; ball.x += ball.vx; ball.y += ball.vy;
      var d = Math.hypot(ball.x - hoop.x, ball.y - hoop.y);
      if (d < hoop.r + ball.r && Math.abs(ball.vx) > 0) {
        score += 1; setHud(score); toast(I18N.score || "Swoosh! +1"); ball.flying = false; reset(); running = false;
      } else if (ball.y > H + 30 || ball.x > W + 30) {
        toast(I18N.miss || "Missed!"); ball.flying = false; reset(); running = false;
      }
    }
    raf = requestAnimationFrame(loop);
  }
  function shoot(ang, pow) {
    if (ball.flying || over) return;
    running = true; attempts += 1; setHud2(attempts);
    ball.vx = Math.cos(ang) * pow; ball.vy = -Math.sin(ang) * pow; ball.flying = true; raf = requestAnimationFrame(loop);
  }
  function pointer(e) {
    var rect = canvas.getBoundingClientRect();
    var cx = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
    var cy = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top;
    return { x: cx * (W / rect.width), y: cy * (H / rect.height) };
  }
  function aimAng() { return Math.atan2(-(hoop.y - ball.y), hoop.x - ball.x); }
  function onDown(e) { if (ball.flying) return; e.preventDefault(); dragStart = pointer(e); }
  function onUp(e) {
    if (!dragStart || ball.flying) return; e.preventDefault();
    var p = pointer(e.changedTouches ? { touches: e.changedTouches } : e);
    var dx = p.x - dragStart.x, dy = p.y - dragStart.y;
    var dist = Math.min(Math.hypot(dx, dy), 220);
    var power = 4 + dist / 14;
    shoot(aimAng(), power); dragStart = null;
  }
  draw(); setHud(0); setHud2(0);
  var bRestart = document.getElementById("btn-restart"), bStart = document.getElementById("btn-start");
  if (bRestart) bRestart.addEventListener("click", function () { score = 0; attempts = 0; setHud(0); setHud2(0); reset(); });
  if (bStart) bStart.addEventListener("click", function () { if (!ball.flying) shoot(aimAng(), 11); });
  canvas.addEventListener("mousedown", onDown);
  canvas.addEventListener("mouseup", onUp);
  canvas.addEventListener("touchstart", onDown, { passive: false });
  canvas.addEventListener("touchend", onUp, { passive: false });
})();
