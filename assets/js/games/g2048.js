/* 2048 */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var SIZE = 4;
  var boardEl = document.getElementById("board");
  var scoreEl = document.getElementById("score");
  var bestEl = document.getElementById("best");
  var toast = document.getElementById("toast");

  var COLORS = {
    2: "#3ec1f3", 4: "#4ade80", 8: "#ffd23f", 16: "#ff8a3d",
    32: "#ff5da2", 64: "#ff5252", 128: "#7c4dff", 256: "#9d4edd",
    512: "#00b4d8", 1024: "#f4a261", 2048: "#ffd700"
  };

  var grid, score, best, won, over;
  best = parseInt(localStorage.getItem("g2048_best") || "0", 10);
  bestEl.textContent = best;

  function reset() {
    grid = [];
    for (var r = 0; r < SIZE; r++) {
      grid.push([0, 0, 0, 0]);
    }
    score = 0;
    won = false;
    over = false;
    scoreEl.textContent = "0";
    addTile();
    addTile();
    render();
  }

  function addTile() {
    var empty = [];
    for (var r = 0; r < SIZE; r++)
      for (var c = 0; c < SIZE; c++)
        if (grid[r][c] === 0) empty.push([r, c]);
    if (!empty.length) return;
    var p = empty[Math.floor(Math.random() * empty.length)];
    grid[p[0]][p[1]] = Math.random() < 0.9 ? 2 : 4;
  }

  function render() {
    boardEl.innerHTML = "";
    for (var r = 0; r < SIZE; r++) {
      for (var c = 0; c < SIZE; c++) {
        var v = grid[r][c];
        var cell = document.createElement("div");
        cell.className = "cell-2048";
        if (v) {
          cell.textContent = v;
          cell.style.background = COLORS[v] || "#1e1e2f";
          if (v >= 128) cell.style.color = "#fff";
          if (v >= 1024) cell.style.fontSize = "1.4rem";
        }
        boardEl.appendChild(cell);
      }
    }
  }

  function slide(row) {
    var arr = row.filter(function (v) { return v !== 0; });
    for (var i = 0; i < arr.length - 1; i++) {
      if (arr[i] === arr[i + 1]) {
        arr[i] *= 2;
        score += arr[i];
        if (arr[i] === 2048 && !won) {
          won = true;
          showToast(msg("win", "🎉 合成 2048！还能继续挑战更高分"));
        }
        arr.splice(i + 1, 1);
      }
    }
    while (arr.length < SIZE) arr.push(0);
    return arr;
  }

  function move(dir) {
    if (over) return;
    var before = JSON.stringify(grid);

    if (dir === "left" || dir === "right") {
      for (var r = 0; r < SIZE; r++) {
        var row = grid[r].slice();
        if (dir === "right") row.reverse();
        row = slide(row);
        if (dir === "right") row.reverse();
        grid[r] = row;
      }
    } else {
      for (var c = 0; c < SIZE; c++) {
        var col = [grid[0][c], grid[1][c], grid[2][c], grid[3][c]];
        if (dir === "down") col.reverse();
        col = slide(col);
        if (dir === "down") col.reverse();
        for (var r2 = 0; r2 < SIZE; r2++) grid[r2][c] = col[r2];
      }
    }

    if (JSON.stringify(grid) === before) return; // 无变化

    addTile();
    scoreEl.textContent = score;
    if (score > best) {
      best = score;
      bestEl.textContent = best;
      localStorage.setItem("g2048_best", String(best));
    }
    render();

    if (!canMove()) {
      over = true;
      showToast(msg("gameOver", "游戏结束！得分 {score}", { score: score }));
    }
  }

  function canMove() {
    for (var r = 0; r < SIZE; r++)
      for (var c = 0; c < SIZE; c++) {
        if (grid[r][c] === 0) return true;
        if (c < SIZE - 1 && grid[r][c] === grid[r][c + 1]) return true;
        if (r < SIZE - 1 && grid[r][c] === grid[r + 1][c]) return true;
      }
    return false;
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2200);
  }

  document.addEventListener("keydown", function (e) {
    var map = { ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down",
                a: "left", d: "right", w: "up", s: "down",
                A: "left", D: "right", W: "up", S: "down" };
    if (map[e.key]) {
      e.preventDefault();
      move(map[e.key]);
    }
  });

  // 触屏滑动
  var sx = 0, sy = 0;
  boardEl.addEventListener("touchstart", function (e) {
    sx = e.touches[0].clientX;
    sy = e.touches[0].clientY;
  }, { passive: true });
  boardEl.addEventListener("touchend", function (e) {
    var dx = e.changedTouches[0].clientX - sx;
    var dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) < 24 && Math.abs(dy) < 24) return;
    if (Math.abs(dx) > Math.abs(dy)) move(dx > 0 ? "right" : "left");
    else move(dy > 0 ? "down" : "up");
  }, { passive: true });

  document.getElementById("btn-restart").addEventListener("click", function () {
    reset();
    showToast(msg("newGame", "新的一局开始！"));
  });

  reset();
})();
