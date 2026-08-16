# -*- coding: utf-8 -*-
"""
多语言静态页面生成脚本
用法：python3 tools/build_i18n.py
生成：中文(根目录) + en/es/ar/ru/ja/ko 六个语言子目录
页面：首页 + 6 个游戏页 + 8 个站点页（About/Contact/Privacy/Terms/Cookie/DMCA/Categories/New Games）
共 49 个游戏/首页 + 8*7=56 个站点页 + sitemap.xml
部署前请把 BASE 改成真实域名。
"""
import json
import os

BASE = "https://games-hub.cc"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LASTMOD = "2026-08-11"

LANG_ORDER = ["en", "zh", "es", "ar", "ru", "ja", "ko"]
DEFAULT_LANG = "en"  # 默认语言：根目录 /

# 游戏分类（slug -> 多语言名称），用于 Categories 页与首页 Game Categories 区
CATEGORIES = [
    dict(slug="action", icon="⚔️"),
    dict(slug="adventure", icon="🗺️"),
    dict(slug="arcade", icon="🕹️"),
    dict(slug="puzzle", icon="🧩"),
    dict(slug="racing", icon="🏎️"),
    dict(slug="sports", icon="⚽"),
    dict(slug="strategy", icon="♟️"),
    dict(slug="multiplayer", icon="👥"),
]

COMMON = {
    "zh": dict(code="zh", htmlLang="zh-CN", dir="ltr", ogLocale="zh_CN", native="中文",
        siteName="街机小游戏乐园", home="首页", navGames="全部游戏", navCategories="游戏分类",
        navNew="最新游戏", navPopular="热门游戏", navAbout="关于我们", navContact="联系我们",
        navPrivacy="隐私政策", navTerms="服务条款", navCookie="Cookie 政策", navDmca="版权声明",
        moreGames="🕹️ 更多游戏", howTo="🎯 玩法说明", tips="💡 高分技巧",
        start="开始", pause="暂停", restart="重新开始", playBtn="开始游戏",
        footer="© 2026 街机小游戏乐园 · 免费在线小游戏，即点即玩",
        stageAria="游戏区", breadcrumbAria="面包屑",
        score="当前得分", best="历史最高", lines="消除行数", level="等级", nxt="下一个",
        minesLeft="剩余地雷", status="状态", time="用时（秒）", moves="步数", pairs="已配对",
        gameStatus="对局状态", difficulty="难度：",
        up="向上", down="向下", left="向左", right="向右", rotate="旋转", drop="直接落底",
        hardDrop="加速下落", catSoon="该分类的专属游戏正在筹备中，先试试下面这些人气小游戏吧：", allCategories="查看全部游戏分类", attempts="出手", steps="步数"),
    "en": dict(code="en", htmlLang="en", dir="ltr", ogLocale="en_US", native="English",
        siteName="Arcade Games Hub", home="Home", navGames="All Games", navCategories="Categories",
        navNew="New Games", navPopular="Popular Games", navAbout="About Us", navContact="Contact Us",
        navPrivacy="Privacy Policy", navTerms="Terms of Service", navCookie="Cookie Policy", navDmca="DMCA / Copyright",
        moreGames="🕹️ More games", howTo="🎯 How to play", tips="💡 Pro tips",
        start="Start", pause="Pause", restart="Restart", playBtn="Play",
        footer="© 2026 Arcade Games Hub · Free online games, play instantly",
        stageAria="Game area", breadcrumbAria="Breadcrumb",
        score="Score", best="Best", lines="Lines", level="Level", nxt="Next",
        minesLeft="Mines left", status="Status", time="Time (s)", moves="Moves", pairs="Pairs",
        gameStatus="Game status", difficulty="Difficulty: ",
        up="Up", down="Down", left="Left", right="Right", rotate="Rotate", drop="Hard drop",
        hardDrop="Soft drop", catSoon="More games for this category are on the way — try these fan favorites for now:", allCategories="View all game categories", attempts="Shots", steps="Steps"),
    "es": dict(code="es", htmlLang="es", dir="ltr", ogLocale="es_ES", native="Español",
        siteName="Arcade de Minijuegos", home="Inicio", navGames="Todos los juegos", navCategories="Categorías",
        navNew="Nuevos juegos", navPopular="Juegos populares", navAbout="Acerca de", navContact="Contáctanos",
        navPrivacy="Política de privacidad", navTerms="Términos del servicio", navCookie="Política de cookies", navDmca="DMCA / Derechos",
        moreGames="🕹️ Más juegos", howTo="🎯 Cómo jugar", tips="💡 Consejos",
        start="Comenzar", pause="Pausa", restart="Reiniciar", playBtn="Jugar",
        footer="© 2026 Arcade de Minijuegos · Juegos en línea gratis, juega al instante",
        stageAria="Zona de juego", breadcrumbAria="Migas de pan",
        score="Puntos", best="Récord", lines="Líneas", level="Nivel", nxt="Siguiente",
        minesLeft="Minas restantes", status="Estado", time="Tiempo (s)", moves="Movimientos", pairs="Parejas",
        gameStatus="Estado de la partida", difficulty="Dificultad: ",
        up="Arriba", down="Abajo", left="Izquierda", right="Derecha", rotate="Girar", drop="Caída instantánea",
        hardDrop="Caída rápida", catSoon="Más juegos de esta categoría están en camino — prueba estos favoritos:", allCategories="Ver todas las categorías", attempts="Tiros", steps="Pasos"),
    "ar": dict(code="ar", htmlLang="ar", dir="rtl", ogLocale="ar_AR", native="العربية",
        siteName="ألعاب الأركيد", home="الرئيسية", navGames="كل الألعاب", navCategories="الفئات",
        navNew="ألعاب جديدة", navPopular="ألعاب رائجة", navAbout="من نحن", navContact="اتصل بنا",
        navPrivacy="سياسة الخصوصية", navTerms="شروط الخدمة", navCookie="سياسة ملفات الارتباط", navDmca="DMCA / حقوق النشر",
        moreGames="🕹️ المزيد من الألعاب", howTo="🎯 طريقة اللعب", tips="💡 نصائح",
        start="ابدأ", pause="إيقاف مؤقت", restart="إعادة", playBtn="العب الآن",
        footer="© 2026 ألعاب الأركيد · ألعاب مجانية عبر الإنترنت، العب فورًا",
        stageAria="منطقة اللعب", breadcrumbAria="مسار التنقل",
        score="النقاط", best="الأفضل", lines="الصفوف", level="المستوى", nxt="التالية",
        minesLeft="الألغام المتبقية", status="الحالة", time="الوقت (ث)", moves="المحاولات", pairs="الأزواج",
        gameStatus="حالة المباراة", difficulty="الصعوبة: ",
        up="أعلى", down="أسفل", left="يسار", right="يمين", rotate="تدوير", drop="إسقاط فوري",
        hardDrop="نزول سريع", catSoon="مزيد من ألعاب هذه الفئة قادمة قريبًا — جرّب هذه المفضلة:", allCategories="عرض كل الفئات", attempts="رميات", steps="خطوات"),
    "ru": dict(code="ru", htmlLang="ru", dir="ltr", ogLocale="ru_RU", native="Русский",
        siteName="Аркадные мини-игры", home="Главная", navGames="Все игры", navCategories="Категории",
        navNew="Новые игры", navPopular="Популярные игры", navAbout="О нас", navContact="Связаться",
        navPrivacy="Политика конфиденциальности", navTerms="Условия обслуживания", navCookie="Политика Cookie", navDmca="DMCA / Авторские права",
        moreGames="🕹️ Ещё игры", howTo="🎯 Как играть", tips="💡 Советы",
        start="Старт", pause="Пауза", restart="Заново", playBtn="Играть",
        footer="© 2026 Аркадные мини-игры · Бесплатные онлайн-игры — играйте сразу",
        stageAria="Игровое поле", breadcrumbAria="Хлебные крошки",
        score="Счёт", best="Рекорд", lines="Линии", level="Уровень", nxt="Далее",
        minesLeft="Мин осталось", status="Статус", time="Время (с)", moves="Ходы", pairs="Пары",
        gameStatus="Статус партии", difficulty="Сложность: ",
        up="Вверх", down="Вниз", left="Влево", right="Вправо", rotate="Поворот", drop="Сбросить",
        hardDrop="Ускорить", catSoon="Ещё игры этой категории готовятся — пока попробуйте эти популярные:", allCategories="Все категории", attempts="Броски", steps="Шаги"),
    "ja": dict(code="ja", htmlLang="ja", dir="ltr", ogLocale="ja_JP", native="日本語",
        siteName="ミニゲームランド", home="ホーム", navGames="ゲーム一覧", navCategories="カテゴリ",
        navNew="新着ゲーム", navPopular="人気ゲーム", navAbout="運営者情報", navContact="お問い合わせ",
        navPrivacy="プライバシーポリシー", navTerms="利用規約", navCookie="Cookie ポリシー", navDmca="DMCA / 著作権",
        moreGames="🕹️ 他のゲーム", howTo="🎯 遊び方", tips="💡 上達のコツ",
        start="スタート", pause="一時停止", restart="もう一度", playBtn="プレイ",
        footer="© 2026 ミニゲームランド · 無料オンラインゲーム、すぐに遊べる",
        stageAria="ゲームエリア", breadcrumbAria="パンくずリスト",
        score="スコア", best="ベスト", lines="消去ライン", level="レベル", nxt="次",
        minesLeft="残り地雷", status="状態", time="タイム（秒）", moves="手数", pairs="ペア成立",
        gameStatus="対局状態", difficulty="難易度：",
        up="上", down="下", left="左", right="右", rotate="回転", drop="即落下",
        hardDrop="高速落下", catSoon="このカテゴリのゲームは準備中です。まずは人気のこちらを:", allCategories="すべてのカテゴリを見る", attempts="シュート", steps="歩数"),
    "ko": dict(code="ko", htmlLang="ko", dir="ltr", ogLocale="ko_KR", native="한국어",
        siteName="미니게임 놀이터", home="홈", navGames="전체 게임", navCategories="카테고리",
        navNew="새로운 게임", navPopular="인기 게임", navAbout="소개", navContact="문의하기",
        navPrivacy="개인정보 처리방침", navTerms="이용 약관", navCookie="쿠키 정책", navDmca="DMCA / 저작권",
        moreGames="🕹️ 다른 게임", howTo="🎯 게임 방법", tips="💡 고득점 팁",
        start="시작", pause="일시정지", restart="다시 시작", playBtn="시작하기",
        footer="© 2026 미니게임 놀이터 · 무료 온라인 게임, 바로 플레이",
        stageAria="게임 영역", breadcrumbAria="탐색 경로",
        score="점수", best="최고 기록", lines="지운 줄", level="레벨", nxt="다음",
        minesLeft="남은 지뢰", status="상태", time="시간(초)", moves="횟수", pairs="맞춘 짝",
        gameStatus="대국 상태", difficulty="난이도: ",
        up="위", down="아래", left="왼쪽", right="오른쪽", rotate="회전", drop="즉시 낙하",
        hardDrop="빠른 낙하", catSoon="이 분류의 게임을 준비 중입니다. 우선 인기 게임을 즐겨보세요:", allCategories="전체 카테고리 보기", attempts="슛", steps="걸음"),
}

