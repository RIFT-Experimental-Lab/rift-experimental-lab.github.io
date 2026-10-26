# -*- coding: utf-8 -*-
"""Build the static R.I.F.T. laboratory site."""

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
NAV = [
    ("index.html", "ГЛАВНАЯ"),
    ("journal.html", "ЖУРНАЛ"),
    ("experiments.html", "ЭКСПЕРИМЕНТЫ"),
    ("laboratory.html", "ЛАБОРАТОРИЯ"),
    ("sources.html", "ИСТОЧНИКИ"),
    ("manifesto.html", "МАНИФЕСТ"),
    ("contact.html", "КОНТАКТ"),
]


def page(filename: str, title: str, body: str) -> None:
    nav_items = []
    for href, label in NAV:
        active = ' aria-current="page"' if href == filename else ""
        nav_items.append(f'<a href="{href}"{active}>{label}</a>')
    nav = "".join(nav_items)
    html = f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#e9e3d6">
  <meta name="description" content="R.I.F.T. Experimental Lab — независимая лаборатория необычных технических экспериментов.">
  <title>{title} — R.I.F.T. Experimental Lab</title>
  <link rel="icon" href="assets/rift-mark.svg" type="image/svg+xml">
  <link rel="stylesheet" href="style.css">
</head>
<body id="top">
  <div class="topline"><div class="wrap"><span>R.I.F.T. / RESEARCH ARCHIVE</span><div class="topline-actions">__LANG_SWITCH__</div></div></div>
  <div class="wrap">
    <header class="masthead">
      <a class="brand" href="index.html" aria-label="R.I.F.T. Experimental Lab — главная">
        <img class="brand-mark" src="assets/rift-mark.svg" alt="" width="74" height="74">
        <span><span class="brand-name">R.I.F.T<em>.</em></span><span class="brand-subtitle">EXPERIMENTAL LAB</span></span>
      </a>
      <div class="masthead-note"><strong>REALITY IRREGULARITIES AND</strong>FLUCTUATIONS TRACKING<br>INDEPENDENT RESEARCH ARCHIVE</div>
    </header>
    <nav class="site-nav" aria-label="Разделы сайта">{nav}</nav>
    {dedent(body).strip()}
  </div>
  <footer class="footer"><div class="wrap"><div><strong>R.I.F.T. EXPERIMENTAL LAB</strong>Reality Irregularities and Fluctuations Tracking</div><div>Founded by Anton Kreighoff</div><div><a href="contact.html">СВЯЗАТЬСЯ ↗</a><br><a href="#top">НАВЕРХ ↑</a></div></div></footer>
</body>
</html>
'''
    (ROOT / filename).write_text(html, encoding="utf-8")


page("index.html", "Исследовательский архив", '''
<section class="hero" aria-labelledby="hero-title">
  <div>
    <div class="eyebrow">ЛАБОРАТОРНЫЙ ЖУРНАЛ / ТИТУЛЬНЫЙ ЛИСТ</div>
    <h1 id="hero-title">Для странных идей нужны <em>хорошие приборы.</em></h1>
    <p class="hero-intro">R.I.F.T. — независимая экспериментальная лаборатория Антона Крайгхоффа. Здесь необычные вопросы превращаются в программы, измерения и записи, к которым можно вернуться.</p>
    <div class="hero-foot"><span>ПРОГРАММИРОВАНИЕ</span><span>ФИЗИЧЕСКИЕ ПРОЦЕССЫ</span><span>ОТКРЫТЫЙ АРХИВ</span></div>
  </div>
  <aside class="hero-aside" aria-label="Заметка на полях">
    <div class="micro">FIG. 01 / CURIOUS OBSERVER</div>
    <svg class="orbit" viewBox="0 0 200 190" fill="none" aria-hidden="true"><circle cx="98" cy="94" r="72" stroke="currentColor"/><circle cx="98" cy="94" r="48" stroke="currentColor" stroke-dasharray="3 5"/><circle cx="98" cy="94" r="22" stroke="currentColor"/><path d="M8 94h180M98 4v180M42 38l112 112M154 38L42 150" stroke="currentColor" stroke-opacity=".55" stroke-width=".7"/><circle cx="98" cy="94" r="4" fill="#a95737"/><circle cx="155" cy="50" r="3" fill="#a95737"/><path d="M154 50l28-24" stroke="#a95737"/></svg>
    <p><strong>Заметка:</strong> исследование начинается с вопроса. Архив — с первой записи.</p>
  </aside>
