# -*- coding: utf-8 -*-
"""
多语言静态页面生成脚本
用法：python3 tools/build_i18n.py
生成：中文(根目录) + en/es/ar/ru/ja/ko 六个语言子目录，共 49 个页面 + sitemap.xml
部署前请把 BASE 改成真实域名。
"""
import json
import os

BASE = "https://games-hub.cc"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LASTMOD = "2026-07-26"

LANG_ORDER = ["en", "zh", "es", "ar", "ru", "ja", "ko"]
DEFAULT_LANG = "en"  # 默认语言：根目录 /

COMMON = {
    "zh": dict(code="zh", htmlLang="zh-CN", dir="ltr", ogLocale="zh_CN", native="中文",
        siteName="街机小游戏乐园", home="首页", navGames="全部游戏", navAbout="关于本站",
        moreGames="🕹️ 更多游戏", howTo="🎯 玩法说明", tips="💡 高分技巧",
        start="开始", pause="暂停", restart="重新开始", playBtn="开始游戏",
        footer="© 2026 街机小游戏乐园 · 免费在线小游戏，即点即玩",
        stageAria="游戏区", breadcrumbAria="面包屑",
        score="当前得分", best="历史最高", lines="消除行数", level="等级", nxt="下一个",
        minesLeft="剩余地雷", status="状态", time="用时（秒）", moves="步数", pairs="已配对",
        gameStatus="对局状态", difficulty="难度：",
        up="向上", down="向下", left="向左", right="向右", rotate="旋转", drop="直接落底",
        hardDrop="加速下落"),
    "en": dict(code="en", htmlLang="en", dir="ltr", ogLocale="en_US", native="English",
        siteName="Arcade Games Hub", home="Home", navGames="All games", navAbout="About",
        moreGames="🕹️ More games", howTo="🎯 How to play", tips="💡 Pro tips",
        start="Start", pause="Pause", restart="Restart", playBtn="Play",
        footer="© 2026 Arcade Games Hub · Free online games, play instantly",
        stageAria="Game area", breadcrumbAria="Breadcrumb",
        score="Score", best="Best", lines="Lines", level="Level", nxt="Next",
        minesLeft="Mines left", status="Status", time="Time (s)", moves="Moves", pairs="Pairs",
        gameStatus="Game status", difficulty="Difficulty: ",
        up="Up", down="Down", left="Left", right="Right", rotate="Rotate", drop="Hard drop",
        hardDrop="Soft drop"),
    "es": dict(code="es", htmlLang="es", dir="ltr", ogLocale="es_ES", native="Español",
        siteName="Arcade de Minijuegos", home="Inicio", navGames="Todos los juegos", navAbout="Acerca de",
        moreGames="🕹️ Más juegos", howTo="🎯 Cómo jugar", tips="💡 Consejos",
        start="Comenzar", pause="Pausa", restart="Reiniciar", playBtn="Jugar",
        footer="© 2026 Arcade de Minijuegos · Juegos en línea gratis, juega al instante",
        stageAria="Zona de juego", breadcrumbAria="Migas de pan",
        score="Puntos", best="Récord", lines="Líneas", level="Nivel", nxt="Siguiente",
        minesLeft="Minas restantes", status="Estado", time="Tiempo (s)", moves="Movimientos", pairs="Parejas",
        gameStatus="Estado de la partida", difficulty="Dificultad: ",
        up="Arriba", down="Abajo", left="Izquierda", right="Derecha", rotate="Girar", drop="Caída instantánea",
        hardDrop="Caída rápida"),
    "ar": dict(code="ar", htmlLang="ar", dir="rtl", ogLocale="ar_AR", native="العربية",
        siteName="ألعاب الأركيد", home="الرئيسية", navGames="كل الألعاب", navAbout="عن الموقع",
        moreGames="🕹️ المزيد من الألعاب", howTo="🎯 طريقة اللعب", tips="💡 نصائح",
        start="ابدأ", pause="إيقاف مؤقت", restart="إعادة", playBtn="العب الآن",
        footer="© 2026 ألعاب الأركيد · ألعاب مجانية عبر الإنترنت، العب فورًا",
        stageAria="منطقة اللعب", breadcrumbAria="مسار التنقل",
        score="النقاط", best="الأفضل", lines="الصفوف", level="المستوى", nxt="التالية",
        minesLeft="الألغام المتبقية", status="الحالة", time="الوقت (ث)", moves="المحاولات", pairs="الأزواج",
        gameStatus="حالة المباراة", difficulty="الصعوبة: ",
        up="أعلى", down="أسفل", left="يسار", right="يمين", rotate="تدوير", drop="إسقاط فوري",
        hardDrop="نزول سريع"),
    "ru": dict(code="ru", htmlLang="ru", dir="ltr", ogLocale="ru_RU", native="Русский",
        siteName="Аркадные мини-игры", home="Главная", navGames="Все игры", navAbout="О сайте",
        moreGames="🕹️ Ещё игры", howTo="🎯 Как играть", tips="💡 Советы",
        start="Старт", pause="Пауза", restart="Заново", playBtn="Играть",
        footer="© 2026 Аркадные мини-игры · Бесплатные онлайн-игры — играйте сразу",
        stageAria="Игровое поле", breadcrumbAria="Хлебные крошки",
        score="Счёт", best="Рекорд", lines="Линии", level="Уровень", nxt="Далее",
        minesLeft="Мин осталось", status="Статус", time="Время (с)", moves="Ходы", pairs="Пары",
        gameStatus="Статус партии", difficulty="Сложность: ",
        up="Вверх", down="Вниз", left="Влево", right="Вправо", rotate="Поворот", drop="Сбросить",
        hardDrop="Ускорить"),
    "ja": dict(code="ja", htmlLang="ja", dir="ltr", ogLocale="ja_JP", native="日本語",
        siteName="ミニゲームランド", home="ホーム", navGames="ゲーム一覧", navAbout="このサイトについて",
        moreGames="🕹️ 他のゲーム", howTo="🎯 遊び方", tips="💡 上達のコツ",
        start="スタート", pause="一時停止", restart="もう一度", playBtn="プレイ",
        footer="© 2026 ミニゲームランド · 無料オンラインゲーム、すぐに遊べる",
        stageAria="ゲームエリア", breadcrumbAria="パンくずリスト",
        score="スコア", best="ベスト", lines="消去ライン", level="レベル", nxt="次",
        minesLeft="残り地雷", status="状態", time="タイム（秒）", moves="手数", pairs="ペア成立",
        gameStatus="対局状態", difficulty="難易度：",
        up="上", down="下", left="左", right="右", rotate="回転", drop="即落下",
        hardDrop="高速落下"),
    "ko": dict(code="ko", htmlLang="ko", dir="ltr", ogLocale="ko_KR", native="한국어",
        siteName="미니게임 놀이터", home="홈", navGames="전체 게임", navAbout="사이트 소개",
        moreGames="🕹️ 다른 게임", howTo="🎯 게임 방법", tips="💡 고득점 팁",
        start="시작", pause="일시정지", restart="다시 시작", playBtn="시작하기",
        footer="© 2026 미니게임 놀이터 · 무료 온라인 게임, 바로 플레이",
        stageAria="게임 영역", breadcrumbAria="탐색 경로",
        score="점수", best="최고 기록", lines="지운 줄", level="레벨", nxt="다음",
        minesLeft="남은 지뢰", status="상태", time="시간(초)", moves="횟수", pairs="맞춘 짝",
        gameStatus="대국 상태", difficulty="난이도: ",
        up="위", down="아래", left="왼쪽", right="오른쪽", rotate="회전", drop="즉시 낙하",
        hardDrop="빠른 낙하"),
}

