#!/usr/bin/env python3
"""NimbleMap SEO P0/P1 fixes (2026-10-24). Windows download version left unchanged."""
from __future__ import annotations

import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
IMG = DOCS / "img"

# ---------- 1. Trust copy (align Pro/FAQ with Privacy; soften absolute "never values") ----------
# Prefer Privacy's precise description. Soften Mac-only wording to "computer".
PRO_OLD_NEW = [
    # EN
    (
        "Your data stays on your Mac. Only layer names, fields and extents are sent, never the values.",
        'Your files stay on your computer. Ask sends your question, layer and field names, extents, any active filter (with its values), selected-object values you ask about, and up to five matching values named in the question — never files, shapes, coordinates, or paths. See <a href="privacy.html">Privacy</a>.',
    ),
    # DE
    (
        "Ihre Daten bleiben auf Ihrem Mac. Gesendet werden nur Layernamen, Felder und Ausdehnungen, niemals die Werte.",
        'Ihre Dateien bleiben auf Ihrem Computer. Ask sendet Ihre Frage, Layer- und Feldnamen, Ausdehnungen, aktive Filter (inkl. Werte), relevante Werte des ausgewählten Objekts und bis zu fünf passende Werte aus der Frage — nie Dateien, Formen, Koordinaten oder Pfade. Siehe <a href="../privacy.html">Privacy</a>.',
    ),
    # ES
    (
        "Tus datos se quedan en tu Mac. Solo se envían los nombres de las capas, los campos y las extensiones, nunca los valores.",
        'Tus archivos se quedan en tu ordenador. Ask envía tu pregunta, nombres de capas y campos, extensiones, filtros activos (con sus valores), valores del objeto seleccionado y hasta cinco coincidencias nombradas en la pregunta — nunca archivos, formas, coordenadas ni rutas. Ver <a href="../privacy.html">Privacy</a>.',
    ),
    # FR
    (
        "Vos données restent sur votre Mac. Seuls les noms des couches, les champs et les emprises sont envoyés, jamais les valeurs.",
        'Vos fichiers restent sur votre ordinateur. Ask envoie votre question, les noms de couches et de champs, les emprises, les filtres actifs (avec leurs valeurs), les valeurs de l’objet sélectionné et jusqu’à cinq valeurs nommées dans la question — jamais les fichiers, formes, coordonnées ou chemins. Voir <a href="../privacy.html">Privacy</a>.',
    ),
    # IT
    (
        "I tuoi dati restano sul Mac. Vengono inviati solo i nomi dei layer, i campi e le estensioni, mai i valori.",
        'I tuoi file restano sul computer. Ask invia la domanda, nomi di layer e campi, estensioni, filtri attivi (con i valori), valori dell’oggetto selezionato e fino a cinque corrispondenze nominate nella domanda — mai file, forme, coordinate o percorsi. Vedi <a href="../privacy.html">Privacy</a>.',
    ),
    # NL
    (
        "Uw gegevens blijven op uw Mac. Alleen namen van kaartlagen, velden en bereiken worden verstuurd, nooit de waarden.",
        'Uw bestanden blijven op uw computer. Ask stuurt uw vraag, laagnamen en veldnamen, bereiken, actieve filters (met waarden), waarden van het geselecteerde object en tot vijf treffers uit de vraag — nooit bestanden, vormen, coördinaten of paden. Zie <a href="../privacy.html">Privacy</a>.',
    ),
    # PT-BR
    (
        "Seus dados ficam no seu Mac. Só os nomes das camadas, os campos e as extensões são enviados, nunca os valores.",
        'Seus arquivos ficam no seu computador. O Ask envia a pergunta, nomes de camadas e campos, extensões, filtros ativos (com valores), valores do objeto selecionado e até cinco correspondências nomeadas na pergunta — nunca arquivos, formas, coordenadas ou caminhos. Ver <a href="../privacy.html">Privacy</a>.',
    ),
    # RU
    (
        "Ваши данные остаются на вашем Mac. Отправляются только названия слоёв, поля и охват — но никогда не значения.",
        'Ваши файлы остаются на компьютере. Ask отправляет вопрос, имена слоёв и полей, охват, активные фильтры (с значениями), значения выбранного объекта и до пяти совпадений из вопроса — никогда файлы, формы, координаты или пути. См. <a href="../privacy.html">Privacy</a>.',
    ),
    # ZH
    (
        "数据留在你的 Mac 上：只发送图层名称、字段和范围，绝不发送数据值",
        '文件留在你的电脑上。提问时会发送你的问题、图层与字段名、范围、当前筛选（含其取值）、所选对象的相关取值，以及问题中点到的最多五个匹配值——不会发送文件本身、几何形状、坐标或路径。详见 <a href="../privacy.html">Privacy</a>',
    ),
    # JA
    (
        "データは Mac の中に残ります。送信されるのはレイヤー名、フィールド、範囲だけで、値は決して送られません。",
        'ファイルはコンピューター内に残ります。Ask は質問、レイヤー名とフィールド名、範囲、有効なフィルター（その値を含む）、選択オブジェクトの関連値、質問で指名された最大5件の一致値を送ります。ファイル本体・形状・座標・パスは送りません。詳細は <a href="../privacy.html">Privacy</a>。',
    ),
    # KO
    (
        "데이터는 Mac에 남습니다. 레이어 이름, 필드, 범위만 전송되며 값은 절대 보내지 않습니다.",
        '파일은 컴퓨터에 남습니다. Ask는 질문, 레이어·필드 이름, 범위, 활성 필터(값 포함), 선택한 객체의 관련 값, 질문에 나온 최대 5개 일치 값을 보냅니다. 파일 자체·도형·좌표·경로는 보내지 않습니다. 자세한 내용은 <a href="../privacy.html">Privacy</a>.',
    ),
]

