/* 扫雷 */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var boardEl = document.getElementById("board");
  var minesEl = document.getElementById("mines");
  var timeEl = document.getElementById("time");
  var statusEl = document.getElementById("status");
  var toast = document.getElementById("toast");
  var diffSel = document.getElementById("difficulty");

  var DIFFS = {
    easy: { rows: 9, cols: 9, mines: 10, name: "初级" },
    medium: { rows: 12, cols: 12, mines: 24, name: "中级" },
    hard: { rows: 16, cols: 16, mines: 40, name: "高级" }
  };

  var ROWS, COLS, MINES;
  var cells, started, over, flags, opened, timer, seconds;

  var NUM_COLORS = ["", "#3ec1f3", "#4ade80", "#ff5252", "#7c4dff", "#ff8a3d", "#00b4d8", "#ff5da2", "#666"];

  function reset() {
    var d = DIFFS[diffSel.value] || DIFFS.easy;
    ROWS = d.rows; COLS = d.cols; MINES = d.mines;
    cells = [];
    for (var r = 0; r < ROWS; r++) {
      var row = [];
      for (var c = 0; c < COLS; c++) row.push({ mine: false, open: false, flag: false, count: 0 });
      cells.push(row);
    }
    started = false;
    over = false;
    flags = 0;
    opened = 0;
    seconds = 0;
    clearInterval(timer);
    timeEl.textContent = "0";
    minesEl.textContent = MINES;
    statusEl.textContent = "🙂";
    render();
  }

  function plantMines(safeR, safeC) {
    var placed = 0;
    while (placed < MINES) {
      var r = Math.floor(Math.random() * ROWS);
      var c = Math.floor(Math.random() * COLS);
      if (cells[r][c].mine) continue;
      if (Math.abs(r - safeR) <= 1 && Math.abs(c - safeC) <= 1) continue; // 首点安全区
      cells[r][c].mine = true;
      placed++;
    }
    for (var r2 = 0; r2 < ROWS; r2++)
      for (var c2 = 0; c2 < COLS; c2++)
        cells[r2][c2].count = countAround(r2, c2);
  }

  function countAround(r, c) {
    var n = 0;
    for (var dr = -1; dr <= 1; dr++)
      for (var dc = -1; dc <= 1; dc++) {
        var nr = r + dr, nc = c + dc;
        if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && cells[nr][nc].mine) n++;
      }
    return n;
  }

  function render() {
    boardEl.innerHTML = "";
    boardEl.style.gridTemplateColumns = "repeat(" + COLS + ", 34px)";
    for (var r = 0; r < ROWS; r++) {
      for (var c = 0; c < COLS; c++) {
        var el = document.createElement("div");
        el.className = "cell-mine";
        el.setAttribute("data-r", r);
        el.setAttribute("data-c", c);
        el.setAttribute("role", "button");
        var cell = cells[r][c];
        if (cell.open) {
          el.classList.add("open");
          if (cell.mine) { el.classList.add("boom"); el.textContent = "💥"; }
          else if (cell.count > 0) {
            el.textContent = cell.count;
            el.style.color = NUM_COLORS[cell.count];
          }
        } else if (cell.flag) {
          el.classList.add("flag");
          el.textContent = "🚩";
        }
        boardEl.appendChild(el);
      }
    }
  }

  function startTimer() {
    timer = setInterval(function () {
      seconds++;
      timeEl.textContent = seconds;
    }, 1000);
  }

  function openCell(r, c) {
    if (over) return;
    var cell = cells[r][c];
    if (cell.open || cell.flag) return;

    if (!started) {
      started = true;
      plantMines(r, c);
      startTimer();
    }

    if (cell.mine) {
      // 游戏结束，翻开所有雷
      over = true;
      clearInterval(timer);
      for (var r2 = 0; r2 < ROWS; r2++)
        for (var c2 = 0; c2 < COLS; c2++)
          if (cells[r2][c2].mine) cells[r2][c2].open = true;
      cell.open = true;
      statusEl.textContent = "😵";
      render();
      showToast(msg("boom", "踩到地雷了！用时 {time} 秒", { time: seconds }));
      return;
    }

    floodOpen(r, c);
    render();
    checkWin();
  }

  function floodOpen(r, c) {
    var stack = [[r, c]];
    while (stack.length) {
      var p = stack.pop();
      var cr = p[0], cc = p[1];
      var cell = cells[cr][cc];
      if (cell.open || cell.flag) continue;
      cell.open = true;
      opened++;
      if (cell.count === 0) {
        for (var dr = -1; dr <= 1; dr++)
          for (var dc = -1; dc <= 1; dc++) {
            var nr = cr + dr, nc = cc + dc;
            if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && !cells[nr][nc].open)
              stack.push([nr, nc]);
          }
      }
    }
  }

  function toggleFlag(r, c) {
    if (over || !started && false) return;
    var cell = cells[r][c];
    if (cell.open) return;
    cell.flag = !cell.flag;
    flags += cell.flag ? 1 : -1;
    minesEl.textContent = MINES - flags;
    render();
  }

  function checkWin() {
    if (opened === ROWS * COLS - MINES) {
      over = true;
      clearInterval(timer);
      statusEl.textContent = "😎";
      showToast(msg("win", "🎉 扫雷成功！用时 {time} 秒", { time: seconds }));
    }
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2400);
  }

  // 点击翻开 / 右键插旗 / 长按插旗
  var pressTimer = null, longPressed = false;

  boardEl.addEventListener("click", function (e) {
    if (longPressed) { longPressed = false; return; }
    var t = e.target.closest(".cell-mine");
    if (!t) return;
    openCell(+t.getAttribute("data-r"), +t.getAttribute("data-c"));
  });

  boardEl.addEventListener("contextmenu", function (e) {
    e.preventDefault();
    var t = e.target.closest(".cell-mine");
    if (!t) return;
    toggleFlag(+t.getAttribute("data-r"), +t.getAttribute("data-c"));
  });

  boardEl.addEventListener("touchstart", function (e) {
    var t = e.target.closest(".cell-mine");
    if (!t) return;
    var r = +t.getAttribute("data-r"), c = +t.getAttribute("data-c");
    longPressed = false;
    pressTimer = setTimeout(function () {
      longPressed = true;
      toggleFlag(r, c);
    }, 450);
  }, { passive: true });

  boardEl.addEventListener("touchend", function () {
    clearTimeout(pressTimer);
  });

  document.getElementById("btn-restart").addEventListener("click", reset);
  diffSel.addEventListener("change", reset);

  reset();
})();