HOME = {
    "zh": dict(
        badge="🎮 全部免费 · 即点即玩",
        h1Pre="经典", h1Hl="小游戏", h1Post="合集<br />打开浏览器就能玩",
        heroP="贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌——6 款陪伴了几代人的经典小游戏，无需下载、无需注册，电脑手机都能流畅游玩。",
        stats=["🕹️ 6 款游戏", "⚡ 零加载等待", "📱 支持手机", "🆓 永久免费"],
        gamesTitle="全部游戏", gamesDesc="挑一款喜欢的，点击「开始游戏」立即开玩。",
        aboutH2="关于街机小游戏乐园",
        aboutP="街机小游戏乐园是一个免费的在线小游戏合集网站。我们相信好游戏不需要复杂的下载和注册流程——点开网页，即刻开玩。站内所有游戏均为纯前端实现，加载快、无广告打扰，并针对手机和电脑都做了适配。",
        chooseH2="为什么选择在线网页小游戏？",
        chooseP="网页小游戏无需安装、不占存储空间，通勤路上、课间休息、工作间隙都能随时来一局。经典的贪吃蛇和俄罗斯方块能锻炼反应速度，2048 和扫雷考验逻辑思维，五子棋和记忆翻牌则适合静下心来动脑。无论你是想打发碎片时间，还是想认真挑战高分，这里都有适合你的选择。",
        metaTitle="街机小游戏乐园 - 免费在线小游戏合集 | 贪吃蛇·2048·俄罗斯方块·扫雷",
        metaDesc="街机小游戏乐园收录 6 款经典免费在线小游戏：贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌。无需下载、无需注册，打开网页即点即玩，支持电脑和手机。",
        metaKeywords="小游戏,在线小游戏,免费小游戏,网页游戏,贪吃蛇,2048,俄罗斯方块,扫雷,五子棋,记忆翻牌,休闲游戏"),
    "en": dict(
        badge="🎮 100% Free · Play instantly",
        h1Pre="Classic", h1Hl="Mini Games", h1Post="<br />Play right in your browser",
        heroP="Snake, 2048, Tetris, Minesweeper, Gomoku and Memory Match — six timeless classics enjoyed for generations. No downloads, no sign-up, smooth play on desktop and mobile.",
        stats=["🕹️ 6 games", "⚡ Loads instantly", "📱 Mobile friendly", "🆓 Free forever"],
        gamesTitle="All games", gamesDesc="Pick a favorite and hit “Play” to jump right in.",
        aboutH2="About Arcade Games Hub",
        aboutP="Arcade Games Hub is a free online collection of mini games. We believe great games need no complicated downloads or sign-ups — open the page and play. Every game is built with pure front-end tech: fast loading, no ads, and fully adapted for both phones and computers.",
        chooseH2="Why play browser mini games?",
        chooseP="Browser mini games need no installation and take up no storage. Play a quick round on your commute, during a break or between tasks. Snake and Tetris sharpen your reflexes, 2048 and Minesweeper train your logic, while Gomoku and Memory Match are perfect for quiet focus. Whether you want to kill a few minutes or chase a new high score, there is something here for you.",
        metaTitle="Arcade Games Hub - Free Online Mini Games | Snake, 2048, Tetris & More",
        metaDesc="Play 6 classic mini games free online: Snake, 2048, Tetris, Minesweeper, Gomoku and Memory Match. No downloads, no sign-up — instant play on desktop and mobile.",
        metaKeywords="mini games,online games,free games,browser games,snake,2048,tetris,minesweeper,gomoku,memory match,casual games"),
    "es": dict(
        badge="🎮 Todo gratis · Juega al instante",
        h1Pre="Clásicos", h1Hl="minijuegos", h1Post="<br />Juega directo en tu navegador",
        heroP="Snake, 2048, Tetris, Buscaminas, Gomoku y Memoria: seis clásicos que han acompañado a varias generaciones. Sin descargas ni registros, en PC y móvil.",
        stats=["🕹️ 6 juegos", "⚡ Carga al instante", "📱 Compatible con móvil", "🆓 Gratis para siempre"],
        gamesTitle="Todos los juegos", gamesDesc="Elige tu favorito y pulsa «Jugar» para empezar.",
        aboutH2="Acerca de Arcade de Minijuegos",
        aboutP="Arcade de Minijuegos es una colección gratuita de juegos en línea. Creemos que un buen juego no necesita descargas ni registros complicados: abre la página y juega. Todos los juegos están hechos con tecnología web pura: cargan rápido, sin anuncios, y están adaptados a móvil y PC.",
        chooseH2="¿Por qué jugar a minijuegos en el navegador?",
        chooseP="Los minijuegos web no se instalan ni ocupan espacio. Juega una partida rápida en el metro, en el recreo o entre tareas. Snake y Tetris entrenan tus reflejos, 2048 y Buscaminas tu lógica, y Gomoku y Memoria son perfectos para concentrarte en calma. Tanto si quieres pasar el rato como batir tu récord, aquí hay algo para ti.",
        metaTitle="Arcade de Minijuegos - Juegos en línea gratis | Snake, 2048, Tetris",
        metaDesc="Juega gratis a 6 minijuegos clásicos en línea: Snake, 2048, Tetris, Buscaminas, Gomoku y Memoria. Sin descargas ni registros, juega al instante en PC y móvil.",
        metaKeywords="minijuegos,juegos online,juegos gratis,juegos de navegador,snake,2048,tetris,buscaminas,gomoku,memoria,juegos casuales"),
    "ar": dict(
        badge="🎮 مجاني بالكامل · العب فورًا",
        h1Pre="ألعاب", h1Hl="كلاسيكية", h1Post="<br />العب مباشرة من متصفحك",
        heroP="الثعبان، 2048، تتريس، كانسة الألغام، غوموكو ولعبة الذاكرة — ست ألعاب كلاسيكية رافقت أجيالًا. بدون تنزيل أو تسجيل، وتعمل بسلاسة على الحاسوب والجوال.",
        stats=["🕹️ 6 ألعاب", "⚡ تحميل فوري", "📱 تدعم الجوال", "🆓 مجانية دائمًا"],
        gamesTitle="كل الألعاب", gamesDesc="اختر لعبتك المفضلة واضغط «العب الآن» لتبدأ فورًا.",
        aboutH2="عن موقع ألعاب الأركيد",
        aboutP="ألعاب الأركيد مجموعة مجانية من الألعاب المصغّرة عبر الإنترنت. نؤمن بأن اللعبة الجيدة لا تحتاج تنزيلًا أو تسجيلًا معقدًا — افتح الصفحة والعب. جميع الألعاب مبنية بتقنيات الويب الخالصة: تحميل سريع، بلا إعلانات، ومتكيفة مع الجوال والحاسوب.",
        chooseH2="لماذا ألعاب المتصفح المصغّرة؟",
        chooseP="ألعاب المتصفح لا تحتاج تثبيتًا ولا تشغل مساحة. العب جولة سريعة في المواصلات أو أثناء الاستراحة أو بين المهام. الثعبان وتتريس يصقلان ردود أفعالك، و2048 وكانسة الألغام تدربان منطقك، بينما غوموكو ولعبة الذاكرة مثاليتان للتركيز بهدوء. سواء أردت تمضية الوقت أو تحطيم رقمك القياسي، ستجد ما يناسبك هنا.",
        metaTitle="ألعاب الأركيد - ألعاب مجانية عبر الإنترنت | الثعبان و2048 وتتريس",
        metaDesc="العب مجانًا 6 ألعاب كلاسيكية عبر الإنترنت: الثعبان، 2048، تتريس، كانسة الألغام، غوموكو ولعبة الذاكرة. بدون تنزيل أو تسجيل، العب فورًا على الحاسوب والجوال.",
        metaKeywords="ألعاب,ألعاب أونلاين,ألعاب مجانية,ألعاب متصفح,الثعبان,2048,تتريس,كانسة الألغام,غوموكو,لعبة الذاكرة"),
    "ru": dict(
        badge="🎮 Всё бесплатно · Играйте сразу",
        h1Pre="Классические", h1Hl="мини-игры", h1Post="<br />Прямо в браузере",
        heroP="Змейка, 2048, Тетрис, Сапёр, Гомоку и Память — шесть легендарных игр, любимых поколениями. Без скачивания и регистрации, плавно работают на компьютере и телефоне.",
        stats=["🕹️ 6 игр", "⚡ Мгновенная загрузка", "📱 На телефоне", "🆓 Бесплатно навсегда"],
        gamesTitle="Все игры", gamesDesc="Выберите игру и нажмите «Играть», чтобы начать.",
        aboutH2="О сайте «Аркадные мини-игры»",
        aboutP="Аркадные мини-игры — бесплатная коллекция онлайн-игр. Мы уверены: хорошей игре не нужны скачивание и регистрация — откройте страницу и играйте. Все игры написаны на чистом фронтенде: быстрая загрузка, никакой рекламы и полная адаптация под телефон и компьютер.",
        chooseH2="Почему браузерные мини-игры?",
        chooseP="Браузерные мини-игры не требуют установки и не занимают места. Сыграйте партию в дороге, на перемене или в перерыве. Змейка и Тетрис тренируют реакцию, 2048 и Сапёр — логику, а Гомоку и Память идеальны для спокойной сосредоточенности. Убить пару минут или побить рекорд — здесь найдётся игра на любой случай.",
        metaTitle="Аркадные мини-игры - Бесплатные онлайн-игры | Змейка, 2048, Тетрис",
        metaDesc="Играйте бесплатно в 6 классических мини-игр онлайн: Змейка, 2048, Тетрис, Сапёр, Гомоку и Память. Без скачивания и регистрации — на компьютере и телефоне.",
        metaKeywords="мини-игры,онлайн игры,бесплатные игры,браузерные игры,змейка,2048,тетрис,сапёр,гомоку,память,казуальные игры"),
    "ja": dict(
        badge="🎮 すべて無料 · すぐ遊べる",
        h1Pre="定番", h1Hl="ミニゲーム", h1Post="集<br />ブラウザで今すぐプレイ",
        heroP="スネーク、2048、テトリス、マインスイーパー、五目並べ、神経衰弱——世代を超えて愛される6つの名作。ダウンロード・登録不要、PCでもスマホでも快適に遊べます。",
        stats=["🕹️ 6ゲーム", "⚡ 待ち時間ゼロ", "📱 スマホ対応", "🆓 ずっと無料"],
        gamesTitle="ゲーム一覧", gamesDesc="好きなゲームを選んで「プレイ」をクリック。",
        aboutH2="ミニゲームランドについて",
        aboutP="ミニゲームランドは無料のオンラインミニゲーム集です。良いゲームにダウンロードも登録もいらない——ページを開けばすぐ遊べる。すべて純粋なフロントエンド技術で作られ、読み込みが速く、広告なし、スマホとPCの両方に最適化されています。",
        chooseH2="ブラウザのミニゲームを選ぶ理由",
        chooseP="ブラウザのミニゲームはインストール不要で容量も使いません。通勤中や休憩時間にサクッと一戦。スネークやテトリスは反射神経を、2048やマインスイーパーは論理力を鍛え、五目並べや神経衰弱はじっくり考えるのにぴったり。暇つぶしにもハイスコア挑戦にも、ここにはあなたに合う一作があります。",
        metaTitle="ミニゲームランド - 無料オンラインゲーム集 | スネーク・2048・テトリス",
        metaDesc="スネーク、2048、テトリス、マインスイーパー、五目並べ、神経衰弱の6つの名作を無料でオンラインプレイ。ダウンロード・登録不要、PCとスマホですぐに遊べます。",
        metaKeywords="ミニゲーム,オンラインゲーム,無料ゲーム,ブラウザゲーム,スネーク,2048,テトリス,マインスイーパー,五目並べ,神経衰弱"),
    "ko": dict(
        badge="🎮 전부 무료 · 바로 플레이",
        h1Pre="클래식", h1Hl="미니게임", h1Post=" 모음<br />브라우저에서 바로 즐기기",
        heroP="스네이크, 2048, 테트리스, 지뢰찾기, 오목, 메모리 카드 — 세대를 넘어 사랑받는 6가지 고전 게임. 다운로드나 회원가입 없이 PC와 모바일에서 바로 플레이하세요.",
        stats=["🕹️ 게임 6종", "⚡ 즉시 로딩", "📱 모바일 지원", "🆓 영구 무료"],
        gamesTitle="전체 게임", gamesDesc="마음에 드는 게임을 골라 「시작하기」를 눌러 바로 플레이하세요.",
        aboutH2="미니게임 놀이터 소개",
        aboutP="미니게임 놀이터는 무료 온라인 미니게임 모음 사이트입니다. 좋은 게임에는 복잡한 다운로드나 회원가입이 필요 없다고 믿습니다 — 페이지를 열면 바로 플레이. 모든 게임은 순수 프런트엔드로 만들어져 로딩이 빠르고 광고 없이, 모바일과 PC 모두에 최적화되어 있습니다.",
        chooseH2="웹 미니게임을 추천하는 이유",
        chooseP="웹 미니게임은 설치가 필요 없고 저장 공간도 차지하지 않습니다. 통근길, 쉬는 시간, 업무 사이에 한 판씩 즐겨보세요. 스네이크와 테트리스는 순발력을, 2048과 지뢰찾기는 논리력을 길러주고, 오목과 메모리 카드는 차분히 집중하기 좋습니다. 시간 때우기든 최고 점수 도전이든, 여기 당신에게 맞는 게임이 있습니다.",
        metaTitle="미니게임 놀이터 - 무료 온라인 미니게임 | 스네이크, 2048, 테트리스",
        metaDesc="스네이크, 2048, 테트리스, 지뢰찾기, 오목, 메모리 카드 등 6가지 고전 미니게임을 무료로 즐기세요. 다운로드·회원가입 없이 PC와 모바일에서 바로 플레이.",
        metaKeywords="미니게임,온라인 게임,무료 게임,웹 게임,스네이크,2048,테트리스,지뢰찾기,오목,메모리 카드,캐주얼 게임"),
}

# 游戏元信息（与语言无关）
GAMES = [
    dict(slug="snake", js="snake.js", icon="🐍", color="var(--green)"),
    dict(slug="2048", js="g2048.js", icon="🔢", color="var(--yellow)"),
    dict(slug="tetris", js="tetris.js", icon="🧱", color="var(--cyan)"),
    dict(slug="minesweeper", js="minesweeper.js", icon="💣", color="var(--orange)"),
    dict(slug="gomoku", js="gomoku.js", icon="⚫", color="var(--pink)"),
    dict(slug="memory", js="memory.js", icon="🃏", color="var(--purple)", bannerLight=True),
]

# ============ 各游戏翻译内容 ============
GDATA = {lang: {} for lang in LANG_ORDER}