HOME = {
    "zh": dict(
        badge="🎮 全部免费 · 即点即玩",
        h1Pre="经典", h1Hl="小游戏", h1Post="合集<br />打开浏览器就能玩",
        heroP="贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌、极速躲避赛车、趣味投篮、迷宫大冒险——9 款陪伴了几代人的经典小游戏，无需下载、无需注册，电脑手机都能流畅游玩。",
        stats=["🕹️ 9 款游戏", "⚡ 零加载等待", "📱 支持手机", "🆓 永久免费"],
        introH2="什么是街机小游戏乐园？",
        introP="街机小游戏乐园（Games Hub）是一个免费的在线浏览器游戏合集网站。我们相信好游戏不需要复杂的下载和注册流程——点开网页，即刻开玩。站内所有游戏均为纯前端实现，加载快、无广告打扰，并针对手机和电脑都做了适配。无论你想打发碎片时间，还是认真挑战高分，这里都有适合你的选择。",
        gamesTitle="全部游戏", gamesDesc="挑一款喜欢的，点击「开始游戏」立即开玩。",
        popularTitle="热门游戏", popularDesc="玩家最常玩的精选合集，闭眼入也不踩雷。",
        categoriesTitle="游戏分类", categoriesDesc="按类型挑选你最爱的玩法。",
        newTitle="最新上架", newDesc="我们持续上新，以下是最新加入的精选游戏。",
        trendingTitle="正在流行", trendingDesc="社区里讨论度最高的小游戏。",
        whyTitle="为什么选择街机小游戏乐园？",
        whyP="网页小游戏无需安装、不占存储空间，通勤路上、课间休息、工作间隙都能随时来一局。经典的贪吃蛇和俄罗斯方块能锻炼反应速度，2048 和扫雷考验逻辑思维，五子棋和记忆翻牌则适合静下心来动脑。无需付费、无需注册，打开即玩。",
        whyItems=[
            ("⚡ 即点即玩", "纯前端实现，无需下载安装，打开网页立刻开玩。"),
            ("📱 全设备适配", "手机、平板、电脑均经过适配，触屏方向与键盘操作都支持。"),
            ("🆓 永久免费", "全部游戏免费，无内购、无付费墙，也没有强制广告打断。"),
            ("🔒 隐私友好", "游戏数据全部保存在本机，我们不收集你的任何个人信息。"),
        ],
        faqTitle="常见问题（FAQ）",
        faq=[
            ("需要下载或注册吗？", "完全不需要。所有游戏都运行在浏览器里，打开页面即可游玩，也不会要求你注册账号。"),
            ("游戏支持手机吗？", "支持。网站对手机和平板做了触屏适配，方向键、滑动等操作在移动端都能正常使用。"),
            ("游戏会收集我的数据吗？", "不会。游戏进度（如最高分）只保存在你自己的浏览器本地，我们不在服务器端收集任何个人信息。"),
            ("网站收录哪些游戏？", "目前收录 9 款经典街机与小游戏：贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌、极速躲避赛车、趣味投篮和迷宫大冒险，并会持续上新。"),
        ],
        aboutH2="关于街机小游戏乐园",
        aboutP="街机小游戏乐园是一个免费的在线小游戏合集网站。我们相信好游戏不需要复杂的下载和注册流程——点开网页，即刻开玩。站内所有游戏均为纯前端实现，加载快、无广告打扰，并针对手机和电脑都做了适配。",
        chooseH2="为什么选择在线网页小游戏？",
        chooseP="网页小游戏无需安装、不占存储空间，通勤路上、课间休息、工作间隙都能随时来一局。经典的贪吃蛇和俄罗斯方块能锻炼反应速度，2048 和扫雷考验逻辑思维，五子棋和记忆翻牌则适合静下心来动脑。无论你是想打发碎片时间，还是想认真挑战高分，这里都有适合你的选择。",
        metaTitle="街机小游戏乐园 - 免费在线小游戏合集 | 贪吃蛇·2048·俄罗斯方块·扫雷",
        metaDesc="街机小游戏乐园收录 9 款经典免费在线小游戏：贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌、极速躲避赛车、趣味投篮、迷宫大冒险。无需下载、无需注册，打开网页即点即玩，支持电脑和手机。",
        metaKeywords="小游戏,在线小游戏,免费小游戏,网页游戏,贪吃蛇,2048,俄罗斯方块,扫雷,五子棋,记忆翻牌,休闲游戏"),
    "en": dict(
        badge="🎮 100% Free · Play instantly",
        h1Pre="Classic", h1Hl="Mini Games", h1Post="<br />Play right in your browser",
        heroP="Snake, 2048, Tetris, Minesweeper, Gomoku and Memory Match — six timeless classics enjoyed for generations. No downloads, no sign-up, smooth play on desktop and mobile.",
        stats=["🕹️ 9 games", "⚡ Loads instantly", "📱 Mobile friendly", "🆓 Free forever"],
        introH2="What is Arcade Games Hub?",
        introP="Arcade Games Hub (Games Hub) is a free online collection of browser games. We believe great games need no complicated downloads or sign-ups — open the page and play. Every game is built with pure front-end tech: fast loading, no ads, and fully adapted for both phones and computers. Whether you want to kill a few minutes or chase a new high score, there is something here for you.",
        gamesTitle="All games", gamesDesc="Pick a favorite and hit “Play” to jump right in.",
        popularTitle="Popular Games", popularDesc="The crowd-favorites our players keep coming back to.",
        categoriesTitle="Game Categories", categoriesDesc="Browse by the kind of fun you are in the mood for.",
        newTitle="New Games", newDesc="We keep adding titles — here are the latest picks.",
        trendingTitle="Trending Games", trendingDesc="The mini games everyone is talking about right now.",
        whyTitle="Why choose Arcade Games Hub?",
        whyP="Browser mini games need no installation and take up no storage. Play a quick round on your commute, during a break or between tasks. Snake and Tetris sharpen your reflexes, 2048 and Minesweeper train your logic, while Gomoku and Memory Match are perfect for quiet focus. No payment, no sign-up — just open and play.",
        whyItems=[
            ("⚡ Instant play", "Pure front-end, no installs. Open the page and the game is ready in a blink."),
            ("📱 Every device", "Tuned for phones, tablets and desktops — touch and keyboard both work."),
            ("🆓 Free forever", "Every game is free: no in-app purchases, no paywalls, no forced ads."),
            ("🔒 Privacy friendly", "Game data stays on your device. We collect no personal information."),
        ],
        faqTitle="Frequently Asked Questions",
        faq=[
            ("Do I need to download or register?", "Not at all. Every game runs in your browser — just open the page and play. No account required."),
            ("Do games work on mobile?", "Yes. The site is touch-optimized for phones and tablets; on-screen directions and swipe controls work smoothly."),
            ("Do you collect my data?", "No. Progress like high scores is saved only in your own browser. We collect no personal data on our servers."),
            ("Which games are included?", "Six classic mini games: Snake, 2048, Tetris, Minesweeper, Gomoku and Memory Match, with more added over time."),
        ],
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
        stats=["🕹️ 9 juegos", "⚡ Carga al instante", "📱 Compatible con móvil", "🆓 Gratis para siempre"],
        introH2="¿Qué es Arcade de Minijuegos?",
        introP="Arcade de Minijuegos (Games Hub) es una colección gratuita de juegos en el navegador. Creemos que un buen juego no necesita descargas ni registros: abre la página y juega. Todos los juegos usan tecnología web pura: cargan rápido, sin anuncios y adaptados a móvil y PC. Ya quieras pasar el rato o batir tu récord, aquí hay algo para ti.",
        gamesTitle="Todos los juegos", gamesDesc="Elige tu favorito y pulsa «Jugar» para empezar.",
        popularTitle="Juegos populares", popularDesc="Los favoritos a los que nuestros jugadores vuelven siempre.",
        categoriesTitle="Categorías", categoriesDesc="Explora según el tipo de diversión que buscas.",
        newTitle="Nuevos juegos", newDesc="Seguimos añadiendo títulos: estas son las últimas incorporaciones.",
        trendingTitle="Juegos en tendencia", trendingDesc="Los minijuegos de los que todos hablan ahora.",
        whyTitle="¿Por qué elegir Arcade de Minijuegos?",
        whyP="Los minijuegos web no se instalan ni ocupan espacio. Juega una partida rápida en el metro, en el recreo o entre tareas. Snake y Tetris entrenan tus reflejos, 2048 y Buscaminas tu lógica, y Gomoku y Memoria son perfectos para concentrarte. Sin pagos ni registros: abre y juega.",
        whyItems=[
            ("⚡ Juego instantáneo", "Web pura, sin instalaciones. Abre la página y el juego está listo."),
            ("📱 Cualquier dispositivo", "Optimizado para móviles, tablets y PC: táctil y teclado funcionan."),
            ("🆓 Gratis para siempre", "Todos los juegos son gratis: sin compras ni anuncios obligatorios."),
            ("🔒 Respetamos tu privacidad", "Los datos quedan en tu dispositivo. No recopilamos información personal."),
        ],
        faqTitle="Preguntas frecuentes",
        faq=[
            ("¿Necesito descargar o registrarme?", "Para nada. Cada juego funciona en el navegador: abre la página y juega. Sin cuenta."),
            ("¿Funcionan en móvil?", "Sí. El sitio está optimizado para táctil; las flechas en pantalla y el deslizamiento funcionan bien."),
            ("¿Recopilan mis datos?", "No. El progreso (como récords) se guarda solo en tu navegador. No recopilamos datos personales."),
            ("¿Qué juegos incluyen?", "Seis clásicos: Snake, 2048, Tetris, Buscaminas, Gomoku y Memoria, con más por venir."),
        ],
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
        stats=["🕹️ 9 ألعاب", "⚡ تحميل فوري", "📱 تدعم الجوال", "🆓 مجانية دائمًا"],
        introH2="ما هو موقع ألعاب الأركيد؟",
        introP="ألعاب الأركيد (Games Hub) مجموعة مجانية من ألعاب المتصفح. نؤمن بأن اللعبة الجيدة لا تحتاج تنزيلًا أو تسجيلًا — افتح الصفحة والعب. جميع الألعاب مبنية بتقنيات الويب الخالصة: تحميل سريع، بلا إعلانات، ومتكيفة مع الجوال والحاسوب. سواء أردت تمضية الوقت أو تحطيم رقمك القياسي، ستجد ما يناسبك.",
        gamesTitle="كل الألعاب", gamesDesc="اختر لعبتك المفضلة واضغط «العب الآن» لتبدأ فورًا.",
        popularTitle="ألعاب رائجة", popularDesc="الألعاب المفضلة التي يعود إليها اللاعبون دائمًا.",
        categoriesTitle="الفئات", categoriesDesc="تصفح حسب نوع المتعة التي ترغب بها.",
        newTitle="ألعاب جديدة", newDesc="نضيف ألعاب باستمرار — هذه أحدث الاختيارات.",
        trendingTitle="ألعاب متداولة", trendingDesc="الألعاب التي يتحدث عنها الجميع الآن.",
        whyTitle="لماذا تختار ألعاب الأركيد؟",
        whyP="ألعاب المتصفح لا تحتاج تثبيتًا ولا تشغل مساحة. العب جولة سريعة في المواصلات أو أثناء الاستراحة. الثعبان وتتريس يصقلان ردود أفعالك، و2048 وكانسة الألغام تدربان منطقك. بلا دفع ولا تسجيل: افتح واكتب.",
        whyItems=[
            ("⚡ لعب فوري", "ويب خالص بلا تنزيلات. افتح الصفحة واللعبة جاهزة."),
            ("📱 كل الأجهزة", "متكيف مع الجوال واللوحي والحاسوب: اللمس وال keyboard يعملان."),
            ("🆓 مجانية دائمًا", "كل الألعاب مجانية: بلا مشتريات أو إعلانات إجبارية."),
            ("🔒 خصوصية آمنة", "البيانات تبقى على جهازك. لا نجمع معلومات شخصية."),
        ],
        faqTitle="الأسئلة الشائعة",
        faq=[
            ("هل أحتاج تنزيلًا أو تسجيلًا؟", "إطلاقًا. كل لعبة تعمل في المتصفح — افتح الصفحة والعب. بلا حساب."),
            ("هل تعمل على الجوال؟", "نعم. الموقع مُحسَّن للمس؛ أسهم الشاشة والسحب يعملان بسلاسة."),
            ("هل تجمعون بياناتي؟", "لا. التقدم مثل الأرقام القياسية يُحفظ في متصفحك فقط. لا نجمع بيانات شخصية."),
            ("ما الألعاب الموجودة؟", "ست ألعاب كلاسيكية: الثعبان و2048 وتتريس وكانسة الألغام وغوموكو والذاكرة، والمزيد قادم."),
        ],
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
        stats=["🕹️ 9 игр", "⚡ Мгновенная загрузка", "📱 На телефоне", "🆓 Бесплатно навсегда"],
        introH2="Что такое «Аркадные мини-игры»?",
        introP="«Аркадные мини-игры» (Games Hub) — бесплатная коллекция браузерных игр. Мы уверены: хорошей игре не нужны скачивание и регистрация — откройте страницу и играйте. Все игры написаны на чистом фронтенде: быстрая загрузка, никакой рекламы и полная адаптация под телефон и компьютер. Убить пару минут или побить рекорд — здесь найдётся игра на любой случай.",
        gamesTitle="Все игры", gamesDesc="Выберите игру и нажмите «Играть», чтобы начать.",
        popularTitle="Популярные игры", popularDesc="Фавориты, к которым игроки возвращаются снова и снова.",
        categoriesTitle="Категории", categoriesDesc="Выбирайте по настроению и жанру.",
        newTitle="Новые игры", newDesc="Мы постоянно добавляем игры — вот свежие поступления.",
        trendingTitle="В тренде", trendingDesc="Мини-игры, о которых все говорят сейчас.",
        whyTitle="Почему выбирают «Аркадные мини-игры»?",
        whyP="Браузерные мини-игры не требуют установки и не занимают места. Сыграйте партию в дороге, на перемене или в перерыве. Змейка и Тетрис тренируют реакцию, 2048 и Сапёр — логику. Без оплаты и регистрации: открыл и играешь.",
        whyItems=[
            ("⚡ Мгновенный старт", "Чистый фронтенд, без установки. Открыли страницу — игра готова."),
            ("📱 Любое устройство", "Адаптировано под телефоны, планшеты и ПК: тач и клавиатура работают."),
            ("🆓 Бесплатно навсегда", "Все игры бесплатны: без покупок и навязчивой рекламы."),
            ("🔒 Приватность", "Данные остаются на вашем устройстве. Мы не собираем личную информацию."),
        ],
        faqTitle="Часто задаваемые вопросы",
        faq=[
            ("Нужно ли скачивать или регистрироваться?", "Совсем нет. Все игры работают в браузере — откройте страницу и играйте. Без аккаунта."),
            ("Игры работают на телефоне?", "Да. Сайт оптимизирован для сенсора; экранные стрелки и свайпы работают плавно."),
            ("Вы собираете мои данные?", "Нет. Прогресс (например, рекорды) сохраняется только в вашем браузере. Мы не собираем личные данные."),
            ("Какие игры доступны?", "Шесть классических: Змейка, 2048, Тетрис, Сапёр, Гомоку и Память, скоро добавим ещё."),
        ],
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
        stats=["🕹️ 9ゲーム", "⚡ 待ち時間ゼロ", "📱 スマホ対応", "🆓 ずっと無料"],
        introH2="ミニゲームランドとは？",
        introP="ミニゲームランド（Games Hub）は無料のオンラインブラウザゲーム集です。良いゲームにダウンロードも登録もいらない——ページを開けばすぐ遊べます。すべて純粋なフロントエンド技術で作られ、読み込みが速く、広告なし、スマホとPCに最適化されています。ちょっとした空き時間にも、ハイスコア挑戦にも最適です。",
        gamesTitle="ゲーム一覧", gamesDesc="好きなゲームを選んで「プレイ」をクリック。",
        popularTitle="人気ゲーム", popularDesc="プレイヤーに何度も愛されている定番たち。",
        categoriesTitle="カテゴリ", categoriesDesc="気分に合わせてジャンルから選べます。",
        newTitle="新着ゲーム", newDesc="随時追加中——最新のラインナップです。",
        trendingTitle="話題のゲーム", trendingDesc="今みんなが遊んでいるミニゲーム。",
        whyTitle="ミニゲームランドを選ぶ理由",
        whyP="ブラウザのミニゲームはインストール不要で容量も使いません。通勤中や休憩時間にサクッと一戦。スネークやテトリスは反射神経を、2048やマインスイーパーは論理力を鍛えます。料金も登録も不要、開くだけですぐ遊べます。",
        whyItems=[
            ("⚡ 即プレイ", "純粋なフロントエンドでインストール不要。ページを開けば準備完了。"),
            ("📱 どの端末でも", "スマホ・タブレット・PCに対応。タッチとキーボード両対応。"),
            ("🆓 永久無料", "すべて無料。課金も強制広告もなし。"),
            ("🔒 プライバシー配慮", "データは端末内に保存。個人情報は収集しません。"),
        ],
        faqTitle="よくある質問",
        faq=[
            ("ダウンロードや登録は必要？", "まったく不要です。すべてブラウザで動き、ページを開くだけで遊べます。アカウントも不要。"),
            ("スマホでも遊べる？", "はい。タッチ操作に最適化されており、画面ボタンやスワイプが滑らかに動きます。"),
            ("データを収集するの？", "いいえ。ハイスコアなどの進行状況はお使いのブラウザのみに保存され、個人データは収集しません。"),
            ("どんなゲームがある？", "スネーク、2048、テトリス、マインスイーパー、五目並べ、神経衰弱の6作品で、今後も追加予定です。"),
        ],
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
        stats=["🕹️ 게임 9종", "⚡ 즉시 로딩", "📱 모바일 지원", "🆓 영구 무료"],
        introH2="미니게임 놀이터란?",
        introP="미니게임 놀이터(Games Hub)는 무료 온라인 브라우저 게임 모음입니다. 좋은 게임에 복잡한 다운로드나 회원가입은 필요 없다고 믿습니다 — 페이지를 열면 바로 플레이. 모든 게임은 순수 프런트엔드로 만들어져 로딩이 빠르고 광고 없이, 모바일과 PC 모두에 최적화되어 있습니다. 잠깐의 휴식에도, 최고 점수 도전에도 딱입니다.",
        gamesTitle="전체 게임", gamesDesc="마음에 드는 게임을 골라 「시작하기」를 눌러 바로 플레이하세요.",
        popularTitle="인기 게임", popularDesc="플레이어들이 자주 찾는 베스트 셀렉션.",
        categoriesTitle="카테고리", categoriesDesc="지금의 기분에 맞는 종류로 골라보세요.",
        newTitle="새로운 게임", newDesc="꾸준히 추가 중 — 최신 픽입니다.",
        trendingTitle="떠오르는 게임", trendingDesc="지금 everyone가 이야기하는 미니게임.",
        whyTitle="왜 미니게임 놀이터인가요?",
        whyP="웹 미니게임은 설치가 필요 없고 저장 공간도 차지하지 않습니다. 통근길, 쉬는 시간, 업무 사이에 한 판씩 즐겨보세요. 스네이크와 테트리스는 순발력을, 2048과 지뢰찾기는 논리력을 길러줍니다. 결제도 가입도 없이, 열면 바로 플레이.",
        whyItems=[
            ("⚡ 즉시 플레이", "순수 프런트엔드로 설치 불필요. 페이지를 열면 준비 완료."),
            ("📱 모든 기기", "스마트폰·태블릿·PC에 최적화. 터치와 키보드 모두 지원."),
            ("🆓 영구 무료", "모든 게임 무료. 인앱 결제나 강제 광고 없음."),
            ("🔒 프라이버시 보호", "데이터는 기기에만 저장. 개인정보는 수집하지 않습니다."),
        ],
        faqTitle="자주 묻는 질문",
        faq=[
            ("다운로드나 가입이 필요한가요?", "전혀 없습니다. 모든 게임은 브라우저에서 동작하며 페이지를 열면 바로 플레이할 수 있습니다. 계정도 불필요합니다."),
            ("모바일에서 되나요?", "네. 터치에 최적화되어 화면 방향키와 스와이프가 부드럽게 동작합니다."),
            ("데이터를 수집하나요?", "아니요. 최고 점수 같은 진행 상황은 사용자의 브라우저에만 저장되며 개인 데이터는 수집하지 않습니다."),
            ("어떤 게임이 있나요?", "스네이크, 2048, 테트리스, 지뢰찾기, 오목, 메모리 카드 6종이며 계속 추가됩니다."),
        ],
        aboutH2="미니게임 놀이터 소개",
        aboutP="미니게임 놀이터는 무료 온라인 미니게임 모음 사이트입니다. 좋은 게임에는 복잡한 다운로드나 회원가입이 필요 없다고 믿습니다 — 페이지를 열면 바로 플레이. 모든 게임은 순수 프런트엔드로 만들어져 로딩이 빠르고 광고 없이, 모바일과 PC 모두에 최적화되어 있습니다.",
        chooseH2="웹 미니게임을 추천하는 이유",
        chooseP="웹 미니게임은 설치가 필요 없고 저장 공간도 차지하지 않습니다. 통근길, 쉬는 시간, 업무 사이에 한 판씩 즐겨보세요. 스네이크와 테트리스는 순발력을, 2048과 지뢰찾기는 논리력을 길러주고, 오목과 메모리 카드는 차분히 집중하기 좋습니다. 시간 때우기든 최고 점수 도전이든, 여기 당신에게 맞는 게임이 있습니다.",
        metaTitle="미니게임 놀이터 - 무료 온라인 미니게임 | 스네이크, 2048, 테트리스",
        metaDesc="스네이크, 2048, 테트리스, 지뢰찾기, 오목, 메모리 카드 등 6가지 고전 미니게임을 무료로 즐기세요. 다운로드·회원가입 없이 PC와 모바일에서 바로 플레이.",
        metaKeywords="미니게임,온라인 게임,무료 게임,웹 게임,스네이크,2048,테트리스,지뢰찾기,오목,메모리 카드,캐주얼 게임"),
}

# 游戏分类的多语言名称（slug -> 各语言标签）
CATEGORY_NAMES = {
    "action":     {"zh": "动作", "en": "Action", "es": "Acción", "ar": "أكشن", "ru": "Экшен", "ja": "アクション", "ko": "액션"},
    "adventure":  {"zh": "冒险", "en": "Adventure", "es": "Aventura", "ar": "مغامرات", "ru": "Приключения", "ja": "アドベンチャー", "ko": "어드벤처"},
    "arcade":     {"zh": "街机", "en": "Arcade", "es": "Arcade", "ar": "أركيد", "ru": "Аркада", "ja": "アーケード", "ko": "아케이드"},
    "puzzle":     {"zh": "益智", "en": "Puzzle", "es": "Puzle", "ar": "ألغاز", "ru": "Головоломки", "ja": "パズル", "ko": "퍼즐"},
    "racing":     {"zh": "竞速", "en": "Racing", "es": "Carreras", "ar": "سباق", "ru": "Гонки", "ja": "レーシング", "ko": "레이싱"},
    "sports":     {"zh": "运动", "en": "Sports", "es": "Deportes", "ar": "رياضة", "ru": "Спорт", "ja": "スポーツ", "ko": "스포츠"},
    "strategy":   {"zh": "策略", "en": "Strategy", "es": "Estrategia", "ar": "استراتيجية", "ru": "Стратегия", "ja": "ストラテジー", "ko": "전략"},
    "multiplayer":{"zh": "多人", "en": "Multiplayer", "es": "Multijugador", "ar": "لاعبون متعددون", "ru": "Мультиплеер", "ja": "マルチプレイ", "ko": "멀티플레이어"},
}

# 分类 -> 游戏 slug 映射（一个游戏可属于多个分类）
CATEGORY_GAMES = {
    "action":     ["snake", "racing"],
    "adventure":  ["adventure"],
    "arcade":     ["snake", "tetris", "racing"],
    "puzzle":     ["2048", "minesweeper", "memory"],
    "racing":     ["racing"],
    "sports":     ["sports"],
    "strategy":   ["2048", "tetris", "minesweeper", "gomoku"],
    "multiplayer":["gomoku"],
}