# EN root pro uses privacy.html (same dir); locales use ../privacy.html — already in replacements above for locales.
# Fix EN privacy href if we used privacy.html in EN string — yes we did.

DL_OLD_NEW = [
    (
        "Not in the free app: everything is read, analysed and drawn on your computer, and it works offline. Basemap tiles are downloaded when you're online, but your data is never sent. In Pro, the Ask box sends the assistant your layer names, field names and extents so it can understand the question, never the values.",
        'Not in the free app: everything is read, analysed and drawn on your computer, and it works offline. Basemap tiles are downloaded when you\'re online, but your map files are never uploaded. In Pro, Ask sends your question, layer and field names, extents, any active filter (with its values), selected-object values you ask about, and up to five matching values named in the question — never files, shapes, coordinates, or paths. See <a href="privacy.html">Privacy</a>.',
    ),
    (
        "In der kostenlosen App nicht: Alles wird auf Ihrem Mac gelesen, analysiert und gezeichnet, und sie funktioniert offline. Kacheln der Hintergrundkarte werden geladen, wenn Sie online sind, aber Ihre Daten werden nie gesendet. In Pro schickt das Fragefeld dem Assistenten die Namen Ihrer Layer, die Feldnamen und die Ausdehnungen, damit er die Frage versteht – niemals die Werte.",
        'In der kostenlosen App nicht: Alles wird auf Ihrem Computer gelesen, analysiert und gezeichnet, und sie funktioniert offline. Kacheln der Hintergrundkarte werden geladen, wenn Sie online sind, aber Ihre Kartendateien werden nie hochgeladen. In Pro schickt Ask Ihre Frage, Layer- und Feldnamen, Ausdehnungen, aktive Filter (inkl. Werte), relevante Werte des ausgewählten Objekts und bis zu fünf passende Werte aus der Frage — nie Dateien, Formen, Koordinaten oder Pfade. Siehe <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "En la aplicación gratuita, no: todo se lee, se analiza y se dibuja en tu Mac, y funciona sin conexión. Las teselas del mapa base se descargan cuando estás conectado, pero tus datos nunca se envían. En Pro, el cuadro de preguntas envía al asistente los nombres de tus capas, los nombres de los campos y sus extensiones para que entienda la pregunta, nunca los valores.",
        'En la aplicación gratuita, no: todo se lee, se analiza y se dibuja en tu ordenador, y funciona sin conexión. Las teselas del mapa base se descargan cuando estás conectado, pero tus archivos de mapa no se suben. En Pro, Ask envía tu pregunta, nombres de capas y campos, extensiones, filtros activos (con valores), valores del objeto seleccionado y hasta cinco coincidencias de la pregunta — nunca archivos, formas, coordenadas ni rutas. Ver <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "Pas dans l’app gratuite : tout est lu, analysé et dessiné sur votre Mac, et elle fonctionne hors ligne. Les tuiles du fond de carte sont téléchargées quand vous êtes en ligne, mais vos données ne sont jamais envoyées. Dans Pro, la zone de question transmet à l’assistant les noms de vos couches, les noms des champs et les emprises pour qu’il comprenne la question, jamais les valeurs.",
        'Pas dans l’app gratuite : tout est lu, analysé et dessiné sur votre ordinateur, et elle fonctionne hors ligne. Les tuiles du fond de carte sont téléchargées quand vous êtes en ligne, mais vos fichiers carte ne sont pas téléversés. Dans Pro, Ask envoie votre question, les noms de couches et de champs, les emprises, les filtres actifs (avec leurs valeurs), les valeurs de l’objet sélectionné et jusqu’à cinq valeurs nommées — jamais fichiers, formes, coordonnées ou chemins. Voir <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "Non nell'app gratuita: tutto viene letto, analizzato e disegnato sul tuo Mac, e funziona offline. Le tessere della mappa di base vengono scaricate quando sei online, ma i tuoi dati non vengono mai inviati. In Pro, la casella Chiedi invia all'assistente i nomi dei layer, i nomi dei campi e le estensioni, così può capire la domanda, ma mai i valori.",
        'Non nell\'app gratuita: tutto viene letto, analizzato e disegnato sul tuo computer, e funziona offline. Le tessere della mappa di base vengono scaricate quando sei online, ma i file mappa non vengono caricati. In Pro, Ask invia la domanda, nomi di layer e campi, estensioni, filtri attivi (con valori), valori dell\'oggetto selezionato e fino a cinque corrispondenze — mai file, forme, coordinate o percorsi. Vedi <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "Niet in de gratis app: alles wordt op uw Mac gelezen, geanalyseerd en getekend, en het werkt offline. Tegels van de achtergrondkaart worden gedownload als u online bent, maar uw gegevens worden nooit verstuurd. In Pro stuurt het vraagvak de assistent de namen van uw kaartlagen, de veldnamen en het bereik, zodat hij de vraag begrijpt, maar nooit de waarden.",
        'Niet in de gratis app: alles wordt op uw computer gelezen, geanalyseerd en getekend, en het werkt offline. Tegels van de achtergrondkaart worden gedownload als u online bent, maar uw kaartbestanden worden niet geüpload. In Pro stuurt Ask uw vraag, laagnamen en veldnamen, bereiken, actieve filters (met waarden), waarden van het geselecteerde object en tot vijf treffers — nooit bestanden, vormen, coördinaten of paden. Zie <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "No app gratuito, não: tudo é lido, analisado e desenhado no seu Mac, e ele funciona offline. Os blocos do mapa base são baixados quando você está on-line, mas seus dados nunca são enviados. No Pro, a caixa Ask envia ao assistente os nomes das camadas, os nomes dos campos e as extensões, para que ele entenda a pergunta, nunca os valores.",
        'No app gratuito, não: tudo é lido, analisado e desenhado no seu computador, e ele funciona offline. Os blocos do mapa base são baixados quando você está on-line, mas seus arquivos de mapa não são enviados. No Pro, o Ask envia a pergunta, nomes de camadas e campos, extensões, filtros ativos (com valores), valores do objeto selecionado e até cinco correspondências — nunca arquivos, formas, coordenadas ou caminhos. Ver <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "В бесплатной версии — нет: всё читается, анализируется и рисуется на вашем Mac, и приложение работает офлайн. Когда вы в сети, скачиваются фрагменты подложки, но ваши данные никуда не отправляются. В Pro поле Ask отправляет помощнику названия слоёв, названия полей и охват, чтобы он понял вопрос, — но никогда не сами значения.",
        'В бесплатной версии — нет: всё читается, анализируется и рисуется на вашем компьютере, и приложение работает офлайн. Когда вы в сети, скачиваются фрагменты подложки, но ваши файлы карты не загружаются. В Pro Ask отправляет вопрос, имена слоёв и полей, охват, активные фильтры (с значениями), значения выбранного объекта и до пяти совпадений — никогда файлы, формы, координаты или пути. См. <a href="../privacy.html">Privacy</a>.',
    ),
    (
        "免费版不会：所有文件都在你的 Mac 上读取、分析和绘制，断网也能用。联网时会下载底图瓦片，但你的数据从不发送出去。Pro 版的提问框会把图层名、字段名和范围发给助手，以便理解你的问题，但从不发送具体数值。",
        '免费版不会：所有文件都在你的电脑上读取、分析和绘制，断网也能用。联网时会下载底图瓦片，但地图文件不会上传。Pro 的提问会发送你的问题、图层与字段名、范围、当前筛选（含取值）、所选对象的相关取值，以及问题中点到的最多五个匹配值——不会发送文件本身、几何、坐标或路径。详见 <a href="../privacy.html">Privacy</a>。',
    ),
    (
        "無料アプリではアップロードされません。すべてのデータは Mac で読み取り・分析・描画され、オフラインでも動作します。オンライン時に背景地図タイルをダウンロードしますが、データ自体は絶対に送信されません。Pro の質問ボックスは質問を理解できるようレイヤー名、フィールド名、範囲をアシスタントに送りますが、値は絶対に送りません。",
        '無料アプリでは地図ファイルはアップロードされません。すべてコンピューター上で読み取り・分析・描画され、オフラインでも動作します。オンライン時に背景地図タイルを取得します。Pro の Ask は質問、レイヤー名・フィールド名、範囲、有効フィルター（値含む）、選択オブジェクトの関連値、質問で指名された最大5件を送ります。ファイル本体・形状・座標・パスは送りません。詳細は <a href="../privacy.html">Privacy</a>。',
    ),
    (
        "무료 앱에서는 업로드되지 않습니다. 모든 데이터는 Mac에서 읽고 분석하고 그리며, 오프라인에서도 작동합니다. 온라인 상태일 때 배경 지도 타일을 내려받지만, 내 데이터는 절대 전송되지 않습니다. Pro의 질문 상자는 질문을 이해할 수 있도록 레이어 이름, 필드 이름, 범위를 어시스턴트에 보내지만, 값은 절대 보내지 않습니다.",
        '무료 앱에서는 지도 파일이 업로드되지 않습니다. 모든 작업은 컴퓨터에서 읽고 분석하고 그리며, 오프라인에서도 작동합니다. 온라인일 때 배경 지도 타일을 받습니다. Pro의 Ask는 질문, 레이어·필드 이름, 범위, 활성 필터(값 포함), 선택한 객체의 관련 값, 질문에 나온 최대 5개 일치 값을 보냅니다. 파일 자체·도형·좌표·경로는 보내지 않습니다. 자세한 내용은 <a href="../privacy.html">Privacy</a>.',
    ),
]