GDATA["zh"] = {
    "snake": dict(name="贪吃蛇", tags=["街机", "反应"],
        cardDesc="控制小蛇吃到食物不断变长，小心别撞墙也别咬到自己，挑战你的最高分！",
        sub="经典街机游戏：吃到食物小蛇就会变长，撞墙或咬到自己就算失败。分数越高，速度越快！",
        howto=["电脑端：使用 <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 或 <kbd>WASD</kbd> 控制方向，<kbd>空格</kbd> 暂停/继续。",
               "手机端：点击屏幕下方的方向按钮控制小蛇。",
               "每吃一个食物得 10 分，小蛇变长一节。",
               "撞到墙壁或自己的身体即游戏结束。",
               "分数越高移动越快，最高分会自动保存在本机。"],
        tips=["尽量沿着边缘走，给自己留出回旋空间。", "蛇身变长后避免走进死角。", "提前规划好转向，不要到食物跟前才拐弯。"],
        title="贪吃蛇在线玩 - 免费经典贪吃蛇小游戏 | 街机小游戏乐园",
        keywords="贪吃蛇,贪吃蛇在线玩,贪吃蛇小游戏,经典贪吃蛇,免费贪吃蛇游戏", canvasAria="贪吃蛇游戏画布"),
    "2048": dict(name="2048", tags=["益智", "数字"],
        cardDesc="滑动合并相同数字，从 2 一路合成 2048，简单规则藏着无穷策略。",
        sub="滑动方块，让相同数字相撞合并，从 2 一路合成 2048！",
        howto=["电脑端：使用 <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 或 <kbd>WASD</kbd> 滑动全部方块。",
               "手机端：在棋盘上向上下左右滑动。",
               "相同数字的方块碰撞时会合并成它们的和。",
               "每次滑动后会随机出现一个新的 2 或 4。",
               "合成 2048 即获胜，棋盘无路可走则游戏结束。"],
        tips=["把最大的数字固定在一个角落，不要轻易移动它。", "尽量只沿两个方向滑动，保持棋盘有序。", "大数字按从大到小蛇形排列，合并效率最高。"],
        title="2048在线玩 - 免费数字合成益智小游戏 | 街机小游戏乐园",
        keywords="2048,2048在线玩,2048小游戏,数字游戏,益智游戏,免费2048", canvasAria="2048 游戏棋盘"),
    "tetris": dict(name="俄罗斯方块", tags=["街机", "经典"],
        cardDesc="旋转、移动、消除整行！经久不衰的方块消除游戏，越玩越上瘾。",
        sub="旋转、移动、堆叠方块，填满一整行就能消除。每消除 10 行升一级，速度越来越快！",
        howto=["<kbd>←</kbd><kbd>→</kbd> 移动方块，<kbd>↓</kbd> 加速下落。",
               "<kbd>↑</kbd> 或 <kbd>W</kbd> 旋转方块，<kbd>空格</kbd> 直接落底。",
               "填满一整行即可消除，一次消除多行得分更高。",
               "方块堆到顶部即游戏结束。"],
        tips=["留出一列竖井，等待长条（I 形）一次消四行。", "尽量保持堆叠表面平整，避免出现空洞。", "等级升高后提前想好下一块的位置。"],
        title="俄罗斯方块在线玩 - 免费经典方块消除游戏 | 街机小游戏乐园",
        keywords="俄罗斯方块,俄罗斯方块在线玩,Tetris,方块游戏,消除游戏,免费小游戏", canvasAria="俄罗斯方块游戏画布"),
    "minesweeper": dict(name="扫雷", tags=["益智", "推理"],
        cardDesc="根据数字提示推理地雷位置，标记全部地雷即可获胜，考验逻辑与运气。",
        sub="数字代表周围 8 格中的地雷数量，推理出所有地雷的位置并插上旗帜！",
        howto=["左键（手机轻点）翻开格子。",
               "右键（手机长按）插旗标记地雷，再次操作取消。",
               "数字表示周围 8 个格子中藏有几颗地雷。",
               "翻开所有非雷格子即获胜，首次点击保证安全。"],
        tips=["从角落和边缘入手，信息更集中。", "数字周围已标满足够的旗，其余格子都可安全翻开。", "不确定时先标记疑问处，从别的区域寻找突破口。"],
        title="扫雷在线玩 - 免费经典扫雷小游戏（初级/中级/高级）| 街机小游戏乐园",
        keywords="扫雷,扫雷在线玩,扫雷小游戏,经典扫雷,益智游戏,免费扫雷", canvasAria="扫雷棋盘",
        diffs=[("easy", "初级 9×9（10 雷）"), ("medium", "中级 12×12（24 雷）"), ("hard", "高级 16×16（40 雷）")]),
    "gomoku": dict(name="五子棋", tags=["棋类", "人机对战"],
        cardDesc="黑白对弈，五子连珠即胜。内置 AI 对手，随时随地来一局。",
        sub="你执黑棋先手，与电脑 AI 对弈，任意方向率先连成五子即获胜！",
        howto=["点击棋盘交叉点落子，你执黑棋先手。",
               "横、竖、斜任意方向率先连成五子即获胜。",
               "电脑 AI 会自动应招，攻守兼备。",
               "棋盘下满未分胜负则为平局。"],
        tips=["开局占据天元附近，控制棋盘中心。", "优先做「活三」「冲四」等进攻棋形。", "进攻的同时留意对方的连三，及时封堵。"],
        title="五子棋在线玩 - 免费人机对战五子棋小游戏 | 街机小游戏乐园",
        keywords="五子棋,五子棋在线玩,五子棋人机对战,五子棋小游戏,棋类游戏,免费五子棋", canvasAria="五子棋棋盘"),
    "memory": dict(name="记忆翻牌", tags=["益智", "记忆力"],
        cardDesc="翻开卡片记住图案，找出所有相同的配对，锻炼你的瞬间记忆力。",
        sub="一次翻开两张卡片，图案相同即可配对。用最少的步数找出全部 8 对图案！",
        howto=["点击卡片将其翻开，每次最多翻开两张。",
               "两张图案相同即配对成功，保持翻开状态。",
               "图案不同会自动盖回，记住它们的位置！",
               "找出全部 8 对图案即获胜，步数越少越厉害。"],
        tips=["按顺序翻牌，在脑海中给每个位置编号。", "翻到新图案时立刻回忆它是否出现过。", "配对成功后排除已翻卡片，缩小记忆范围。"],
        title="记忆翻牌在线玩 - 免费记忆力训练小游戏 | 街机小游戏乐园",
        keywords="记忆翻牌,翻牌游戏,记忆力游戏,配对游戏,益智小游戏,免费小游戏", canvasAria="记忆翻牌卡片区"),
}

GDATA["en"] = {
    "snake": dict(name="Snake", tags=["Arcade", "Reflex"],
        cardDesc="Guide the snake to eat and grow longer. Don't hit the walls or yourself — chase the high score!",
        sub="The arcade classic: eat food to grow longer — hit a wall or your own tail and it's over. The higher your score, the faster it gets!",
        howto=["Desktop: steer with <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> or <kbd>WASD</kbd>, <kbd>Space</kbd> to pause/resume.",
               "Mobile: tap the arrow buttons below the screen.",
               "Each food is worth 10 points and grows the snake by one segment.",
               "Hitting a wall or your own body ends the game.",
               "The snake speeds up as your score grows; your best score is saved on this device."],
        tips=["Stay near the edges to keep room to maneuver.", "Once the snake grows long, avoid dead ends.", "Plan your turns early — don't swerve right at the food."],
        title="Snake Online - Play Free Classic Snake Game | Arcade Games Hub",
        keywords="snake,snake online,snake game,classic snake,free snake game", canvasAria="Snake game board"),
    "2048": dict(name="2048", tags=["Puzzle", "Numbers"],
        cardDesc="Slide and merge matching numbers from 2 all the way to 2048. Simple rules, endless strategy.",
        sub="Slide the tiles, merge matching numbers and build your way from 2 to 2048!",
        howto=["Desktop: use <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> or <kbd>WASD</kbd> to slide all tiles.",
               "Mobile: swipe up, down, left or right on the board.",
               "Tiles with the same number merge into their sum when they collide.",
               "A new 2 or 4 appears after every move.",
               "Reach 2048 to win; the game ends when no moves remain."],
        tips=["Keep your biggest tile in one corner and avoid moving it.", "Try to slide in only two directions to keep the board tidy.", "Arrange big numbers in a descending snake pattern for efficient merges."],
        title="2048 Online - Play Free Number Puzzle Game | Arcade Games Hub",
        keywords="2048,2048 online,2048 game,number puzzle,puzzle game,free 2048", canvasAria="2048 game board"),
    "tetris": dict(name="Tetris", tags=["Arcade", "Classic"],
        cardDesc="Rotate, drop and clear full lines in the timeless block-stacking classic.",
        sub="Rotate, move and stack the falling pieces — complete a row to clear it. Level up every 10 lines!",
        howto=["<kbd>←</kbd><kbd>→</kbd> move the piece, <kbd>↓</kbd> speeds up the fall.",
               "<kbd>↑</kbd> or <kbd>W</kbd> rotates, <kbd>Space</kbd> drops the piece instantly.",
               "Complete a full row to clear it; clearing multiple rows at once scores more.",
               "The game ends when the stack reaches the top."],
        tips=["Keep one column open as a well for the I-piece to clear four lines.", "Keep the surface flat and avoid holes.", "At higher levels, plan where the next piece goes in advance."],
        title="Tetris Online - Play Free Classic Block Game | Arcade Games Hub",
        keywords="tetris,tetris online,block game,classic tetris,free tetris", canvasAria="Tetris game board"),
    "minesweeper": dict(name="Minesweeper", tags=["Puzzle", "Logic"],
        cardDesc="Use number clues to deduce where the mines are. Flag them all to win!",
        sub="The number tells you how many mines hide in the 8 surrounding cells. Deduce and flag them all!",
        howto=["Left-click (tap on mobile) to reveal a cell.",
               "Right-click (long-press on mobile) to place or remove a flag.",
               "A number shows how many mines are in the 8 surrounding cells.",
               "Reveal all safe cells to win; your first click is always safe."],
        tips=["Start from corners and edges where clues are easier.", "If a number already has enough flags around it, the rest of its neighbors are safe.", "Not sure? Mark the cell and break through from another area first."],
        title="Minesweeper Online - Play Free Classic Puzzle Game | Arcade Games Hub",
        keywords="minesweeper,minesweeper online,minesweeper game,classic minesweeper,free minesweeper", canvasAria="Minesweeper board",
        diffs=[("easy", "Easy 9×9 (10 mines)"), ("medium", "Medium 12×12 (24 mines)"), ("hard", "Hard 16×16 (40 mines)")]),
    "gomoku": dict(name="Gomoku", tags=["Board", "vs AI"],
        cardDesc="Black vs White — first to connect five stones wins. Play against the built-in AI anytime.",
        sub="You play Black and move first against the AI — connect five stones in any direction to win!",
        howto=["Click an intersection to place your stone; you play Black and move first.",
               "First to connect five stones in any direction — row, column or diagonal — wins.",
               "The built-in AI plays White with a balance of attack and defense.",
               "A full board with no winner is a draw."],
        tips=["Open near the center to control the board.", "Build open threes and fours to force the pace.", "Watch for the AI's threes and block them in time."],
        title="Gomoku Online - Play Free Five in a Row vs AI | Arcade Games Hub",
        keywords="gomoku,gomoku online,five in a row,gomoku vs ai,board game,free gomoku", canvasAria="Gomoku board"),
    "memory": dict(name="Memory Match", tags=["Puzzle", "Memory"],
        cardDesc="Flip cards, remember the icons and match all the pairs to train your memory.",
        sub="Flip two cards at a time — matching icons stay open. Clear all 8 pairs in as few moves as possible!",
        howto=["Click a card to flip it; at most two cards stay open at once.",
               "Matching icons stay face up — pair found!",
               "Different icons flip back over. Remember where they were!",
               "Find all 8 pairs to win — fewer moves means a better score."],
        tips=["Flip in order and mentally number the positions.", "When a new icon appears, recall if you have seen it before.", "Exclude matched pairs to shrink what you need to remember."],
        title="Memory Match Online - Free Memory Training Game | Arcade Games Hub",
        keywords="memory match,memory game,matching pairs,card flip game,brain training,free memory game", canvasAria="Memory match cards"),
}