</section>
<div class="content-grid home-grid">
  <main class="primary">
    <section aria-labelledby="journal-title">
      <div class="section-title" id="journal-title"><span>LAB JOURNAL / ЖУРНАЛ</span><small>ЗАПИСЬ 001</small></div>
      <article class="journal-article">
        <div class="paper-meta"><span><b>ЗАПИСЬ 001</b></span><span>О ЛАБОРАТОРИИ</span></div>
        <h2>Зачем существует R.I.F.T.</h2>
        <p>Есть идеи, которые сначала звучат как сюжет научной фантастики. Интересно не просто обсуждать их, а находить наблюдаемые процессы, собирать инструменты и оставлять проверяемую запись того, что получилось.</p>
        <a class="article-link" href="journal.html">ЧИТАТЬ ЗАПИСЬ В ЖУРНАЛЕ ↗</a>
      </article>
    </section>
    <section class="experiment" aria-labelledby="experiment-title">
      <div class="experiment-heading"><div class="micro">EXPERIMENT 001 / CURRENT FILE</div><span class="experiment-status status-observing">В ПРОЦЕССЕ НАБЛЮДЕНИЯ</span></div>
      <h2 id="experiment-title">TimeLineStamp</h2>
      <p>Первый эксперимент лаборатории: суточный цифровой отпечаток физических событий из квантовой случайности и измерений солнечного ветра.</p>
      <p class="experiment-goal"><span>ЦЕЛЬ</span>Заметить возможную смену временной линии по расхождению записи с памятью наблюдателя.</p>
      <div class="experiment-links"><a href="experiments.html">ОТКРЫТЬ ДОСЬЕ ↗</a><a href="https://rift-experimental-lab.github.io/TimeLineStamp/" target="_blank" rel="noopener noreferrer">ЖИВАЯ СТРАНИЦА ↗</a></div>
    </section>
  </main>
  <aside class="sidebar" aria-label="Боковая колонка">
    <section class="sidebar-section"><div class="section-title"><span>INDEX OF ROOMS</span><small>КАРТА</small></div><ul class="sidebar-list"><li><a href="laboratory.html">Устройство лаборатории</a></li><li><a href="sources.html">Источники данных</a></li><li><a href="manifesto.html">Короткий манифест</a></li></ul></section>
    <section class="sidebar-section"><div class="section-title"><span>ACTIVE FILE</span><small>001</small></div><div class="file-card"><span>ТЕКУЩИЙ ЭКСПЕРИМЕНТ</span><strong>TimeLineStamp</strong><p>Суточный отпечаток физических событий.</p><a href="experiments.html">СМОТРЕТЬ ДОСЬЕ ↗</a></div></section>

  </aside>
</div>
<section class="doorways" aria-label="Разделы архива">
  <a class="doorway" href="journal.html"><span>01 / FIELD NOTES</span><strong>Журнал</strong><small>Заметки, решения и ход экспериментов.</small><b>ОТКРЫТЬ ↗</b></a>
  <a class="doorway" href="laboratory.html"><span>02 / THE WORKBENCH</span><strong>Лаборатория</strong><small>Устройства, фотографии и истории с рабочего стола.</small><b>ОТКРЫТЬ ↗</b></a>
  <a class="doorway" href="sources.html"><span>03 / SOURCE INDEX</span><strong>Источники</strong><small>Данные и документы, к которым мы обращаемся.</small><b>ОТКРЫТЬ ↗</b></a>