DL_OLD_NEW.append((
    '無料版ではありません。すべて Mac の中で読み込み・分析・描画され、オフラインでも動作します。オンライン時には背景地図のタイルをダウンロードしますが、あなたのデータが送信されることはありません。Pro の質問ボックスでは、質問を理解するためにレイヤー名、フィールド名、範囲をアシスタントに送りますが、値そのものは決して送りません。',
    '無料版ではありません。すべてコンピューター上で読み込み・分析・描画され、オフラインでも動作します。オンライン時には背景地図のタイルを取得しますが、地図ファイルはアップロードされません。Pro の Ask は質問、レイヤー名・フィールド名、範囲、有効フィルター（値含む）、選択オブジェクトの関連値、質問で指名された最大5件を送ります。ファイル本体・形状・座標・パスは送りません。詳細は <a href="../privacy.html">Privacy</a>。',
))


def apply_replacements(pairs: list[tuple[str, str]]) -> list[str]:
    notes = []
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
                notes.append(f"{path.relative_to(ROOT)}: replaced trust snippet")
        if text != orig:
            path.write_text(text, encoding="utf-8")
    return notes


# ---------- 2. Footer Privacy + Terms ----------
# Insert after About link in foot-links. Locale pages need ../privacy.html and ../terms.html.
FOOT_EN = re.compile(
    r'(<p class="foot-links">)(.*?)(</p>)',
    re.DOTALL,
)