GDATA["es"] = {
    "snake": dict(name="Snake", tags=["Arcade", "Reflejos"],
        cardDesc="Guía a la serpiente para comer y crecer. ¡Evita chocar contigo misma y supera tu récord!",
        sub="El clásico arcade: come para crecer; choca contra el muro o tu cola y pierdes. ¡A más puntos, más velocidad!",
        howto=["En PC: gira con <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> o <kbd>WASD</kbd>, <kbd>Espacio</kbd> para pausar/continuar.",
               "En móvil: toca los botones de dirección bajo la pantalla.",
               "Cada comida vale 10 puntos y alarga la serpiente un segmento.",
               "Chocar contra la pared o tu propio cuerpo termina la partida.",
               "La velocidad aumenta con los puntos; tu récord se guarda en el dispositivo."],
        tips=["Muévete cerca de los bordes para tener espacio de maniobra.", "Con una serpiente larga, evita los callejones sin salida.", "Anticipa los giros, no esperes a llegar a la comida."],
        title="Snake online - Juega gratis al clásico juego de la serpiente | Arcade de Minijuegos",
        keywords="snake,snake online,juego de la serpiente,serpiente clásica,juego gratis", canvasAria="Tablero del juego Snake"),
    "2048": dict(name="2048", tags=["Puzle", "Números"],
        cardDesc="Desliza y combina números iguales hasta llegar a 2048. Reglas simples, estrategia infinita.",
        sub="¡Desliza las fichas, combina números iguales y llega de 2 a 2048!",
        howto=["En PC: usa <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> o <kbd>WASD</kbd> para deslizar todas las fichas.",
               "En móvil: desliza el dedo sobre el tablero en cualquier dirección.",
               "Las fichas con el mismo número se fusionan al chocar.",
               "Tras cada movimiento aparece un 2 o un 4 nuevo.",
               "Llega a 2048 para ganar; si no hay movimientos, la partida termina."],
        tips=["Fija tu número mayor en una esquina y no lo muevas.", "Intenta deslizar solo en dos direcciones para mantener el orden.", "Ordena los números de mayor a menor en forma de serpiente para fusionar mejor."],
        title="2048 online - Juega gratis al puzle de números | Arcade de Minijuegos",
        keywords="2048,2048 online,juego 2048,puzle de números,juego gratis 2048", canvasAria="Tablero del juego 2048"),
    "tetris": dict(name="Tetris", tags=["Arcade", "Clásico"],
        cardDesc="Gira, mueve y elimina líneas completas en el clásico de bloques que nunca pasa de moda.",
        sub="Gira, mueve y apila las piezas; completa filas para eliminarlas. ¡Sube de nivel cada 10 líneas!",
        howto=["<kbd>←</kbd><kbd>→</kbd> mueven la pieza, <kbd>↓</kbd> acelera la caída.",
               "<kbd>↑</kbd> o <kbd>W</kbd> gira la pieza, <kbd>Espacio</kbd> la deja caer de golpe.",
               "Completa una fila para eliminarla; varias filas a la vez dan más puntos.",
               "La partida termina cuando la pila llega arriba."],
        tips=["Deja un pozo de una columna para la pieza I y borra cuatro líneas de golpe.", "Mantén la superficie plana y evita huecos.", "En niveles altos, decide dónde irá la siguiente pieza con antelación."],
        title="Tetris online - Juega gratis al clásico juego de bloques | Arcade de Minijuegos",
        keywords="tetris,tetris online,juego de bloques,tetris clásico,tetris gratis", canvasAria="Tablero del juego Tetris"),
    "minesweeper": dict(name="Buscaminas", tags=["Puzle", "Lógica"],
        cardDesc="Deduce dónde están las minas con las pistas numéricas y márcalas todas para ganar.",
        sub="El número indica cuántas minas hay en las 8 casillas vecinas. ¡Dedúcelo y márcalas todas!",
        howto=["Clic izquierdo (toque en móvil) para revelar una casilla.",
               "Clic derecho (pulsación larga en móvil) para poner o quitar una bandera.",
               "El número indica cuántas minas hay en las 8 casillas vecinas.",
               "Revela todas las casillas seguras para ganar; el primer clic siempre es seguro."],
        tips=["Empieza por esquinas y bordes, donde hay menos incógnitas.", "Si un número ya tiene suficientes banderas alrededor, el resto es seguro.", "¿Dudas? Marca la casilla y abre camino por otra zona."],
        title="Buscaminas online - Juega gratis al clásico puzle | Arcade de Minijuegos",
        keywords="buscaminas,buscaminas online,juego buscaminas,buscaminas clásico,buscaminas gratis", canvasAria="Tablero de Buscaminas",
        diffs=[("easy", "Fácil 9×9 (10 minas)"), ("medium", "Medio 12×12 (24 minas)"), ("hard", "Difícil 16×16 (40 minas)")]),
    "gomoku": dict(name="Gomoku", tags=["Tablero", "vs IA"],
        cardDesc="Cinco en raya gana. Enfréntate a la IA integrada cuando quieras.",
        sub="Juegas con negras y mueves primero contra la IA: ¡conecta cinco piedras en cualquier dirección para ganar!",
        howto=["Haz clic en una intersección para colocar tu piedra; juegas con negras y mueves primero.",
               "Gana quien conecte cinco piedras seguidas en cualquier dirección.",
               "La IA integrada juega con blancas, atacando y defendiendo.",
               "Si el tablero se llena sin ganador, es empate."],
        tips=["Abre cerca del centro para dominar el tablero.", "Crea tres y cuatros abiertos para presionar.", "Vigila los tres de la IA y tápalos a tiempo."],
        title="Gomoku online - Juega gratis a cinco en raya contra la IA | Arcade de Minijuegos",
        keywords="gomoku,gomoku online,cinco en raya,gomoku contra ia,juego de tablero,gomoku gratis", canvasAria="Tablero de Gomoku"),
    "memory": dict(name="Memoria", tags=["Puzle", "Memoria"],
        cardDesc="Voltea las cartas, recuerda los dibujos y encuentra todas las parejas para entrenar tu memoria.",
        sub="Voltea dos cartas a la vez: si coinciden, se quedan abiertas. ¡Encuentra las 8 parejas en el menor número de movimientos!",
        howto=["Toca una carta para voltearla; solo dos pueden estar abiertas a la vez.",
               "Si los dibujos coinciden, la pareja queda descubierta.",
               "Si no, se voltean de nuevo. ¡Recuerda dónde estaban!",
               "Encuentra las 8 parejas para ganar; menos movimientos, mejor puntuación."],
        tips=["Voltea en orden y numera mentalmente las posiciones.", "Al ver un dibujo nuevo, recuerda si ya apareció.", "Descarta las parejas logradas para reducir lo que memorizas."],
        title="Juego de memoria online - Entrena tu memoria gratis | Arcade de Minijuegos",
        keywords="juego de memoria,memoria online,parejas,voltea cartas,entrenar memoria,juego gratis", canvasAria="Cartas del juego de memoria"),
}

GDATA["ar"] = {
    "snake": dict(name="الثعبان", tags=["أركيد", "سرعة بديهة"],
        cardDesc="وجّه الثعبان ليأكل الطعام ويكبر، وتجنّب الاصطدام بالجدران أو بجسمك لتحقق أعلى نتيجة!",
        sub="لعبة الأركيد الكلاسيكية: كُل لتكبر، وإذا اصطدمت بجدار أو بجسمك تخسر. كلما زادت نقاطك زادت السرعة!",
        howto=["على الحاسوب: وجّه بالأسهم <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> أو <kbd>WASD</kbd>، و<kbd>مسافة</kbd> للإيقاف المؤقت/المتابعة.",
               "على الجوال: اضغط أزرار الاتجاهات أسفل الشاشة.",
               "كل قطعة طعام تمنحك 10 نقاط وتزيد طول الثعبان قطعة.",
               "الاصطدام بالجدار أو بجسمك ينهي اللعبة.",
               "تزداد السرعة كلما ارتفعت نقاطك، ويُحفظ أفضل رقم على جهازك."],
        tips=["حاول السير قرب الحواف لتترك لنفسك مجالًا للمناورة.", "عندما يطول الثعبان، تجنّب الطرق المسدودة.", "خطّط للانعطاف مبكرًا ولا تنتظر حتى تصل إلى الطعام."],
        title="لعبة الثعبان أونلاين - العب مجانًا اللعبة الكلاسيكية | ألعاب الأركيد",
        keywords="لعبة الثعبان,الثعبان أونلاين,لعبة الأفعى,الثعبان الكلاسيكية,لعبة مجانية", canvasAria="لوحة لعبة الثعبان"),
    "2048": dict(name="2048", tags=["ألغاز", "أرقام"],
        cardDesc="حرّك المربعات وادمج الأرقام المتشابهة من 2 حتى 2048. قواعد بسيطة واستراتيجية لا تنتهي.",
        sub="حرّك المربعات وادمج الأرقام المتطابقة لتصنع 2048!",
        howto=["على الحاسوب: استخدم الأسهم <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> أو <kbd>WASD</kbd> لتحريك كل المربعات.",
               "على الجوال: اسحب بإصبعك على اللوحة بأي اتجاه.",
               "المربعات المتطابقة تندمج عند اصطدامها لتصبح مجموعهما.",
               "بعد كل حركة يظهر رقم 2 أو 4 جديد.",
               "اصنع 2048 لتفوز؛ وتنتهي اللعبة عندما لا تبقى حركات ممكنة."],
        tips=["ثبّت أكبر رقم في زاوية واحدة وتجنّب تحريكه.", "حاول التحريك في اتجاهين فقط للحفاظ على ترتيب اللوحة.", "رتّب الأرقام الكبيرة تنازليًا بشكل متعرج لتسهيل الدمج."],
        title="لعبة 2048 أونلاين - لغز الأرقام المجاني | ألعاب الأركيد",
        keywords="2048,لعبة 2048,2048 أونلاين,لغز الأرقام,لعبة مجانية", canvasAria="لوحة لعبة 2048"),
    "tetris": dict(name="تتريس", tags=["أركيد", "كلاسيكية"],
        cardDesc="دوّر وحرّك القطع وأكمل الصفوف لتفجيرها في اللعبة الكلاسيكية الخالدة.",
        sub="دوّر القطع المتساقطة وحرّكها ورصّها؛ أكمل صفًا لإزالته، وكل 10 صفوف ترفع مستواك!",
        howto=["الأسهم <kbd>←</kbd><kbd>→</kbd> لتحريك القطعة، <kbd>↓</kbd> لتسريع النزول.",
               "<kbd>↑</kbd> أو <kbd>W</kbd> لتدوير القطعة، و<kbd>مسافة</kbd> لإسقاطها فورًا.",
               "أكمل صفًا كاملًا لإزالته؛ وإزالة عدة صفوف دفعة واحدة تمنح نقاطًا أكثر.",
               "تنتهي اللعبة عندما تصل القطع المتراكمة إلى الأعلى."],
        tips=["اترك عمودًا فارغًا كبئر لقطعة I لتفجير أربعة صفوف دفعة واحدة.", "حافظ على سطح مستوٍ وتجنّب الفجوات.", "في المستويات العالية، خطّط مسبقًا لمكان القطعة التالية."],
        title="تتريس أونلاين - العب مجانًا لعبة القطع الكلاسيكية | ألعاب الأركيد",
        keywords="تتريس,تتريس أونلاين,لعبة القطع,تتريس كلاسيكية,لعبة مجانية", canvasAria="لوحة لعبة تتريس"),
    "minesweeper": dict(name="كانسة الألغام", tags=["ألغاز", "منطق"],
        cardDesc="استنتج مواقع الألغام من الأرقام وعلّمها كلها بالأعلام لتفوز!",
        sub="الرقم يخبرك بعدد الألغام في الخلايا الثماني المحيطة. استنتج وعلّمها جميعًا!",
        howto=["نقرة يسارية (أو لمسة على الجوال) لكشف الخلية.",
               "نقرة يمينية (أو لمسة مطوّلة) لوضع علم أو إزالته.",
               "الرقم يوضح عدد الألغام في الخلايا الثماني المحيطة.",
               "اكشف كل الخلايا الآمنة لتفوز؛ أول نقرة تكون آمنة دائمًا."],
        tips=["ابدأ من الزوايا والحواف حيث تكون الأدلة أوضح.", "إذا كان حول رقمٍ ما أعلام كافية، فبقية جيرانه آمنون.", "غير متأكد؟ علّم الخلية وافتح طريقًا من منطقة أخرى."],
        title="كانسة الألغام أونلاين - العب مجانًا اللغز الكلاسيكي | ألعاب الأركيد",
        keywords="كانسة الألغام,كانسة الألغام أونلاين,لعبة الألغام,ألغاز منطقية,لعبة مجانية", canvasAria="لوحة كانسة الألغام",
        diffs=[("easy", "سهل 9×9 (10 ألغام)"), ("medium", "متوسط 12×12 (24 لغمًا)"), ("hard", "صعب 16×16 (40 لغمًا)")]),
    "gomoku": dict(name="غوموكو", tags=["لوحة", "ضد الذكاء الاصطناعي"],
        cardDesc="أول من يصل خمسة أحجار متتالية يفوز. تحدَّ الذكاء الاصطناعي في أي وقت.",
        sub="تلعب بالأسود أولًا ضد الذكاء الاصطناعي — صِل خمسة أحجار في أي اتجاه لتفوز!",
        howto=["انقر على نقطة تقاطع لوضع حجرك؛ تلعب بالأسود وتبدأ أولًا.",
               "أول من يصل خمسة أحجار متتالية في أي اتجاه — أفقي أو عمودي أو قطري — يفوز.",
               "يلعب الذكاء الاصطناعي بالأبيض بهجوم ودفاع متوازنين.",
               "امتلاء اللوحة دون فائز يعني التعادل."],
        tips=["ابدأ قرب المركز للسيطرة على اللوحة.", "ابنِ «ثلاثيات» و«رباعيات» مفتوحة للضغط على الخصم.", "راقب ثلاثيات الخصم وسدّها في الوقت المناسب."],
        title="غوموكو أونلاين - العب مجانًا ضد الذكاء الاصطناعي | ألعاب الأركيد",
        keywords="غوموكو,غوموكو أونلاين,خمسة في صف,لعبة لوحة,لعبة مجانية", canvasAria="لوحة غوموكو"),
    "memory": dict(name="لعبة الذاكرة", tags=["ألغاز", "ذاكرة"],
        cardDesc="اقلب البطاقات وتذكّر الرموز وطابق جميع الأزواج لتدرب ذاكرتك.",
        sub="اقلب بطاقتين في كل مرة؛ إذا تطابقتا تبقيان مكشوفتين. اعثر على الأزواج الثمانية بأقل عدد من المحاولات!",
        howto=["انقر على بطاقة لقلبها؛ يمكن فتح بطاقتين كحد أقصى في المرة.",
               "إذا تطابق الرمزان تبقى البطاقتان مكشوفتين.",
               "إذا اختلفا تُغلقان مجددًا — تذكّر موضعيهما!",
               "اعثر على الأزواج الثمانية كلها لتفوز؛ وكلما قلّت المحاولات كان أفضل."],
        tips=["اقلب البطاقات بترتيب ورقّم المواضع في ذهنك.", "عند ظهور رمز جديد تذكّر إن كنت رأيته سابقًا.", "استبعد الأزواج المكتشفة لتقليل ما عليك حفظه."],
        title="لعبة الذاكرة أونلاين - درّب ذاكرتك مجانًا | ألعاب الأركيد",
        keywords="لعبة الذاكرة,لعبة تطابق البطاقات,تدريب الذاكرة,ألعاب ذكاء,لعبة مجانية", canvasAria="بطاقات لعبة الذاكرة"),
}