</section>
''')


page("journal.html", "Журнал", '''
<header class="page-lead"><span class="eyebrow">SECTION 01 / LAB JOURNAL</span><h1>Журнал лаборатории</h1><p>Записи о том, как вопросы становятся экспериментами: идеи, решения, источники и изменения в работе приборов.</p></header>
<div class="content-grid inner-grid">
  <main class="primary">
    <div class="section-title"><span>INDEX OF ENTRIES</span><small>002 / 001</small></div>
    <article class="journal-article journal-full" id="entry-002">
      <div class="paper-meta"><span><b>ЗАПИСЬ 002</b></span><span><time datetime="2026-10-26">2026-10-26</time> / EXPERIMENT 001</span></div>
      <h2>TimeLineStamp на главном экране</h2>
      <p>Мы выпустили виджет TimeLineStamp для главного экрана Android. Он показывает последнее зафиксированное суточное число, дату записи UTC и полноту данных.</p>
      <p>Последнее показание остаётся на экране без интернета. Приложение работает на Android 8 и новее, интерфейс — на английском. Подписанный APK можно скачать со страницы эксперимента.</p>
      <a class="article-link" href="https://rift-experimental-lab.github.io/TimeLineStamp/#android-widget">СКАЧАТЬ ВИДЖЕТ ДЛЯ ANDROID ↗</a>
    </article>
    <article class="journal-article journal-full" id="entry-001">
      <div class="paper-meta"><span><b>ЗАПИСЬ 001</b></span><span>О ЛАБОРАТОРИИ</span></div>
      <h2>Зачем существует R.I.F.T.</h2>
      <p>Есть идеи, которые сначала звучат как сюжет научной фантастики. Интересно не просто обсуждать их, а находить наблюдаемые процессы, собирать инструменты и оставлять проверяемую запись того, что получилось.</p>
      <p>R.I.F.T. — место для таких попыток. Научные знания, программирование и доступное оборудование помогают превратить вопрос в процедуру, а результат — в запись, к которой можно вернуться.</p>
      <p>Первое досье архива — <a href="experiments.html">TimeLineStamp</a>. В журнале будут появляться заметки о том, как устроены эксперименты, почему выбраны конкретные источники и что меняется в методике.</p>
    </article>
    <div class="journal-end"><span>END OF ENTRY 001</span><a href="experiments.html">ДАЛЕЕ: EXPERIMENT 001 ↗</a></div>
  </main>
  <aside class="sidebar"><section class="sidebar-section"><div class="section-title"><span>ON THIS PAGE</span><small>АРХИВ</small></div><ul class="sidebar-list"><li><a href="#entry-002">002 / Виджет для Android</a></li><li><a href="#entry-001">001 / Зачем существует R.I.F.T.</a></li></ul></section><div class="margin-note">Журнал хранит вопросы, решения и изменения в работе лаборатории.</div></aside>