def add_privacy_terms_to_footers() -> int:
    n = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if "foot-links" not in text:
            continue
        if "privacy.html" in text and 'foot-links">' in text:
            # may already have privacy in footer
            m = FOOT_EN.search(text)
            if m and "privacy.html" in m.group(2):
                continue
        # Determine relative prefix for privacy/terms (EN-only pages)
        rel = path.relative_to(DOCS)
        prefix = "../" if len(rel.parts) > 1 else ""
        privacy = f'{prefix}privacy.html'
        terms = f'{prefix}terms.html'

        def repl(m):
            inner = m.group(2)
            if "privacy.html" in inner:
                return m.group(0)
            # Append before closing
            addition = f' · <a href="{privacy}">Privacy</a> · <a href="{terms}">Terms</a>'
            # Prefer inserting after About if present
            if "About</a>" in inner or "关于作者</a>" in inner:
                inner2 = re.sub(
                    r'(<a href="[^"]*about\.html"[^>]*>[^<]*</a>)',
                    r'\1' + addition,
                    inner,
                    count=1,
                )
                if inner2 != inner:
                    return m.group(1) + inner2 + m.group(3)
            return m.group(1) + inner + addition + m.group(3)

        new_text, count = FOOT_EN.subn(repl, text, count=1)
        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            n += 1
    return n