GDATA["ru"] = {
    "snake": dict(name="Змейка", tags=["Аркада", "Реакция"],
        cardDesc="Управляйте змейкой, ешьте и растите. Не врезайтесь в стены и в себя — ставьте рекорды!",
        sub="Классика аркад: ешьте и растите — столкнётесь со стеной или с собой, и игра окончена. Чем выше счёт, тем выше скорость!",
        howto=["На компьютере: стрелки <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> или <kbd>WASD</kbd>, <kbd>пробел</kbd> — пауза/продолжить.",
               "На телефоне: кнопки направлений под экраном.",
               "Каждая еда даёт 10 очков и удлиняет змейку на один сегмент.",
               "Столкновение со стеной или с собственным телом завершает игру.",
               "Скорость растёт вместе со счётом; рекорд сохраняется на устройстве."],
        tips=["Держитесь ближе к краям, чтобы было место для манёвра.", "Длинной змейкой избегайте тупиков.", "Планируйте повороты заранее, не поворачивайте вплотную к еде."],
        title="Змейка онлайн - Играть бесплатно в классическую змейку | Аркадные мини-игры",
        keywords="змейка,змейка онлайн,игра змейка,классическая змейка,бесплатная змейка", canvasAria="Поле игры «Змейка»"),
    "2048": dict(name="2048", tags=["Головоломка", "Числа"],
        cardDesc="Сдвигайте и объединяйте одинаковые числа до 2048. Простые правила, бесконечная стратегия.",
        sub="Сдвигайте плитки и объединяйте одинаковые числа от 2 до 2048!",
        howto=["На компьютере: стрелки <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> или <kbd>WASD</kbd> сдвигают все плитки.",
               "На телефоне: свайп по полю в нужную сторону.",
               "Одинаковые плитки при столкновении объединяются в их сумму.",
               "После каждого хода появляется новая двойка или четвёрка.",
               "Соберите 2048, чтобы победить; игра окончена, когда ходов нет."],
        tips=["Держите самое большое число в одном углу и не двигайте его.", "Старайтесь сдвигать только в двух направлениях, сохраняя порядок.", "Раскладывайте числа по убыванию «змейкой» — так объединять проще."],
        title="2048 онлайн - Играть бесплатно в числовую головоломку | Аркадные мини-игры",
        keywords="2048,2048 онлайн,игра 2048,числовая головоломка,бесплатная игра", canvasAria="Поле игры 2048"),
    "tetris": dict(name="Тетрис", tags=["Аркада", "Классика"],
        cardDesc="Вращайте фигуры и очищайте линии в легендарном Тетрисе.",
        sub="Вращайте и складывайте падающие фигуры — заполненные ряды исчезают. Новый уровень каждые 10 линий!",
        howto=["<kbd>←</kbd><kbd>→</kbd> двигают фигуру, <kbd>↓</kbd> — ускоренное падение.",
               "<kbd>↑</kbd> или <kbd>W</kbd> — поворот, <kbd>пробел</kbd> — мгновенное падение.",
               "Заполните ряд, чтобы убрать его; несколько рядов сразу дают больше очков.",
               "Игра заканчивается, когда стопка достигает верха."],
        tips=["Оставляйте «колодец» в одну клетку для палки (I) и убирайте сразу 4 линии.", "Держите поверхность ровной, без пустот.", "На высоких уровнях заранее решайте, куда ставить следующую фигуру."],
        title="Тетрис онлайн - Играть бесплатно в классический тетрис | Аркадные мини-игры",
        keywords="тетрис,тетрис онлайн,игра тетрис,классический тетрис,бесплатный тетрис", canvasAria="Поле игры «Тетрис»"),
    "minesweeper": dict(name="Сапёр", tags=["Головоломка", "Логика"],
        cardDesc="По цифрам вычислите мины и отметьте их все флажками!",
        sub="Цифра подсказывает, сколько мин в восьми соседних клетках. Вычислите и пометьте все!",
        howto=["Левый клик (тап на телефоне) — открыть клетку.",
               "Правый клик (долгое нажатие на телефоне) — поставить или снять флажок.",
               "Цифра показывает, сколько мин в восьми соседних клетках.",
               "Откройте все безопасные клетки, чтобы победить; первый ход всегда безопасен."],
        tips=["Начинайте с углов и краёв — там меньше неизвестных.", "Если вокруг цифры уже стоит нужное число флажков, остальные соседи безопасны.", "Не уверены — пометьте клетку и прорвитесь с другой стороны."],
        title="Сапёр онлайн - Играть бесплатно в классического сапёра | Аркадные мини-игры",
        keywords="сапёр,сапёр онлайн,игра сапёр,классический сапёр,бесплатный сапёр", canvasAria="Поле игры «Сапёр»",
        diffs=[("easy", "Легко 9×9 (10 мин)"), ("medium", "Средне 12×12 (24 мины)"), ("hard", "Сложно 16×16 (40 мин)")]),
    "gomoku": dict(name="Гомоку", tags=["Настольная", "Против ИИ"],
        cardDesc="Пять в ряд — играйте против встроенного ИИ в любое время.",
        sub="Вы играете чёрными и ходите первым против ИИ — выстройте пять камней в ряд, чтобы победить!",
        howto=["Нажмите на пересечение линий, чтобы поставить камень; вы играете чёрными и ходите первым.",
               "Побеждает тот, кто первым выстроит пять камней в ряд в любом направлении.",
               "Встроенный ИИ играет белыми, атакуя и защищаясь.",
               "Если доска заполнена, а победителя нет — ничья."],
        tips=["Начинайте ближе к центру, чтобы контролировать доску.", "Стройте открытые тройки и четвёрки, чтобы диктовать игру.", "Следите за тройками соперника и вовремя их перекрывайте."],
        title="Гомоку онлайн - Играть бесплатно пять в ряд против ИИ | Аркадные мини-игры",
        keywords="гомоку,гомоку онлайн,пять в ряд,гомоку против ии,настольная игра,бесплатно", canvasAria="Доска гомоку"),
    "memory": dict(name="Память", tags=["Головоломка", "Память"],
        cardDesc="Переворачивайте карты и находите все пары — тренируйте память!",
        sub="Открывайте по две карты — совпавшие остаются открытыми. Найдите все 8 пар за минимум ходов!",
        howto=["Нажмите на карту, чтобы перевернуть её; одновременно открыты не более двух.",
               "Совпавшие картинки остаются открытыми — пара найдена!",
               "Разные переворачиваются обратно — запомните их места!",
               "Найдите все 8 пар; чем меньше ходов, тем лучше результат."],
        tips=["Открывайте по порядку и мысленно нумеруйте позиции.", "Увидев новую картинку, сразу вспоминайте, попадалась ли она.", "Найденные пары исключайте из памяти — так проще."],
        title="Игра на память онлайн - Тренируйте память бесплатно | Аркадные мини-игры",
        keywords="игра на память,найди пару,карты память,тренировка памяти,бесплатная игра", canvasAria="Карты игры на память"),
}

