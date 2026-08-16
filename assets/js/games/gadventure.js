/* Adventure — escape the maze. Arrow keys / WASD / on-screen pad. */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  var canvas = document.getElementById("game-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var W = canvas.width, H = canvas.height;
  var maze = [
    "1111111111111111",
    "1000000010000001",
    "1011111010111101",
    "1010000000100001",
    "1010111111101101",
    "1000100000001001",
    "1110101111110101",
    "1000101000010001",
    "1011101011110101",
    "1010001000000101",
    "1010110111110101",
    "1000010000000001",
    "1111010111110111",
    "1000010000000001",
    "1011111111111101",
    "1000000000000001"
  ];
  var rows = maze.length, cols = maze[0].length, cs = Math.floor(Math.min(W, H) / cols);
  var offX = (W - cs * cols) / 2, offY = (H - cs * rows) / 2;
  var cell = { x: 1, y: 1 };
  var exit = { x: cols - 2, y: rows - 2 }, steps = 0, won = false;

  function setHud(v) { var e = document.getElementById("steps"); if (e) e.textContent = v; }
  function toast(m) { var t = document.getElementById("toast"); if (t) { t.textContent = m; t.classList.add("show"); setTimeout(function () { t.classList.remove("show"); }, 2000); } }
  function reset() { cell = { x: 1, y: 1 }; steps = 0; won = false; setHud(0); }
  function blocked(nx, ny) { return maze[ny][nx] === "1"; }
  function move(dx, dy) {
    if (won) return;
    var nx = cell.x + dx, ny = cell.y + dy;
    if (nx < 0 || ny < 0 || nx >= cols || ny >= rows) return;
    if (blocked(nx, ny)) return;
    cell.x = nx; cell.y = ny; steps += 1; setHud(steps);
    if (cell.x === exit.x && cell.y === exit.y) { won = true; toast((I18N.win || "🎉 You escaped in {steps} steps!").replace("{steps}", steps)); }
    draw();
  }
  function draw() {
    ctx.fillStyle = "#1d2440"; ctx.fillRect(0, 0, W, H);
    for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
      if (maze[y][x] === "1") { ctx.fillStyle = "#3a4a7a"; ctx.fillRect(offX + x * cs, offY + y * cs, cs, cs); }
    }
    ctx.fillStyle = "#36e07a"; ctx.fillRect(offX + exit.x * cs + 3, offY + exit.y * cs + 3, cs - 6, cs - 6);
    ctx.beginPath(); ctx.fillStyle = "#ffd35d";
    ctx.arc(offX + cell.x * cs + cs / 2, offY + cell.y * cs + cs / 2, cs / 2 - 3, 0, Math.PI * 2); ctx.fill();
  }
  function key(e) {
    var k = e.key.toLowerCase();
    if (k === "arrowup" || k === "w") move(0, -1);
    else if (k === "arrowdown" || k === "s") move(0, 1);
    else if (k === "arrowleft" || k === "a") move(-1, 0);
    else if (k === "arrowright" || k === "d") move(1, 0);
  }
  draw(); setHud(0);
  var bRestart = document.getElementById("btn-restart");
  if (bRestart) bRestart.addEventListener("click", function () { reset(); draw(); });
  document.addEventListener("keydown", key);
  var pad = document.querySelector(".pad");
  if (pad) {
    pad.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = b.getAttribute("data-dir");
        if (d === "up") move(0, -1); else if (d === "down") move(0, 1);
        else if (d === "left") move(-1, 0); else if (d === "right") move(1, 0);
      });
    });
  }
})();