# ---------- 3. Canonical homepage links (index.html → ./ or ../ or lang/) ----------
INDEX_HREF = re.compile(
    r'href="((?:\.\./)*(?:[a-z]{2}(?:-[a-z]+)?/)?)index\.html(#[^"]*)?"'
)

def fix_index_html_links() -> int:
    n = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")

        def repl(m):
            prefix = m.group(1) or ""
            frag = m.group(2) or ""
            if prefix == "":
                # same-directory homepage → ./
                return f'href="./{frag}"' if frag else 'href="./"'
            # prefix like zh/ or ../zh/ or ../
            if prefix.endswith("/"):
                return f'href="{prefix}{frag}"' if frag else f'href="{prefix}"'
            return f'href="{prefix}/{frag}"' if frag else f'href="{prefix}/"'

        new_text, c = INDEX_HREF.subn(repl, text)
        # Also fix bare "../index.html" already covered. Fix "href=\"index.html\"" done.
        if c:
            path.write_text(new_text, encoding="utf-8")
            n += c
    return n


# ---------- 4. Schema: WebSite + Person; link SoftwareApplication ----------
PERSON_JSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": "https://nimblemap.com/about.html#person",
    "name": "Kangning Huang",
    "alternateName": "Ken Huang",
    "url": "https://kangning-huang.com/",
    "jobTitle": "Assistant Professor of Environmental Studies",
    "affiliation": {
        "@type": "CollegeOrUniversity",
        "name": "NYU Shanghai",
        "url": "https://shanghai.nyu.edu/",
    },
    "sameAs": [
        "https://kangning-huang.com/",
        "https://github.com/kangning-huang",
    ],
}

WEBSITE_JSON = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://nimblemap.com/#website",
    "name": "NimbleMap",
    "alternateName": "凌波微图",
    "url": "https://nimblemap.com/",
    "inLanguage": ["en", "zh-Hans", "de", "es", "fr", "it", "nl", "pt-BR", "ru", "ja", "ko"],
    "publisher": {"@id": "https://nimblemap.com/about.html#person"},
}

def update_software_block(text: str, page_url: str, in_lang: str | None = None) -> str:
    """Rewrite SoftwareApplication publisher to @id ref; add sameAs, author."""
    pattern = re.compile(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        re.DOTALL,
    )

    def repl(m):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            return m.group(0)
        if data.get("@type") != "SoftwareApplication":
            return m.group(0)
        data["@id"] = "https://nimblemap.com/#app"
        data["sameAs"] = "https://github.com/kangning-huang/NimbleMap"
        data["author"] = {"@id": "https://nimblemap.com/about.html#person"}
        data["publisher"] = {"@id": "https://nimblemap.com/about.html#person"}
        # Do NOT touch softwareVersion or downloadUrl / Windows links
        out = json.dumps(data, ensure_ascii=False, indent=2)
        return f'<script type="application/ld+json">\n{out}\n</script>'

    return pattern.sub(repl, text, count=1)


def inject_schema() -> None:
    # Homepage EN: add WebSite + keep SoftwareApplication updated; also add Person once on about
    home = DOCS / "index.html"
    text = home.read_text(encoding="utf-8")
    text = update_software_block(text, "https://nimblemap.com/")
    if '"@type": "WebSite"' not in text and '"@type":"WebSite"' not in text:
        website = json.dumps(WEBSITE_JSON, ensure_ascii=False, indent=2)
        person = json.dumps(PERSON_JSON, ensure_ascii=False, indent=2)
        # Insert before </head>
        extra = (
            f'<script type="application/ld+json">\n{website}\n</script>\n'
            f'<script type="application/ld+json">\n{person}\n</script>\n'
        )
        text = text.replace("</head>", extra + "</head>", 1)
    home.write_text(text, encoding="utf-8")

    about = DOCS / "about.html"
    at = about.read_text(encoding="utf-8")
    if "about.html#person" not in at:
        person = json.dumps(PERSON_JSON, ensure_ascii=False, indent=2)
        at = at.replace(
            "</head>",
            f'<script type="application/ld+json">\n{person}\n</script>\n</head>',
            1,
        )
        about.write_text(at, encoding="utf-8")

    # Other pages with SoftwareApplication (download + locale homes/downloads)
    for path in DOCS.rglob("*.html"):
        if path.name not in {"index.html", "download.html"} and not path.name.endswith("download.html"):
            # only index and download carry SoftwareApplication
            pass
        t = path.read_text(encoding="utf-8")
        if "SoftwareApplication" not in t:
            continue
        if path == home:
            continue
        nt = update_software_block(t, "")
        if nt != t:
            path.write_text(nt, encoding="utf-8")