GDATA["ja"] = {
    "snake": dict(name="スネーク", tags=["アーケード", "反射神経"],
        cardDesc="ヘビを操作してエサを食べて成長。壁や自分にぶつからないようハイスコアを目指そう！",
        sub="定番アーケード：エサを食べてどんどん伸びよう。壁や自分の体にぶつかると終了。点数が上がるほど速くなる！",
        howto=["パソコン：矢印キー <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> または <kbd>WASD</kbd> で操作、<kbd>スペース</kbd> で一時停止/再開。",
               "スマホ：画面下の方向ボタンで操作します。",
               "エサを食べると10点獲得、ヘビが1つ伸びます。",
               "壁や自分の体にぶつかるとゲームオーバー。",
               "スコアが上がるほどスピードアップ。最高記録は端末に保存されます。"],
        tips=["なるべく端に沿って動き、逃げ道を確保しよう。", "体が長くなったら行き止まりに注意。", "エサの手前で曲がるのではなく、早めに進路を決めよう。"],
        title="スネークゲーム - 無料オンライン | ミニゲームランド",
        keywords="スネーク,スネークゲーム,蛇ゲーム,無料ゲーム,オンライン", canvasAria="スネークゲームの盤面"),
    "2048": dict(name="2048", tags=["パズル", "数字"],
        cardDesc="同じ数字をスライドで合体させて2048を目指そう。シンプルなルールに奥深い戦略。",
        sub="タイルをスライドして同じ数字を合体、2から2048を目指そう！",
        howto=["パソコン：矢印キー <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> または <kbd>WASD</kbd> で全タイルをスライド。",
               "スマホ：盤面上で上下左右にスワイプ。",
               "同じ数字のタイルがぶつかると合体して合計になります。",
               "1手ごとに新しい 2 か 4 が出現。",
               "2048を作れば勝利。動かせなくなったらゲーム終了。"],
        tips=["最大の数字を角に固定し、むやみに動かさない。", "2方向だけで動かすと盤面が整理しやすい。", "大きい数字を蛇行状に並べると合体しやすい。"],
        title="2048 ゲーム - 無料オンラインパズル | ミニゲームランド",
        keywords="2048,2048ゲーム,数字パズル,無料ゲーム,オンライン", canvasAria="2048の盤面"),
    "tetris": dict(name="テトリス", tags=["アーケード", "名作"],
        cardDesc="回転・移動してラインを消す、不朽の落ちものパズル。",
        sub="落ちてくるブロックを回転・移動して積もう。段がそろうと消え、10段ごとにレベルアップ！",
        howto=["<kbd>←</kbd><kbd>→</kbd> で移動、<kbd>↓</kbd> で高速落下。",
               "<kbd>↑</kbd> または <kbd>W</kbd> で回転、<kbd>スペース</kbd> で即落下。",
               "一段そろえると消去。複数段同時消しで高得点。",
               "ブロックが上まで積み上がるとゲームオーバー。"],
        tips=["1列の井戸を残してIミノで4段消しを狙おう。", "表面を平らに保ち、穴を作らない。", "レベルが上がったら次のミノの置き場を先に決めよう。"],
        title="テトリス - 無料オンライン | ミニゲームランド",
        keywords="テトリス,テトリス無料,落ちものパズル,ブロックゲーム,オンライン", canvasAria="テトリスの盤面"),
    "minesweeper": dict(name="マインスイーパー", tags=["パズル", "推理"],
        cardDesc="数字を手がかりに地雷を推理。すべてに旗を立てればクリア！",
        sub="数字は周囲8マスの地雷の数。推理して全部に旗を立てよう！",
        howto=["左クリック（スマホはタップ）でマスを開く。",
               "右クリック（長押し）で旗を立てる/外す。",
               "数字は周囲8マスに隠れた地雷の数を示します。",
               "地雷以外の全マスを開けばクリア。最初の1手は必ず安全。"],
        tips=["角や辺から攻めると情報が絞りやすい。", "数字の周りに必要な旗がそろったら、残りのマスは安全。", "迷ったらマークして別の場所から突破口を探そう。"],
        title="マインスイーパー - 無料オンライン | ミニゲームランド",
        keywords="マインスイーパー,マインスイーパ,地雷ゲーム,無料ゲーム,オンライン", canvasAria="マインスイーパーの盤面",
        diffs=[("easy", "初級 9×9（地雷10個）"), ("medium", "中級 12×12（地雷24個）"), ("hard", "上級 16×16（地雷40個）")]),
    "gomoku": dict(name="五目並べ", tags=["ボード", "AI対戦"],
        cardDesc="五つ並べた方が勝ち。AI相手にいつでも対局できます。",
        sub="あなたは黒の先手。AI相手に縦・横・斜めどこでも先に5つ並べれば勝ち！",
        howto=["盤の交点をクリックして石を置きます。あなたは黒の先手です。",
               "縦・横・斜めのいずれかで先に5つ並べた方が勝ち。",
               "内蔵AIが白を担当し、攻守バランスよく応じます。",
               "盤が埋まって勝負がつかなければ引き分け。"],
        tips=["序盤は中央付近を取って主導権を握ろう。", "「活三」や「四」を作って攻めよう。", "相手の三には早めに防備を。"],
        title="五目並べ - AI対戦・無料オンライン | ミニゲームランド",
        keywords="五目並べ,五目並べオンライン,AI対戦,ボードゲーム,無料ゲーム", canvasAria="五目並べの盤面"),
    "memory": dict(name="神経衰弱", tags=["パズル", "記憶力"],
        cardDesc="カードをめくって絵柄を覚え、すべてのペアを見つけよう。",
        sub="一度に2枚めくって絵柄をそろえよう。8ペアすべてをできるだけ少ない手数で見つけよう！",
        howto=["カードをクリックしてめくります。同時に開けるのは2枚まで。",
               "絵柄がそろえばペア成立、そのまま開いた状態に。",
               "違えば裏返ります。どこに何があったか覚えよう！",
               "8ペアすべて見つければクリア。少ない手数ほど高評価。"],
        tips=["順番にめくりながら位置に番号を振って覚えよう。", "新しい絵が出たら、以前見たかすぐ思い出そう。", "そろったペアは記憶から外して範囲を絞ろう。"],
        title="神経衰弱ゲーム - 無料オンライン | ミニゲームランド",
        keywords="神経衰弱,めくりゲーム,記憶力ゲーム,ペア探し,無料ゲーム", canvasAria="神経衰弱のカード"),
}

GDATA["ko"] = {
    "snake": dict(name="스네이크", tags=["아케이드", "순발력"],
        cardDesc="뱀을 조종해 먹이를 먹고 길어지세요. 벽이나 몸에 부딪히지 않고 최고 점수에 도전!",
        sub="고전 아케이드: 먹이를 먹고 길어지세요. 벽이나 자기 몸에 부딪히면 끝! 점수가 오를수록 빨라집니다.",
        howto=["PC: 방향키 <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 또는 <kbd>WASD</kbd>로 조종, <kbd>스페이스바</kbd>로 일시정지/계속.",
               "모바일: 화면 아래 방향 버튼으로 조종하세요.",
               "먹이 하나당 10점을 얻고 뱀이 한 칸 길어집니다.",
               "벽이나 자기 몸에 부딪히면 게임이 끝납니다.",
               "점수가 오를수록 속도가 빨라지며 최고 기록은 기기에 저장됩니다."],
        tips=["가장자리를 따라 움직여 회피 공간을 확보하세요.", "몸이 길어지면 막다른 길은 피하세요.", "먹이 앞에서 급하게 꺾지 말고 미리 방향을 정하세요."],
        title="스네이크 게임 - 무료 온라인 클래식 뱀 게임 | 미니게임 놀이터",
        keywords="스네이크,뱀 게임,스네이크 게임,무료 게임,온라인 게임", canvasAria="스네이크 게임 보드"),
    "2048": dict(name="2048", tags=["퍼즐", "숫자"],
        cardDesc="같은 숫자를 밀어 합치며 2048까지 만들어 보세요. 간단한 규칙, 무한한 전략.",
        sub="타일을 밀어 같은 숫자를 합치고 2부터 2048까지 만들어 보세요!",
        howto=["PC: 방향키 <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 또는 <kbd>WASD</kbd>로 모든 타일을 밀기.",
               "모바일: 보드 위를 상하좌우로 스와이프하세요.",
               "같은 숫자 타일이 부딪히면 합쳐져 합계가 됩니다.",
               "매 이동 후 새로운 2 또는 4가 나타납니다.",
               "2048을 만들면 승리, 움직일 수 없으면 게임 종료."],
        tips=["가장 큰 숫자를 한 모서리에 고정하고 움직이지 마세요.", "두 방향으로만 밀어 보드를 정돈하세요.", "큰 숫자를 큰 것부터 지그재그로 배열하면 합치기 쉽습니다."],
        title="2048 게임 - 무료 온라인 숫자 퍼즐 | 미니게임 놀이터",
        keywords="2048,2048 게임,숫자 퍼즐,무료 게임,온라인 게임", canvasAria="2048 게임 보드"),
    "tetris": dict(name="테트리스", tags=["아케이드", "고전"],
        cardDesc="블록을 돌리고 쌓아 줄을 지우는 영원한 고전 게임.",
        sub="떨어지는 블록을 돌리고 쌓아 줄을 채우면 사라집니다. 10줄마다 레벨 업!",
        howto=["<kbd>←</kbd><kbd>→</kbd> 이동, <kbd>↓</kbd> 빠른 낙하.",
               "<kbd>↑</kbd> 또는 <kbd>W</kbd> 회전, <kbd>스페이스바</kbd> 즉시 낙하.",
               "한 줄을 가득 채우면 사라지고, 여러 줄 동시 제거 시 점수가 더 높습니다.",
               "블록이 꼭대기까지 쌓이면 게임 종료."],
        tips=["한 칸짜리 우물을 남겨 I 블록으로 4줄을 노리세요.", "표면을 평평하게 유지하고 구멍을 만들지 마세요.", "레벨이 오르면 다음 블록 위치를 미리 정하세요."],
        title="테트리스 - 무료 온라인 클래식 블록 게임 | 미니게임 놀이터",
        keywords="테트리스,테트리스 게임,블록 게임,무료 게임,온라인 게임", canvasAria="테트리스 게임 보드"),
    "minesweeper": dict(name="지뢰찾기", tags=["퍼즐", "추리"],
        cardDesc="숫자 힌트로 지뢰 위치를 추리하고 모두 깃발을 꽂으면 승리!",
        sub="숫자는 주변 8칸의 지뢰 수입니다. 추리해서 모두 깃발을 꽂으세요!",
        howto=["왼쪽 클릭(모바일은 탭)으로 칸 열기.",
               "오른쪽 클릭(길게 누르기)으로 깃발 꽂기/제거.",
               "숫자는 주변 8칸에 숨은 지뢰 수를 뜻합니다.",
               "지뢰가 아닌 칸을 모두 열면 승리. 첫 클릭은 항상 안전합니다."],
        tips=["모서리와 가장자리부터 시작하면 추리가 쉽습니다.", "숫자 주변에 필요한 깃발이 다 꽂혔다면 나머지 칸은 안전합니다.", "애매하면 표시해 두고 다른 구역부터 뚫으세요."],
        title="지뢰찾기 - 무료 온라인 클래식 퍼즐 | 미니게임 놀이터",
        keywords="지뢰찾기,지뢰찾기 게임,클래식 퍼즐,무료 게임,온라인 게임", canvasAria="지뢰찾기 보드",
        diffs=[("easy", "초급 9×9 (지뢰 10개)"), ("medium", "중급 12×12 (지뢰 24개)"), ("hard", "고급 16×16 (지뢰 40개)")]),
    "gomoku": dict(name="오목", tags=["보드", "AI 대전"],
        cardDesc="먼저 다섯 개를 연결하면 승리. 내장 AI와 언제든 대국하세요.",
        sub="당신은 흑돌 선수! AI를 상대로 먼저 다섯 개를 연결하면 승리합니다.",
        howto=["바둑판 교차점을 클릭해 돌을 놓으세요. 당신은 흑돌 선수입니다.",
               "가로·세로·대각선으로 먼저 5개를 연결하면 승리.",
               "내장 AI가 백돌을 두며 공수 균형을 맞춥니다.",
               "판이 다 차도 승부가 나지 않으면 무승부."],
        tips=["초반엔 중앙 부근을 차지해 주도권을 잡으세요.", "열린 3과 4를 만들어 공격하세요.", "상대의 3이 보이면 제때 막으세요."],
        title="오목 게임 - AI 대전 무료 온라인 | 미니게임 놀이터",
        keywords="오목,오목 게임,오목 AI 대전,보드 게임,무료 게임", canvasAria="오목 판"),
    "memory": dict(name="메모리 카드", tags=["퍼즐", "기억력"],
        cardDesc="카드를 뒤집어 그림을 기억하고 모든 짝을 찾아 기억력을 훈련하세요.",
        sub="한 번에 두 장씩 뒤집어 같은 그림을 맞추세요. 8쌍을 최대한 적은 횟수로 찾아보세요!",
        howto=["카드를 클릭해 뒤집으세요. 한 번에 최대 두 장까지 열립니다.",
               "그림이 같으면 짝이 맞아 열린 상태로 유지됩니다.",
               "다르면 다시 뒤집히니 위치를 기억하세요!",
               "8쌍을 모두 찾으면 승리. 적은 횟수일수록 좋은 기록입니다."],
        tips=["순서대로 뒤집으며 위치에 번호를 매겨 기억하세요.", "새 그림이 나오면 전에 봤는지 바로 떠올리세요.", "맞춘 짝은 기억에서 지워 범위를 줄이세요."],
        title="메모리 카드 게임 - 기억력 훈련 무료 온라인 | 미니게임 놀이터",
        keywords="메모리 카드,짝 맞추기,기억력 게임,카드 뒤집기,무료 게임", canvasAria="메모리 카드 영역"),
}