</div>
''')


page("experiments.html", "Эксперименты", '''
<header class="page-lead"><span class="eyebrow">SECTION 02 / EXPERIMENT INDEX</span><h1>Эксперименты</h1><p>Наблюдение приводит к идее, идея — к фантазии, фантазия — к эксперименту, и эксперимент — к наблюдению.</p></header>
<section class="experiment experiment-page" aria-labelledby="exp-title"><div class="experiment-heading"><div class="micro">EXPERIMENT 001 / PHYSICAL EVENT FINGERPRINT</div><span class="experiment-status status-observing">В ПРОЦЕССЕ НАБЛЮДЕНИЯ</span></div><h2 id="exp-title">TimeLineStamp</h2><p>Запись физических событий за сутки: два публичных квантовых маяка и данные о солнечном ветре. После завершения дня измерения превращаются в хеш и короткое число для сравнения с памятью наблюдателя.</p><p class="experiment-goal"><span>ЦЕЛЬ ЭКСПЕРИМЕНТА</span>Заметить возможную смену временной линии по расхождению между запомненным числом и текущей записью за те же сутки.</p><div class="experiment-links"><a href="https://rift-experimental-lab.github.io/TimeLineStamp/" target="_blank" rel="noopener noreferrer">СТРАНИЦА ЭКСПЕРИМЕНТА ↗</a><a href="https://github.com/RIFT-Experimental-Lab/TimeLineStamp" target="_blank" rel="noopener noreferrer">КОД И МЕТОДИКА ↗</a></div></section>
<div class="status-key" aria-label="Обозначения статусов"><span>СТАТУСЫ ДОСЬЕ</span><span class="experiment-status status-observing">В ПРОЦЕССЕ НАБЛЮДЕНИЯ</span><span class="experiment-status status-confirmed">ИДЕЯ ПОДТВЕРЖДЕНА</span></div>
<section class="fact-grid" aria-label="Принцип эксперимента"><article><span>01 / INPUT</span><h3>Измерения</h3><p>Квантовая случайность и меняющиеся условия солнечного ветра.</p></article><article><span>02 / RECORD</span><h3>Суточная запись</h3><p>После завершения суток данные фиксируются вместе с полным SHA-256 хешем.</p></article><article><span>03 / COMPARISON</span><h3>Сравнение</h3><p>Короткое число помогает человеку заметить возможное расхождение с тем, что он помнит.</p></article></section>
<div class="page-tail"><a href="sources.html">ПОСМОТРЕТЬ ИСТОЧНИКИ ДАННЫХ ↗</a></div>
''')


page("laboratory.html", "Лаборатория", '''
<header class="page-lead"><span class="eyebrow">SECTION 03 / THE WORKBENCH</span><h1>Устройство лаборатории</h1><p>Карманные обсерватории, вычислительные системы и ассистенты с характером. У каждого инструмента есть лабораторное имя, конкретная задача и место для фотографии.</p></header>
<div class="lab-intro"><span>INVENTORY / 003</span><p>Названия — часть языка лаборатории. Фотографии здесь пока обозначены макетами кадров: настоящие снимки займут их место после съёмки.</p></div>
<section class="equipment" aria-labelledby="equipment-title"><div class="section-title" id="equipment-title"><span>EQUIPMENT FILES / КАРТОТЕКА</span><small>ФОТО + ХАРАКТЕРИСТИКИ + ЗАМЕТКА</small></div>
  <article class="equipment-card">
    <div class="photo-frame" role="img" aria-label="Место для фотографии карманной обсерватории"><span class="photo-cross top-left"></span><span class="photo-cross bottom-right"></span><div class="photo-target"><span>PHOTO 001 / FIELD UNIT</span><strong>КАРМАННАЯ ОБСЕРВАТОРИЯ</strong><small>СКОРО</small></div><span class="photo-corner">R.I.F.T. / LAB RECORD</span></div>
    <div class="equipment-copy"><div class="paper-meta"><span><b>ИНВЕНТАРЬ 001</b></span><span>НОСИМЫЙ УЗЕЛ</span></div><h2>Карманная обсерватория</h2><p>Небольшой автономный наблюдатель: собирает публичные потоки измерений из разных точек мира, анализирует поступающие записи и хранит их для дальнейшей проверки.</p><dl><div><dt>РОЛЬ</dt><dd>Сбор, анализ и хранение данных</dd></div><div><dt>РЕЖИМ</dt><dd>Автономное наблюдение</dd></div><div><dt>КАДР</dt><dd>Фотография полевого узла</dd></div></dl></div>
  </article>
  <article class="equipment-card reverse">
    <div class="photo-frame photo-frame--terra" role="img" aria-label="Место для фотографии терра-компьютерной системы"><span class="photo-cross top-left"></span><span class="photo-cross bottom-right"></span><div class="photo-target"><span>PHOTO 002 / CONTROL DESK</span><strong>ТЕРРА-СИСТЕМА</strong><small>СКОРО</small></div><span class="photo-corner">R.I.F.T. / LAB RECORD</span></div>
    <div class="equipment-copy"><div class="paper-meta"><span><b>ИНВЕНТАРЬ 002</b></span><span>КОМАНДНАЯ СИСТЕМА</span></div><h2>Терра-компьютерная система</h2><p>Центральная консоль лаборатории. Здесь рождаются идеи, пишется код, собираются протоколы и принимаются решения о том, какой эксперимент запускать следующим.</p><dl><div><dt>РОЛЬ</dt><dd>Управление лабораторией</dd></div><div><dt>РЕЖИМ</dt><dd>Проектирование и разработка</dd></div><div><dt>КАДР</dt><dd>Фотография рабочего места</dd></div></dl></div>
  </article>
  <article class="equipment-card">
    <div class="photo-frame photo-frame--crt" role="img" aria-label="Место для фотографии ассистента номер 762 на CRT-телевизоре"><div class="crt-bezel"><div class="crt-screen"><span>MODEL 762 / VISUAL FEED</span><strong>762</strong><small>СКОРО</small></div></div><span class="photo-corner">R.I.F.T. / LAB RECORD</span></div>
    <div class="equipment-copy"><div class="paper-meta"><span><b>ИНВЕНТАРЬ 003</b></span><span>ЦИФРОВОЙ АССИСТЕНТ</span></div><h2>Искусственная модель ассистента № 762</h2><p>Гуманоидный цифровой ассистент помогает превращать идеи в схемы, код и работающие прототипы. Для лабораторного архива его облик появится на CRT-экране.</p><dl><div><dt>РОЛЬ</dt><dd>Техническая реализация идей</dd></div><div><dt>ИНТЕРФЕЙС</dt><dd>Диалог и визуальный образ на экране</dd></div><div><dt>КАДР</dt><dd>Фотография CRT-телевизора</dd></div></dl></div>
  </article>
