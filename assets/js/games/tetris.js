/* 俄罗斯方块 */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var COLS = 10, ROWS = 20, CELL = 24;
  var canvas = document.getElementById("game-canvas");
  var ctx = canvas.getContext("2d");
  var nextCanvas = document.getElementById("next-canvas");
  var nctx = nextCanvas.getContext("2d");
  var scoreEl = document.getElementById("score");
  var linesEl = document.getElementById("lines");
  var levelEl = document.getElementById("level");
  var toast = document.getElementById("toast");

  var SHAPES = {
    I: [[1, 1, 1, 1]],
    J: [[1, 0, 0], [1, 1, 1]],
    L: [[0, 0, 1], [1, 1, 1]],
    O: [[1, 1], [1, 1]],
    S: [[0, 1, 1], [1, 1, 0]],
    T: [[0, 1, 0], [1, 1, 1]],
    Z: [[1, 1, 0], [0, 1, 1]]
  };
  var COLORS = {
    I: "#3ec1f3", J: "#7c4dff", L: "#ff8a3d", O: "#ffd23f",
    S: "#4ade80", T: "#ff5da2", Z: "#ff5252"
  };
  var KEYS = Object.keys(SHAPES);

  var board, current, next, px, py, score, lines, level, timer, running, over;

  function newBoard() {
    board = [];
    for (var r = 0; r < ROWS; r++) board.push(new Array(COLS).fill(null));
  }

  function randomPiece() {
    var k = KEYS[Math.floor(Math.random() * KEYS.length)];
    return { shape: SHAPES[k].map(function (row) { return row.slice(); }), color: COLORS[k] };
  }

  function spawn() {
    current = next || randomPiece();
    next = randomPiece();
    px = Math.floor((COLS - current.shape[0].length) / 2);
    py = 0;
    drawNext();
    if (collides(px, py, current.shape)) {
      gameOver();
    }
  }

  function collides(x, y, shape) {
    for (var r = 0; r < shape.length; r++) {
      for (var c = 0; c < shape[r].length; c++) {
        if (!shape[r][c]) continue;
        var bx = x + c, by = y + r;
        if (bx < 0 || bx >= COLS || by >= ROWS) return true;
        if (by >= 0 && board[by][bx]) return true;
      }
    }
    return false;
  }

  function merge() {
    current.shape.forEach(function (row, r) {
      row.forEach(function (v, c) {
        if (v && py + r >= 0) board[py + r][px + c] = current.color;
      });
    });
  }

  function clearLines() {
    var cleared = 0;
    for (var r = ROWS - 1; r >= 0; r--) {
      if (board[r].every(function (v) { return v; })) {
        board.splice(r, 1);
        board.unshift(new Array(COLS).fill(null));
        cleared++;
        r++;
      }
    }
    if (cleared) {
      var points = [0, 100, 300, 500, 800][cleared] * level;
      score += points;
      lines += cleared;
      var newLevel = Math.floor(lines / 10) + 1;
      if (newLevel !== level) {
        level = newLevel;
        levelEl.textContent = level;
        restartLoop();
      }
      scoreEl.textContent = score;
      linesEl.textContent = lines;
    }
  }

  function rotate() {
    var s = current.shape;
    var rotated = s[0].map(function (_, i) {
      return s.map(function (row) { return row[i]; }).reverse();
    });
    if (!collides(px, py, rotated)) current.shape = rotated;
    else if (!collides(px - 1, py, rotated)) { px--; current.shape = rotated; }
    else if (!collides(px + 1, py, rotated)) { px++; current.shape = rotated; }
  }

  function moveDown() {
    if (!running) return;
    if (!collides(px, py + 1, current.shape)) {
      py++;
    } else {
      merge();
      clearLines();
      spawn();
    }
    draw();
  }

  function hardDrop() {
    if (!running) return;
    while (!collides(px, py + 1, current.shape)) { py++; score += 2; }
    scoreEl.textContent = score;
    merge();
    clearLines();
    spawn();
    draw();
  }

  function draw() {
    ctx.fillStyle = "#141428";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    for (var x = 1; x < COLS; x++) {
      ctx.beginPath(); ctx.moveTo(x * CELL, 0); ctx.lineTo(x * CELL, ROWS * CELL); ctx.stroke();
    }
    for (var y = 1; y < ROWS; y++) {
      ctx.beginPath(); ctx.moveTo(0, y * CELL); ctx.lineTo(COLS * CELL, y * CELL); ctx.stroke();
    }

    board.forEach(function (row, r) {
      row.forEach(function (color, c) {
        if (color) drawCell(ctx, c, r, color);
      });
    });

    if (current) {
      // 落点虚影
      var gy = py;
      while (!collides(px, gy + 1, current.shape)) gy++;
      current.shape.forEach(function (row, r) {
        row.forEach(function (v, c) {
          if (v) {
            ctx.strokeStyle = "rgba(255,255,255,0.25)";
            ctx.strokeRect((px + c) * CELL + 2, (gy + r) * CELL + 2, CELL - 4, CELL - 4);
          }
        });
      });
      current.shape.forEach(function (row, r) {
        row.forEach(function (v, c) {
          if (v) drawCell(ctx, px + c, py + r, current.color);
        });
      });
    }
  }

  function drawCell(context, c, r, color) {
    context.fillStyle = color;
    context.fillRect(c * CELL + 1, r * CELL + 1, CELL - 2, CELL - 2);
    context.fillStyle = "rgba(255,255,255,0.25)";
    context.fillRect(c * CELL + 1, r * CELL + 1, CELL - 2, 5);
  }

  function drawNext() {
    nctx.fillStyle = "#141428";
    nctx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
    var s = next.shape;
    var offX = Math.floor((4 - s[0].length) / 2);
    var offY = Math.floor((4 - s.length) / 2);
    var NC = 18;
    s.forEach(function (row, r) {
      row.forEach(function (v, c) {
        if (v) {
          nctx.fillStyle = next.color;
          nctx.fillRect((offX + c) * NC + 12, (offY + r) * NC + 6, NC - 2, NC - 2);
        }
      });
    });
  }

  function restartLoop() {
    clearInterval(timer);
    timer = setInterval(moveDown, Math.max(100, 800 - (level - 1) * 70));
  }

  function gameOver() {
    clearInterval(timer);
    running = false;
    over = true;
    showToast(msg("gameOver", "游戏结束！得分 {score}", { score: score }));
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2200);
  }

  function start() {
    if (running) return;
    if (over) reset();
    running = true;
    restartLoop();
  }

  function pause() {
    if (!running) return;
    clearInterval(timer);
    running = false;
    showToast(msg("paused", "已暂停"));
  }

  function reset() {
    newBoard();
    score = 0; lines = 0; level = 1; over = false;
    scoreEl.textContent = "0";
    linesEl.textContent = "0";
    levelEl.textContent = "1";
    next = null;
    spawn();
    draw();
  }

  document.addEventListener("keydown", function (e) {
    var k = e.key;
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].indexOf(k) !== -1) e.preventDefault();
    if (!running) {
      if (k === " ") start();
      return;
    }
    if (k === "ArrowLeft" || k === "a" || k === "A") { if (!collides(px - 1, py, current.shape)) px--; }
    else if (k === "ArrowRight" || k === "d" || k === "D") { if (!collides(px + 1, py, current.shape)) px++; }
    else if (k === "ArrowDown" || k === "s" || k === "S") { moveDown(); score++; scoreEl.textContent = score; }
    else if (k === "ArrowUp" || k === "w" || k === "W") rotate();
    else if (k === " ") hardDrop();
    else if (k === "p" || k === "P") { pause(); }
    draw();
  });

  document.querySelectorAll(".pad button").forEach(function (btn) {
    btn.addEventListener("touchstart", function (e) {
      e.preventDefault();
      var a = btn.getAttribute("data-act");
      if (!running) { start(); return; }
      if (a === "left" && !collides(px - 1, py, current.shape)) px--;
      else if (a === "right" && !collides(px + 1, py, current.shape)) px++;
      else if (a === "down") moveDown();
      else if (a === "rotate") rotate();
      else if (a === "drop") hardDrop();
      draw();
    }, { passive: false });
  });

  document.getElementById("btn-start").addEventListener("click", start);
  document.getElementById("btn-pause").addEventListener("click", pause);
  document.getElementById("btn-restart").addEventListener("click", function () {
    reset();
    running = true;
    restartLoop();
  });

  reset();
})();