# ============ 游戏内 JS 提示文案（注入 window.GAME_I18N） ============
JS_I18N = {
    "zh": {
        "snake": {"gameOver": "游戏结束！得分 {score}", "paused": "已暂停"},
        "2048": {"win": "🎉 合成 2048！还能继续挑战更高分", "gameOver": "游戏结束！得分 {score}", "newGame": "新的一局开始！"},
        "tetris": {"gameOver": "游戏结束！得分 {score}", "paused": "已暂停"},
        "minesweeper": {"boom": "踩到地雷了！用时 {time} 秒", "win": "🎉 扫雷成功！用时 {time} 秒"},
        "gomoku": {"yourTurn": "轮到你落子（黑棋）", "youWin": "🎉 你赢了！", "youWinToast": "🎉 恭喜，五子连珠！",
                   "aiWins": "电脑获胜，再来一局？", "aiWinsToast": "电脑获胜，点击重新开始再战！",
                   "draw": "平局！", "drawToast": "棋盘已满，平局！", "thinking": "电脑思考中…"},
        "memory": {"win": "🎉 全部配对成功！{moves} 步 · {time} 秒", "card": "卡片 {n}"},
    },
    "en": {
        "snake": {"gameOver": "Game over! Score: {score}", "paused": "Paused"},
        "2048": {"win": "🎉 You made 2048! Keep going for a higher score", "gameOver": "Game over! Score: {score}", "newGame": "New game started!"},
        "tetris": {"gameOver": "Game over! Score: {score}", "paused": "Paused"},
        "minesweeper": {"boom": "Boom! You hit a mine. Time: {time}s", "win": "🎉 Cleared! Time: {time}s"},
        "gomoku": {"yourTurn": "Your turn (Black)", "youWin": "🎉 You win!", "youWinToast": "🎉 Congratulations, five in a row!",
                   "aiWins": "The computer wins. Play again?", "aiWinsToast": "The computer wins — hit Restart for a rematch!",
                   "draw": "It's a draw!", "drawToast": "Board full — it's a draw!", "thinking": "Computer is thinking…"},
        "memory": {"win": "🎉 All pairs found! {moves} moves · {time}s", "card": "Card {n}"},
    },
    "es": {
        "snake": {"gameOver": "¡Fin del juego! Puntos: {score}", "paused": "En pausa"},
        "2048": {"win": "🎉 ¡Lograste 2048! Sigue por más puntos", "gameOver": "¡Fin del juego! Puntos: {score}", "newGame": "¡Nueva partida!"},
        "tetris": {"gameOver": "¡Fin del juego! Puntos: {score}", "paused": "En pausa"},
        "minesweeper": {"boom": "¡Boom! Pisaste una mina. Tiempo: {time} s", "win": "🎉 ¡Completado! Tiempo: {time} s"},
        "gomoku": {"yourTurn": "Tu turno (negras)", "youWin": "🎉 ¡Ganaste!", "youWinToast": "🎉 ¡Felicidades, cinco en raya!",
                   "aiWins": "Gana la computadora. ¿Otra?", "aiWinsToast": "Gana la computadora: pulsa Reiniciar para la revancha",
                   "draw": "¡Empate!", "drawToast": "Tablero lleno: ¡empate!", "thinking": "La computadora piensa…"},
        "memory": {"win": "🎉 ¡Todas las parejas! {moves} movimientos · {time} s", "card": "Carta {n}"},
    },
    "ar": {
        "snake": {"gameOver": "انتهت اللعبة! النقاط: {score}", "paused": "إيقاف مؤقت"},
        "2048": {"win": "🎉 صنعت 2048! واصل لتحقيق نقاط أعلى", "gameOver": "انتهت اللعبة! النقاط: {score}", "newGame": "بدأت جولة جديدة!"},
        "tetris": {"gameOver": "انتهت اللعبة! النقاط: {score}", "paused": "إيقاف مؤقت"},
        "minesweeper": {"boom": "بوم! دست على لغم. الوقت: {time} ث", "win": "🎉 أُنجز! الوقت: {time} ث"},
        "gomoku": {"yourTurn": "دورك (الأسود)", "youWin": "🎉 فزت!", "youWinToast": "🎉 تهانينا، خمسة متتالية!",
                   "aiWins": "فاز الحاسوب. جولة أخرى؟", "aiWinsToast": "فاز الحاسوب — اضغط «إعادة» للثأر!",
                   "draw": "تعادل!", "drawToast": "اللوحة ممتلئة — تعادل!", "thinking": "الحاسوب يفكر…"},
        "memory": {"win": "🎉 كل الأزواج! {moves} محاولة · {time} ث", "card": "بطاقة {n}"},
    },
    "ru": {
        "snake": {"gameOver": "Игра окончена! Счёт: {score}", "paused": "Пауза"},
        "2048": {"win": "🎉 2048 собрано! Продолжайте ради рекорда", "gameOver": "Игра окончена! Счёт: {score}", "newGame": "Новая игра!"},
        "tetris": {"gameOver": "Игра окончена! Счёт: {score}", "paused": "Пауза"},
        "minesweeper": {"boom": "Бум! Вы наступили на мину. Время: {time} с", "win": "🎉 Поле очищено! Время: {time} с"},
        "gomoku": {"yourTurn": "Ваш ход (чёрные)", "youWin": "🎉 Вы победили!", "youWinToast": "🎉 Поздравляем, пять в ряд!",
                   "aiWins": "Победил компьютер. Ещё партию?", "aiWinsToast": "Победил компьютер — нажмите «Заново» для реванша!",
                   "draw": "Ничья!", "drawToast": "Доска заполнена — ничья!", "thinking": "Компьютер думает…"},
        "memory": {"win": "🎉 Все пары найдены! {moves} ходов · {time} с", "card": "Карта {n}"},
    },
    "ja": {
        "snake": {"gameOver": "ゲームオーバー！スコア {score}", "paused": "一時停止中"},
        "2048": {"win": "🎉 2048達成！さらにハイスコアを目指そう", "gameOver": "ゲームオーバー！スコア {score}", "newGame": "新しいゲーム開始！"},
        "tetris": {"gameOver": "ゲームオーバー！スコア {score}", "paused": "一時停止中"},
        "minesweeper": {"boom": "地雷を踏んだ！タイム {time} 秒", "win": "🎉 クリア！タイム {time} 秒"},
        "gomoku": {"yourTurn": "あなたの番（黒）", "youWin": "🎉 あなたの勝ち！", "youWinToast": "🎉 おめでとう、五目並べ！",
                   "aiWins": "コンピュータの勝ち。もう一局？", "aiWinsToast": "コンピュータの勝ち。リスタートでもう一度！",
                   "draw": "引き分け！", "drawToast": "盤が埋まりました。引き分け！", "thinking": "コンピュータが考え中…"},
        "memory": {"win": "🎉 全ペア完成！{moves} 手 · {time} 秒", "card": "カード {n}"},
    },
    "ko": {
        "snake": {"gameOver": "게임 종료! 점수: {score}", "paused": "일시정지됨"},
        "2048": {"win": "🎉 2048 달성! 더 높은 점수에 도전하세요", "gameOver": "게임 종료! 점수: {score}", "newGame": "새 게임 시작!"},
        "tetris": {"gameOver": "게임 종료! 점수: {score}", "paused": "일시정지됨"},
        "minesweeper": {"boom": "지뢰를 밟았습니다! 시간: {time}초", "win": "🎉 성공! 시간: {time}초"},
        "gomoku": {"yourTurn": "당신의 차례 (흑돌)", "youWin": "🎉 당신의 승리!", "youWinToast": "🎉 축하합니다, 오목 완성!",
                   "aiWins": "컴퓨터 승리. 한 판 더?", "aiWinsToast": "컴퓨터가 이겼습니다. 다시 시작을 눌러 재대결하세요!",
                   "draw": "무승부!", "drawToast": "판이 가득 찼습니다. 무승부!", "thinking": "컴퓨터가 생각 중…"},
        "memory": {"win": "🎉 모든 짝 완성! {moves}회 · {time}초", "card": "카드 {n}"},
    },
}

# ============ 页面模板与生成 ============

def prefix(lang):
    return "" if lang == DEFAULT_LANG else "/" + lang


def page_url(lang, rel):
    return BASE + prefix(lang) + rel


def hreflang_block(rel):
    lines = []
    for lang in LANG_ORDER:
        lines.append('  <link rel="alternate" hreflang="%s" href="%s" />' % (COMMON[lang]["htmlLang"], page_url(lang, rel)))
    lines.append('  <link rel="alternate" hreflang="x-default" href="%s" />' % page_url(DEFAULT_LANG, rel))
    return "\n".join(lines)


def lang_switcher(rel, cur):
    items = []
    for lang in LANG_ORDER:
        href = prefix(lang) + rel
        cls = ' class="cur"' if lang == cur else ""
        items.append('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (
            href, COMMON[lang]["htmlLang"], COMMON[lang]["htmlLang"], cls, COMMON[lang]["native"]))
    return ('<details class="lang-switch"><summary aria-label="Language / 语言">🌐 ' +
            COMMON[cur]["native"] + '</summary><ul>' + "".join(items) + "</ul></details>")


def head(lang, rel, title, desc, keywords, jsonlds, is_home):
    c = COMMON[lang]
    canonical = page_url(lang, rel)
    og_image = '\n  <meta property="og:image" content="%s/assets/og-cover.png" />' % BASE if is_home else ""
    jsonld_html = "\n".join(
        '  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(j, ensure_ascii=False, indent=2)
        for j in jsonlds)
    return """<!DOCTYPE html>
<html lang="{htmlLang}" dir="{dir}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
{hreflang}

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{siteName}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />{og_image}
  <meta property="og:locale" content="{ogLocale}" />
  <meta name="twitter:card" content="{twcard}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <meta name="theme-color" content="#ffd23f" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap" /></noscript>
  <link rel="stylesheet" href="/assets/css/style.css" />

{jsonld}
</head>""".format(htmlLang=c["htmlLang"], dir=c["dir"], title=title, desc=desc, keywords=keywords,
                 canonical=canonical, hreflang=hreflang_block(rel), siteName=c["siteName"],
                 og_image=og_image, ogLocale=c["ogLocale"],
                 twcard="summary_large_image" if is_home else "summary", jsonld=jsonld_html)


def header(lang, rel, current):
    c = COMMON[lang]
    p = prefix(lang)
    return """<body>
  <header class="site-header">
    <nav class="nav" aria-label="主导航">
      <a class="logo" href="{p}/"><span class="logo-icon" aria-hidden="true">🕹️</span>{siteName}</a>
      <ul class="nav-links">
        <li><a href="{p}/"{home_cur}>{home}</a></li>
        <li><a href="{p}/#games">{navGames}</a></li>
        {about_li}
      </ul>
      {switcher}
    </nav>
  </header>""".format(p=p, siteName=c["siteName"], home=c["home"], navGames=c["navGames"],
                      home_cur=' aria-current="page"' if current == "home" else "",
                      about_li='<li><a href="%s/#about">%s</a></li>' % (p, c["navAbout"]) if current == "home" else "",
                      switcher=lang_switcher(rel, lang))


def footer(lang):
    c = COMMON[lang]
    p = prefix(lang)
    links = ['<li><a href="%s/">%s</a></li>' % (p, c["home"])]
    for g in GAMES:
        links.append('<li><a href="%s/games/%s/">%s %s</a></li>' % (p, g["slug"], g["icon"], GDATA[lang][g["slug"]]["name"]))
    return """  <footer class="site-footer">
    <ul class="footer-links">
      {links}
    </ul>
    <p>{footer}</p>
  </footer>
</body>
</html>
""".format(links="\n      ".join(links), footer=c["footer"])


def breadcrumb(lang, items):
    c = COMMON[lang]
    lis = []
    for i, (name, url) in enumerate(items):
        if url:
            lis.append('<li><a href="%s">%s</a></li>' % (url, name))
        else:
            lis.append('<li aria-current="page">%s</li>' % name)
    return """  <nav class="breadcrumb" aria-label="{aria}">
    <ol>
      {lis}
    </ol>
  </nav>""".format(aria=c["breadcrumbAria"], lis="\n      ".join(lis))


def video_game_ld(lang, slug):
    g = GDATA[lang][slug]
    return {"@context": "https://schema.org", "@type": "VideoGame",
            "name": g["name"], "url": page_url(lang, "/games/%s/" % slug),
            "description": g["cardDesc"], "genre": g["tags"][0],
            "gamePlatform": "Web Browser", "applicationCategory": "Game",
            "operatingSystem": "Any", "inLanguage": COMMON[lang]["htmlLang"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}


def breadcrumb_ld(lang, items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": name,
                                 "item": page_url(lang, url)} for i, (name, url) in enumerate(items)]}