# 分类页多语言副标题（出现在分类落地页 H1 下方）
CATEGORY_SUB = {
    "action":     {"zh": "考验反应与操作的刺激玩法。", "en": "Fast reflexes and quick reactions.",
                   "es": "Reflejos rápidos y acción pura.", "ar": "ردود فعل سريعة وأكشن نقي.",
                   "ru": "Быстрые реакции и чистый экшен.", "ja": "素早い反応とアクション。",
                   "ko": "빠른 반응과 액션."},
    "adventure":  {"zh": "探索与解谜的奇趣旅程。", "en": "Explore and discover new worlds.",
                   "es": "Explora y descubre mundos nuevos.", "ar": "استكشف واكتشف عوالم جديدة.",
                   "ru": "Исследуйте и открывайте новые миры.", "ja": "新しい世界を探検。",
                   "ko": "새로운 세계를 탐험하세요."},
    "arcade":     {"zh": "经典街机，点开即玩。", "en": "Classic arcade fun, play instantly.",
                   "es": "Diversión arcade clásica, al instante.", "ar": "متعة الأركيد الكلاسيكي فوراً.",
                   "ru": "Классическая аркада, играй сразу.", "ja": "懐かしのアーケード。",
                   "ko": "클래식 아케이드, 바로 플레이."},
    "puzzle":     {"zh": "烧脑益智，越玩越聪明。", "en": "Brain-teasing puzzles to train your mind.",
                   "es": "Puzzles para entrenar la mente.", "ar": "ألغاز لتدريب العقل.",
                   "ru": "Головоломки для тренировки ума.", "ja": "頭を使うパズル。",
                   "ko": "두뇌를 훈련하는 퍼즐."},
    "racing":     {"zh": "极速飙车，畅快淋漓。", "en": "High-speed racing thrills.",
                   "es": "Emoción a toda velocidad.", "ar": "إثارة السباق بأقصى سرعة.",
                   "ru": "Гоночная лихорадка на скорости.", "ja": "ハイスピード・レース。",
                   "ko": "고속 레이싱 스릴."},
    "sports":     {"zh": "竞技运动，挥洒热情。", "en": "Sports and competitive fun.",
                   "es": "Deportes y diversión competitiva.", "ar": "رياضة ومنافسة ممتعة.",
                   "ru": "Спорт и азарт соревнований.", "ja": "スポーツと競技。",
                   "ko": "스포츠와 경쟁의 재미."},
    "strategy":   {"zh": "运筹帷幄，步步为营。", "en": "Plan, think and outsmart your rival.",
                   "es": "Planifica y supera a tu rival.", "ar": "خطط وتفوق على خصمك.",
                   "ru": "Планируй и обыграй соперника.", "ja": "戦略でライバルに勝つ。",
                   "ko": "계획으로 라이벌을 이기세요."},
    "multiplayer":{"zh": "与好友或 AI 同场竞技。", "en": "Play against friends or smart AI.",
                   "es": "Juega contra amigos o la IA.", "ar": "العب ضد الأصدقاء أو الذكاء الاصطناعي.",
                   "ru": "Играй с друзьями или ИИ.", "ja": "友達やAIと対戦。",
                   "ko": "친구나 AI와 대결."},
}

