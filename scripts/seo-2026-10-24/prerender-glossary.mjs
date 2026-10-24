#!/usr/bin/env node
/**
 * Pre-render glossary <dl> entries into static HTML for all locales.
 * Keeps glossary.js search/filter as progressive enhancement.
 */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');
const DOCS = path.join(ROOT, 'docs');
const ASSETS = path.join(DOCS, 'assets');

const LOCALES = [
  { code: 'en', dir: '', htmlLang: 'en', dataExtra: null },
  { code: 'zh', dir: 'zh', htmlLang: 'zh-Hans', dataExtra: null }, // uses zh fields in glossary-data.js
  { code: 'de', dir: 'de', htmlLang: 'de', dataExtra: 'glossary-de.js' },
  { code: 'es', dir: 'es', htmlLang: 'es', dataExtra: 'glossary-es.js' },
  { code: 'fr', dir: 'fr', htmlLang: 'fr', dataExtra: 'glossary-fr.js' },
  { code: 'it', dir: 'it', htmlLang: 'it', dataExtra: 'glossary-it.js' },
  { code: 'nl', dir: 'nl', htmlLang: 'nl', dataExtra: 'glossary-nl.js' },
  { code: 'pt-br', dir: 'pt-br', htmlLang: 'pt-BR', dataExtra: 'glossary-pt-br.js' },
  { code: 'ru', dir: 'ru', htmlLang: 'ru', dataExtra: 'glossary-ru.js' },
  { code: 'ja', dir: 'ja', htmlLang: 'ja', dataExtra: 'glossary-ja.js' },
  { code: 'ko', dir: 'ko', htmlLang: 'ko', dataExtra: 'glossary-ko.js' },
];

function loadSandbox(extraFile) {
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(path.join(ASSETS, 'glossary-data.js'), 'utf8'), sandbox);
  if (extraFile) {
    vm.runInContext(fs.readFileSync(path.join(ASSETS, extraFile), 'utf8'), sandbox);
  }
  return sandbox;
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function buildEntries(locale) {
  const sandbox = loadSandbox(locale.dataExtra);
  const data = JSON.parse(JSON.stringify(sandbox.window.LM_GLOSSARY));
  const L = sandbox.window.LM_GLOSSARY_L10N || null;
  const lang = locale.htmlLang;
  const zh = !L && lang.indexOf('zh') === 0;

  const T = L
    ? L.ui
    : zh
      ? { where: '在应用里', see: '在教程中查看', also: '又称' }
      : { where: 'In the app', see: 'See it in a workflow', also: 'Also' };

  const PAGES = L
    ? L.pages
    : zh
      ? {
          'workflow-typhoons.html': '台风：哪些风暴最猛烈',
          'workflow-heatwave.html': '2023 年热浪：随时间变化',
          'workflow-walled-cities.html': '1866 年的中国城墙',
        }
      : {
          'workflow-typhoons.html': 'Typhoons: the strongest storms',
          'workflow-heatwave.html': 'The 2023 heatwave over time',
          'workflow-walled-cities.html': 'Walled cities of China, 1866',
        };

  data.forEach((e) => {
    const x = L && L.terms[e.id];
    if (x) {
      e._t = x.t;
      e._d = x.d;
      e._w = x.w;
      e._other = e.en;
      e._alt = (x.alt || []).concat(e.alt);
    } else if (zh) {
      e._t = e.zh;
      e._d = e.d_zh;
      e._w = e.w_zh;
      e._other = e.en;
      e._alt = e.alt;
    } else {
      e._t = e.en;
      e._d = e.d_en;
      e._w = e.w_en;
      e._other = L ? '' : e.zh;
      e._alt = e.alt;
    }
  });

  const sorted = data.slice().sort((a, b) => {
    if (zh) return a.zh.localeCompare(b.zh, 'zh-Hans-CN');
    return a._t.localeCompare(b._t, lang);
  });

  const parts = [];
  for (const e of sorted) {
    const main = e._t;
    const other = e._other;
    const alt = e._alt.filter((a) => a !== main && a !== other).slice(0, 5);
    const seeHref = e.see || '';
    const seePage = seeHref ? seeHref.split('#')[0] : '';
    parts.push(
      `<div class="entry" id="${esc(e.id)}">` +
        `<dt>${esc(main)}${other && other !== main ? ` <span class="alt">${esc(other)}</span>` : ''}` +
        ` <a class="anchor" href="#${esc(e.id)}" aria-label="#${esc(e.id)}">#</a></dt>` +
        `<dd><p>${e._d}</p>` +
        `<div class="where"><b>${esc(T.where)}</b><span>${e._w}</span></div>` +
        (seeHref
          ? `<div class="where"><b>${esc(T.see)}</b><a href="${esc(seeHref)}">${esc(PAGES[seePage] || seeHref)} →</a></div>`
          : '') +
        (alt.length
          ? `<div class="where"><b>${esc(T.also)}</b><span>${alt.map(esc).join(' · ')}</span></div>`
          : '') +
        `</dd></div>`
    );
  }
  return { html: parts.join('\n'), count: sorted.length, ids: sorted.map((e) => e.id) };
}

const NOSCRIPT = {
  en: 'Search and filtering need JavaScript. The definitions below are still readable without it.',
  zh: '搜索和筛选需要启用 JavaScript。下面的释义在关闭脚本时仍可阅读。',
  de: 'Suche und Filter brauchen JavaScript. Die Definitionen unten sind auch ohne lesbar.',
  es: 'La búsqueda y el filtro necesitan JavaScript. Las definiciones de abajo se pueden leer sin él.',
  fr: 'La recherche et le filtre nécessitent JavaScript. Les définitions ci-dessous restent lisibles sans.',
  it: 'Ricerca e filtri richiedono JavaScript. Le definizioni qui sotto restano leggibili senza.',
  nl: 'Zoeken en filteren hebben JavaScript nodig. De definities hieronder blijven leesbaar zonder.',
  'pt-br': 'A busca e o filtro precisam de JavaScript. As definições abaixo continuam legíveis sem ele.',
  ru: 'Поиск и фильтр требуют JavaScript. Определения ниже читаются и без него.',
  ja: '検索と絞り込みには JavaScript が必要です。以下の定義はオフでも読めます。',
  ko: '검색과 필터에는 JavaScript가 필요합니다. 아래 정의는 꺼져 있어도 읽을 수 있습니다.',
};

function inject(filePath, locale, built) {
  let html = fs.readFileSync(filePath, 'utf8');
  const dlRe = /<dl id="glossary" class="glossary">[\s\S]*?<\/dl>/;
  if (!dlRe.test(html)) throw new Error('glossary dl missing: ' + filePath);
  html = html.replace(dlRe, `<dl id="glossary" class="glossary">\n${built.html}\n</dl>`);

  // Update noscript copy
  const ns = NOSCRIPT[locale.code] || NOSCRIPT.en;
  html = html.replace(/<noscript><p class="empty">[\s\S]*?<\/p><\/noscript>/, `<noscript><p class="empty">${esc(ns)}</p></noscript>`);

  fs.writeFileSync(filePath, html);
  return built;
}

let total = 0;
for (const loc of LOCALES) {
  const file = loc.dir
    ? path.join(DOCS, loc.dir, 'glossary.html')
    : path.join(DOCS, 'glossary.html');
  const built = buildEntries(loc);
  inject(file, loc, built);
  total += built.count;
  console.log(`${loc.code}: ${built.count} terms → ${path.relative(ROOT, file)}`);
}
console.log('done, entries written across locales:', total);