def home_page(lang):
    c, h = COMMON[lang], HOME[lang]
    p = prefix(lang)

    cards = []
    for g in GAMES:
        d = GDATA[lang][g["slug"]]
        style = "background:%s;" % g["color"]
        if g.get("bannerLight"):
            style += "color:#fff;"
        tags = "".join('<span class="tag">%s</span>' % t for t in d["tags"])
        cards.append("""        <li>
          <article class="game-card">
            <div class="card-banner" style="{style}" aria-hidden="true">{icon}</div>
            <div class="card-body">
              <h3>{name}</h3>
              <div class="card-tags">{tags}</div>
              <p>{desc}</p>
              <a class="btn play-link" href="{p}/games/{slug}/">{play}</a>
            </div>
          </article>
        </li>""".format(style=style, icon=g["icon"], name=d["name"], tags=tags,
                        desc=d["cardDesc"], p=p, slug=g["slug"], play=c["playBtn"]))

    website_ld = {"@context": "https://schema.org", "@type": "WebSite",
                  "name": c["siteName"], "url": page_url(lang, "/"),
                  "description": h["metaDesc"], "inLanguage": c["htmlLang"]}
    itemlist_ld = {"@context": "https://schema.org", "@type": "ItemList",
                   "name": h["gamesTitle"],
                   "itemListElement": [
                       {"@type": "ListItem", "position": i + 1,
                        "item": {"@type": "VideoGame", "name": GDATA[lang][g["slug"]]["name"],
                                 "url": page_url(lang, "/games/%s/" % g["slug"]),
                                 "applicationCategory": "Game",
                                 "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}
                       for i, g in enumerate(GAMES)]}

    stats = "".join("<span>%s</span>" % s for s in h["stats"])

    body = """  <main>
    <section class="hero">
      <span class="hero-badge">{badge}</span>
      <h1>{h1Pre}<span class="hl">{h1Hl}</span>{h1Post}</h1>
      <p>{heroP}</p>
      <div class="hero-stats">{stats}</div>
    </section>

    <section class="section" id="games" aria-labelledby="games-title">
      <h2 class="section-title" id="games-title">{gamesTitle}</h2>
      <p class="section-desc">{gamesDesc}</p>
      <ul class="game-grid">
{cards}
      </ul>
    </section>

    <section class="prose" id="about" aria-labelledby="about-title">
      <h2 id="about-title">{aboutH2}</h2>
      <p>{aboutP}</p>
      <h2>{chooseH2}</h2>
      <p>{chooseP}</p>
    </section>
  </main>
""".format(badge=h["badge"], h1Pre=h["h1Pre"], h1Hl=h["h1Hl"], h1Post=h["h1Post"],
           heroP=h["heroP"], stats=stats, gamesTitle=h["gamesTitle"], gamesDesc=h["gamesDesc"],
           cards="\n".join(cards), aboutH2=h["aboutH2"], aboutP=h["aboutP"],
           chooseH2=h["chooseH2"], chooseP=h["chooseP"])

    return (head(lang, "/", h["metaTitle"], h["metaDesc"], h["metaKeywords"],
                 [website_ld, itemlist_ld], is_home=True) + "\n" +
            header(lang, "/", "home") + "\n" + body + "\n" + footer(lang))


def hud_item(label, value, vid=None):
    id_attr = ' id="%s"' % vid if vid else ""
    return '<div class="hud-item"><small>%s</small><span%s>%s</span></div>' % (label, id_attr, value)


def btn(cls, bid, label):
    return '<button class="btn %s" id="%s" type="button">%s</button>' % (cls, bid, label)


def stage_html(lang, slug, gmeta):
    c = COMMON[lang]
    d = GDATA[lang][slug]

    if slug == "snake":
        hud = hud_item(c["score"], "0", "score") + hud_item(c["best"], "0", "best")
        canvas = '<canvas id="game-canvas" width="400" height="400" role="img" aria-label="%s"></canvas>' % d["canvasAria"]
        controls = btn("btn-green", "btn-start", c["start"]) + btn("btn-cyan", "btn-pause", c["pause"]) + btn("btn-pink", "btn-restart", c["restart"])
        pad = """<div class="pad" aria-label="Touch controls">
          <span></span><button type="button" data-dir="up" aria-label="{up}">▲</button><span></span>
          <button type="button" data-dir="left" aria-label="{left}">◀</button>
          <button type="button" data-dir="down" aria-label="{down}">▼</button>
          <button type="button" data-dir="right" aria-label="{right}">▶</button>
        </div>""".format(up=c["up"], left=c["left"], down=c["down"], right=c["right"])

    elif slug == "2048":
        hud = hud_item(c["score"], "0", "score") + hud_item(c["best"], "0", "best")
        canvas = '<div id="board" class="grid-board board-2048" role="grid" aria-label="%s"></div>' % d["canvasAria"]
        controls = btn("btn-pink", "btn-restart", c["restart"])
        pad = ""

    elif slug == "tetris":
        hud = hud_item(c["score"], "0", "score") + hud_item(c["lines"], "0", "lines") + hud_item(c["level"], "1", "level")
        canvas = """<div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;justify-content:center;">
          <canvas id="game-canvas" width="240" height="480" role="img" aria-label="{aria}"></canvas>
          <div style="display:flex;flex-direction:column;gap:8px;align-items:center;">
            <strong>{nxt}</strong>
            <canvas id="next-canvas" width="96" height="84" style="background:#141428;border:3px solid var(--ink);border-radius:12px;" role="img" aria-label="{nxt}"></canvas>
          </div>
        </div>""".format(aria=d["canvasAria"], nxt=c["nxt"])
        controls = btn("btn-green", "btn-start", c["start"]) + btn("btn-cyan", "btn-pause", c["pause"]) + btn("btn-pink", "btn-restart", c["restart"])
        pad = """<div class="pad" aria-label="Touch controls" style="grid-template-columns:repeat(5,60px);grid-template-rows:56px;">
          <button type="button" data-act="left" aria-label="{left}">◀</button>
          <button type="button" data-act="rotate" aria-label="{rotate}">⟳</button>
          <button type="button" data-act="right" aria-label="{right}">▶</button>
          <button type="button" data-act="down" aria-label="{hardDrop}">▼</button>
          <button type="button" data-act="drop" aria-label="{drop}">⤓</button>
        </div>""".format(left=c["left"], rotate=c["rotate"], right=c["right"], hardDrop=c["hardDrop"], drop=c["drop"])

    elif slug == "minesweeper":
        hud = hud_item(c["minesLeft"], "10", "mines") + hud_item(c["status"], "🙂", "status") + hud_item(c["time"], "0", "time")
        options = "".join('<option value="%s"%s>%s</option>' % (v, ' selected' if i == 0 else "", label)
                          for i, (v, label) in enumerate(d["diffs"]))
        canvas = """<div class="controls-row">
          <label for="difficulty" style="font-weight:700;">{diff}</label>
          <select id="difficulty" style="font-family:inherit;font-size:1rem;padding:6px 12px;border:3px solid var(--ink);border-radius:10px;background:#fff;">
            {options}
          </select>
          {restart}
        </div>
        <div style="overflow-x:auto;max-width:100%;">
          <div id="board" class="grid-board board-mine" role="grid" aria-label="{aria}"></div>
        </div>""".format(diff=c["difficulty"], options=options,
                         restart=btn("btn-pink", "btn-restart", c["restart"]), aria=d["canvasAria"])
        controls = ""
        pad = ""

    elif slug == "gomoku":
        hud = hud_item(c["gameStatus"], JS_I18N[lang]["gomoku"]["yourTurn"], "status")
        canvas = '<canvas id="game-canvas" width="480" height="480" style="background:#f5c96b;" role="img" aria-label="%s"></canvas>' % d["canvasAria"]
        controls = btn("btn-pink", "btn-restart", c["restart"])
        pad = ""

    elif slug == "memory":
        hud = hud_item(c["moves"], "0", "moves") + hud_item(c["pairs"], "0 / 8", "pairs") + hud_item(c["time"], "0", "time")
        canvas = '<div id="board" class="grid-board board-memory" role="grid" aria-label="%s"></div>' % d["canvasAria"]
        controls = btn("btn-pink", "btn-restart", c["restart"])
        pad = ""

    controls_html = '<div class="controls-row">%s</div>' % controls if controls else ""
    return """      <section class="stage" aria-label="{stageAria}">
        <div class="hud">
          {hud}
        </div>
        {canvas}
        {controls}
        {pad}
      </section>""".format(stageAria=c["stageAria"], hud=hud, canvas=canvas, controls=controls_html, pad=pad)


def game_page(lang, slug):
    c = COMMON[lang]
    d = GDATA[lang][slug]
    gmeta = next(g for g in GAMES if g["slug"] == slug)
    p = prefix(lang)
    rel = "/games/%s/" % slug

    howto = "\n            ".join("<li>%s</li>" % x for x in d["howto"])
    tips = "\n            ".join("<li>%s</li>" % x for x in d["tips"])

    more = []
    for g in GAMES:
        if g["slug"] == slug:
            continue
        more.append('<li><a href="%s/games/%s/">%s %s</a></li>' % (p, g["slug"], g["icon"], GDATA[lang][g["slug"]]["name"]))

    jsonlds = [video_game_ld(lang, slug),
               breadcrumb_ld(lang, [(c["home"], "/"), (d["name"], rel)])]

    game_i18n = json.dumps(JS_I18N[lang][slug], ensure_ascii=False)

    body = """{breadcrumb}

  <main class="game-page">
    <h1>{icon} {name}</h1>
    <p class="game-sub">{sub}</p>

    <div class="game-layout">
{stage}

      <aside class="side-panel">
        <section class="panel">
          <h2>{howTo}</h2>
          <ul>
            {howto}
          </ul>
        </section>
        <section class="panel">
          <h2>{tipsT}</h2>
          <ul>
            {tips}
          </ul>
        </section>
        <section class="panel">
          <h2>{moreGames}</h2>
          <ul class="more-games">
            {more}
          </ul>
        </section>
      </aside>
    </div>
  </main>

  <div class="toast" id="toast" role="status"></div>

  <script>window.GAME_I18N = {gameI18n};</script>
  <script src="/assets/js/games/{js}" defer></script>
""".format(breadcrumb=breadcrumb(lang, [(c["home"], p + "/"), (d["name"], None)]),
           icon=gmeta["icon"], name=d["name"], sub=d["sub"],
           stage=stage_html(lang, slug, gmeta), howTo=c["howTo"], howto=howto,
           tipsT=c["tips"], tips=tips, moreGames=c["moreGames"],
           more="\n            ".join(more), gameI18n=game_i18n, js=gmeta["js"])

    return (head(lang, rel, d["title"], d["cardDesc"], d["keywords"], jsonlds, is_home=False) + "\n" +
            header(lang, rel, "game") + "\n" + body + footer(lang))


def write(rel_path, content):
    path = os.path.join(ROOT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_sitemap():
    urls = ["/"] + ["/games/%s/" % g["slug"] for g in GAMES]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in urls:
        # 每个语言一个 <url> 条目，含全部 alternate
        for lang in LANG_ORDER:
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % page_url(lang, rel))
            for alt in LANG_ORDER:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s" />' % (
                    COMMON[alt]["htmlLang"], page_url(alt, rel)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s" />' % page_url(DEFAULT_LANG, rel))
            out.append("    <lastmod>%s</lastmod>" % LASTMOD)
            out.append("    <changefreq>%s</changefreq>" % ("weekly" if rel == "/" else "monthly"))
            out.append("    <priority>%s</priority>" % ("1.0" if rel == "/" else "0.8"))
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    count = 0
    for lang in LANG_ORDER:
        write(prefix(lang) + "/index.html", home_page(lang))
        count += 1
        for g in GAMES:
            write(prefix(lang) + "/games/%s/index.html" % g["slug"], game_page(lang, g["slug"]))
            count += 1
    write("/sitemap.xml", build_sitemap())
    print("生成完成：%d 个页面 + sitemap.xml" % count)


if __name__ == "__main__":
    main()