# 站点页（About/Contact/Privacy/Terms/Cookie/DMCA/Categories/New）的通用多语言文案
PAGES = {
    "zh": dict(
        aboutTitle="关于街机小游戏乐园",
        aboutH2a="我们是谁",
        aboutPa="街机小游戏乐园（Games Hub）是一个完全免费的在线浏览器游戏合集网站。我们由一群热爱经典小游戏的开发者与设计师组成，目标是把陪伴了几代人的好游戏，用最轻量、最干净的方式重新呈现给今天的玩家。",
        aboutH2b="我们为什么创建这个网站",
        aboutPb="市面上的游戏平台往往充斥着弹窗广告、强制注册和臃肿的客户端下载。我们相信好游戏应该「点开即玩」——你不需要安装任何东西，也不需要交出个人信息，打开网页就能开始一局。",
        aboutH2c="我们提供什么",
        aboutPc="目前我们收录 9 款经典小游戏：贪吃蛇、2048、俄罗斯方块、扫雷、五子棋、记忆翻牌、极速躲避赛车、趣味投篮和迷宫大冒险，全部为纯前端实现，加载快、无广告、适配手机与电脑。我们会持续上新，把更多优质的小游戏带到这里。",
        contactTitle="联系我们",
        contactP="如果你对网站有任何建议、发现游戏故障，或希望合作，欢迎通过以下渠道联系我们。我们通常会在一至两个工作日内回复。",
        contactEmail="contact@games-hub.cc",
        privacyTitle="隐私政策",
        privacyP="本隐私政策说明街机小游戏乐园（以下简称「本站」）如何对待你的信息。本站高度重视你的隐私，并尽量以最简方式运营。",
        privacyItems=[
            ("我们收集什么", "本站不会在服务器端收集你的任何个人信息。你无需注册账号，所有游戏都不要求提交姓名、邮箱或电话等数据。"),
            ("游戏数据如何存储", "游戏进度（如最高分、已完成关卡）仅保存在你自己的浏览器本地存储（localStorage）中，不会上传到任何服务器。清除浏览器数据即可删除这些信息。"),
            ("Cookie 与本地存储", "本站仅使用必要的本地存储来记住你的语言偏好与游戏进度，不使用第三方追踪 Cookie。详见《Cookie 政策》。"),
            ("第三方服务", "本站可能通过 Google AdSense 展示广告。广告服务商可能使用 Cookie 来投放与你相关的广告。相关数据处理受 Google 隐私政策约束。"),
            ("分析工具", "本站可能使用 Google Analytics 等匿名分析工具来了解访问情况，这些数据不包含可直接识别你个人的信息。"),
            ("儿童隐私", "本站不针对 13 岁以下儿童设计，也不会故意收集儿童的个人信息。"),
            ("政策变更", "如本政策发生变更，我们将在本页更新日期并发布新版。"),
        ],
        termsTitle="服务条款",
        termsP="访问和使用街机小游戏乐园（以下简称「本站」）即表示你同意以下条款。请仔细阅读。",
        termsItems=[
            ("使用许可", "本站提供的所有游戏与内容仅供个人、非商业性的娱乐与教育使用。你可以在自己的设备上免费游玩。"),
            ("知识产权", "本站游戏的实现代码、页面设计与文案由本站团队创作并保留权利。游戏名称、商标可能属于各自的权利人。"),
            ("免责声明", "游戏按「现状」提供，不附带任何明示或暗示的担保。对于因使用本站而产生的任何直接或间接损失，本站不承担责任。"),
            ("可接受使用", "你同意不尝试破解、反向工程或以任何方式干扰本站正常运行，也不将本站内容用于任何非法目的。"),
            ("条款变更", "本站可能随时更新本条款，更新后继续使用即视为接受新条款。"),
        ],
        cookieTitle="Cookie 政策",
        cookieP="本政策说明街机小游戏乐园（以下简称「本站」）如何使用 Cookie 与类似的本地存储技术。",
        cookieItems=[
            ("必要的本地存储", "本站使用浏览器本地存储（localStorage）来记住你的语言选择与游戏进度。这些技术对网站正常运行必不可少，无法关闭。"),
            ("广告 Cookie", "本站通过 Google AdSense 展示广告。Google 可能使用 Cookie 来投放个性化广告并衡量广告效果。你可以在 Google 广告设置中管理相关偏好。"),
            ("如何管理", "你可以通过浏览器设置清除或阻止 Cookie。但请注意，禁用本地存储可能导致游戏进度无法保存。"),
        ],
        dmcaTitle="DMCA / 版权声明",
        dmcaP="街机小游戏乐园尊重他人的知识产权。如果你认为本站内容侵犯了你的版权，请按以下流程提出下架请求。",
        dmcaItems=[
            ("侵权投诉", "请提供：1) 你主张被侵权的作品说明；2) 侵权内容在本站的链接；3) 你的联系方式；4) 你善意相信该使用未经授权的声明。"),
            ("联系方式", "请将侵权投诉发送至 contact@games-hub.cc，我们将在收到后及时处理。"),
            ("免责声明", "本站游戏均为原创或公有领域经典玩法的独立实现，不包含受版权保护的第三方素材。"),
        ],
        categoriesTitle="游戏分类",
        categoriesDesc="按类型浏览，快速找到你最爱的玩法。",
        newTitle="最新上架",
        newDesc="我们持续上新，以下是本站全部精选游戏。",
        popularTitle="热门游戏",
        popularDesc="玩家最常玩的精选合集。",
    ),
    "en": dict(
        aboutTitle="About Arcade Games Hub",
        aboutH2a="Who we are",
        aboutPa="Arcade Games Hub (Games Hub) is a completely free online collection of browser games. We are a small team of developers and designers who love classic mini games, and our goal is to bring the games that accompanied generations back to today's players in the lightest, cleanest way possible.",
        aboutH2b="Why we built this site",
        aboutPb="Many gaming platforms are crowded with pop-up ads, forced sign-ups and bloated client downloads. We believe a good game should be „play on click“ — no installs, no personal data, just open the page and start.",
        aboutH2c="What we offer",
        aboutPc="Today we host 6 classic mini games: Snake, 2048, Tetris, Minesweeper, Gomoku and Memory Match. All are pure front-end, fast-loading, ad-free and tuned for both mobile and desktop. We keep adding more quality mini games over time.",
        contactTitle="Contact Us",
        contactP="If you have suggestions, found a bug, or want to collaborate, reach out through the channel below. We usually reply within one to two business days.",
        contactEmail="contact@games-hub.cc",
        privacyTitle="Privacy Policy",
        privacyP="This Privacy Policy explains how Arcade Games Hub („the Site“) handles your information. We take your privacy seriously and run the Site in the simplest way possible.",
        privacyItems=[
            ("What we collect", "The Site does not collect any personal information on our servers. No account is required, and no game asks for your name, email or phone."),
            ("How game data is stored", "Game progress (such as high scores) is saved only in your own browser's local storage (localStorage). It is never uploaded. Clearing your browser data removes it."),
            ("Cookies & local storage", "We only use necessary local storage to remember your language preference and game progress. We do not use third-party tracking cookies. See our Cookie Policy."),
            ("Third-party services", "The Site may show ads via Google AdSense. The ad provider may use cookies to serve relevant ads. Their data handling is governed by Google's Privacy Policy."),
            ("Analytics", "We may use anonymous analytics such as Google Analytics to understand traffic. This data cannot directly identify you."),
            ("Children's privacy", "The Site is not targeted at children under 13 and we do not knowingly collect their personal information."),
            ("Changes", "If this policy changes, we will update the date and publish a new version on this page."),
        ],
        termsTitle="Terms of Service",
        termsP="By accessing and using Arcade Games Hub („the Site“) you agree to the following terms. Please read them carefully.",
        termsItems=[
            ("License", "All games and content on the Site are provided for personal, non-commercial entertainment and education. You may play them for free on your own devices."),
            ("Intellectual property", "The implementation code, design and copy on the Site are created by our team and reserved. Game names and trademarks may belong to their respective owners."),
            ("Disclaimer", "Games are provided „as is“ without any express or implied warranty. The Site is not liable for any direct or indirect loss arising from use."),
            ("Acceptable use", "You agree not to attempt to crack, reverse-engineer or interfere with the Site, nor use its content for any unlawful purpose."),
            ("Changes", "We may update these terms at any time; continued use after an update means you accept the new terms."),
        ],
        cookieTitle="Cookie Policy",
        cookieP="This policy explains how Arcade Games Hub („the Site“) uses cookies and similar local storage technologies.",
        cookieItems=[
            ("Essential local storage", "We use browser local storage (localStorage) to remember your language choice and game progress. This is essential and cannot be turned off."),
            ("Advertising cookies", "We display ads via Google AdSense. Google may use cookies to serve personalized ads and measure performance. You can manage preferences in Google's ad settings."),
            ("How to manage", "You can clear or block cookies in your browser settings. Note that disabling local storage may stop game progress from being saved."),
        ],
        dmcaTitle="DMCA / Copyright",
        dmcaP="Arcade Games Hub respects the intellectual property of others. If you believe content on the Site infringes your copyright, please submit a takedown request as below.",
        dmcaItems=[
            ("Infringement notice", "Please provide: 1) a description of the work you claim is infringed; 2) the URL of the infringing content on the Site; 3) your contact info; 4) a statement of good-faith belief that the use is unauthorized."),
            ("Contact", "Send infringement notices to contact@games-hub.cc and we will act promptly."),
            ("Disclaimer", "Our games are original or independent implementations of public-domain classic gameplay and contain no copyrighted third-party assets."),
        ],
        categoriesTitle="Game Categories",
        categoriesDesc="Browse by type and find your favorite kind of fun fast.",
        newTitle="New Games",
        newDesc="We keep adding — here are all the curated games on the Site.",
        popularTitle="Popular Games",
        popularDesc="The crowd-favorites our players keep coming back to.",
    ),
    "es": dict(
        aboutTitle="Acerca de Arcade de Minijuegos",
        aboutH2a="Quiénes somos",
        aboutPa="Arcade de Minijuegos (Games Hub) es una colección gratuita de juegos en el navegador. Somos un pequeño equipo de desarrolladores y diseñadores apasionados por los clásicos, y queremos traer esos juegos a los jugadores de hoy de la forma más ligera y limpia.",
        aboutH2b="Por qué creamos este sitio",
        aboutPb="Muchas plataformas están llenas de anuncios emergentes, registros obligatorios y descargas pesadas. Creemos que un buen juego debe ser „juega al instante“: sin instalar nada ni dar datos personales.",
        aboutH2c="Qué ofrecemos",
        aboutPc="Hoy tenemos 6 clásicos: Snake, 2048, Tetris, Buscaminas, Gomoku y Memoria. Todos son web pura, rápidos, sin anuncios y adaptados a móvil y PC. Seguiremos añadiendo más.",
        contactTitle="Contáctanos",
        contactP="Si tienes sugerencias, encuentras un fallo o quieres colaborar, escríbenos por el canal de abajo. Normalmente respondemos en uno o dos días hábiles.",
        contactEmail="contact@games-hub.cc",
        privacyTitle="Política de privacidad",
        privacyP="Esta Política de privacidad explica cómo Arcade de Minijuegos („el Sitio“) trata tu información. Nos tomamos tu privacidad en serio.",
        privacyItems=[
            ("Qué recopilamos", "El Sitio no recopila información personal en nuestros servidores. No se requiere cuenta y ningún juego pide tu nombre, correo o teléfono."),
            ("Cómo se guardan los datos", "El progreso (como récords) se guarda solo en el almacenamiento local de tu navegador. Nunca se sube. Borrar los datos del navegador lo elimina."),
            ("Cookies y almacenamiento", "Usamos solo almacenamiento local necesario para recordar idioma y progreso. Sin cookies de rastreo de terceros. Ver Política de cookies."),
            ("Servicios de terceros", "Podemos mostrar anuncios con Google AdSense. El proveedor puede usar cookies para anuncios relevantes, según la Política de privacidad de Google."),
            ("Analítica", "Podemos usar analítica anónima como Google Analytics. Estos datos no te identifican directamente."),
            ("Privacidad infantil", "El Sitio no está dirigido a menores de 13 años y no recopilamos a sabiendas sus datos."),
            ("Cambios", "Si cambia, actualizaremos la fecha y publicaremos la nueva versión aquí."),
        ],
        termsTitle="Términos del servicio",
        termsP="Al acceder y usar Arcade de Minijuegos („el Sitio“) aceptas los siguientes términos.",
        termsItems=[
            ("Licencia", "Todos los juegos y contenidos son para uso personal, no comercial, de entretenimiento y educación. Puedes jugarlos gratis en tus dispositivos."),
            ("Propiedad intelectual", "El código, diseño y textos son de nuestro equipo. Los nombres y marcas pueden pertenecer a sus dueños."),
            ("Exención", "Los juegos se ofrecen „tal cual“, sin garantía. El Sitio no se responsabiliza por pérdidas derivadas del uso."),
            ("Uso aceptable", "No intentes hackear, ingeniería inversa ni interferir con el Sitio, ni usarlo con fines ilegales."),
            ("Cambios", "Podemos actualizar estos términos; el uso continuado implica aceptación."),
        ],
        cookieTitle="Política de cookies",
        cookieP="Esta política explica cómo Arcade de Minijuegos („el Sitio“) usa cookies y tecnologías similares.",
        cookieItems=[
            ("Almacenamiento esencial", "Usamos almacenamiento local para recordar idioma y progreso. Es esencial y no se puede desactivar."),
            ("Cookies publicitarias", "Mostramos anuncios con Google AdSense. Google puede usar cookies para anuncios personalizados. Puedes gestionarlo en ajustes de Google."),
            ("Cómo gestionar", "Puedes borrar o bloquear cookies en tu navegador. Desactivar el almacenamiento local puede detener el guardado del progreso."),
        ],
        dmcaTitle="DMCA / Derechos de autor",
        dmcaP="Arcade de Minijuegos respeta la propiedad intelectual. Si crees que algo infringe tu copyright, envía una solicitud de retiro.",
        dmcaItems=[
            ("Aviso de infracción", "Proporciona: 1) descripción de la obra; 2) URL en el Sitio; 3) tu contacto; 4) declaración de buena fe."),
            ("Contacto", "Envía avisos a contact@games-hub.cc y actuaremos pronto."),
            ("Exención", "Nuestros juegos son implementaciones originales de juegos clásicos de dominio público, sin material de terceros con copyright."),
        ],
        categoriesTitle="Categorías",
        categoriesDesc="Explora por tipo y encuentra tu diversión favorita.",
        newTitle="Nuevos juegos",
        newDesc="Seguimos añadiendo — aquí están todos los juegos curados.",
        popularTitle="Juegos populares",
        popularDesc="Los favoritos a los que vuelven los jugadores.",
    ),
    "ar": dict(
        aboutTitle="عن موقع ألعاب الأركيد",
        aboutH2a="من نحن",
        aboutPa="ألعاب الأركيد (Games Hub) مجموعة مجانية من ألعاب المتصفح. نحن فريق صغير من المطورين والمصممين الذين يحبون الألعاب الكلاسيكية، وهدفنا إعادة تقديم الألعاب التي رافقت الأجيال للاعبين اليوم بأخف وأنظف طريقة.",
        aboutH2b="لماذا أنشأنا هذا الموقع",
        aboutPb="الكثير من المنصات مليئة بالنوافذ المنبثقة والتسجيل الإجباري والتنزيلات الضخمة. نؤمن بأن اللعبة الجيدة يجب أن تكون «العب فورًا» — بلا تنزيل وبلا بيانات شخصية.",
        aboutH2c="ماذا نقدم",
        aboutPc="نستضيف اليوم 6 ألعاب كلاسيكية: الثعبان و2048 وتتريس وكانسة الألغام وغوموكو والذاكرة. كلها ويب خالص، سريعة، بلا إعلانات ومتكيفة مع الجوال والحاسوب. وسنضيف المزيد.",
        contactTitle="اتصل بنا",
        contactP="إن كان لديك اقتراح أو وجدت خللاً أو تود التعاون، راسلنا عبر القناة أدناه. نرد عادة خلال يوم أو يومين عمل.",
        contactEmail="contact@games-hub.cc",
        privacyTitle="سياسة الخصوصية",
        privacyP="تشرح هذه السياسة كيف يتعامل موقع ألعاب الأركيد („الموقع“) مع معلوماتك. نأخذ خصوصيتك بجدية.",
        privacyItems=[
            ("ماذا نجمع", "لا يجمع الموقع أي معلومات شخصية على خوادمنا. لا حساب مطلوب ولا لعبة تطلب اسمك أو بريدك."),
            ("كيف تُحفظ البيانات", "يُحفظ التقدم (مثل الأرقام القياسية) فقط في التخزين المحلي لمتصفحك. لا يُرفع أبدًا. مسح بيانات المتصفح يحذفه."),
            ("ملفات الارتباط", "نستخدم فقط التخزين المحلي الضروري لحفظ اللغة والتقدم. بلا ملفات تتبع من طرف ثالث. انظر سياسة ملفات الارتباط."),
            ("خدمات الطرف الثالث", "قد نعرض إعلانات عبر Google AdSense. قد يستخدم المزود ملفات ارتباط لإعلانات ذات صلة حسب سياسة Google."),
            ("التحليلات", "قد نستخدم تحليلات مجهولة مثل Google Analytics. هذه البيانات لا تحدد هويتك."),
            ("خصوصية الأطفال", "الموقع ليس موجهًا لمن دون 13 عامًا ولا نجمع بياناتهم عمدًا."),
            ("التغييرات", "عند أي تغيير نحدّث التاريخ وننشر النسخة الجديدة هنا."),
        ],
        termsTitle="شروط الخدمة",
        termsP="بالوصول إلى موقع ألعاب الأركيد („الموقع“) واستخدامه فإنك توافق على الشروط التالية.",
        termsItems=[
            ("الترخيص", "جميع الألعاب والمحتوى للاستخدام الشخصي غير التجاري للترفيه والتعليم. تلعبها مجانًا على أجهزتك."),
            ("الملكية الفكرية", "الكود والتصميم والنصوص من فريقنا. الأسماء والعلامات قد تعود لأصحابها."),
            ("إخلاء المسؤولية", "تُقدم الألعاب «كما هي» بلا ضمان. الموقع غير مسؤول عن أي خسارة ناتجة عن الاستخدام."),
            ("الاستخدام المقبول", "لا تحاول اختراق الموقع أو الهندسة العكسية أو التدخل فيه، ولا تستخدمه لأغراض غير قانونية."),
            ("التغييرات", "قد نحدّث الشروط؛ الاستمرار في الاستخدام يعني القبول."),
        ],
        cookieTitle="سياسة ملفات الارتباط",
        cookieP="تشرح هذه السياسة كيف يستخدم موقع ألعاب الأركيد ملفات الارتباط والتقنيات المشابهة.",
        cookieItems=[
            ("التخزين المحلي الضروري", "نستخدم التخزين المحلي لحفظ اللغة والتقدم. وهو ضروري ولا يمكن تعطيله."),
            ("ملفات إعلانية", "نعرض إعلانات عبر Google AdSense. قد يستخدم Google ملفات ارتباط لإعلانات مخصصة. يمكنك إدارتها في إعدادات Google."),
            ("كيفية الإدارة", "يمكنك مسح أو حظر ملفات الارتباط في متصفحك. تعطيل التخزين المحلي قد يوقف حفظ التقدم."),
        ],
        dmcaTitle="DMCA / حقوق النشر",
        dmcaP="يحترم موقع ألعاب الأركيد الملكية الفكرية للآخرين. إن اعتقدت أن محتوى ينتهك حقوقك، أرسل طلب إزالة.",
        dmcaItems=[
            ("إشعار الانتهاك", "يرجى تقديم: 1) وصف العمل؛ 2) رابط المحتوى؛ 3) بيانات اتصالك؛ 4) تصريح حسن نية."),
            ("التواصل", "أرسل الإشعارات إلى contact@games-hub.cc وسنتصرف فورًا."),
            ("إخلاء", "ألعابنا تطبيقات أصلية لأساليب كلاسيكية مشاع، بلا مواد محمية لجهات خارجية."),
        ],
        categoriesTitle="الفئات",
        categoriesDesc="تصفح حسب النوع واعثر على متعتك المفضلة.",
        newTitle="ألعاب جديدة",
        newDesc="نضيف باستمرار — إليك جميع الألعاب المنتقاة.",
        popularTitle="ألعاب رائجة",
        popularDesc="الألعاب المفضلة التي يعود إليها اللاعبون.",
    ),
    "ru": dict(
        aboutTitle="О сайте «Аркадные мини-игры»",
        aboutH2a="Кто мы",
        aboutPa="«Аркадные мини-игры» (Games Hub) — бесплатная коллекция браузерных игр. Мы небольшая команда разработчиков и дизайнеров, любящих классику, и хотим вернуть игры, сопровождавшие поколения, сегодняшним игрокам в самом лёгком виде.",
        aboutH2b="Почему мы создали сайт",
        aboutPb="Многие платформы завалены всплывающей рекламой, принудительной регистрацией и тяжёлыми клиентами. Мы верим, что хорошая игра — «открой и играй»: без установки и личных данных.",
        aboutH2c="Что мы предлагаем",
        aboutPc="Сегодня у нас 6 классических игр: Змейка, 2048, Тетрис, Сапёр, Гомоку и Память. Все на чистом фронтенде, быстрые, без рекламы и адаптированы под телефон и ПК. Будем добавлять ещё.",
        contactTitle="Связаться с нами",
        contactP="Если есть предложения, нашли баг или хотите сотрудничать — напишите ниже. Обычно отвечаем за один-два рабочих дня.",
        contactEmail="contact@games-hub.cc",
        privacyTitle="Политика конфиденциальности",
        privacyP="Эта Политика объясняет, как «Аркадные мини-игры» („Сайт“) обрабатывают вашу информацию. Мы серьёзно относимся к приватности.",
        privacyItems=[
            ("Что мы собираем", "Сайт не собирает личную информацию на серверах. Аккаунт не нужен, игра не запрашивает имя, почту или телефон."),
            ("Как хранятся данные", "Прогресс (рекорды) сохраняется только в локальном хранилище вашего браузера. Не загружается. Очистка данных удаляет его."),
            ("Cookies", "Используем только нужное локальное хранилище для языка и прогресса. Без сторонних трекеров. См. Политику Cookie."),
            ("Сторонние сервисы", "Можем показывать рекламу через Google AdSense. Провайдер может использовать cookies согласно политике Google."),
            ("Аналитика", "Можем использовать анонимную аналитику, например Google Analytics. Она не идентифицирует вас."),
            ("Дети", "Сайт не для детей младше 13 лет, мы не собираем их данные намеренно."),
            ("Изменения", "При изменениях обновим дату и опубликуем новую версию здесь."),
        ],
        termsTitle="Условия обслуживания",
        termsP="Доступом и использованием сайта („Сайт“) вы соглашаетесь со следующими условиями.",
        termsItems=[
            ("Лицензия", "Все игры и контент — для личного некоммерческого развлечения и обучения. Играйте бесплатно на своих устройствах."),
            ("Интеллектуальная собственность", "Код, дизайн и тексты — нашей команды. Названия и бренды могут принадлежать владельцам."),
            ("Отказ", "Игры предоставляются «как есть» без гарантий. Сайт не отвечает за убытки от использования."),
            ("Допустимое использование", "Не пытайтесь взломать, реверс-инжиниринг или помешать работе сайта, не используйте его незаконно."),
            ("Изменения", "Можем обновить условия; продолжение использования означает согласие."),
        ],
        cookieTitle="Политика Cookie",
        cookieP="Эта политика объясняет, как сайт использует cookie и похожие технологии.",
        cookieItems=[
            ("Нужное хранилище", "Используем локальное хранилище для языка и прогресса. Это необходимо и не отключается."),
            ("Рекламные cookie", "Показываем рекламу через Google AdSense. Google может использовать cookie для персонализации. Управляйте в настройках Google."),
            ("Как управлять", "Можно удалить или блокировать cookie в браузере. Отключение хранилища может остановить сохранение прогресса."),
        ],
        dmcaTitle="DMCA / Авторские права",
        dmcaP="Сайт уважает чужую интеллектуальную собственность. Если считаете, что контент нарушает ваши права, отправьте запрос на удаление.",
        dmcaItems=[
            ("Уведомление", "Укажите: 1) описание работы; 2) URL на сайте; 3) ваши контакты; 4) заявление добросовестности."),
            ("Контакт", "Отправляйте уведомления на contact@games-hub.cc, мы отреагируем быстро."),
            ("Отказ", "Наши игры — оригинальные реализации классики общего достояния без защищённых материалов."),
        ],
        categoriesTitle="Категории",
        categoriesDesc="Выбирайте по жанру и находите любимое.",
        newTitle="Новые игры",
        newDesc="Постоянно добавляем — вот все курируемые игры.",
        popularTitle="Популярные игры",
        popularDesc="Фавориты, к которым возвращаются игроки.",
    ),
    "ja": dict(
        aboutTitle="ミニゲームランドについて",
        aboutH2a="私たちについて",
        aboutPa="ミニゲームランド（Games Hub）は完全無料のオンラインブラウザゲーム集です。クラシックゲームを愛する少人数の開発者・デザイナーチームで、世代を超えて愛される名作を今日のプレイヤーへ最軽量・最清潔な形で届けることが目標です。",
        aboutH2b="このサイトを作った理由",
        aboutPb="多くのプラットフォームはポップアップ広告や強制登録、重いクライアントダウンロードだらけです。良いゲームは「開くだけで遊べる」べきだと私たちは信じています。",
        aboutH2c="提供内容",
        aboutPc="現在はスネーク、2048、テトリス、マインスイーパー、五目並べ、神経衰弱の6作品を提供。すべて純粋なフロントエンドで、読み込みが速く広告なし、スマホとPCに最適化されています。今後も追加予定です。",
        contactTitle="お問い合わせ",
        contactP="ご提案、不具合の報告、協業のご相談は下記まで。通常1〜2営業日以内に返信します。",
        contactEmail="contact@games-hub.cc",
        privacyTitle="プライバシーポリシー",
        privacyP="本ポリシーはミニゲームランド（「本サイト」）の情報取り扱いを説明します。私たちはプライバシーを重視し、最もシンプルな運営を心がけています。",
        privacyItems=[
            ("収集するもの", "本サイトはサーバー上で個人情報を収集しません。アカウント不要で、いかなるゲームも名前やメールを求めません。"),
            ("データの保存", "進行状況（ハイスコア等）はお使いのブラウザのローカルストレージのみに保存され、アップロードされません。ブラウザデータを削除すれば消えます。"),
            ("Cookie", "言語と進行状況を覚えるための必要なローカルストレージのみ使用し、第三者トラッキングCookieは使いません。Cookieポリシーを参照。"),
            ("第三者サービス", "Google AdSenseで広告を表示する場合があり、プロバイダが関連広告のためにCookieを使用することがあります。取り扱いはGoogleのポリシーに従います。"),
            ("分析", "Google Analytics等の匿名分析を利用することがあり、これらは個人を特定しません。"),
            ("児童のプライバシー", "本サイトは13歳未満を対象としておらず、児童の個人情報を意図的に収集しません。"),
            ("変更", "変更時は日付を更新し、本ページで新バージョンを公開します。"),
        ],
        termsTitle="利用規約",
        termsP="ミニゲームランド（「本サイト」）へのアクセス・利用は以下の規約に同意したことを意味します。",
        termsItems=[
            ("ライセンス", "すべてのゲームとコンテンツは個人かつ非商用の娯楽・学習用です。ご自身の端末で無料で遊べます。"),
            ("知的財産", "実装コード・デザイン・文案は当チームの作成物です。ゲーム名や商標は各権利者に帰属する場合があります。"),
            ("免責", "ゲームは「現状有姿」で提供され、いかなる保証もありません。利用による損害について本サイトは責任を負いません。"),
            ("禁止事項", "クラックやリバースエンジニアリング、運営の妨害、違法な利用はしないでください。"),
            ("変更", "規約は随時更新され、更新後の利用で新規約に同意したとみなします。"),
        ],
        cookieTitle="Cookie ポリシー",
        cookieP="本ポリシーは本サイトがCookie等のローカルストレージ技術をどう使うかを説明します。",
        cookieItems=[
            ("必須のローカルストレージ", "言語と進行状況を覚えるためのローカルストレージを使用します。これは必須で無効化できません。"),
            ("広告Cookie", "Google AdSenseで広告を表示する場合があり、Googleがパーソナライズ広告のためにCookieを使用することがあります。Googleの広告設定で管理できます。"),
            ("管理方法", "ブラウザ設定でCookieを削除・ブロックできます。ただしローカルストレージを無効にすると進行状況が保存されなくなる場合があります。"),
        ],
        dmcaTitle="DMCA / 著作権",
        dmcaP="ミニゲームランドは他人の知的財産を尊重します。コンテンツが著作権を侵害していると思われる場合は下記により申し立てください。",
        dmcaItems=[
            ("侵害申立", "1) 被侵害作品の説明 2) 該当URL 3) 連絡先 4) 無断利用と信じる善意の声明をご提供ください。"),
            ("連絡先", "申立は contact@games-hub.cc まで。速やかに対応します。"),
            ("免責", "当サイトのゲームはパブリックドメインのクラシック玩法の独創的実装であり、第三者の著作物は含みません。"),
        ],
        categoriesTitle="カテゴリ",
        categoriesDesc="ジャンルから選んでお気に入りを見つけよう。",
        newTitle="新着ゲーム",
        newDesc="随時追加中 — すべてのキュレーション済みゲーム。",
        popularTitle="人気ゲーム",
        popularDesc="プレイヤーに愛される定番。",
    ),
    "ko": dict(
        aboutTitle="미니게임 놀이터 소개",
        aboutH2a="우리는 누구인가요",
        aboutPa="미니게임 놀이터(Games Hub)는 완전 무료 온라인 브라우저 게임 모음입니다. 클래식 미니게임을 사랑하는 소규모 개발자·디자이너 팀으로, 세대를 넘어 사랑받은 게임을 오늘의 플레이어에게 가장 가볍고 깨끗한 형태로 전하고자 합니다.",
        aboutH2b="이 사이트를 만든 이유",
        aboutPb="많은 플랫폼은 팝업 광고, 강제 가입, 무거운 클라이언트 다운로드로 가득합니다. 좋은 게임은 ‘열면 바로 플레이’여야 한다고 우리는 믿습니다.",
        aboutH2c="우리가 제공하는 것",
        aboutPc="현재 스네이크, 2048, 테트리스, 지뢰찾기, 오목, 메모리 카드 6종을 제공합니다. 모두 순수 프런트엔드로 빠르고 광고 없이, 모바일과 PC에 최적화되어 있습니다. 계속 추가할 예정입니다.",
        contactTitle="문의하기",
        contactP="제안, 버그 신고, 협업을 원하시면 아래 채널로 연락 주세요. 보통 1~2 영업일 내에 답변합니다.",
        contactEmail="contact@games-hub.cc",
        privacyTitle="개인정보 처리방침",
        privacyP="본 방침은 미니게임 놀이터(‘본 사이트’)의 정보 처리 방식을 설명합니다. 우리는 개인정보를 중요하게 여기며 가장 단순하게 운영합니다.",
        privacyItems=[
            ("수집 항목", "본 사이트는 서버에서 개인정보를 수집하지 않습니다. 계정이 필요 없으며 어떤 게임도 이름·이메일을 묻지 않습니다."),
            ("데이터 저장", "진행 상황(최고 점수 등)은 사용자의 브라우저 로컬 스토리지에만 저장되며 업로드되지 않습니다. 브라우저 데이터를 지우면 삭제됩니다."),
            ("Cookie", "언어와 진행 상황을 기억하는 필수 로컬 스토리지만 사용하며 제3자 추적 Cookie는 쓰지 않습니다. 쿠키 정책 참조."),
            ("제3자 서비스", "Google AdSense로 광고를 표시할 수 있으며, 제공업체가 관련 광고를 위해 Cookie를 사용할 수 있습니다. 처리는 Google 방침을 따릅니다."),
            ("분석", "Google Analytics 등 익명 분석을 사용할 수 있으며 개인을 식별하지 않습니다."),
            ("아동 프라이버시", "본 사이트는 13세 미만을 대상으로 하지 않으며 고의로 수집하지 않습니다."),
            ("변경", "변경 시 날짜를 갱신하고 새 버전을 게시합니다."),
        ],
        termsTitle="이용 약관",
        termsP="미니게임 놀이터(‘본 사이트’) 이용 시 다음 약관에 동의하는 것으로 봅니다.",
        termsItems=[
            ("라이선스", "모든 게임과 콘텐츠는 개인적·비상업적 오락과 학습용입니다. 본인 기기에서 무료로 즐길 수 있습니다."),
            ("지식재산권", "구현 코드·디자인·문구는 당 팀의 작성물입니다. 게임명·상표는 각 권리자에 귀속될 수 있습니다."),
            ("면책", "게임은 ‘있는 그대로’ 제공되며 어떠한 보증도 없습니다. 이용으로 인한 손해에 대해 책임지지 않습니다."),
            ("금지 행위", "크래킹·리버스 엔지니어링·운영 방해·불법 이용은 금지합니다."),
            ("변경", "약관은 수시로 업데이트되며, 이후 이용 시 새 약관에 동의한 것으로 봅니다."),
        ],
        cookieTitle="쿠키 정책",
        cookieP="본 정책은 본 사이트가 Cookie 등 로컬 스토리지 기술을 어떻게 사용하는지 설명합니다.",
        cookieItems=[
            ("필수 로컬 스토리지", "언어와 진행 상황을 기억하기 위한 로컬 스토리지를 사용하며 필수라 비활성화할 수 없습니다."),
            ("광고 Cookie", "Google AdSense로 광고를 표시할 수 있으며 Google이 맞춤 광고를 위해 Cookie를 사용할 수 있습니다. Google 광고 설정에서 관리하세요."),
            ("관리 방법", "브라우저 설정에서 Cookie를 삭제·차단할 수 있습니다. 단 로컬 스토리지를 끄면 진행 상황이 저장되지 않을 수 있습니다."),
        ],
        dmcaTitle="DMCA / 저작권",
        dmcaP="미니게임 놀이터는 타인의 지식재산을 존중합니다. 콘텐츠가 저작권을 침해한다고 판단되면 아래 절차로 삭제를 요청하세요.",
        dmcaItems=[
            ("침해 신고", "1) 침해 주장 작품 설명 2) 해당 URL 3) 연락처 4) 무단 이용을 선의로 믿는 진술을 제공하세요."),
            ("연락처", "신고는 contact@games-hub.cc 로 보내주시면 신속히 조치합니다."),
            ("면책", "우리 게임은 퍼블릭 도메인 클래식玩法의 독자적 구현이며 제3자 저작물을 포함하지 않습니다."),
        ],
        categoriesTitle="카테고리",
        categoriesDesc="장르별로 둘러보고 취향에 맞는 게임을 찾으세요.",
        newTitle="새로운 게임",
        newDesc="꾸준히 추가 중 — 모든 큐레이션 게임.",
        popularTitle="인기 게임",
        popularDesc="플레이어가 자주 찾는 베스트.",
    ),
}

