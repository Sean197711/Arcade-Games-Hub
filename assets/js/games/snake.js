/* 贪吃蛇 */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var canvas = document.getElementById("game-canvas");
  var ctx = canvas.getContext("2d");
  var GRID = 20, CELL = canvas.width / GRID;
  var scoreEl = document.getElementById("score");
  var bestEl = document.getElementById("best");
  var toast = document.getElementById("toast");

  var snake, dir, nextDir, food, score, best, speed, timer, running, dead;

  best = parseInt(localStorage.getItem("snake_best") || "0", 10);
  bestEl.textContent = best;

  function reset() {
    snake = [{ x: 10, y: 10 }, { x: 9, y: 10 }, { x: 8, y: 10 }];
    dir = { x: 1, y: 0 };
    nextDir = dir;
    score = 0;
    speed = 160;
    dead = false;
    scoreEl.textContent = "0";
    placeFood();
    draw();
  }

  function placeFood() {
    while (true) {
      var f = { x: Math.floor(Math.random() * GRID), y: Math.floor(Math.random() * GRID) };
      var onSnake = snake.some(function (s) { return s.x === f.x && s.y === f.y; });
      if (!onSnake) { food = f; return; }
    }
  }

  function tick() {
    dir = nextDir;
    var head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

    if (head.x < 0 || head.y < 0 || head.x >= GRID || head.y >= GRID ||
        snake.some(function (s) { return s.x === head.x && s.y === head.y; })) {
      gameOver();
      return;
    }

    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
      score += 10;
      scoreEl.textContent = score;
      if (score > best) {
        best = score;
        bestEl.textContent = best;
        localStorage.setItem("snake_best", String(best));
      }
      if (speed > 70) speed -= 4;
      placeFood();
      restartLoop();
    } else {
      snake.pop();
    }
    draw();
  }

  function draw() {
    ctx.fillStyle = "#141428";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 网格
    ctx.strokeStyle = "rgba(255,255,255,0.05)";
    for (var i = 1; i < GRID; i++) {
      ctx.beginPath(); ctx.moveTo(i * CELL, 0); ctx.lineTo(i * CELL, canvas.height); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, i * CELL); ctx.lineTo(canvas.width, i * CELL); ctx.stroke();
    }

    // 食物
    ctx.fillStyle = "#ff5da2";
    ctx.beginPath();
    ctx.arc(food.x * CELL + CELL / 2, food.y * CELL + CELL / 2, CELL / 2 - 3, 0, Math.PI * 2);
    ctx.fill();

    // 蛇
    snake.forEach(function (s, idx) {
      ctx.fillStyle = idx === 0 ? "#ffd23f" : "#4ade80";
      var pad = idx === 0 ? 2 : 3;
      roundRect(s.x * CELL + pad, s.y * CELL + pad, CELL - pad * 2, CELL - pad * 2, 5);
    });
  }

  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
    ctx.fill();
  }

  function restartLoop() {
    clearInterval(timer);
    timer = setInterval(tick, speed);
  }

  function gameOver() {
    clearInterval(timer);
    running = false;
    dead = true;
    showToast(msg("gameOver", "游戏结束！得分 {score}", { score: score }));
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2000);
  }

  function start() {
    if (running) return;
    if (dead) reset();
    running = true;
    restartLoop();
  }

  function pause() {
    if (!running) return;
    clearInterval(timer);
    running = false;
    showToast(msg("paused", "已暂停"));
  }

  function setDir(x, y) {
    if (dir.x === -x && dir.y === -y) return; // 禁止掉头
    nextDir = { x: x, y: y };
  }

  document.addEventListener("keydown", function (e) {
    var k = e.key;
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].indexOf(k) !== -1) e.preventDefault();
    if (k === "ArrowUp" || k === "w" || k === "W") setDir(0, -1);
    else if (k === "ArrowDown" || k === "s" || k === "S") setDir(0, 1);
    else if (k === "ArrowLeft" || k === "a" || k === "A") setDir(-1, 0);
    else if (k === "ArrowRight" || k === "d" || k === "D") setDir(1, 0);
    else if (k === " ") { running ? pause() : start(); }
  });

  document.querySelectorAll(".pad button").forEach(function (btn) {
    btn.addEventListener("touchstart", function (e) {
      e.preventDefault();
      var d = btn.getAttribute("data-dir");
      if (d === "up") setDir(0, -1);
      else if (d === "down") setDir(0, 1);
      else if (d === "left") setDir(-1, 0);
      else if (d === "right") setDir(1, 0);
      if (!running) start();
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