</section>
<div class="page-tail"><a href="contact.html">ЕСТЬ ВОПРОС О ЛАБОРАТОРИИ? НАПИСАТЬ ↗</a></div>
''')


page("sources.html", "Источники", '''
<header class="page-lead"><span class="eyebrow">SECTION 04 / SOURCE REGISTRY</span><h1>Источники данных</h1><p>Общий каталог источников лаборатории. Рядом с каждым потоком указано, в каких экспериментах он используется; внутри — схема от физического процесса до данных в нашей записи.</p></header>
<div class="registry-intro"><span>В КАТАЛОГЕ: 04 ПОТОКА / 03 ОПЕРАТОРА</span><p>Откройте карточку источника, чтобы увидеть, что именно измеряется, кто публикует результат и какие поля получает эксперимент.</p></div>
<section class="source-registry" aria-label="Общий каталог источников">
  <details class="source-record" open>
    <summary><span class="registry-number">01 / QUANTUM</span><span class="registry-name">NIST Randomness Beacon<small>Публичные импульсы случайности · США</small></span><span class="registry-experiment">EXPERIMENT 001<br><b>TimeLineStamp</b></span><span class="registry-toggle" aria-hidden="true"></span></summary>
    <div class="registry-body">
      <p class="registry-explain">Маяк NIST публикует помеченные временем импульсы случайности. В его системе используется в том числе квантовый генератор на регистрации фотонов. TimeLineStamp выбирает один импульс каждые пять минут.</p>
      <div class="data-flow" role="group" aria-label="От регистрации фотонов до записи TimeLineStamp"><div class="flow-step"><span>01 / ФИЗИКА</span><strong>Регистрация фотонов</strong><small>квантовый источник случайности</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step"><span>02 / ПУБЛИКАЦИЯ</span><strong>Импульс NIST</strong><small>новый публичный пульс каждую минуту</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step flow-step--last"><span>03 / НАША ЗАПИСЬ</span><strong>Пульс раз в 5 минут</strong><small>одно значение для каждого слота UTC</small></div></div>
      <div class="field-readout"><span>ЧТО ПОЛУЧАЕМ</span><div><code>localRandomValue</code><code>timeStamp</code><code>chainIndex</code><code>pulseIndex</code></div><p>Случайная строка длиной 512 бит, время публикации и идентификаторы импульса.</p></div>
      <div class="registry-links"><a href="https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20" target="_blank" rel="noopener noreferrer">ОПИСАНИЕ NIST ↗</a><a href="https://beacon.nist.gov/beacon/2.0/pulse/last" target="_blank" rel="noopener noreferrer">ПОСЛЕДНИЙ ИМПУЛЬС ↗</a><a href="experiments.html">EXP. 001 ↗</a></div>
    </div>
  </details>
  <details class="source-record">
    <summary><span class="registry-number">02 / QUANTUM</span><span class="registry-name">NQSN Beacon<small>Публичные импульсы случайности · Сингапур</small></span><span class="registry-experiment">EXPERIMENT 001<br><b>TimeLineStamp</b></span><span class="registry-toggle" aria-hidden="true"></span></summary>
    <div class="registry-body">
      <p class="registry-explain">Два квантовых генератора NQSN измеряют флуктуации электромагнитного вакуума. Маяк объединяет их выводы в 512-битное значение и публикует его в каждом минутном импульсе. TimeLineStamp выбирает один импульс каждые пять минут.</p>
      <div class="data-flow" role="group" aria-label="От флуктуаций вакуума до записи TimeLineStamp"><div class="flow-step"><span>01 / ФИЗИКА</span><strong>Флуктуации вакуума</strong><small>два квантовых генератора</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step"><span>02 / ПУБЛИКАЦИЯ</span><strong>Импульс NQSN</strong><small>512 бит каждую минуту</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step flow-step--last"><span>03 / НАША ЗАПИСЬ</span><strong>Пульс раз в 5 минут</strong><small>вторая независимая последовательность</small></div></div>
      <div class="field-readout"><span>ЧТО ПОЛУЧАЕМ</span><div><code>localRandomValue</code><code>timeStamp</code><code>chainIndex</code><code>pulseIndex</code></div><p>Случайная строка длиной 512 бит; время и индексы указывают конкретный импульс. Внешний компонент пульса NQSN не входит в расчёт суточного отпечатка.</p></div>
      <div class="registry-links"><a href="https://quantum-entropy.sg/sources/" target="_blank" rel="noopener noreferrer">КАК УСТРОЕН ИСТОЧНИК ↗</a><a href="https://quantum-entropy.sg/api/beacon/" target="_blank" rel="noopener noreferrer">API МАЯКА ↗</a><a href="experiments.html">EXP. 001 ↗</a></div>
    </div>
  </details>
  <details class="source-record">
    <summary><span class="registry-number">03 / SOLAR WIND</span><span class="registry-name">NOAA · магнитное поле<small>Минутный поток rtsw_mag_1m</small></span><span class="registry-experiment">EXPERIMENT 001<br><b>TimeLineStamp</b></span><span class="registry-toggle" aria-hidden="true"></span></summary>
    <div class="registry-body">
      <p class="registry-explain">Солнечный ветер несёт магнитное поле. Магнитометр активного космического аппарата измеряет его, а NOAA публикует минутные записи. Активный аппарат может переключаться между DSCOVR и ACE.</p>
      <div class="data-flow" role="group" aria-label="От магнитного поля солнечного ветра до записи TimeLineStamp"><div class="flow-step"><span>01 / ФИЗИКА</span><strong>Магнитное поле</strong><small>меняется вместе с солнечным ветром</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step"><span>02 / ПРИБОР</span><strong>Магнитометр</strong><small>аппарат у точки L1 · DSCOVR или ACE</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step flow-step--last"><span>03 / НАША ЗАПИСЬ</span><strong>Поток NOAA</strong><small>одна запись за минуту</small></div></div>
      <div class="field-readout"><span>ЧТО ПОЛУЧАЕМ</span><div><code>bt</code><code>bx_gsm</code><code>by_gsm</code><code>bz_gsm</code><code>time_tag</code><code>source</code></div><p>Общая величина поля, три компонента в координатах GSM, время и название аппарата. TimeLineStamp берёт только активные записи с хорошим общим флагом качества.</p></div>
      <div class="registry-links"><a href="https://www.swpc.noaa.gov/products/real-time-solar-wind" target="_blank" rel="noopener noreferrer">ОПИСАНИЕ NOAA ↗</a><a href="https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json" target="_blank" rel="noopener noreferrer">ПОТОК JSON ↗</a><a href="experiments.html">EXP. 001 ↗</a></div>
    </div>
  </details>
  <details class="source-record">
    <summary><span class="registry-number">04 / SOLAR WIND</span><span class="registry-name">NOAA · плазма<small>Минутный поток rtsw_wind_1m</small></span><span class="registry-experiment">EXPERIMENT 001<br><b>TimeLineStamp</b></span><span class="registry-toggle" aria-hidden="true"></span></summary>
    <div class="registry-body">
      <p class="registry-explain">Плазменный прибор активного космического аппарата наблюдает поток протонов солнечного ветра. NOAA публикует скорость, плотность и температуру этого потока в минутных записях.</p>
      <div class="data-flow" role="group" aria-label="От протонов солнечного ветра до записи TimeLineStamp"><div class="flow-step"><span>01 / ФИЗИКА</span><strong>Поток протонов</strong><small>частицы солнечного ветра</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step"><span>02 / ПРИБОР</span><strong>Датчик плазмы</strong><small>активный аппарат · DSCOVR или ACE</small></div><span class="flow-connector" aria-hidden="true">→</span><div class="flow-step flow-step--last"><span>03 / НАША ЗАПИСЬ</span><strong>Поток NOAA</strong><small>одна запись за минуту</small></div></div>
      <div class="field-readout"><span>ЧТО ПОЛУЧАЕМ</span><div><code>proton_speed</code><code>proton_density</code><code>proton_temperature</code><code>time_tag</code><code>source</code></div><p>Скорость, плотность и температура протонов, время и аппарат. TimeLineStamp берёт только активные записи с хорошим общим флагом качества.</p></div>
      <div class="registry-links"><a href="https://www.swpc.noaa.gov/products/real-time-solar-wind" target="_blank" rel="noopener noreferrer">ОПИСАНИЕ NOAA ↗</a><a href="https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json" target="_blank" rel="noopener noreferrer">ПОТОК JSON ↗</a><a href="experiments.html">EXP. 001 ↗</a></div>
    </div>
  </details>