# 游戏元信息（与语言无关）
GAMES = [
    dict(slug="snake", js="snake.js", icon="🐍", color="var(--green)"),
    dict(slug="2048", js="g2048.js", icon="🔢", color="var(--yellow)"),
    dict(slug="tetris", js="tetris.js", icon="🧱", color="var(--cyan)"),
    dict(slug="minesweeper", js="minesweeper.js", icon="💣", color="var(--orange)"),
    dict(slug="gomoku", js="gomoku.js", icon="⚫", color="var(--pink)"),
    dict(slug="memory", js="memory.js", icon="🃏", color="var(--purple)", bannerLight=True),
    dict(slug="racing", js="gracing.js", icon="🏎️", color="var(--orange)"),
    dict(slug="sports", js="gsports.js", icon="⚽", color="var(--cyan)"),
    dict(slug="adventure", js="gadventure.js", icon="🗺️", color="var(--purple)"),
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
        sub="一次翻开两张，找出全部 8 对相同图案，用最少的步数完成挑战！",
        howto=["点击卡片翻开，一次最多翻开两张。",
               "图案相同则配对成功并保持翻开。",
               "不同则自动盖回，记住它们的位置！",
               "找出全部 8 对即获胜，步数越少成绩越好。"],
        tips=["按顺序翻牌并给位置编号，方便记忆。", "新图案出现时立刻回想是否见过。", "已配对的从记忆中划掉，缩小范围。"],
        title="记忆翻牌在线玩 - 免费记忆力训练小游戏 | 街机小游戏乐园",
        keywords="记忆翻牌,记忆翻牌在线玩,翻牌游戏,记忆力游戏,配对游戏,免费小游戏", canvasAria="记忆翻牌游戏区"),
    "racing": dict(name="极速躲避赛车", tags=["赛车", "反应", "街机"],
        cardDesc="在车流中左右变道躲避来车，考验你的反应与手速，跑得越久分数越高！",
        sub="你驾驶一辆车在四车道公路上飞驰，左右变道躲避迎面而来的车辆，生存越久得分越高。",
        howto=["电脑端：<kbd>←</kbd><kbd>→</kbd> 或 <kbd>A</kbd><kbd>D</kbd> 左右变道，<kbd>空格</kbd> 暂停/继续。",
               "手机端：点击屏幕下方的 ◀ ▶ 按钮变道。",
               "躲避所有来车，相撞即游戏结束。",
               "每成功躲过一辆车得 1 分，车速会越来越快。"],
        tips=["提前观察上方车流，预判空隙再变道。", "不要连续急变道，留足反应空间。", "车速加快时保持冷静，优先保证不碰撞。"],
        title="极速躲避赛车在线玩 - 免费赛车躲避小游戏 | 街机小游戏乐园",
        keywords="赛车游戏,躲避赛车,赛车小游戏,反应游戏,街机赛车,免费赛车", canvasAria="赛车躲避游戏区"),
    "sports": dict(name="趣味投篮", tags=["体育", "投篮", "反应"],
        cardDesc="拖动瞄准、松手投篮，把球投入篮筐，命中越多得分越高！",
        sub="在罚球线外拖动调整角度与力度，松手投篮，命中篮筐即可得分，挑战你的投篮手感！",
        howto=["在画面上方按住并拖动，松开即按方向投篮。",
               "也可以点击「开始」按钮自动瞄准投篮。",
               "球进入篮筐即得分，投失可继续尝试。",
               "投得越准，连续命中越多，分数越高。"],
        tips=["瞄准时让投射方向指向篮筐中心。", "力度适中，过大或过小都容易偏出。", "连续命中能保持手感，越打越准。"],
        title="趣味投篮在线玩 - 免费投篮体育小游戏 | 街机小游戏乐园",
        keywords="投篮游戏,篮球游戏,投篮小游戏,体育游戏,免费篮球,在线投篮", canvasAria="投篮游戏区"),
    "adventure": dict(name="迷宫大冒险", tags=["冒险", "解谜", "迷宫"],
        cardDesc="操控角色在迷宫中穿行，找到绿色出口逃出生天，用最少步数通关！",
        sub="用方向键或屏幕按钮操控小黄球，穿过蓝色墙壁组成的迷宫，抵达绿色出口即通关。",
        howto=["电脑端：<kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 或 <kbd>WASD</kbd> 移动。",
               "手机端：点击屏幕下方的方向按钮移动。",
               "蓝色方块是墙壁，黄色小球是你。",
               "走到绿色出口方块即通关，步数越少越好。"],
        tips=["先观察整体结构，规划大致路线。", "遇死胡同及时回头，不必硬闯。", "记住走过的岔路，避免绕圈。"],
        title="迷宫大冒险在线玩 - 免费迷宫冒险解谜小游戏 | 街机小游戏乐园",
        keywords="迷宫游戏,迷宫在线玩,迷宫小游戏,冒险游戏,解谜游戏,免费迷宫", canvasAria="迷宫冒险游戏区"),
}
# 其余语言的 GDATA 保持与原始脚本一致（省略展示，沿用既有数据）
GDATA["en"] = {
    "snake": dict(name="Snake", tags=["Arcade", "Action"],
        cardDesc="Guide the snake to eat and grow — don't hit the wall or yourself. Chase your high score!",
        sub="Eat food to grow longer; hitting a wall or yourself ends the game. Faster as you score!",
        howto=["Desktop: arrows or <kbd>WASD</kbd> to steer, <kbd>Space</kbd> to pause.",
               "Mobile: use the on-screen direction pad.",
               "Each food gives 10 points and grows the snake by one.",
               "Hitting a wall or your own body ends the game.",
               "Higher score means faster speed; best score is saved locally."],
        tips=["Stick to the edges to keep room to turn.", "Avoid dead ends once the snake is long.", "Plan turns early, before you reach the food."],
        title="Play Snake Online - Free Classic Snake Game | Arcade Games Hub",
        keywords="snake,snake online,play snake,classic snake,free snake game", canvasAria="Snake game canvas"),
    "2048": dict(name="2048", tags=["Puzzle", "Numbers"],
        cardDesc="Slide to merge equal tiles and build up to 2048. Simple rules, endless strategy.",
        sub="Slide tiles, merge equal numbers, and climb from 2 all the way to 2048!",
        howto=["Desktop: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> or <kbd>WASD</kbd> to slide.",
               "Mobile: swipe up/down/left/right on the board.",
               "Equal tiles merge into their sum when they collide.",
               "A new 2 or 4 appears after each move.",
               "Reach 2048 to win; no moves left means game over."],
        tips=["Keep the largest tile pinned in a corner.", "Slide along only two directions to stay ordered.", "Arrange big tiles in a snake pattern for fast merges."],
        title="Play 2048 Online - Free Number Puzzle Game | Arcade Games Hub",
        keywords="2048,2048 online,2048 game,number puzzle,puzzle game,free 2048", canvasAria="2048 game board"),
    "tetris": dict(name="Tetris", tags=["Arcade", "Classic"],
        cardDesc="Rotate, move and clear full lines! The timeless block-drop game that never gets old.",
        sub="Rotate and stack blocks; fill a full row to clear it. Level up every 10 lines — faster!",
        howto=["<kbd>←</kbd><kbd>→</kbd> move, <kbd>↓</kbd> soft drop.",
               "<kbd>↑</kbd>/<kbd>W</kbd> rotate, <kbd>Space</kbd> hard drop.",
               "Clear a full row to score; multiple rows at once score more.",
               "Stack reaching the top ends the game."],
        tips=["Leave a vertical well for the I-piece to clear four lines.", "Keep the surface flat to avoid holes.", "Plan the next piece's spot as levels rise."],
        title="Play Tetris Online - Free Classic Block Game | Arcade Games Hub",
        keywords="tetris,tetris online,play tetris,block game,puzzle game,free tetris", canvasAria="Tetris game canvas"),
    "minesweeper": dict(name="Minesweeper", tags=["Puzzle", "Logic"],
        cardDesc="Use number clues to deduce mine locations and flag them all. Pure logic and luck.",
        sub="Numbers show how many mines sit in the 8 surrounding cells. Flag them all to win!",
        howto=["Left click (tap) to reveal a cell.",
               "Right click (long press) to flag a mine, again to cancel.",
               "A number tells how many mines are around it.",
               "Reveal all non-mine cells to win; first click is always safe."],
        tips=["Start from corners and edges for clearer info.", "When enough flags surround a number, other cells are safe.", "Mark unsure cells and break elsewhere first."],
        title="Play Minesweeper Online - Free Classic Puzzle (Easy/Medium/Hard) | Arcade Games Hub",
        keywords="minesweeper,minesweeper online,free minesweeper,classic minesweeper,puzzle game", canvasAria="Minesweeper board",
        diffs=[("easy", "Easy 9×9 (10 mines)"), ("medium", "Medium 12×12 (24 mines)"), ("hard", "Hard 16×16 (40 mines)")]),
    "gomoku": dict(name="Gomoku", tags=["Board", "VS AI"],
        cardDesc="Connect five in a row to win. Built-in AI opponent — play anytime.",
        sub="You play black and move first against the computer AI. Connect five in any direction to win!",
        howto=["Click a board intersection to place a stone; you are black.",
               "Connect five horizontally, vertically or diagonally to win.",
               "The AI responds automatically, balancing attack and defense.",
               "A full board with no winner is a draw."],
        tips=["Take the center early to control the board.", "Build open-threes and fours to attack.", "Watch the opponent's threes and block in time."],
        title="Play Gomoku Online - Free Gomoku vs AI | Arcade Games Hub",
        keywords="gomoku,gomoku online,gomoku vs ai,board game,five in a row,free gomoku", canvasAria="Gomoku board"),
    "memory": dict(name="Memory Match", tags=["Puzzle", "Memory"],
        cardDesc="Flip cards, remember the pictures and find every matching pair. Train your memory.",
        sub="Flip two at a time to match all 8 pairs. Fewer moves means a better score!",
        howto=["Click a card to flip it; up to two may be open.",
               "Matching pictures stay revealed.",
               "Non-matching cards flip back — remember where they were!",
               "Find all 8 pairs to win; fewer moves is better."],
        tips=["Flip in order and number the spots to remember.", "Recall instantly when a new picture appears.", "Drop matched pairs from memory to shrink the field."],
        title="Play Memory Match Online - Free Memory Training Game | Arcade Games Hub",
        keywords="memory match,memory game,matching game,memory training,card game,free game", canvasAria="Memory game area"),
    "racing": dict(name="Dodge Racer", tags=["Racing", "Arcade", "Reaction"],
        cardDesc="Weave through traffic and dodge oncoming cars. How long can you survive?",
        sub="Drive down a four-lane highway, switch lanes to dodge traffic, and score for every car you pass.",
        howto=["Desktop: <kbd>←</kbd><kbd>→</kbd> or <kbd>A</kbd><kbd>D</kbd> to change lanes, <kbd>Space</kbd> to pause.",
               "Mobile: tap the ◀ ▶ buttons below the game.",
               "Avoid all oncoming cars; a crash ends the game.",
               "Each car dodged scores 1 point; the speed keeps rising."],
        tips=["Watch the traffic ahead and pick gaps early.", "Don't swerve repeatedly — keep room to react.", "Stay calm as the speed climbs; avoid collisions first."],
        title="Play Dodge Racer Online - Free Car Dodging Game | Arcade Games Hub",
        keywords="racing game,car dodging,dodge racer,arcade racing,reaction game,free racing", canvasAria="Car dodging area"),
    "sports": dict(name="Hoops Shoot", tags=["Sports", "Basketball", "Reaction"],
        cardDesc="Drag to aim, release to shoot. Sink as many baskets as you can!",
        sub="Drag on the screen to set angle and power, release to shoot. Score every ball that drops through the hoop.",
        howto=["Press and drag on the screen, then release to shoot toward the hoop.",
               "Or click Start for an auto-aimed shot.",
               "A ball through the hoop scores; misses can be retried.",
               "The more you sink in a row, the higher your score."],
        tips=["Aim so the trajectory points at the hoop center.", "Use moderate power — too much or too little misses.", "Sink consecutively to keep your rhythm."],
        title="Play Hoops Shoot Online - Free Basketball Sports Game | Arcade Games Hub",
        keywords="basketball game,hooting game,basketball,shoot hoop,sports game,free basketball", canvasAria="Basketball shooting area"),
    "adventure": dict(name="Maze Adventure", tags=["Adventure", "Puzzle", "Maze"],
        cardDesc="Guide your hero through the maze and reach the green exit with the fewest steps!",
        sub="Use the arrow keys or on-screen buttons to move the yellow ball through the blue-walled maze to the green exit.",
        howto=["Desktop: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> or <kbd>WASD</kbd> to move.",
               "Mobile: tap the direction buttons below the game.",
               "Blue blocks are walls; the yellow ball is you.",
               "Reach the green exit tile to win; fewer steps is better."],
        tips=["Survey the whole maze and plan a rough route.", "Turn back at dead ends instead of forcing through.", "Remember branching paths to avoid looping."],
        title="Play Maze Adventure Online - Free Maze Puzzle Game | Arcade Games Hub",
        keywords="maze game,maze online,maze puzzle,adventure game,puzzle game,free maze", canvasAria="Maze adventure area"),
}
GDATA["es"] = {
    "snake": dict(name="Snake", tags=["Arcade", "Acción"],
        cardDesc="Guía a la serpiente para comer y crecer, sin chocar con la pared ni contigo mismo.",
        sub="Come para crecer; chocar con la pared o contigo mismo termina el juego. ¡Más rápido al subir!",
        howto=["PC: flechas o <kbd>WASD</kbd>; <kbd>Espacio</kbd> pausa.", "Móvil: usa las flechas en pantalla.",
               "Cada comida suma 10 y alarga la serpiente.", "Chocar con pared o cuerpo termina el juego.",
               "A mayor puntaje, más velocidad; el récord se guarda."],
        tips=["Ve por los bordes para tener espacio.", "Evita callejones sin salida.", "Gira antes de llegar a la comida."],
        title="Juega Snake en línea - Clásico gratis | Arcade de Minijuegos",
        keywords="snake,snake online,jugar snake,serpiente clásica", canvasAria="Lienzo de Snake"),
    "2048": dict(name="2048", tags=["Puzle", "Números"],
        cardDesc="Desliza para unir tiles iguales hasta 2048. Reglas simples, estrategia infinita.",
        sub="Une números iguales y sube de 2 a 2048.",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> o <kbd>WASD</kbd>.", "Móvil: desliza en el tablero.",
               "Iguales se suman al chocar.", "Aparece un 2 o 4 tras cada movimiento.", "Llega a 2048 para ganar."],
        tips=["Fija el mayor en una esquina.", "Desliza en dos direcciones.", "Ordena en serpentín."],
        title="Juega 2048 en línea - Puzzle gratis | Arcade de Minijuegos",
        keywords="2048,2048 online,juego 2048,puzzle números", canvasAria="Tablero 2048"),
    "tetris": dict(name="Tetris", tags=["Arcade", "Clásico"],
        cardDesc="Rota, mueve y borra líneas. El clásico que nunca pasa de moda.",
        sub="Rellena una fila completa para borrarla. ¡Sube de nivel cada 10 líneas!",
        howto=["<kbd>←</kbd><kbd>→</kbd> mover, <kbd>↓</kbd> bajar.", "<kbd>↑</kbd>/<kbd>W</kbd> rotar, <kbd>Espacio</kbd> soltar.",
               "Borra filas para puntuar.", "Llegar arriba termina el juego."],
        tips=["Deja un pozo para la I.", "Mantén la superficie plana.", "Planifica la siguiente pieza."],
        title="Juega Tetris en línea - Clásico gratis | Arcade de Minijuegos",
        keywords="tetris,tetris online,jugar tetris,bloques", canvasAria="Lienzo de Tetris"),
    "minesweeper": dict(name="Buscaminas", tags=["Puzle", "Lógica"],
        cardDesc="Usa las pistas para deducir las minas y marcarlas. Lógica pura.",
        sub="Los números indican minas vecinas. ¡Marca todas para ganar!",
        howto=["Clic izquierdo revela.", "Clic derecho (mantener) marca mina.", "El número indica minas cercanas.",
               "Revela todo lo que no es mina para ganar."],
        tips=["Empieza en esquinas.", "Con suficientes banderas, lo demás es seguro.", "Marca lo dudoso y rompe por otro lado."],
        title="Juega Buscaminas en línea - Clásico gratis | Arcade de Minijuegos",
        keywords="buscaminas,buscaminas online,gratis,lógica", canvasAria="Tablero Buscaminas",
        diffs=[("easy", "Fácil 9×9 (10)"), ("medium", "Medio 12×12 (24)"), ("hard", "Difícil 16×16 (40)")]),
    "gomoku": dict(name="Gomoku", tags=["Tablero", "VS IA"],
        cardDesc="Conecta cinco en línea para ganar. IA integrada.",
        sub="Juegas con negro y mueves primero. ¡Conecta cinco para ganar!",
        howto=["Clic en intersección, eres negro.", "Cinco en cualquier dirección gana.", "La IA responde sola.", "Tablero lleno es empate."],
        tips=["Toma el centro.", "Haz tres y cuatro abiertos.", "Bloquea al rival."],
        title="Juega Gomoku en línea - VS IA gratis | Arcade de Minijuegos",
        keywords="gomoku,gomoku online,ia,tablero", canvasAria="Tablero Gomoku"),
    "memory": dict(name="Memoria", tags=["Puzle", "Memoria"],
        cardDesc="Voltea cartas y encuentra las parejas. Entrena la memoria.",
        sub="Voltea dos a la vez y empareja las 8 parejas.",
        howto=["Clic para voltear, máximo dos.", "Iguales quedan visibles.", "Distintas se ocultan.", "8 parejas para ganar."],
        tips=["Numera las posiciones.", "Recuerda nuevas.", "Borra emparejadas."],
        title="Juega Memoria en línea - Gratis | Arcade de Minijuegos",
        keywords="memoria,juego memoria,emparejar", canvasAria="Área Memoria"),
    "racing": dict(name="Esquiva Coches", tags=["Carreras", "Arcade", "Reacción"],
        cardDesc="Esquiva el tráfico y sobrevive. ¿Cuánto aguantas sin chocar?",
        sub="Conduce por una autopista de cuatro carriles, cambia de carril y esquiva coches. Cada uno esquivado suma puntos.",
        howto=["PC: <kbd>←</kbd><kbd>→</kbd> o <kbd>A</kbd><kbd>D</kbd> para cambiar de carril, <kbd>Espacio</kbd> pausa.",
               "Móvil: toca los botones ◀ ▶ bajo el juego.",
               "Evita todos los coches; chocar termina la partida.",
               "Cada coche esquivado da 1 punto; la velocidad sube."],
        tips=["Mira el tráfico y elige huecos pronto.", "No zigzaguees; deja margen.", "Calma cuando sube la velocidad."],
        title="Juega a Esquiva Coches Online - Carreras Gratis | MiniJuegos",
        keywords="carreras,esquivar coches,arcade,reacción,juego gratis", canvasAria="Zona de coches"),
    "sports": dict(name="Tiro Libre", tags=["Deportes", "Baloncesto", "Reacción"],
        cardDesc="Arrastra para apuntar y suelta para lanzar. ¡Encesta cuantas puedas!",
        sub="Arrastra para ajustar ángulo y potencia, suelta para lanzar. Cada canasta suma puntos.",
        howto=["Pulsa y arrastra en la pantalla, suelta para lanzar.",
               "O pulsa Iniciar para un tiro automático.",
               "Encestar puntúa; puedes reintentar los fallos.",
               "Más aciertos seguidos, más puntos."],
        tips=["Apunta al centro del aro.", "Potencia media; ni mucho ni poco.", "Encadena aciertos para el ritmo."],
        title="Juega a Tiro Libre Online - Baloncesto Gratis | MiniJuegos",
        keywords="baloncesto,tiro,deportes,juego gratis", canvasAria="Zona de tiro"),
    "adventure": dict(name="Aventura en el Laberinto", tags=["Aventura", "Puzle", "Laberinto"],
        cardDesc="Guía a tu héroe por el laberinto hasta la salida verde ¡con pocos pasos!",
        sub="Usa las flechas o los botones para mover la bola amarilla por el laberinto hasta la salida verde.",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> o <kbd>WASD</kbd> para mover.",
               "Móvil: toca los botones de dirección.",
               "Los bloques azules son muros; la bola amarilla eres tú.",
               "Llega a la salida verde para ganar."],
        tips=["Observa el laberinto y planea.", "Vuelve en callejones sin forzar.", "Recuerda las ramas para no girar."],
        title="Juega a Aventura en el Laberinto Online - Puzle Gratis | MiniJuegos",
        keywords="laberinto,aventura,puzle,juego gratis", canvasAria="Zona de laberinto"),
}
GDATA["ar"] = {
    "snake": dict(name="الثعبان", tags=["أركيد", "أكشن"],
        cardDesc="وجّه الثعبان ليأكل وينمو دون أن يضرب الجدار أو نفسه.",
        sub="كل الطعام فيطول الثعبان؛ الضرب بالجدار أو بنفسه ينهي اللعبة.",
        howto=["الحاسوب: الأسهم أو <kbd>WASD</kbd>؛ <kbd>مسافة</kbd> إيقاف.", "الجوال: أزرار الشاشة.",
               "كل طعام +10 ويطول الثعبان.", "الضرب ينهي اللعبة.", "السرعة تزداد مع النقاط."],
        tips=["سر على الحواف.", "تجنب الزوايا الميتة.", "خطط مبكرًا."],
        title="العب الثعبان أونلاين - كلاسيكي مجاني | ألعاب الأركيد",
        keywords="ثعبان,ثعبان أونلاين,لعبة ثعبان", canvasAria="لوحة الثعبان"),
    "2048": dict(name="2048", tags=["ألغاز", "أرقام"],
        cardDesc="اسحب لدمج المربعات المتساوية حتى 2048.",
        sub="ادمج الأرقام المتساوية واصعد من 2 إلى 2048.",
        howto=["الحاسوب: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd>.", "الجوال: اسحب على اللوحة.",
               "المتساوية تندمج.", "يظهر 2 أو 4 بعد كل حركة.", "اصل 2048 لتفوز."],
        tips=["ثبّت الأكبر في زاوية.", "سر باتجاهين.", "رتّب بشكل متعرج."],
        title="العب 2048 أونلاين - لغز مجاني | ألعاب الأركيد",
        keywords="2048,2048 أونلاين,لغز أرقام", canvasAria="لوحة 2048"),
    "tetris": dict(name="تتريس", tags=["أركيد", "كلاسيكي"],
        cardDesc="أدر واجمع وامسح الصفوف. الكلاسيكي الخالد.",
        sub="املأ صفًا كاملًا لتمسحه. ترتقي كل 10 صفوف!",
        howto=["<kbd>←</kbd><kbd>→</kbd> تحريك، <kbd>↓</kbd> إسقاط.", "<kbd>↑</kbd>/<kbd>W</kbd> تدوير، <kbd>مسافة</kbd> إسقاط فوري.",
               "امسح الصفوف لتسجل.", "الوصول للأعلى ينهي اللعبة."],
        tips=["اترك بئرًا للقطعة I.", "حافظ على السطح مستويًا.", "خطط للتالية."],
        title="العب تتريس أونلاين - كلاسيكي مجاني | ألعاب الأركيد",
        keywords="تتريس,تتريس أونلاين,مكعبات", canvasAria="لوحة تتريس"),
    "minesweeper": dict(name="كانسة الألغام", tags=["ألغاز", "منطق"],
        cardDesc="استخدم الأرقام لاستنتاج الألغام وضع عليها الأعلام.",
        sub="الأرقام تدل على الألغام المجاورة. ضع الأعلام لتفوز!",
        howto=["نقرة تكشف.", "نقرة يمين (ضغط طويل) تضع علمًا.", "الرقم يدل على الألغام.", "اكشف كل غير الملغم لتفوز."],
        tips=["ابدأ من الزوايا.", "مع أعلام كافية الباقي آمن.", "علّم المشكوك فيه."],
        title="العب كانسة الألغام أونلاين - كلاسيكي مجاني | ألعاب الأركيد",
        keywords="كانسة ألغام,ألغام أونلاين,منطق", canvasAria="لوحة الألغام",
        diffs=[("easy", "سهل 9×9 (10)"), ("medium", "متوسط 12×12 (24)"), ("hard", "صعب 16×16 (40)")]),
    "gomoku": dict(name="غوموكو", tags=["لوحة", "ضد حاسوب"],
        cardDesc="صل خمسة على التوالي لتفوز. ذكاء اصطناعي مدمج.",
        sub="تلعب بالأسود أولًا. صل خمسة لتفوز!",
        howto=["انقر التقاطع، أنت الأسود.", "خمسة بأي اتجاه تفوز.", "الحاسوب يرد تلقائيًا.", "لوحة ممتلئة تعادل."],
        tips=["استولِ على المركز.", "اصنع ثلاثة وأربعة مفتوحة.", "اقطع الخصم."],
        title="العب غوموكو أونلاين - ضد حاسوب مجاني | ألعاب الأركيد",
        keywords="غوموكو,غوموكو أونلاين,لوحة", canvasAria="لوحة غوموكو"),
    "memory": dict(name="الذاكرة", tags=["ألغاز", "ذاكرة"],
        cardDesc="اقلب البطاقات وطابق الصور. درب ذاكرتك.",
        sub="اقلب اثنتين في كل مرة وطابق الثماني أزواج.",
        howto=["انقر للقلب، أقصاها اثنتان.", "المتطابق يبقى ظاهرًا.", "غير المتطابق يُغطى.", "8 أزواج تفوز."],
        tips=["رقّم المواقع.", "تذكر الجديد.", "احذف المطابق."],
        title="العب الذاكرة أونلاين - مجاني | ألعاب الأركيد",
        keywords="ذاكرة,لعبة ذاكرة,مطابقة", canvasAria="منطقة الذاكرة"),
    "racing": dict(name="سباق التفادي", tags=["سباق", "أركيد", "ردة فعل"],
        cardDesc="تفادَ السيارات القادمة وانجُ من التصادم. كم تدوم؟",
        sub="اقود سيارتك على طريق بأربعة مسارات، بدّل المسار وتفادَ السيارات. كل سيارة تتفاداها تعطي نقطة.",
        howto=["الكمبيوتر: <kbd>←</kbd><kbd>→</kbd> أو <kbd>A</kbd><kbd>D</kbd> لتبديل المسار، <kbd>مسافة</kbd> إيقاف.",
               "الهاتف: انقر أزرار ◀ ▶ أسفل اللعبة.",
               "تجنّب كل السيارات؛ التصادم ينهي اللعبة.",
               "كل سيارة تتفاداها نقطة واحدة؛ السرعة تزداد."],
        tips=["راقب السيارات واختر الفراغات مبكرًا.", "لا تغير المسار كثيرًا.", "اهدأ مع زيادة السرعة."],
        title="العب سباق التفادي مجانًا | ألعاب مصغرة",
        keywords="سباق,تفادي,أركيد,رد فعل,لعبة مجانية", canvasAria="منطقة السباق"),
    "sports": dict(name="رمية السلة", tags=["رياضة", "سلة", "ردة فعل"],
        cardDesc="اسحب لتصوب وأفلت لتطلق. سدّد ما استطعت!",
        sub="اسحب لضبط الزاوية والقوة، أفلت لتطلق. كل كرة بالسلة نقطة.",
        howto=["اضغط واسحب على الشاشة ثم أفلت لتسديد.",
               "أو انقر بدء لتسديدة تلقائية.",
               "الكرة بالسلة تُسجَّل؛ يمكن إعادة المحاولة.",
               "الإصابات المتتالية ترفع النقاط."],
        tips=["صوّب نحو مركز الحلقة.", "قوة متوسطة.", "سلسلة الإصابات تحافظ على الإيقاع."],
        title="العب رمية السلة مجانًا | ألعاب مصغرة",
        keywords="سلة,رمي,رياضة,لعبة مجانية", canvasAria="منطقة السلة"),
    "adventure": dict(name="مغامرة المتاهة", tags=["مغامرات", "ألغاز", "متاهة"],
        cardDesc="قُد بطلَك عبر المتاهة إلى المخرج الأخضر بأقل خطوات!",
        sub="استخدم الأسهم أو الأزرار لتحريك الكرة الصفراء عبر المتاهة حتى المخرج الأخضر.",
        howto=["الكمبيوتر: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> أو <kbd>WASD</kbd> للتحرك.",
               "الهاتف: انقر أزرار الاتجاه.",
               "الكتل الزرقاء جدران؛ الكرة الصفراء أنت.",
               "الوصول للمخرج الأخضر يفوز."],
        tips=["تأمل المتاهة وخطّط.", "عُد عند الطريق المسدود.", "تذكّر الفروع لتجنب الدوران."],
        title="العب مغامرة المتاهة مجانًا | ألعاب مصغرة",
        keywords="متاهة,مغامرة,ألغاز,لعبة مجانية", canvasAria="منطقة المتاهة"),
}
GDATA["ru"] = {
    "snake": dict(name="Змейка", tags=["Аркада", "Экшен"],
        cardDesc="Веди змейку к еде и расти, не врезаясь в стену или себя.",
        sub="Ешь, чтобы расти; удар о стену или себя — конец. Быстрее с ростом очков!",
        howto=["ПК: стрелки или <kbd>WASD</kbd>; <kbd>Пробел</kbd> пауза.", "Телефон: экранные стрелки.",
               "Еда +10 и удлиняет.", "Удар заканчивает игру.", "Скорость растёт."],
        tips=["Держись краёв.", "Избегай тупиков.", "Поворачивай заранее."],
        title="Играть в Змейку онлайн - Классика бесплатно | Аркадные мини-игры",
        keywords="змейка,змейка онлайн,классическая", canvasAria="Поле Змейки"),
    "2048": dict(name="2048", tags=["Головоломка", "Числа"],
        cardDesc="Сдвигай, соединяй равные плитки до 2048.",
        sub="Соединяй числа и поднимайся от 2 до 2048.",
        howto=["ПК: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd>.", "Телефон: свайп.", "Равные складываются.",
               "Появляются 2 или 4.", "Достигни 2048."],
        tips=["Держи большее в углу.", "Сдвигай в два направления.", "Змейка для порядка."],
        title="Играть в 2048 онлайн - Пазл бесплатно | Аркадные мини-игры",
        keywords="2048,2048 онлайн,числовой пазл", canvasAria="Поле 2048"),
    "tetris": dict(name="Тетрис", tags=["Аркада", "Классика"],
        cardDesc="Крути, двигай, убирай ряды. Вечная классика.",
        sub="Заполни ряд — и он исчезнет. Уровень каждые 10 рядов!",
        howto=["<kbd>←</kbd><kbd>→</kbd> двигать, <kbd>↓</kbd> мягко.", "<kbd>↑</kbd>/<kbd>W</kbd> крутить, <kbd>Пробел</kbd> бросить.",
               "Убирай ряды.", "Доверху — конец."],
        tips=["Оставь колодец для I.", "Держи ровно.", "Планируй следующую."],
        title="Играть в Тетрис онлайн - Классика бесплатно | Аркадные мини-игры",
        keywords="тетрис,тетрис онлайн,блоки", canvasAria="Поле Тетриса"),
    "minesweeper": dict(name="Сапёр", tags=["Головоломка", "Логика"],
        cardDesc="По цифрам найди мины и пометь их флажками.",
        sub="Цифры — число мин вокруг. Пометь все, чтобы выиграть!",
        howto=["Левый клик открывает.", "Правый (долгое) ставит флаг.", "Цифра — мины рядом.", "Открой все не мины."],
        tips=["Начни с углов.", "С флагами остальное безопасно.", "Отметь сомнительное."],
        title="Играть в Сапёра онлайн - Классика бесплатно | Аркадные мини-игры",
        keywords="сапёр,сапёр онлайн,логика", canvasAria="Поле Сапёра",
        diffs=[("easy", "Легко 9×9 (10)"), ("medium", "Средне 12×12 (24)"), ("hard", "Сложно 16×16 (40)")]),
    "gomoku": dict(name="Гомоку", tags=["Доска", "Против ИИ"],
        cardDesc="Соедини пять подряд, чтобы выиграть. ИИ встроен.",
        sub="Ты чёрными и ходишь первым. Соедини пять!",
        howto=["Клик по точке, ты чёрный.", "Пять в любую сторону — победа.", "ИИ отвечает.", "Поле полно — ничья."],
        tips=["Бери центр.", "Делай открытые тройки.", "Блокируй соперника."],
        title="Играть в Гомоку онлайн - Против ИИ бесплатно | Аркадные мини-игры",
        keywords="гомоку,гомоку онлайн,доска", canvasAria="Поле Гомоку"),
    "memory": dict(name="Память", tags=["Головоломка", "Память"],
        cardDesc="Переворачивай карты и ищи пары. Тренируй память.",
        sub="Переворачивай по две и найди 8 пар.",
        howto=["Клик, максимум две.", "Одинаковые остаются.", "Разные скрываются.", "8 пар — победа."],
        tips=["Нумеруй позиции.", "Помни новое.", "Убирай пары."],
        title="Играть в Память онлайн - Бесплатно | Аркадные мини-игры",
        keywords="память,игра память,пары", canvasAria="Поле Памяти"),
    "racing": dict(name="Гонки-Увёрты", tags=["Гонки", "Аркада", "Реакция"],
        cardDesc="Уворачивайся от машин и выживай. Сколько продержишься?",
        sub="Езжай по четырёхполосному шоссе, меняй полосу и уворачивайся. Каждая машина — очко.",
        howto=["ПК: <kbd>←</kbd><kbd>→</kbd> или <kbd>A</kbd><kbd>D</kbd> менять полосу, <kbd>Пробел</kbd> пауза.",
               "Телефон: кнопки ◀ ▶ под игрой.",
               "Избегай всех машин; столкновение — конец.",
               "Каждая увёрнутая машина +1 очко; скорость растёт."],
        tips=["Смотри вперёд и выбирай промежутки.", "Не шарахайся резко.", "Спокойнее при росте скорости."],
        title="Играть в Гонки-Увёрты Онлайн - Гонки Бесплатно | Мини-игры",
        keywords="гонки,увороты,аркада,реакция,бесплатно", canvasAria="Зона гонок"),
    "sports": dict(name="Баскет-Бросок", tags=["Спорт", "Баскетбол", "Реакция"],
        cardDesc="Тяни чтобы прицелиться, отпусти чтобы бросить. Забей побольше!",
        sub="Тяни для угла и силы, отпусти для броска. Каждый мяч в кольце — очко.",
        howto=["Нажми и тяни на экране, отпусти для броска.",
               "Или нажми Старт для авто-броска.",
               "Мяч в кольце считается; промахи можно повторить.",
               "Подряд забитые повышают счёт."],
        tips=["Целься в центр кольца.", "Средняя сила.", "Серия попаданий держит ритм."],
        title="Играть в Баскет-Бросок Онлайн - Спорт Бесплатно | Мини-игры",
        keywords="баскетбол,бросок,спорт,бесплатно", canvasAria="Зона броска"),
    "adventure": dict(name="Лабиринт-Приключение", tags=["Приключения", "Головоломка", "Лабиринт"],
        cardDesc="Веди героя через лабиринт к зелёному выходу за меньше шагов!",
        sub="Стрелками или кнопками веди жёлтый шар через лабиринт к зелёному выходу.",
        howto=["ПК: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> или <kbd>WASD</kbd> двигаться.",
               "Телефон: кнопки направлений.",
               "Синие блоки — стены; жёлтый шар — ты.",
               "Дойди до зелёного выхода, чтобы выиграть."],
        tips=["Осмотри лабиринт и планируй.", "Возвращайся в тупиках.", "Помни развилки, чтобы не кружить."],
        title="Играть в Лабиринт-Приключение Онлайн - Головоломка Бесплатно | Мини-игры",
        keywords="лабиринт,приключение,головоломка,бесплатно", canvasAria="Зона лабиринта"),
}
GDATA["ja"] = {
    "snake": dict(name="スネーク", tags=["アーケード", "アクション"],
        cardDesc="ヘビを操って餌を食べて長くしよう。壁や自分に当てないように。",
        sub="餌を食べると長くなる。壁や自分に当たると終了。早くなる!",
        howto=["PC: 矢印か <kbd>WASD</kbd>; <kbd>空格</kbd> 一時停止。", "スマホ: 画面ボタン。",
               "餌で+10、長くなる。", "当たると終了。", "早くなる。"],
        tips=["端を走る。", "袋小路を避ける。", "早めに曲がる。"],
        title="スネークを無料で遊ぶ | ミニゲームランド",
        keywords="スネーク,スネーク オンライン,クラシック", canvasAria="スネーク盤"),
    "2048": dict(name="2048", tags=["パズル", "数字"],
        cardDesc="同じタイルをスライドして合体、2048を目指そう。",
        sub="同じ数字を合体させ2から2048へ。",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd>。", "スマホ: スワイプ。", "同じは合体。",
               "每回2か4が出る。", "2048で勝ち。"],
        tips=["最大を隅に。", "2方向に。", "蛇行配置。"],
        title="2048を無料で遊ぶ | ミニゲームランド",
        keywords="2048,2048 オンライン,数字パズル", canvasAria="2048盤"),
    "tetris": dict(name="テトリス", tags=["アーケード", "クラシック"],
        cardDesc="回して積んで列を消そう。永遠の名作。",
        sub="列を埋めると消える。10列ごとにレベルアップ!",
        howto=["<kbd>←</kbd><kbd>→</kbd> 移動, <kbd>↓</kbd> 軟着陸。", "<kbd>↑</kbd>/<kbd>W</kbd> 回転, <kbd>空格</kbd> 即落下。",
               "列を消す。", "上端で終了。"],
        tips=["I用の井戸を空ける。", "表面を平らに。", "次を考えろ。"],
        title="テトリスを無料で遊ぶ | ミニゲームランド",
        keywords="テトリス,テトリス オンライン,ブロック", canvasAria="テトリス盤"),
    "minesweeper": dict(name="マインスイーパー", tags=["パズル", "ロジック"],
        cardDesc="数字を手がかりに地雷を推理し、すべて旗を立てよう。",
        sub="数字は周囲の地雷数。すべて旗を立てれば勝ち!",
        howto=["左クリックで開く。", "右(長押し)で旗。", "数字は周囲の地雷。", "非地雷を全部開くと勝ち。"],
        tips=["角から。", "旗が十分なら残り安全。", "怪しいをマーク。"],
        title="マインスイーパーを無料で遊ぶ | ミニゲームランド",
        keywords="マインスイーパー,オンライン,ロジック", canvasAria="マイン盤",
        diffs=[("easy", "易 9×9 (10)"), ("medium", "中 12×12 (24)"), ("hard", "難 16×16 (40)")]),
    "gomoku": dict(name="五目並べ", tags=["盤上", "AI対戦"],
        cardDesc="五つ並べて勝ち。AI内蔵。",
        sub="あなたは黒で先手。五つ並べて勝ち!",
        howto=["交点をクリック、黒。", "五つで勝ち。", "AIが応手。", "盤埋まれば引き分け。"],
        tips=["中心を取る。", "活三・四を作る。", "相手を塞ぐ。"],
        title="五目並べを無料で遊ぶ | ミニゲームランド",
        keywords="五目並べ,オンライン,AI", canvasAria="五目盤"),
    "memory": dict(name="神経衰弱", tags=["パズル", "記憶"],
        cardDesc="カードをめくりペアを見つけよう。記憶を鍛える。",
        sub="2枚ずつめくり8ペアを見つける。",
        howto=["クリックでめくる、最大2枚。", "同じは開いたまま。", "違うは戻る。", "8ペアで勝ち。"],
        tips=["位置を番号付け。", "新しいを覚える。", "ペアを消す。"],
        title="神経衰弱を無料で遊ぶ | ミニゲームランド",
        keywords="神経衰弱,記憶,カード", canvasAria="神経衰弱盤"),
    "racing": dict(name="避けレース", tags=["レーシング", "アーケード", "反応"],
        cardDesc="車を避けて生き残ろう。どれだけ走れる？",
        sub="4車線の高速道路で車線を変え、迎え来る車を避ける。避けるごとに得点。",
        howto=["PC: <kbd>←</kbd><kbd>→</kbd> または <kbd>A</kbd><kbd>D</kbd> で車線変更、<kbd>Space</kbd> 一時停止。",
               "スマホ: ゲーム下の ◀ ▶ ボタン。",
               "すべての車を避ける。衝突で終了。",
               "避けるごとに1点。速度は上がる。"],
        tips=["前方の車を見て早めに空きを。", "急に何度も変えない。", "速くなっても冷静に。"],
        title="避けレースを無料で遊ぶ | ミニゲームランド",
        keywords="レーシング,避け,アーケード,反応,無料", canvasAria="レースエリア"),
    "sports": dict(name="シュート", tags=["スポーツ", "バスケ", "反応"],
        cardDesc="ドラッグで狙い、離してシュート。たくさん決めよう！",
        sub="ドラッグで角度と力を調整、離してシュート。ゴール毎に得点。",
        howto=["画面を押してドラッグ、離してシュート。",
               "または「開始」で自動シュート。",
               "決まれば得点。外しても再挑戦可。",
               "連続決勝で得点アップ。"],
        tips=["リング中央を狙う。", "力は中程度。", "連続でリズムを。"],
        title="シュートを無料で遊ぶ | ミニゲームランド",
        keywords="バスケ,シュート,スポーツ,無料", canvasAria="シュートエリア"),
    "adventure": dict(name="迷路アドベンチャー", tags=["アドベンチャー", "パズル", "迷路"],
        cardDesc="迷路を抜けて緑の出口へ、少ない歩数で！",
        sub="矢印やボタンで黄色の玉を動かし、迷路を抜けて緑の出口へ。",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> または <kbd>WASD</kbd> で移動。",
               "スマホ: 方向ボタン。",
               "青ブロックは壁。黄色の玉があなた。",
               "緑の出口へ行けばクリア。"],
        tips=["全体を見てルートを。", "行き止まりは戻る。", "分岐を覚えてぐるぐる防ぐ。"],
        title="迷路アドベンチャーを無料で遊ぶ | ミニゲームランド",
        keywords="迷路,アドベンチャー,パズル,無料", canvasAria="迷路エリア"),
}
GDATA["ko"] = {
    "snake": dict(name="스네이크", tags=["아케이드", "액션"],
        cardDesc="뱀이를 굴려 먹이를 먹여 키우세요. 벽이나 자신에게 부딪히지 않게.",
        sub="먹으면 길어집니다. 벽이나 자신에 부딪히면 종료. 빨라집니다!",
        howto=["PC: 화살표나 <kbd>WASD</kbd>; <kbd>스페이스</kbd> 일시정지.", "모바일: 화면 버튼.",
               "먹이 +10, 길어짐.", "부딪히면 종료.", "빠르게!"],
        tips=["가장자리로.", "막다른 곳 피하기.", "미리 회전."],
        title="스네이크 무료 플레이 | 미니게임 놀이터",
        keywords="스네이크,스네이크 온라인,클래식", canvasAria="스네이크 판"),
    "2048": dict(name="2048", tags=["퍼즐", "숫자"],
        cardDesc="같은 타일을 밀어 합치고 2048까지.",
        sub="같은 숫자를 합쳐 2에서 2048로.",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd>.", "모바일: 스와이프.", "같은 것은 합쳐짐.",
               "매번 2 또는 4 등장.", "2048로 승리."],
        tips=["큰 수를 모서리에.", "두 방향으로.", "지그재그 배열."],
        title="2048 무료 플레이 | 미니게임 놀이터",
        keywords="2048,2048 온라인,숫자 퍼즐", canvasAria="2048 판"),
    "tetris": dict(name="테트리스", tags=["아케이드", "클래식"],
        cardDesc="돌리고 쌓아 줄을 지우는 영원한 고전.",
        sub="줄을 채우면 사라집니다. 10줄마다 레벨 업!",
        howto=["<kbd>←</kbd><kbd>→</kbd> 이동, <kbd>↓</kbd> 빠른 낙하.", "<kbd>↑</kbd>/<kbd>W</kbd> 회전, <kbd>스페이스</kbd> 즉시 낙하.",
               "줄 지우기.", "꼭대기까지 쌓이면 종료."],
        tips=["I용 우물 남기기.", "표면 평평하게.", "다음 조각 계획."],
        title="테트리스 무료 플레이 | 미니게임 놀이터",
        keywords="테트리스,테트리스 온라인,블록", canvasAria="테트리스 판"),
    "minesweeper": dict(name="지뢰찾기", tags=["퍼즐", "추리"],
        cardDesc="숫자로 지뢰를 추리하고 모두 깃발을 꽂으세요.",
        sub="숫자는 주변 지뢰 수. 모두 꽂으면 승리!",
        howto=["왼쪽 클릭 열기.", "오른쪽(길게) 깃발.", "숫자는 주변 지뢰.", "비지뢰 다 열면 승리."],
        tips=["모서리부터.", "깃발 충분하면 나머지 안전.", "의심 가는 곳 표시."],
        title="지뢰찾기 무료 플레이 | 미니게임 놀이터",
        keywords="지뢰찾기,온라인,추리", canvasAria="지뢰판",
        diffs=[("easy", "초급 9×9 (10)"), ("medium", "중급 12×12 (24)"), ("hard", "고급 16×16 (40)")]),
    "gomoku": dict(name="오목", tags=["보드", "AI 대전"],
        cardDesc="다섯 개 연결하면 승리. 내장 AI.",
        sub="당신은 흑돌 선수. 다섯 개 연결하면 승리!",
        howto=["교차점 클릭, 흑돌.", "다섯 개로 승리.", "AI가 응수.", "판 가득 이면 무승부."],
        tips=["중앙 차지.", "열린 3·4 만들기.", "상대 막기."],
        title="오목 무료 플레이 | 미니게임 놀이터",
        keywords="오목,온라인,AI", canvasAria="오목 판"),
    "memory": dict(name="메모리 카드", tags=["퍼즐", "기억력"],
        cardDesc="카드를 뒤집어 짝을 찾으세요. 기억력 훈련.",
        sub="한 번에 두 장씩, 8쌍 찾기.",
        howto=["클릭해 뒤집기, 최대 두 장.", "같으면 열림.", "다르면 닫힘.", "8쌍이면 승리."],
        tips=["위치 번호 매기기.", "새 그림 기억.", "짝 지우기."],
        title="메모리 카드 무료 플레이 | 미니게임 놀이터",
        keywords="메모리,짝 맞추기,기억력", canvasAria="메모리 판"),
    "racing": dict(name="회피 레이싱", tags=["레이싱", "아케이드", "반응"],
        cardDesc="차를 피해 살아남으세요. 얼마나 버티나요?",
        sub="4차선 고속도로에서 차선을 바꿔 오는 차를 피하세요. 피할 때마다 점수.",
        howto=["PC: <kbd>←</kbd><kbd>→</kbd> 또는 <kbd>A</kbd><kbd>D</kbd> 차선 변경, <kbd>Space</kbd> 일시정지.",
               "모바일: 게임 아래 ◀ ▶ 버튼.",
               "모든 차를 피하세요. 충돌 시 종료.",
               "피할 때마다 1점. 속도는 빨라집니다."],
        tips=["앞차를 미리 보고 틈을 택하세요.", "길게 움직이지 마세요.", "빠를수록 침착하게."],
        title="회피 레이싱 무료 플레이 | 미니게임",
        keywords="레이싱,회피,아케이드,반응,무료", canvasAria="레이싱 영역"),
    "sports": dict(name="슛 게임", tags=["스포츠", "농구", "반응"],
        cardDesc="드래그로 조준하고 놓아 슛. 많이 넣으세요!",
        sub="드래그로 각도와 힘을 조절해 놓으세요. 림에 들어갈 때마다 점수.",
        howto=["화면을 누르고 드래그 후 놓아 슛.",
               "또는 시작으로 자동 슛.",
               "들어가면 득점. 실패도 재시도.",
               "연속 성공으로 점수 UP."],
        tips=["림 중앙을 조준.", "적당한 힘.", "연속으로 리듬 유지."],
        title="슛 게임 무료 플레이 | 미니게임",
        keywords="농구,슛,스포츠,무료", canvasAria="슛 영역"),
    "adventure": dict(name="미로 어드벤처", tags=["어드벤처", "퍼즐", "미로"],
        cardDesc="미로를 빠져나와 초록 출구까지, 적은 걸음으로!",
        sub="방향키나 버튼으로 노란 공을 움직여 미로를 빠져나와 초록 출구로.",
        howto=["PC: <kbd>↑</kbd><kbd>↓</kbd><kbd>←</kbd><kbd>→</kbd> 또는 <kbd>WASD</kbd> 이동.",
               "모바일: 방향 버튼.",
               "파란 블록은 벽. 노란 공이 당신.",
               "초록 출구 도착 시 클리어."],
        tips=["미로를 보고 경로 계획.", "막다른 길은 되돌아가기.", "갈림길 기억해 빙글빙글 방지."],
        title="미로 어드벤처 무료 플레이 | 미니게임",
        keywords="미로,어드벤처,퍼즐,무료", canvasAria="미로 영역"),
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
        "racing": {"gameOver": "撞车了！得分 {score}", "paused": "已暂停", "score": "得分"},
        "sports": {"score": "命中 +1", "miss": "没进！再试一次"},
        "adventure": {"win": "🎉 你用 {steps} 步逃出迷宫！"},
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
        "racing": {"gameOver": "Crash! Score: {score}", "paused": "Paused", "score": "Score"},
        "sports": {"score": "Swoosh! +1", "miss": "Missed! Try again"},
        "adventure": {"win": "🎉 You escaped in {steps} steps!"},
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
        "racing": {"gameOver": "¡Choque! Puntos: {score}", "paused": "En pausa", "score": "Puntos"},
        "sports": {"score": "¡Canasta! +1", "miss": "¡Fallo! Inténtalo"},
        "adventure": {"win": "🎉 ¡Saliste en {steps} pasos!"},
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
        "racing": {"gameOver": "تصادم! النقاط: {score}", "paused": "إيقاف مؤقت", "score": "النقاط"},
        "sports": {"score": "هدف! +1", "miss": "أخطأت! حاول"},
        "adventure": {"win": "🎉 خرجت في {steps} خطوة!"},
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
        "racing": {"gameOver": "Столкновение! Счёт: {score}", "paused": "Пауза", "score": "Счёт"},
        "sports": {"score": "Точно! +1", "miss": "Мимо! Ещё раз"},
        "adventure": {"win": "🎉 Вы вышли за {steps} шагов!"},
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
        "racing": {"gameOver": "衝突！スコア {score}", "paused": "一時停止", "score": "スコア"},
        "sports": {"score": "決まった！+1", "miss": "外れた！もう一度"},
        "adventure": {"win": "🎉 {steps} 歩で脱出！"},
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
        "racing": {"gameOver": "충돌! 점수 {score}", "paused": "일시정지", "score": "점수"},
        "sports": {"score": "득점! +1", "miss": "실패! 다시"},
        "adventure": {"win": "🎉 {steps}걸음으로 탈출!"},
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


