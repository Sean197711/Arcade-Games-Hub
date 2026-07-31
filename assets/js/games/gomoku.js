/* 五子棋（人机对战） */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var SIZE = 15;
  var canvas = document.getElementById("game-canvas");
  var ctx = canvas.getContext("2d");
  var CELL = canvas.width / (SIZE + 1);
  var OFFSET = CELL;
  var statusEl = document.getElementById("status");
  var toast = document.getElementById("toast");

  var board, playerTurn, over, thinking;

  function reset() {
    board = [];
    for (var r = 0; r < SIZE; r++) board.push(new Array(SIZE).fill(0));
    playerTurn = true;
    over = false;
    thinking = false;
    statusEl.textContent = msg("yourTurn", "轮到你落子（黑棋）");
    draw();
  }

  function draw() {
    ctx.fillStyle = "#f5c96b";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#8a5a2b";
    ctx.lineWidth = 1.5;
    for (var i = 0; i < SIZE; i++) {
      ctx.beginPath();
      ctx.moveTo(OFFSET, OFFSET + i * CELL);
      ctx.lineTo(OFFSET + (SIZE - 1) * CELL, OFFSET + i * CELL);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(OFFSET + i * CELL, OFFSET);
      ctx.lineTo(OFFSET + i * CELL, OFFSET + (SIZE - 1) * CELL);
      ctx.stroke();
    }

    // 星位
    var stars = [3, 7, 11];
    ctx.fillStyle = "#8a5a2b";
    stars.forEach(function (r) {
      stars.forEach(function (c) {
        ctx.beginPath();
        ctx.arc(OFFSET + c * CELL, OFFSET + r * CELL, 4, 0, Math.PI * 2);
        ctx.fill();
      });
    });

    for (var r2 = 0; r2 < SIZE; r2++) {
      for (var c2 = 0; c2 < SIZE; c2++) {
        if (board[r2][c2] !== 0) drawStone(r2, c2, board[r2][c2]);
      }
    }
  }

  function drawStone(r, c, color) {
    var x = OFFSET + c * CELL, y = OFFSET + r * CELL;
    var radius = CELL * 0.42;
    var grad = ctx.createRadialGradient(x - 4, y - 4, 2, x, y, radius);
    if (color === 1) {
      grad.addColorStop(0, "#666");
      grad.addColorStop(1, "#111");
    } else {
      grad.addColorStop(0, "#fff");
      grad.addColorStop(1, "#ccc");
    }
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = color === 1 ? "#000" : "#999";
    ctx.stroke();
  }

  function checkWin(r, c, color) {
    var dirs = [[1, 0], [0, 1], [1, 1], [1, -1]];
    for (var d = 0; d < dirs.length; d++) {
      var count = 1;
      for (var s = 1; s <= 1; s++) {
        // 两个方向延伸
      }
      for (var sign = -1; sign <= 1; sign += 2) {
        var nr = r + dirs[d][0] * sign, nc = c + dirs[d][1] * sign;
        while (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && board[nr][nc] === color) {
          count++;
          nr += dirs[d][0] * sign;
          nc += dirs[d][1] * sign;
        }
      }
      if (count >= 5) return true;
    }
    return false;
  }

  // 评估某个空点放 color 棋子的价值
  function evaluate(r, c, color) {
    var score = 0;
    var dirs = [[1, 0], [0, 1], [1, 1], [1, -1]];
    var table = { 1: 10, 2: 100, 3: 1000, 4: 10000, 5: 100000 };
    dirs.forEach(function (d) {
      var total = 1, openEnds = 0;
      [-1, 1].forEach(function (sign) {
        var nr = r + d[0] * sign, nc = c + d[1] * sign;
        var run = 0;
        while (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && board[nr][nc] === color) {
          run++;
          nr += d[0] * sign;
          nc += d[1] * sign;
        }
        total += run;
        if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && board[nr][nc] === 0) openEnds++;
      });
      var key = Math.min(total, 5);
      score += table[key] * (openEnds > 0 ? openEnds : 0.1);
    });
    return score;
  }

  function aiMove() {
    var bestScore = -1, bestMoves = [];
    var hasStone = board.some(function (row) { return row.some(function (v) { return v !== 0; }); });

    if (!hasStone) {
      place(7, 7, 2);
      return;
    }

    for (var r = 0; r < SIZE; r++) {
      for (var c = 0; c < SIZE; c++) {
        if (board[r][c] !== 0) continue;
        if (!nearStone(r, c)) continue;
        var attack = evaluate(r, c, 2);
        var defense = evaluate(r, c, 1);
        var s = attack * 1.1 + defense;
        if (s > bestScore) { bestScore = s; bestMoves = [[r, c]]; }
        else if (s === bestScore) bestMoves.push([r, c]);
      }
    }

    var pick = bestMoves[Math.floor(Math.random() * bestMoves.length)];
    place(pick[0], pick[1], 2);
  }

  function nearStone(r, c) {
    for (var dr = -2; dr <= 2; dr++)
      for (var dc = -2; dc <= 2; dc++) {
        var nr = r + dr, nc = c + dc;
        if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && board[nr][nc] !== 0) return true;
      }
    return false;
  }

  function place(r, c, color) {
    board[r][c] = color;
    draw();
    if (checkWin(r, c, color)) {
      over = true;
      if (color === 1) {
        statusEl.textContent = msg("youWin", "🎉 你赢了！");
        showToast(msg("youWinToast", "🎉 恭喜，五子连珠！"));
      } else {
        statusEl.textContent = msg("aiWins", "电脑获胜，再来一局？");
        showToast(msg("aiWinsToast", "电脑获胜，点击重新开始再战！"));
      }
      return;
    }
    if (board.every(function (row) { return row.every(function (v) { return v !== 0; }); })) {
      over = true;
      statusEl.textContent = msg("draw", "平局！");
      showToast(msg("drawToast", "棋盘已满，平局！"));
      return;
    }
    if (color === 2) {
      playerTurn = true;
      thinking = false;
      statusEl.textContent = msg("yourTurn", "轮到你落子（黑棋）");
    }
  }

  canvas.addEventListener("click", function (e) {
    if (over || !playerTurn || thinking) return;
    var rect = canvas.getBoundingClientRect();
    var scaleX = canvas.width / rect.width;
    var scaleY = canvas.height / rect.height;
    var x = (e.clientX - rect.left) * scaleX;
    var y = (e.clientY - rect.top) * scaleY;
    var c = Math.round((x - OFFSET) / CELL);
    var r = Math.round((y - OFFSET) / CELL);
    if (r < 0 || r >= SIZE || c < 0 || c >= SIZE) return;
    if (board[r][c] !== 0) return;

    playerTurn = false;
    thinking = true;
    place(r, c, 1);
    if (over) return;
    statusEl.textContent = msg("thinking", "电脑思考中…");
    setTimeout(aiMove, 350);
  });

  // 触屏
  canvas.addEventListener("touchend", function (e) {
    e.preventDefault();
    var t = e.changedTouches[0];
    canvas.dispatchEvent(new MouseEvent("click", { clientX: t.clientX, clientY: t.clientY }));
  });

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2400);
  }

  document.getElementById("btn-restart").addEventListener("click", reset);

  reset();
})();