</section>
<div class="page-tail"><a href="https://github.com/RIFT-Experimental-Lab/TimeLineStamp" target="_blank" rel="noopener noreferrer">ПРАВИЛА ОБРАБОТКИ В РЕПОЗИТОРИИ ↗</a></div>
''')


page("manifesto.html", "Манифест", '''
<header class="page-lead"><span class="eyebrow">SECTION 05 / NOTES ON METHOD</span><h1>Манифест</h1><p>Несколько рабочих принципов лаборатории.</p></header>
<section class="manifesto manifesto-page" aria-label="Принципы лаборатории"><div class="manifesto-head"><h2>Четыре заметки</h2><span class="micro">R.I.F.T. / FIELD COPY</span></div><ol><li>Странная идея — достаточный повод поставить эксперимент.</li><li>Эксперименту нужны метод, прибор и запись.</li><li>Данные создают точку для наблюдения.</li><li>Наблюдатель — самая важная часть эксперимента.</li></ol></section>
<div class="manifesto-after"><p>R.I.F.T. работает с вопросами, которые легко оставить в области фантазии. Нам интереснее построить что-то работающее и посмотреть, что оно покажет. Так появляются устройства, код, журнальные записи и новые вопросы.</p><a href="journal.html">ВЕРНУТЬСЯ К ЖУРНАЛУ ↗</a></div>
''')


page("contact.html", "Контакт", '''
<header class="page-lead"><span class="eyebrow">SECTION 06 / CONTACT</span><h1>На связи</h1><p>Вопросы об экспериментах, идеи для лаборатории и сообщения о расхождениях можно отправить напрямую.</p></header>
<div class="contact-grid"><section class="contact-card"><span>DIRECT LINE / EMAIL</span><h2>Написать в лабораторию</h2><p>Для обсуждения экспериментов и сообщений о TimeLineStamp.</p><a href="mailto:rift.research@outlook.com">rift.research@outlook.com ↗</a></section><section class="contact-card"><span>PUBLIC RECORD / GITHUB</span><h2>Открыть организацию</h2><p>Код, описание проектов и профиль лаборатории.</p><a href="https://github.com/RIFT-Experimental-Lab" target="_blank" rel="noopener noreferrer">R.I.F.T. на GitHub ↗</a></section></div>
''')

from localization import build_locales

build_locales(ROOT, [filename for filename, _ in NAV])
print("Built", len(NAV), "pages in 3 languages")