# 顶部导航：Home / Games / Categories / New Games / Popular Games
def header(lang, rel, current):
    c = COMMON[lang]
    p = prefix(lang)
    links = [
        '<li><a href="{p}/"{cur}>{home}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "home" else "", home=c["home"]),
        '<li><a href="{p}/#games"{cur}>{navGames}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "games" else "", navGames=c["navGames"]),
        '<li><a href="{p}/categories/"{cur}>{navCategories}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "categories" else "", navCategories=c["navCategories"]),
        '<li><a href="{p}/new-games/"{cur}>{navNew}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "new" else "", navNew=c["navNew"]),
        '<li><a href="{p}/popular-games/"{cur}>{navPopular}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "popular" else "", navPopular=c["navPopular"]),
        '<li><a href="{p}/about/"{cur}>{navAbout}</a></li>'.format(p=p, cur=' aria-current="page"' if current == "about" else "", navAbout=c["navAbout"]),
    ]
    return """<body>
  <header class="site-header">
    <nav class="nav" aria-label="主导航">
      <a class="logo" href="{p}/"><span class="logo-icon" aria-hidden="true">🕹️</span>{siteName}</a>
      <ul class="nav-links">
        {links}
      </ul>
      {switcher}
    </nav>
  </header>""".format(p=p, siteName=c["siteName"], links="\n        ".join(links), switcher=lang_switcher(rel, lang))