# ---------- 5. Images: WebP + srcset + fetchpriority on homepage hero ----------
HOMEPAGE_IMGS = [
    "open-storms.jpg",
    "open-earthquakes.jpg",
    "open-heatwave.jpg",
    "open-relief.jpg",
    "open-volcanoes.jpg",
    "open-click.jpg",
    "open-search.jpg",
    "open-time.jpg",
    "open-zoom.jpg",
    "typhoons-card.jpg",
    "walls-satellite.jpg",
    "pro-ask.jpg",
    "points-earthquakes.jpg",
    "areas-countries.jpg",
    "welcome.jpg",
    "hero-poster.jpg",
    "hero-poster-zh.jpg",
]

def make_webp() -> list[str]:
    made = []
    for name in HOMEPAGE_IMGS:
        src = IMG / name
        if not src.exists():
            continue
        dest = IMG / (src.stem + ".webp")
        if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
            made.append(str(dest.name) + " (skip)")
            continue
        im = Image.open(src)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        im.save(dest, "WEBP", quality=82, method=6)
        # also a 800w variant for srcset
        w800 = IMG / (src.stem + "-800.webp")
        im2 = im.copy()
        im2.thumbnail((800, 800 * im.height // im.width))
        im2.save(w800, "WEBP", quality=80, method=6)
        made.append(dest.name)
    return made


IMG_TAG = re.compile(
    r'<img(?P<pre>[^>]*?)\ssrc="(?P<src>img/([^"/]+)\.(jpg|jpeg|png))"(?P<post>[^>]*)>',
    re.IGNORECASE,
)

def upgrade_homepage_images(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    count = 0

    def repl(m):
        nonlocal count
        src = m.group("src")
        stem_ext = m.group(3)  # wrong - fix
        return m.group(0)

    # More careful: only img/ jpeg/png that have webp siblings used on homepage
    def repl2(m):
        nonlocal count
        full = m.group(0)
        src = m.group("src")
        # extract filename
        fname = src.split("/")[-1]
        stem = Path(fname).stem
        webp = IMG / f"{stem}.webp"
        webp800 = IMG / f"{stem}-800.webp"
        if not webp.exists():
            return full
        # parse attributes roughly
        attrs = full[4:-1]  # inside img
        # Build picture
        alt_m = re.search(r'\salt="([^"]*)"', full)
        alt = alt_m.group(1) if alt_m else ""
        wh = ""
        wm = re.search(r'\swidth="(\d+)"', full)
        hm = re.search(r'\sheight="(\d+)"', full)
        if wm and hm:
            wh = f' width="{wm.group(1)}" height="{hm.group(1)}"'
        loading = ""
        lm = re.search(r'\sloading="([^"]+)"', full)
        if lm:
            loading = f' loading="{lm.group(1)}"'
        cls = ""
        cm = re.search(r'\sclass="([^"]+)"', full)
        if cm:
            cls = f' class="{cm.group(1)}"'
        aria = ""
        am = re.search(r'\saria-hidden="([^"]+)"', full)
        if am:
            aria = f' aria-hidden="{am.group(1)}"'
        # hero first slide: fetchpriority
        fp = ""
        if stem == "open-storms" and 'class="slide is-on"' in full:
            fp = ' fetchpriority="high"'
            # remove loading=lazy if any
            loading = ""
        srcset = f'img/{stem}-800.webp 800w, img/{stem}.webp 1600w' if webp800.exists() else f'img/{stem}.webp'
        sizes = '(max-width: 800px) 100vw, 800px'
        count += 1
        return (
            f'<picture>'
            f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img{cls} src="{src}" alt="{alt}"{wh}{loading}{fp}{aria} decoding="async">'
            f'</picture>'
        )

    new_text = IMG_TAG.sub(repl2, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return count


# ---------- 6. Meta descriptions over 160 chars; weak titles ----------
TITLE_OVERRIDES = {
    # path relative to docs → (title, description optional)
    "help.html": ("NimbleMap Help: open map files and explore them", None),
    "glossary.html": ("NimbleMap Glossary: map words in plain English", None),
    "about.html": ("About NimbleMap and Kangning Huang", None),
}

def shorten(s: str, limit: int = 155) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= limit:
        return s
    cut = s[: limit - 1]
    # prefer sentence end
    for sep in [". ", "; ", ", ", " — ", " - ", " "]:
        i = cut.rfind(sep)
        if i >= 80:
            cut = cut[: i + (1 if sep.startswith(".") else 0)]
            break
    return cut.rstrip(" ,;:-") + "…"


def fix_metas() -> tuple[int, int]:
    desc_n = title_n = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        orig = text
        rel = str(path.relative_to(DOCS))

        def desc_repl(m):
            nonlocal desc_n
            content = m.group(1)
            if len(content) <= 160:
                return m.group(0)
            desc_n += 1
            return m.group(0).replace(content, shorten(content), 1)

        text = re.sub(
            r'<meta name="description" content="([^"]*)">',
            desc_repl,
            text,
            count=1,
        )
        # also og:description if long
        def og_repl(m):
            content = m.group(1)
            if len(content) <= 160:
                return m.group(0)
            return m.group(0).replace(content, shorten(content), 1)

        text = re.sub(
            r'<meta property="og:description" content="([^"]*)">',
            og_repl,
            text,
            count=1,
        )

        if rel in TITLE_OVERRIDES:
            new_title, _ = TITLE_OVERRIDES[rel]
            text2, c = re.subn(
                r"<title>[^<]*</title>",
                f"<title>{new_title}</title>",
                text,
                count=1,
            )
            if c:
                text = text2
                title_n += 1
                text = re.sub(
                    r'<meta property="og:title" content="[^"]*">',
                    f'<meta property="og:title" content="{new_title}">',
                    text,
                    count=1,
                )

        if text != orig:
            path.write_text(text, encoding="utf-8")
    return desc_n, title_n


# ---------- 7. llms.txt ----------
LLMS = """# NimbleMap (凌波微图)

> Free desktop app that opens downloaded map data as a map in seconds.
> Formats: Shapefile, GeoPackage, NetCDF, GeoTIFF, GPX, KML, CSV with coordinates.
> Platforms: Mac (Apple silicon, macOS 13+) and Windows 10/11 (x64). No GIS training, no setup.
> Chinese name: 凌波微图.
> Also available as a no-install browser try at https://nimblemap.app/ (files still stay on your computer).

Primary URL: https://nimblemap.com/
Canonical repo / releases: https://github.com/kangning-huang/NimbleMap

## Key pages

- [Home (EN)](https://nimblemap.com/)
- [Home (ZH 简体中文 / 凌波微图)](https://nimblemap.com/zh/)
- [Download](https://nimblemap.com/download.html)
- [Data sources](https://nimblemap.com/data.html)
- [Help](https://nimblemap.com/help.html)
- [Glossary](https://nimblemap.com/glossary.html)
- [Pro / Ask](https://nimblemap.com/pro.html)
- [About](https://nimblemap.com/about.html)
- [Privacy](https://nimblemap.com/privacy.html)
- [Terms](https://nimblemap.com/terms.html)
- [Workflow: typhoons](https://nimblemap.com/workflow-typhoons.html)
- [Workflow: 2023 heatwave](https://nimblemap.com/workflow-heatwave.html)
- [Workflow: walled cities](https://nimblemap.com/workflow-walled-cities.html)
- [Sitemap](https://nimblemap.com/sitemap.xml)
- [Changelog](https://github.com/kangning-huang/NimbleMap/blob/main/CHANGELOG.md)

## Languages

English (default), 简体中文 (zh), Deutsch (de), Español (es), Français (fr), Italiano (it), Nederlands (nl), Português Brasil (pt-br), Русский (ru), 日本語 (ja), 한국어 (ko).
Each locale lives under https://nimblemap.com/<lang>/ with hreflang on the pages.

## Downloads

- [Mac DMG (latest)](https://github.com/kangning-huang/NimbleMap/releases/latest/download/NimbleMap-macos-arm64.dmg)
- Windows x64 installer: site currently links the tagged `v0.7.1` Windows build (`NimbleMap-windows-x64-setup.exe`); a newer Windows build is deferred until the next Windows release (schema/Mac may show 0.7.4).

## Product facts for agents

- Alternate name: 凌波微图
- Application category: desktop map / GIS viewer utilities
- Free core; NimbleMap Pro is the in-app Ask box (sign-in, free with an account)
- Native desktop app for Mac and Windows; optional browser try at nimblemap.app (not a hosted web GIS — processing stays on the device)
- When Ask is used, Privacy describes exactly what metadata and limited values are sent; map files, shapes, coordinates and paths are not uploaded
"""


def write_llms() -> None:
    (DOCS / "llms.txt").write_text(LLMS, encoding="utf-8")


# ---------- 8. Sitemap lastmod → today for touched content pages (optional quick) ----------
def bump_sitemap_lastmod(date: str = "2026-10-24") -> int:
    path = DOCS / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(r"<lastmod>2026-10-23</lastmod>", f"<lastmod>{date}</lastmod>", text)
    if n:
        path.write_text(new, encoding="utf-8")
    return n


# ---------- 9. BreadcrumbList on a few English inner pages (optional) ----------
BREADCRUMBS = {
    "help.html": [("Home", "https://nimblemap.com/"), ("Help", "https://nimblemap.com/help.html")],
    "glossary.html": [("Home", "https://nimblemap.com/"), ("Glossary", "https://nimblemap.com/glossary.html")],
    "data.html": [("Home", "https://nimblemap.com/"), ("Data", "https://nimblemap.com/data.html")],
    "pro.html": [("Home", "https://nimblemap.com/"), ("Pro", "https://nimblemap.com/pro.html")],
    "download.html": [("Home", "https://nimblemap.com/"), ("Download", "https://nimblemap.com/download.html")],
    "about.html": [("Home", "https://nimblemap.com/"), ("About", "https://nimblemap.com/about.html")],
    "workflow-typhoons.html": [
        ("Home", "https://nimblemap.com/"),
        ("Help", "https://nimblemap.com/help.html"),
        ("Typhoons workflow", "https://nimblemap.com/workflow-typhoons.html"),
    ],
    "workflow-heatwave.html": [
        ("Home", "https://nimblemap.com/"),
        ("Help", "https://nimblemap.com/help.html"),
        ("Heatwave workflow", "https://nimblemap.com/workflow-heatwave.html"),
    ],
    "workflow-walled-cities.html": [
        ("Home", "https://nimblemap.com/"),
        ("Help", "https://nimblemap.com/help.html"),
        ("Walled cities workflow", "https://nimblemap.com/workflow-walled-cities.html"),
    ],
}


def add_breadcrumbs() -> int:
    n = 0
    for rel, crumbs in BREADCRUMBS.items():
        path = DOCS / rel
        text = path.read_text(encoding="utf-8")
        if "BreadcrumbList" in text:
            continue
        items = []
        for i, (name, url) in enumerate(crumbs, 1):
            items.append(
                {
                    "@type": "ListItem",
                    "position": i,
                    "name": name,
                    "item": url,
                }
            )
        block = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items,
        }
        script = (
            f'<script type="application/ld+json">\n{json.dumps(block, ensure_ascii=False, indent=2)}\n</script>\n'
        )
        text = text.replace("</head>", script + "</head>", 1)
        path.write_text(text, encoding="utf-8")
        n += 1
    return n


def main() -> None:
    print("=== trust copy ===")
    notes = apply_replacements(PRO_OLD_NEW + DL_OLD_NEW)
    print(f"replacements hit files: {len(notes)}")
    for x in notes[:30]:
        print(" ", x)

    print("=== footers ===")
    print("footers updated:", add_privacy_terms_to_footers())

    print("=== index.html links ===")
    print("link replacements:", fix_index_html_links())

    print("=== schema ===")
    inject_schema()
    print("schema injected")

    print("=== images ===")
    print("webp:", make_webp())
    # Upgrade EN homepage and ZH homepage (main LCP pages)
    for p in [DOCS / "index.html", DOCS / "zh" / "index.html"]:
        if p.exists():
            c = upgrade_homepage_images(p)
            print(f"picture tags on {p.relative_to(ROOT)}: {c}")

    print("=== metas ===")
    d, t = fix_metas()
    print(f"shortened descriptions: {d}, titles: {t}")

    print("=== llms.txt ===")
    write_llms()

    print("=== sitemap lastmod ===")
    print("bumped:", bump_sitemap_lastmod())

    print("=== breadcrumbs ===")
    print("pages:", add_breadcrumbs())

    print("DONE")


if __name__ == "__main__":
    main()
