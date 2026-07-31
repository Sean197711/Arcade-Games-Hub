/* 记忆翻牌 */
(function () {
  "use strict";
  var I18N = window.GAME_I18N || {};
  function msg(key, def, vars) {
    var s = I18N[key] || def;
    if (vars) for (var k in vars) s = s.replace("{" + k + "}", vars[k]);
    return s;
  }
  var boardEl = document.getElementById("board");
  var movesEl = document.getElementById("moves");
  var pairsEl = document.getElementById("pairs");
  var timeEl = document.getElementById("time");
  var toast = document.getElementById("toast");

  var ICONS = ["🍎", "🚀", "🎸", "🌈", "🐱", "⚽", "🍩", "🎁"];
  var TOTAL = ICONS.length;

  var deck, flipped, matched, moves, lock, seconds, timer, started;

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function reset() {
    deck = shuffle(ICONS.concat(ICONS));
    flipped = [];
    matched = 0;
    moves = 0;
    lock = false;
    seconds = 0;
    started = false;
    clearInterval(timer);
    movesEl.textContent = "0";
    pairsEl.textContent = "0 / " + TOTAL;
    timeEl.textContent = "0";
    render();
  }

  function render() {
    boardEl.innerHTML = "";
    deck.forEach(function (icon, i) {
      var card = document.createElement("div");
      card.className = "card-mem";
      card.setAttribute("data-i", i);
      card.setAttribute("role", "button");
      card.setAttribute("aria-label", msg("card", "卡片 {n}", { n: i + 1 }));
      card.textContent = icon;
      boardEl.appendChild(card);
    });
  }

  function startTimer() {
    started = true;
    timer = setInterval(function () {
      seconds++;
      timeEl.textContent = seconds;
    }, 1000);
  }

  boardEl.addEventListener("click", function (e) {
    var card = e.target.closest(".card-mem");
    if (!card || lock) return;
    if (card.classList.contains("flipped") || card.classList.contains("matched")) return;

    if (!started) startTimer();

    card.classList.add("flipped");
    flipped.push(card);

    if (flipped.length === 2) {
      moves++;
      movesEl.textContent = moves;
      var a = flipped[0], b = flipped[1];
      if (a.textContent === b.textContent) {
        a.classList.add("matched");
        b.classList.add("matched");
        matched++;
        pairsEl.textContent = matched + " / " + TOTAL;
        flipped = [];
        if (matched === TOTAL) {
          clearInterval(timer);
          showToast(msg("win", "🎉 全部配对成功！{moves} 步 · {time} 秒", { moves: moves, time: seconds }));
        }
      } else {
        lock = true;
        setTimeout(function () {
          a.classList.remove("flipped");
          b.classList.remove("flipped");
          flipped = [];
          lock = false;
        }, 750);
      }
    }
  });

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 3000);
  }

  document.getElementById("btn-restart").addEventListener("click", reset);

  reset();
})();