# 页脚：站点页链接 + 游戏链接
def footer(lang):
    c = COMMON[lang]
    p = prefix(lang)
    site_links = [
        '<li><a href="%s/">%s</a></li>' % (p, c["home"]),
        '<li><a href="%s/categories/">%s</a></li>' % (p, c["navCategories"]),
        '<li><a href="%s/new-games/">%s</a></li>' % (p, c["navNew"]),
        '<li><a href="%s/popular-games/">%s</a></li>' % (p, c["navPopular"]),
        '<li><a href="%s/about/">%s</a></li>' % (p, c["navAbout"]),
        '<li><a href="%s/contact/">%s</a></li>' % (p, c["navContact"]),
        '<li><a href="%s/privacy/">%s</a></li>' % (p, c["navPrivacy"]),
        '<li><a href="%s/terms/">%s</a></li>' % (p, c["navTerms"]),
        '<li><a href="%s/cookie/">%s</a></li>' % (p, c["navCookie"]),
        '<li><a href="%s/dmca/">%s</a></li>' % (p, c["navDmca"]),
    ]
    game_links = ['<li><a href="%s/games/%s/">%s %s</a></li>' % (p, g["slug"], g["icon"], GDATA[lang][g["slug"]]["name"]) for g in GAMES]
    return """  <footer class="site-footer">
    <div class="footer-cols">
      <div>
        <h3>{siteName}</h3>
        <ul class="footer-links">
          {site_links}
        </ul>
      </div>
      <div>
        <h3>{gamesH3}</h3>
        <ul class="footer-links">
          {game_links}
        </ul>
      </div>
    </div>
    <p>{footer}</p>
  </footer>
</body>
</html>
""".format(siteName=c["siteName"], site_links="\n          ".join(site_links),
           gamesH3=c["navGames"], game_links="\n          ".join(game_links), footer=c["footer"])


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


# 生成游戏卡片网格（用于首页、热门、最新等）
def game_cards(lang, slugs=None):
    c = COMMON[lang]
    p = prefix(lang)
    gs = GAMES if slugs is None else [g for g in GAMES if g["slug"] in slugs]
    cards = []
    for g in gs:
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
    return "\n".join(cards)


def home_page(lang):
    c, h = COMMON[lang], HOME[lang]
    p = prefix(lang)

    stats = "".join("<span>%s</span>" % s for s in h["stats"])

    # 分类卡片
    cat_items = []
    for cat in CATEGORIES:
        name = CATEGORY_NAMES[cat["slug"]][lang]
        cat_items.append(
            '<li class="cat-card"><a href="{p}/categories/{slug}/"><span class="cat-icon" aria-hidden="true">{icon}</span>'
            '<span class="cat-name">{name}</span></a></li>'.format(
                p=p, slug=cat["slug"], icon=cat["icon"], name=name))
    cats_html = "\n              ".join(cat_items)

    # 热门 / 最新 / 流行：本站目前 6 款游戏，按不同顺序呈现以丰富板块
    popular_slugs = ["snake", "2048", "tetris", "minesweeper", "gomoku", "memory"]
    new_slugs = ["memory", "gomoku", "minesweeper", "tetris", "2048", "snake"]
    trending_slugs = ["tetris", "snake", "2048", "gomoku", "memory", "minesweeper"]

    # FAQ
    faq_items = []
    for q, a in h["faq"]:
        faq_items.append("""        <div class="faq-item">
          <h3 class="faq-q">{q}</h3>
          <p class="faq-a">{a}</p>
        </div>""".format(q=q, a=a))
    faq_html = "\n".join(faq_items)

    # Why items
    why_items = []
    for icon_title, desc in h["whyItems"]:
        why_items.append("""          <li class="why-item">
            <span class="why-title">{t}</span>
            <p>{d}</p>
          </li>""".format(t=icon_title, d=desc))
    why_html = "\n".join(why_items)

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
    org_ld = {"@context": "https://schema.org", "@type": "Organization",
              "name": c["siteName"], "url": page_url(lang, "/"),
              "logo": BASE + "/favicon.svg",
              "contactPoint": {"@type": "ContactPoint", "email": "contact@games-hub.cc",
                               "contactType": "customer support"}}

    body = """  <main>
    <section class="hero">
      <span class="hero-badge">{badge}</span>
      <h1>{h1Pre}<span class="hl">{h1Hl}</span>{h1Post}</h1>
      <p>{heroP}</p>
      <div class="hero-stats">{stats}</div>
      <a class="btn hero-cta" href="{p}/#games">{playGames}</a>
    </section>

    <section class="section" id="intro" aria-labelledby="intro-title">
      <h2 class="section-title" id="intro-title">{introH2}</h2>
      <p class="section-desc">{introP}</p>
    </section>

    <section class="section" id="games" aria-labelledby="games-title">
      <h2 class="section-title" id="games-title">{gamesTitle}</h2>
      <p class="section-desc">{gamesDesc}</p>
      <ul class="game-grid">
{cards}
      </ul>
    </section>

    <section class="section" id="categories" aria-labelledby="categories-title">
      <h2 class="section-title" id="categories-title">{categoriesTitle}</h2>
      <p class="section-desc">{categoriesDesc}</p>
      <ul class="cat-grid">
{cats}
      </ul>
    </section>

    <section class="section" id="popular" aria-labelledby="popular-title">
      <h2 class="section-title" id="popular-title">{popularTitle}</h2>
      <p class="section-desc">{popularDesc}</p>
      <ul class="game-grid">
{popular}
      </ul>
    </section>

    <section class="section" id="new" aria-labelledby="new-title">
      <h2 class="section-title" id="new-title">{newTitle}</h2>
      <p class="section-desc">{newDesc}</p>
      <ul class="game-grid">
{new}
      </ul>
    </section>

    <section class="section" id="trending" aria-labelledby="trending-title">
      <h2 class="section-title" id="trending-title">{trendingTitle}</h2>
      <p class="section-desc">{trendingDesc}</p>
      <ul class="game-grid">
{trending}
      </ul>
    </section>

    <section class="section why" id="why" aria-labelledby="why-title">
      <h2 class="section-title" id="why-title">{whyTitle}</h2>
      <p class="section-desc">{whyP}</p>
      <ul class="why-grid">
{why}
      </ul>
    </section>

    <section class="prose" id="about" aria-labelledby="about-title">
      <h2 id="about-title">{aboutH2}</h2>
      <p>{aboutP}</p>
      <h2>{chooseH2}</h2>
      <p>{chooseP}</p>
    </section>

    <section class="section faq" id="faq" aria-labelledby="faq-title">
      <h2 class="section-title" id="faq-title">{faqTitle}</h2>
      <div class="faq-list">
{faq}
      </div>
    </section>
  </main>
""".format(p=p, badge=h["badge"], h1Pre=h["h1Pre"], h1Hl=h["h1Hl"], h1Post=h["h1Post"],
           heroP=h["heroP"], stats=stats, playGames=c["navGames"],
           introH2=h["introH2"], introP=h["introP"],
           gamesTitle=h["gamesTitle"], gamesDesc=h["gamesDesc"], cards=game_cards(lang),
           categoriesTitle=h["categoriesTitle"], categoriesDesc=h["categoriesDesc"], cats=cats_html,
           popularTitle=h["popularTitle"], popularDesc=h["popularDesc"], popular=game_cards(lang, popular_slugs),
           newTitle=h["newTitle"], newDesc=h["newDesc"], new=game_cards(lang, new_slugs),
           trendingTitle=h["trendingTitle"], trendingDesc=h["trendingDesc"], trending=game_cards(lang, trending_slugs),
           whyTitle=h["whyTitle"], whyP=h["whyP"], why=why_html,
           aboutH2=h["aboutH2"], aboutP=h["aboutP"], chooseH2=h["chooseH2"], chooseP=h["chooseP"],
           faqTitle=h["faqTitle"], faq=faq_html)

    return (head(lang, "/", h["metaTitle"], h["metaDesc"], h["metaKeywords"],
                 [website_ld, itemlist_ld, org_ld], is_home=True) + "\n" +
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
          <div class="grid-board board-mine" id="board" role="grid" aria-label="{aria}"></div>
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

    elif slug == "racing":
        hud = hud_item(c["score"], "0", "score")
        canvas = '<canvas id="game-canvas" width="400" height="520" role="img" aria-label="%s"></canvas>' % d["canvasAria"]
        controls = btn("btn-green", "btn-start", c["start"]) + btn("btn-cyan", "btn-pause", c["pause"]) + btn("btn-pink", "btn-restart", c["restart"])
        pad = """<div class="pad" aria-label="Touch controls">
          <span></span><span></span><span></span>
          <button type="button" data-dir="left" aria-label="{left}">◀</button>
          <span></span>
          <button type="button" data-dir="right" aria-label="{right}">▶</button>
        </div>""".format(left=c["left"], right=c["right"])

    elif slug == "sports":
        hud = hud_item(c["score"], "0", "score") + hud_item(c["attempts"], "0", "attempts")
        canvas = '<canvas id="game-canvas" width="420" height="520" role="img" aria-label="%s"></canvas>' % d["canvasAria"]
        controls = btn("btn-green", "btn-start", c["start"]) + btn("btn-pink", "btn-restart", c["restart"])
        pad = ""

    elif slug == "adventure":
        hud = hud_item(c["steps"], "0", "steps")
        canvas = '<canvas id="game-canvas" width="480" height="480" role="img" aria-label="%s"></canvas>' % d["canvasAria"]
        controls = btn("btn-pink", "btn-restart", c["restart"])
        pad = """<div class="pad" aria-label="Touch controls" style="grid-template-columns:repeat(3,56px);grid-template-rows:56px;">
          <span></span><button type="button" data-dir="up" aria-label="{up}">▲</button><span></span>
          <button type="button" data-dir="left" aria-label="{left}">◀</button>
          <button type="button" data-dir="down" aria-label="{down}">▼</button>
          <button type="button" data-dir="right" aria-label="{right}">▶</button>
        </div>""".format(up=c["up"], left=c["left"], down=c["down"], right=c["right"])

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
            header(lang, rel, "games") + "\n" + body + footer(lang))


# ============ 站点页（About / Contact / Privacy / Terms / Cookie / DMCA / Categories / New / Popular） ============

# 站点页 slug -> 对应的 PAGES 字段前缀与类型
SITE_PAGES = {
    "about":   dict(key="about", current="about"),
    "contact": dict(key="contact", current="contact"),
    "privacy": dict(key="privacy", current="privacy"),
    "terms":   dict(key="terms", current="terms"),
    "cookie":  dict(key="cookie", current="cookie"),
    "dmca":    dict(key="dmca", current="dmca"),
    "categories": dict(key="categories", current="categories"),
    "new-games": dict(key="new", current="new"),
    "popular-games": dict(key="popular", current="popular"),
}


def site_page(lang, slug):
    c = COMMON[lang]
    pg = PAGES[lang]
    p = prefix(lang)
    rel = "/%s/" % slug

    title_map = {
        "about": pg["aboutTitle"], "contact": pg["contactTitle"], "privacy": pg["privacyTitle"],
        "terms": pg["termsTitle"], "cookie": pg["cookieTitle"], "dmca": pg["dmcaTitle"],
        "categories": pg["categoriesTitle"], "new-games": pg["newTitle"], "popular-games": pg["popularTitle"],
    }
    desc_map = {
        "about": pg["aboutPa"], "contact": pg["contactP"], "privacy": pg["privacyP"],
        "terms": pg["termsP"], "cookie": pg["cookieP"], "dmca": pg["dmcaP"],
        "categories": pg["categoriesDesc"], "new-games": pg["newDesc"], "popular-games": pg["popularDesc"],
    }
    title = title_map[slug]
    desc = desc_map[slug]

    # 不同页面主体内容
    if slug == "about":
        sections = """
      <h2>{a}</h2>
      <p>{pa}</p>
      <h2>{b}</h2>
      <p>{pb}</p>
      <h2>{c}</h2>
      <p>{pc}</p>
""".format(a=pg["aboutH2a"], pa=pg["aboutPa"], b=pg["aboutH2b"], pb=pg["aboutPb"],
           c=pg["aboutH2c"], pc=pg["aboutPc"])
    elif slug == "contact":
        sections = """
      <p>{p}</p>
      <p class="contact-email">📧 <a href="mailto:{email}">{email}</a></p>
""".format(p=pg["contactP"], email=pg["contactEmail"])
    else:
        # privacy / terms / cookie / dmca：条目列表
        items = pg.get(slug + "Items", [])
        lis = []
        for i_head, i_body in items:
            lis.append("""        <div class="legal-item">
          <h2>{h}</h2>
          <p>{b}</p>
        </div>""".format(h=i_head, b=i_body))
        sections = "\n".join(lis)

    # categories / new-games / popular-games 显示游戏网格
    grid_html = ""
    if slug == "categories":
        cat_items = []
        for cat in CATEGORIES:
            name = CATEGORY_NAMES[cat["slug"]][lang]
            cat_items.append(
                '<li class="cat-card"><a href="{p}/categories/{slug}/"><span class="cat-icon" aria-hidden="true">{icon}</span>'
                '<span class="cat-name">{name}</span></a></li>'.format(
                    p=p, slug=cat["slug"], icon=cat["icon"], name=name))
        grid_html = """
    <section class="section" aria-labelledby="cats-title">
      <ul class="cat-grid">
{cols}
      </ul>
    </section>""".format(cols="\n        ".join(cat_items))
    elif slug in ("new-games", "popular-games"):
        order = (["memory", "gomoku", "minesweeper", "tetris", "2048", "snake"]
                 if slug == "new-games" else ["snake", "2048", "tetris", "minesweeper", "gomoku", "memory"])
        grid_html = """
    <section class="section" aria-labelledby="grid-title">
      <ul class="game-grid">
{grid}
      </ul>
    </section>""".format(grid=game_cards(lang, order))

    jsonlds = [breadcrumb_ld(lang, [(c["home"], "/"), (title, rel)])]

    body = """{breadcrumb}

  <main class="legal-page">
    <h1>{title}</h1>
    <p class="legal-intro">{desc}</p>
{sections}{grid}
  </main>
""".format(breadcrumb=breadcrumb(lang, [(c["home"], p + "/"), (title, None)]),
           title=title, desc=desc, sections=sections, grid=grid_html)

    return (head(lang, rel, "%s | %s" % (title, c["siteName"]), desc, c["siteName"], jsonlds, is_home=False) +
            "\n" + header(lang, rel, SITE_PAGES[slug]["current"]) + "\n" + body + footer(lang))


def category_page(lang, cat_slug):
    """生成单一分类的落地页：/categories/<slug>/"""
    c = COMMON[lang]
    p = prefix(lang)
    cat = next(x for x in CATEGORIES if x["slug"] == cat_slug)
    name = CATEGORY_NAMES[cat_slug][lang]
    sub = CATEGORY_SUB[cat_slug][lang]
    rel = "/categories/%s/" % cat_slug
    icon = cat["icon"]

    game_slugs = CATEGORY_GAMES.get(cat_slug, [])
    if game_slugs:
        grid_html = """
    <section class="section" aria-labelledby="grid-title">
      <ul class="game-grid">
{grid}
      </ul>
    </section>""".format(grid=game_cards(lang, game_slugs))
    else:
        # 暂无专属游戏：显示推荐全部游戏 + 友好提示
        grid_html = """
    <section class="section" aria-labelledby="grid-title">
      <p class="section-desc">{soon}</p>
      <ul class="game-grid">
{grid}
      </ul>
    </section>""".format(soon=c["catSoon"], grid=game_cards(lang, [g["slug"] for g in GAMES]))

    jsonlds = [breadcrumb_ld(lang, [(c["home"], "/"), (c["navCategories"], "/categories/"), (name, rel)])]

    body = """{breadcrumb}

  <main class="legal-page">
    <h1>{icon} {name}</h1>
    <p class="legal-intro">{sub}</p>
{grid}
    <p style="margin-top:28px"><a class="btn" href="{p}/categories/">{allCats}</a></p>
  </main>
""".format(breadcrumb=breadcrumb(lang, [(c["home"], p + "/"), (c["navCategories"], p + "/categories/"), (name, None)]),
           icon=icon, name=name, sub=sub, grid=grid_html,
           p=p, allCats=c["allCategories"])

    return (head(lang, rel, "%s | %s" % (name, c["siteName"]), sub, c["siteName"], jsonlds, is_home=False) +
            "\n" + header(lang, rel, "categories") + "\n" + body + footer(lang))


def write(rel_path, content):
    path = os.path.join(ROOT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_sitemap():
    # 首页 + 游戏页 + 站点页
    site_urls = ["/", "/categories/", "/new-games/", "/popular-games/",
                 "/about/", "/contact/", "/privacy/", "/terms/", "/cookie/", "/dmca/"]
    urls = site_urls + ["/games/%s/" % g["slug"] for g in GAMES]
    urls += ["/categories/%s/" % cat["slug"] for cat in CATEGORIES]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<?xml-stylesheet type="text/xsl" href="sitemap.xsl"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in urls:
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
        write(prefix(lang) + "/index.html", home_page(lang)); count += 1
        for g in GAMES:
            write(prefix(lang) + "/games/%s/index.html" % g["slug"], game_page(lang, g["slug"])); count += 1
        for slug in SITE_PAGES:
            write(prefix(lang) + "/%s/index.html" % slug, site_page(lang, slug)); count += 1
        for cat in CATEGORIES:
            write(prefix(lang) + "/categories/%s/index.html" % cat["slug"], category_page(lang, cat["slug"])); count += 1
    write("/sitemap.xml", build_sitemap())
    print("生成完成：%d 个页面 + sitemap.xml" % count)


if __name__ == "__main__":
    main()
