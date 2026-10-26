"""Generate English, Russian and Simplified Chinese pages from the Russian source."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re


# Russian source text -> (English, Simplified Chinese).
TEXT: dict[str, tuple[str, str]] = {
    # Shared shell and navigation.
    "Исследовательский архив — R.I.F.T. Experimental Lab": ("Research Archive — R.I.F.T. Experimental Lab", "研究档案 — R.I.F.T. Experimental Lab"),
    "Журнал — R.I.F.T. Experimental Lab": ("Journal — R.I.F.T. Experimental Lab", "实验日志 — R.I.F.T. Experimental Lab"),
    "Эксперименты — R.I.F.T. Experimental Lab": ("Experiments — R.I.F.T. Experimental Lab", "实验项目 — R.I.F.T. Experimental Lab"),
    "Лаборатория — R.I.F.T. Experimental Lab": ("Laboratory — R.I.F.T. Experimental Lab", "实验室 — R.I.F.T. Experimental Lab"),
    "Источники — R.I.F.T. Experimental Lab": ("Data Sources — R.I.F.T. Experimental Lab", "数据来源 — R.I.F.T. Experimental Lab"),
    "Манифест — R.I.F.T. Experimental Lab": ("Manifesto — R.I.F.T. Experimental Lab", "实验室宣言 — R.I.F.T. Experimental Lab"),
    "Контакт — R.I.F.T. Experimental Lab": ("Contact — R.I.F.T. Experimental Lab", "联系 — R.I.F.T. Experimental Lab"),
    "R.I.F.T. Experimental Lab — независимая лаборатория необычных технических экспериментов.": ("R.I.F.T. Experimental Lab — an independent laboratory for unusual technical experiments.", "R.I.F.T. 实验室——探索非凡技术实验的独立实验室。"),
    "R.I.F.T. Experimental Lab — главная": ("R.I.F.T. Experimental Lab — home", "R.I.F.T. 实验室——首页"),
    "Разделы сайта": ("Site sections", "网站栏目"),
    "R.I.F.T. / RESEARCH ARCHIVE": ("R.I.F.T. / RESEARCH ARCHIVE", "R.I.F.T. / 研究档案"),
    "EXPERIMENTAL LAB": ("EXPERIMENTAL LAB", "实验室"),
    "REALITY IRREGULARITIES AND": ("REALITY IRREGULARITIES AND", "现实异常与"),
    "FLUCTUATIONS TRACKING": ("FLUCTUATIONS TRACKING", "波动追踪"),
    "INDEPENDENT RESEARCH ARCHIVE": ("INDEPENDENT RESEARCH ARCHIVE", "独立研究档案"),
    "ГЛАВНАЯ": ("HOME", "首页"),
    "ЖУРНАЛ": ("JOURNAL", "日志"),
    "ЭКСПЕРИМЕНТЫ": ("EXPERIMENTS", "实验"),
    "ЛАБОРАТОРИЯ": ("LABORATORY", "实验室"),
    "ИСТОЧНИКИ": ("SOURCES", "数据来源"),
    "МАНИФЕСТ": ("MANIFESTO", "宣言"),
    "КОНТАКТ": ("CONTACT", "联系"),
    "R.I.F.T. EXPERIMENTAL LAB": ("R.I.F.T. EXPERIMENTAL LAB", "R.I.F.T. 实验室"),
    "Reality Irregularities and Fluctuations Tracking": ("Reality Irregularities and Fluctuations Tracking", "现实异常与波动追踪"),
    "Founded by Anton Kreighoff": ("Founded by Anton Kreighoff", "由 Anton Kreighoff 创立"),
    "СВЯЗАТЬСЯ ↗": ("CONTACT ↗", "联系我们 ↗"),
    "НАВЕРХ ↑": ("BACK TO TOP ↑", "返回顶部 ↑"),

    # Home.
    "ЛАБОРАТОРНЫЙ ЖУРНАЛ / ТИТУЛЬНЫЙ ЛИСТ": ("LAB JOURNAL / COVER SHEET", "实验日志 / 扉页"),
    "Для странных идей нужны": ("Strange ideas need", "奇特的想法需要"),
    "хорошие приборы.": ("good instruments.", "可靠的仪器。"),
    "R.I.F.T. — независимая экспериментальная лаборатория Антона Крайгхоффа. Здесь необычные вопросы превращаются в программы, измерения и записи, к которым можно вернуться.": ("R.I.F.T. is an independent experimental laboratory founded by Anton Kreighoff. Here, unusual questions become software, measurements, and records we can revisit.", "R.I.F.T. 是由 Anton Kreighoff 创立的独立实验室。在这里，不寻常的问题会变成程序、测量和可供回查的记录。"),
    "ПРОГРАММИРОВАНИЕ": ("SOFTWARE", "程序开发"),
    "ФИЗИЧЕСКИЕ ПРОЦЕССЫ": ("PHYSICAL PROCESSES", "物理过程"),
    "ОТКРЫТЫЙ АРХИВ": ("OPEN ARCHIVE", "开放档案"),
    "Заметка на полях": ("Margin note", "页边注"),
    "FIG. 01 / CURIOUS OBSERVER": ("FIG. 01 / CURIOUS OBSERVER", "图 01 / 好奇的观察者"),
    "Заметка:": ("Note:", "旁注："),
    "исследование начинается с вопроса. Архив — с первой записи.": ("research begins with a question. An archive begins with its first entry.", "研究始于一个问题，档案始于第一条记录。"),
    "LAB JOURNAL / ЖУРНАЛ": ("LAB JOURNAL / NOTES", "实验日志 / 笔记"),
    "ЗАПИСЬ 001": ("ENTRY 001", "记录 001"),
    "О ЛАБОРАТОРИИ": ("ABOUT THE LAB", "关于实验室"),
    "Зачем существует R.I.F.T.": ("Why R.I.F.T. exists", "R.I.F.T. 为何存在"),
    "Есть идеи, которые сначала звучат как сюжет научной фантастики. Интересно не просто обсуждать их, а находить наблюдаемые процессы, собирать инструменты и оставлять проверяемую запись того, что получилось.": ("Some ideas sound like science fiction at first. We want to do more than discuss them: find observable processes, assemble instruments, and keep a verifiable record of what happens.", "有些想法乍听像科幻故事。我们想做的不只是讨论它们，而是寻找可观测的过程、组装工具，并留下可核查的实验记录。"),
    "ЧИТАТЬ ЗАПИСЬ В ЖУРНАЛЕ ↗": ("READ THE JOURNAL ENTRY ↗", "阅读日志 ↗"),
    "EXPERIMENT 001 / CURRENT FILE": ("EXPERIMENT 001 / CURRENT FILE", "实验 001 / 当前档案"),
    "В ПРОЦЕССЕ НАБЛЮДЕНИЯ": ("UNDER OBSERVATION", "观察中"),
    "Первый эксперимент лаборатории: суточный цифровой отпечаток физических событий из квантовой случайности и измерений солнечного ветра.": ("The laboratory's first experiment: a daily digital fingerprint of physical events built from quantum randomness and solar-wind measurements.", "实验室的第一个项目：利用量子随机性和太阳风测量数据，为每天的物理事件生成数字指纹。"),
    "ЦЕЛЬ": ("AIM", "目标"),
    "Заметить возможную смену временной линии по расхождению записи с памятью наблюдателя.": ("Look for a possible timeline change through a discrepancy between the record and an observer's memory.", "通过记录与观察者记忆之间的差异，寻找可能的时间线变化。"),
    "ОТКРЫТЬ ДОСЬЕ ↗": ("OPEN DOSSIER ↗", "打开档案 ↗"),
    "ЖИВАЯ СТРАНИЦА ↗": ("LIVE EXPERIMENT ↗", "实验页面 ↗"),
    "Боковая колонка": ("Sidebar", "侧栏"),
    "INDEX OF ROOMS": ("INDEX OF ROOMS", "栏目索引"),
    "КАРТА": ("MAP", "导航"),
    "Устройство лаборатории": ("Inside the laboratory", "实验室设备"),
    "Источники данных": ("Data sources", "数据来源"),
    "Короткий манифест": ("Short manifesto", "简短宣言"),
    "ACTIVE FILE": ("ACTIVE FILE", "当前档案"),
    "ТЕКУЩИЙ ЭКСПЕРИМЕНТ": ("CURRENT EXPERIMENT", "当前实验"),
    "Суточный отпечаток физических событий.": ("A daily fingerprint of physical events.", "物理事件的每日指纹。"),
    "СМОТРЕТЬ ДОСЬЕ ↗": ("VIEW DOSSIER ↗", "查看档案 ↗"),
    "Разделы архива": ("Archive sections", "档案栏目"),
    "01 / FIELD NOTES": ("01 / FIELD NOTES", "01 / 研究笔记"),
    "Журнал": ("Journal", "实验日志"),
    "Заметки, решения и ход экспериментов.": ("Notes, decisions, and experimental progress.", "笔记、决策与实验进展。"),
    "ОТКРЫТЬ ↗": ("OPEN ↗", "打开 ↗"),
    "02 / THE WORKBENCH": ("02 / THE WORKBENCH", "02 / 工作台"),
    "Лаборатория": ("Laboratory", "实验室"),
    "Устройства, фотографии и истории с рабочего стола.": ("Instruments, photographs, and notes from the workbench.", "设备、照片与工作台上的记录。"),
    "03 / SOURCE INDEX": ("03 / SOURCE INDEX", "03 / 数据来源索引"),
    "Источники": ("Sources", "数据来源"),
    "Данные и документы, к которым мы обращаемся.": ("Data feeds and documents used by the lab.", "实验室使用的数据流与文档。"),

    # Journal.
    "ЗАПИСЬ 002": ("ENTRY 002", "记录 002"),
    "TimeLineStamp на главном экране": ("TimeLineStamp on the home screen", "主屏幕上的 TimeLineStamp"),
    "Мы выпустили виджет TimeLineStamp для главного экрана Android. Он показывает последнее зафиксированное суточное число, дату записи UTC и полноту данных.": ("We have released an Android home screen widget for TimeLineStamp. It displays the latest sealed daily number, the UTC date of the record, and data completeness.", "我们发布了适用于 Android 主屏幕的 TimeLineStamp 小组件。它显示最新封存的每日数字、记录的 UTC 日期及数据完整度。"),
    "Последнее показание остаётся на экране без интернета. Приложение работает на Android 8 и новее, интерфейс — на английском. Подписанный APK можно скачать со страницы эксперимента.": ("The last reading remains visible offline. The app works on Android 8 or newer, its interface is in English, and the signed APK can be downloaded from the experiment page.", "离线时仍可查看上次读数。应用支持 Android 8 及以上版本，界面为英文。可从实验页面下载已签名的 APK。"),
    "СКАЧАТЬ ВИДЖЕТ ДЛЯ ANDROID ↗": ("DOWNLOAD THE ANDROID WIDGET ↗", "下载 ANDROID 小组件 ↗"),
    "002 / Виджет для Android": ("002 / Android widget", "002 / Android 小组件"),
    "Журнал лаборатории": ("Laboratory journal", "实验室日志"),
    "Записи о том, как вопросы становятся экспериментами: идеи, решения, источники и изменения в работе приборов.": ("A record of how questions become experiments: ideas, decisions, sources, and changes to the instruments.", "记录问题如何变成实验：想法、决策、数据来源，以及仪器使用方式的变化。"),
    "INDEX OF ENTRIES": ("INDEX OF ENTRIES", "记录目录"),
    "ПЕРВАЯ ЗАПИСЬ": ("FIRST ENTRY", "首篇记录"),
    "R.I.F.T. — место для таких попыток. Научные знания, программирование и доступное оборудование помогают превратить вопрос в процедуру, а результат — в запись, к которой можно вернуться.": ("R.I.F.T. exists for attempts like these. Scientific knowledge, software, and accessible equipment turn a question into a procedure and a result into a record worth revisiting.", "R.I.F.T. 正是为这样的尝试而设。科学知识、程序开发与可获得的设备，让问题变成可执行的步骤，也让结果成为可以回查的记录。"),
    "Первое досье архива —": ("The archive's first dossier is", "档案中的第一份实验卷宗是"),
    ". В журнале будут появляться заметки о том, как устроены эксперименты, почему выбраны конкретные источники и что меняется в методике.": (". The journal will document how experiments work, why particular sources were chosen, and what changes in the method.", "。日志会记录实验如何运作、为何选用特定数据来源，以及方法有哪些变化。"),
    "END OF ENTRY 001": ("END OF ENTRY 001", "记录 001 结束"),
    "ДАЛЕЕ: EXPERIMENT 001 ↗": ("NEXT: EXPERIMENT 001 ↗", "下一篇：实验 001 ↗"),
    "ON THIS PAGE": ("ON THIS PAGE", "本页目录"),
    "АРХИВ": ("ARCHIVE", "档案"),
    "001 / Зачем существует R.I.F.T.": ("001 / Why R.I.F.T. exists", "001 / R.I.F.T. 为何存在"),
    "Журнал хранит вопросы, решения и изменения в работе лаборатории.": ("The journal keeps a record of questions, decisions, and changes in the laboratory's work.", "日志记录实验室的问题、决策和工作变化。"),

    # Experiment index.
    "Эксперименты": ("Experiments", "实验项目"),
    "Наблюдение приводит к идее, идея — к фантазии, фантазия — к эксперименту, и эксперимент — к наблюдению.": ("Observation leads to an idea; an idea to imagination; imagination to an experiment; and the experiment back to observation.", "观察催生想法，想法引出想象，想象促成实验，实验又回到观察。"),
    "EXPERIMENT 001 / PHYSICAL EVENT FINGERPRINT": ("EXPERIMENT 001 / PHYSICAL EVENT FINGERPRINT", "实验 001 / 物理事件指纹"),
    "Запись физических событий за сутки: два публичных квантовых маяка и данные о солнечном ветре. После завершения дня измерения превращаются в хеш и короткое число для сравнения с памятью наблюдателя.": ("A record of one day's physical events from two public quantum beacons and solar-wind measurements. Once the day ends, the readings become a hash and a short number that an observer can compare with memory.", "记录一天内的物理事件，数据来自两个公开量子随机信标和太阳风测量。当天结束后，测量值会生成哈希和一组简短数字，供观察者与记忆中的数字比较。"),
    "ЦЕЛЬ ЭКСПЕРИМЕНТА": ("EXPERIMENT AIM", "实验目标"),
    "Заметить возможную смену временной линии по расхождению между запомненным числом и текущей записью за те же сутки.": ("Look for a possible timeline change through a discrepancy between a remembered number and the current record for the same day.", "通过对比记忆中的数字与同一天当前显示的记录，寻找可能的时间线变化。"),
    "СТРАНИЦА ЭКСПЕРИМЕНТА ↗": ("EXPERIMENT PAGE ↗", "实验页面 ↗"),
    "КОД И МЕТОДИКА ↗": ("CODE AND METHOD ↗", "代码与方法 ↗"),
    "Обозначения статусов": ("Status key", "状态说明"),
    "СТАТУСЫ ДОСЬЕ": ("DOSSIER STATUS", "档案状态"),
    "ИДЕЯ ПОДТВЕРЖДЕНА": ("IDEA CONFIRMED", "想法已获证实"),
    "Принцип эксперимента": ("How the experiment works", "实验原理"),
    "01 / INPUT": ("01 / INPUT", "01 / 输入"),
    "Измерения": ("Measurements", "测量"),
    "Квантовая случайность и меняющиеся условия солнечного ветра.": ("Quantum randomness and changing solar-wind conditions.", "量子随机性与不断变化的太阳风状态。"),
    "02 / RECORD": ("02 / RECORD", "02 / 记录"),
    "Суточная запись": ("Daily record", "每日记录"),
    "После завершения суток данные фиксируются вместе с полным SHA-256 хешем.": ("After the day ends, the data are sealed with a full SHA-256 hash.", "当天结束后，数据与完整的 SHA-256 哈希一起固定。"),
    "03 / COMPARISON": ("03 / COMPARISON", "03 / 对比"),
    "Сравнение": ("Comparison", "对比"),
    "Короткое число помогает человеку заметить возможное расхождение с тем, что он помнит.": ("A short number helps a person notice a possible discrepancy with what they remember.", "简短的数字帮助人发现当前记录与记忆之间可能存在的差异。"),
    "ПОСМОТРЕТЬ ИСТОЧНИКИ ДАННЫХ ↗": ("VIEW DATA SOURCES ↗", "查看数据来源 ↗"),
}

TEXT.update({
    # Laboratory.
    "Карманные обсерватории, вычислительные системы и ассистенты с характером. У каждого инструмента есть лабораторное имя, конкретная задача и место для фотографии.": ("Pocket observatories, computing systems, and assistants with a personality. Each instrument has a laboratory name, a specific task, and a place for its photograph.", "袖珍观测站、计算系统，还有颇具个性的助理。每件设备都有实验室名称、明确的任务和专属的照片位置。"),
    "INVENTORY / 003": ("INVENTORY / 003", "设备清单 / 003"),
    "Названия — часть языка лаборатории. Фотографии здесь пока обозначены макетами кадров: настоящие снимки займут их место после съёмки.": ("These names are part of the laboratory's vocabulary. Photo frames mark where actual images will appear once taken.", "这些名称是实验室语言的一部分。目前的相框只是占位；拍摄完成后会换成真实照片。"),
    "EQUIPMENT FILES / КАРТОТЕКА": ("EQUIPMENT FILES / INDEX", "设备档案 / 索引"),
    "ФОТО + ХАРАКТЕРИСТИКИ + ЗАМЕТКА": ("PHOTO + SPECIFICATIONS + NOTE", "照片 + 参数 + 备注"),
    "Место для фотографии карманной обсерватории": ("Placeholder for a photograph of the Pocket Observatory", "袖珍观测站照片占位"),
    "PHOTO 001 / FIELD UNIT": ("PHOTO 001 / FIELD UNIT", "照片 001 / 现场单元"),
    "КАРМАННАЯ ОБСЕРВАТОРИЯ": ("POCKET OBSERVATORY", "袖珍观测站"),
    "СКОРО": ("COMING SOON", "即将呈现"),
    "R.I.F.T. / LAB RECORD": ("R.I.F.T. / LAB RECORD", "R.I.F.T. / 实验室记录"),
    "ИНВЕНТАРЬ 001": ("INVENTORY 001", "设备 001"),
    "НОСИМЫЙ УЗЕЛ": ("PORTABLE UNIT", "便携单元"),
    "Карманная обсерватория": ("Pocket Observatory", "袖珍观测站"),
    "Небольшой автономный наблюдатель: собирает публичные потоки измерений из разных точек мира, анализирует поступающие записи и хранит их для дальнейшей проверки.": ("A compact autonomous observer. It collects public measurement feeds from around the world, analyzes incoming records, and stores them for later review.", "一台小型自主观测设备：从世界各地收集公开测量数据流，分析收到的记录，并保存起来以备复核。"),
    "РОЛЬ": ("ROLE", "用途"),
    "Сбор, анализ и хранение данных": ("Data collection, analysis, and storage", "数据采集、分析与存储"),
    "РЕЖИМ": ("MODE", "模式"),
    "Автономное наблюдение": ("Autonomous observation", "自主观测"),
    "КАДР": ("PHOTO", "照片"),
    "Фотография полевого узла": ("Photograph of the field unit", "现场单元照片"),
    "Место для фотографии терра-компьютерной системы": ("Placeholder for a photograph of the Terra Computing System", "Terra 计算系统照片占位"),
    "PHOTO 002 / CONTROL DESK": ("PHOTO 002 / CONTROL DESK", "照片 002 / 控制台"),
    "ТЕРРА-СИСТЕМА": ("TERRA SYSTEM", "TERRA 系统"),
    "ИНВЕНТАРЬ 002": ("INVENTORY 002", "设备 002"),
    "КОМАНДНАЯ СИСТЕМА": ("COMMAND SYSTEM", "指挥系统"),
    "Терра-компьютерная система": ("Terra Computing System", "Terra 计算系统"),
    "Центральная консоль лаборатории. Здесь рождаются идеи, пишется код, собираются протоколы и принимаются решения о том, какой эксперимент запускать следующим.": ("The laboratory's central console. Ideas take shape here, code is written, protocols are assembled, and the next experiment is chosen.", "实验室的中央控制台。想法在这里形成，代码在这里编写，实验方案在这里整理，下一项实验也在这里决定。"),
    "Управление лабораторией": ("Laboratory control", "实验室管理"),
    "Проектирование и разработка": ("Design and development", "设计与开发"),
    "Фотография рабочего места": ("Photograph of the workstation", "工作台照片"),
    "Место для фотографии ассистента номер 762 на CRT-телевизоре": ("Placeholder for a photograph of Assistant Model 762 on a CRT television", "CRT 电视上的 762 号助理模型照片占位"),
    "MODEL 762 / VISUAL FEED": ("MODEL 762 / VISUAL FEED", "型号 762 / 视觉信号"),
    "ИНВЕНТАРЬ 003": ("INVENTORY 003", "设备 003"),
    "ЦИФРОВОЙ АССИСТЕНТ": ("DIGITAL ASSISTANT", "数字助理"),
    "Искусственная модель ассистента № 762": ("Artificial Assistant Model No. 762", "人工助理模型 762 号"),
    "Гуманоидный цифровой ассистент помогает превращать идеи в схемы, код и работающие прототипы. Для лабораторного архива его облик появится на CRT-экране.": ("A humanoid digital assistant helps turn ideas into diagrams, code, and working prototypes. Its laboratory portrait will appear on a CRT screen.", "人形数字助理帮助把想法转化为图表、代码和可运行的原型。它在实验室档案中的形象将出现在 CRT 屏幕上。"),
    "Техническая реализация идей": ("Technical implementation of ideas", "想法的技术实现"),
    "ИНТЕРФЕЙС": ("INTERFACE", "交互方式"),
    "Диалог и визуальный образ на экране": ("Conversation and an on-screen presence", "对话与屏幕上的形象"),
    "Фотография CRT-телевизора": ("Photograph of the CRT television", "CRT 电视照片"),
    "ЕСТЬ ВОПРОС О ЛАБОРАТОРИИ? НАПИСАТЬ ↗": ("A QUESTION ABOUT THE LAB? WRITE TO US ↗", "对实验室有疑问？写信给我们 ↗"),

    # Source registry.
    "Общий каталог источников": ("Complete source registry", "完整数据来源目录"),
    "Общий каталог источников лаборатории. Рядом с каждым потоком указано, в каких экспериментах он используется; внутри — схема от физического процесса до данных в нашей записи.": ("The laboratory's shared source registry. Each feed lists the experiments that use it; open a record to follow the path from physical process to stored data.", "这是实验室共用的数据来源目录。每条数据流都标明使用它的实验；展开条目即可看到从物理过程到存储数据的完整路径。"),
    "В КАТАЛОГЕ: 04 ПОТОКА / 03 ОПЕРАТОРА": ("IN THE REGISTRY: 04 FEEDS / 03 OPERATORS", "目录包含：04 条数据流 / 03 家运营方"),
    "Откройте карточку источника, чтобы увидеть, что именно измеряется, кто публикует результат и какие поля получает эксперимент.": ("Open a source record to see what is measured, who publishes the result, and which fields the experiment receives.", "展开来源条目，查看测量对象、发布方以及实验实际获取的字段。"),
    "Публичные импульсы случайности · США": ("Public randomness pulses · United States", "公开随机脉冲 · 美国"),
    "Публичные импульсы случайности · Сингапур": ("Public randomness pulses · Singapore", "公开随机脉冲 · 新加坡"),
    "Маяк NIST публикует помеченные временем импульсы случайности. В его системе используется в том числе квантовый генератор на регистрации фотонов. TimeLineStamp выбирает один импульс каждые пять минут.": ("The NIST beacon publishes timestamped randomness pulses. Its system includes a quantum generator based on photon detection. TimeLineStamp selects one pulse every five minutes.", "NIST 信标发布带时间戳的随机脉冲。其系统包括基于光子探测的量子随机数发生器。TimeLineStamp 每五分钟选取一个脉冲。"),
    "От регистрации фотонов до записи TimeLineStamp": ("From photon detection to the TimeLineStamp record", "从光子探测到 TimeLineStamp 记录"),
    "01 / ФИЗИКА": ("01 / PHYSICS", "01 / 物理过程"),
    "Регистрация фотонов": ("Photon detection", "光子探测"),
    "квантовый источник случайности": ("quantum source of randomness", "量子随机性来源"),
    "02 / ПУБЛИКАЦИЯ": ("02 / PUBLICATION", "02 / 发布"),
    "Импульс NIST": ("NIST pulse", "NIST 脉冲"),
    "новый публичный пульс каждую минуту": ("one new public pulse per minute", "每分钟发布一个新脉冲"),
    "03 / НАША ЗАПИСЬ": ("03 / OUR RECORD", "03 / 本实验记录"),
    "Пульс раз в 5 минут": ("One pulse every 5 minutes", "每 5 分钟一个脉冲"),
    "одно значение для каждого слота UTC": ("one value for each UTC slot", "每个 UTC 时段取一个值"),
    "ЧТО ПОЛУЧАЕМ": ("FIELDS RECEIVED", "获取字段"),
    "Случайная строка длиной 512 бит, время публикации и идентификаторы импульса.": ("A 512-bit random string, publication time, and pulse identifiers.", "一条 512 位随机字符串、发布时间及脉冲标识符。"),
    "ОПИСАНИЕ NIST ↗": ("NIST DOCUMENTATION ↗", "NIST 文档 ↗"),
    "ПОСЛЕДНИЙ ИМПУЛЬС ↗": ("LATEST PULSE ↗", "最新脉冲 ↗"),
    "Два квантовых генератора NQSN измеряют флуктуации электромагнитного вакуума. Маяк объединяет их выводы в 512-битное значение и публикует его в каждом минутном импульсе. TimeLineStamp выбирает один импульс каждые пять минут.": ("Two NQSN quantum generators measure fluctuations in the electromagnetic vacuum. The beacon combines their outputs into a 512-bit value published in each minute's pulse. TimeLineStamp selects one pulse every five minutes.", "NQSN 的两台量子发生器测量电磁真空涨落。信标将它们的输出合成为 512 位数值，每分钟通过一个脉冲发布。TimeLineStamp 每五分钟选取一个脉冲。"),
    "От флуктуаций вакуума до записи TimeLineStamp": ("From vacuum fluctuations to the TimeLineStamp record", "从真空涨落到 TimeLineStamp 记录"),
    "Флуктуации вакуума": ("Vacuum fluctuations", "真空涨落"),
    "два квантовых генератора": ("two quantum generators", "两台量子发生器"),
    "Импульс NQSN": ("NQSN pulse", "NQSN 脉冲"),
    "512 бит каждую минуту": ("512 bits every minute", "每分钟 512 位"),
    "вторая независимая последовательность": ("a second independent sequence", "第二组独立序列"),
    "Случайная строка длиной 512 бит; время и индексы указывают конкретный импульс. Внешний компонент пульса NQSN не входит в расчёт суточного отпечатка.": ("A 512-bit random string; time and indices identify the exact pulse. The NQSN pulse's external component is excluded from the daily fingerprint.", "一条 512 位随机字符串；时间和索引用于定位具体脉冲。NQSN 脉冲的外部成分不参与每日指纹的计算。"),
    "КАК УСТРОЕН ИСТОЧНИК ↗": ("HOW THE SOURCE WORKS ↗", "来源原理 ↗"),
    "API МАЯКА ↗": ("BEACON API ↗", "信标 API ↗"),
    "NOAA · магнитное поле": ("NOAA · magnetic field", "NOAA · 磁场"),
    "NOAA · плазма": ("NOAA · plasma", "NOAA · 等离子体"),
    "Минутный поток rtsw_mag_1m": ("Minute feed rtsw_mag_1m", "分钟数据流 rtsw_mag_1m"),
    "Минутный поток rtsw_wind_1m": ("Minute feed rtsw_wind_1m", "分钟数据流 rtsw_wind_1m"),
    "Солнечный ветер несёт магнитное поле. Магнитометр активного космического аппарата измеряет его, а NOAA публикует минутные записи. Активный аппарат может переключаться между DSCOVR и ACE.": ("The solar wind carries a magnetic field. A magnetometer on the active spacecraft measures it, and NOAA publishes minute records. The active spacecraft may switch between DSCOVR and ACE.", "太阳风携带磁场。当前工作的航天器使用磁力计进行测量，NOAA 发布分钟级记录。当前航天器可能在 DSCOVR 与 ACE 之间切换。"),
    "От магнитного поля солнечного ветра до записи TimeLineStamp": ("From the solar-wind magnetic field to the TimeLineStamp record", "从太阳风磁场到 TimeLineStamp 记录"),
    "Магнитное поле": ("Magnetic field", "磁场"),
    "меняется вместе с солнечным ветром": ("changes with the solar wind", "随太阳风变化"),
    "02 / ПРИБОР": ("02 / INSTRUMENT", "02 / 仪器"),
    "Магнитометр": ("Magnetometer", "磁力计"),
    "аппарат у точки L1 · DSCOVR или ACE": ("spacecraft near L1 · DSCOVR or ACE", "L1 附近的航天器 · DSCOVR 或 ACE"),
    "Поток NOAA": ("NOAA feed", "NOAA 数据流"),
    "одна запись за минуту": ("one record per minute", "每分钟一条记录"),
    "Общая величина поля, три компонента в координатах GSM, время и название аппарата. TimeLineStamp берёт только активные записи с хорошим общим флагом качества.": ("Total field strength, three components in GSM coordinates, time, and spacecraft name. TimeLineStamp uses only active records with a good overall quality flag.", "磁场总强度、GSM 坐标系中的三个分量、时间和航天器名称。TimeLineStamp 仅使用总质量标记良好的有效记录。"),
    "ОПИСАНИЕ NOAA ↗": ("NOAA DOCUMENTATION ↗", "NOAA 文档 ↗"),
    "ПОТОК JSON ↗": ("JSON FEED ↗", "JSON 数据流 ↗"),
    "Плазменный прибор активного космического аппарата наблюдает поток протонов солнечного ветра. NOAA публикует скорость, плотность и температуру этого потока в минутных записях.": ("A plasma instrument on the active spacecraft observes the solar wind's proton stream. NOAA publishes its speed, density, and temperature in minute records.", "当前工作的航天器使用等离子体仪器观测太阳风中的质子流。NOAA 以分钟级记录发布其速度、密度和温度。"),
    "От протонов солнечного ветра до записи TimeLineStamp": ("From solar-wind protons to the TimeLineStamp record", "从太阳风质子到 TimeLineStamp 记录"),
    "Поток протонов": ("Proton stream", "质子流"),
    "частицы солнечного ветра": ("solar-wind particles", "太阳风粒子"),
    "Датчик плазмы": ("Plasma sensor", "等离子体传感器"),
    "активный аппарат · DSCOVR или ACE": ("active spacecraft · DSCOVR or ACE", "当前航天器 · DSCOVR 或 ACE"),
    "Скорость, плотность и температура протонов, время и аппарат. TimeLineStamp берёт только активные записи с хорошим общим флагом качества.": ("Proton speed, density, and temperature, plus time and spacecraft. TimeLineStamp uses only active records with a good overall quality flag.", "质子的速度、密度和温度，以及时间和航天器信息。TimeLineStamp 仅使用总质量标记良好的有效记录。"),
    "ПРАВИЛА ОБРАБОТКИ В РЕПОЗИТОРИИ ↗": ("PROCESSING RULES IN THE REPOSITORY ↗", "仓库中的处理规则 ↗"),
})

TEXT.update({
    # Manifesto.
    "Манифест": ("Manifesto", "实验室宣言"),
    "Несколько рабочих принципов лаборатории.": ("A few working principles of the laboratory.", "实验室的几条工作原则。"),
    "Принципы лаборатории": ("Laboratory principles", "实验室原则"),
    "Четыре заметки": ("Four notes", "四条笔记"),
    "R.I.F.T. / FIELD COPY": ("R.I.F.T. / FIELD COPY", "R.I.F.T. / 现场手记"),
    "Странная идея — достаточный повод поставить эксперимент.": ("An unusual idea is reason enough to run an experiment.", "一个奇特的想法，就足以成为开展实验的理由。"),
    "Эксперименту нужны метод, прибор и запись.": ("An experiment needs a method, an instrument, and a record.", "实验需要方法、仪器和记录。"),
    "Данные создают точку для наблюдения.": ("Data create a point of observation.", "数据为观察建立一个基点。"),
    "Наблюдатель — самая важная часть эксперимента.": ("The observer is the most important part of the experiment.", "观察者是实验中最重要的一部分。"),
    "R.I.F.T. работает с вопросами, которые легко оставить в области фантазии. Нам интереснее построить что-то работающее и посмотреть, что оно покажет. Так появляются устройства, код, журнальные записи и новые вопросы.": ("R.I.F.T. works with questions that could easily remain fiction. We would rather build something that works and see what it shows. That is how instruments, code, journal entries, and new questions emerge.", "R.I.F.T. 探索那些很容易被留在幻想中的问题。我们更愿意做出真正能运行的东西，看看它会显示什么。设备、代码、日志记录和新的问题便由此产生。"),
    "ВЕРНУТЬСЯ К ЖУРНАЛУ ↗": ("RETURN TO JOURNAL ↗", "返回日志 ↗"),

    # Contact.
    "На связи": ("Get in touch", "保持联系"),
    "Вопросы об экспериментах, идеи для лаборатории и сообщения о расхождениях можно отправить напрямую.": ("Questions about experiments, ideas for the laboratory, and reports of discrepancies can be sent directly.", "有关实验的问题、给实验室的想法，以及对记录差异的报告，都可以直接发送给我们。"),
    "DIRECT LINE / EMAIL": ("DIRECT LINE / EMAIL", "直接联系 / 邮件"),
    "Написать в лабораторию": ("Write to the laboratory", "写信给实验室"),
    "Для обсуждения экспериментов и сообщений о TimeLineStamp.": ("For discussions about experiments and reports concerning TimeLineStamp.", "用于讨论实验或报告与 TimeLineStamp 有关的情况。"),
    "PUBLIC RECORD / GITHUB": ("PUBLIC RECORD / GITHUB", "公开档案 / GITHUB"),
    "Открыть организацию": ("Visit the organization", "访问组织主页"),
    "Код, описание проектов и профиль лаборатории.": ("Code, project descriptions, and the laboratory profile.", "代码、项目介绍和实验室简介。"),
    "R.I.F.T. на GitHub ↗": ("R.I.F.T. on GitHub ↗", "GitHub 上的 R.I.F.T. ↗"),
})

# Labels that are already in English in the Russian source but need Chinese UI text.
CHINESE_LABELS: dict[str, str] = {
    "SECTION 01 / LAB JOURNAL": "第 01 部分 / 实验日志",
    "SECTION 02 / EXPERIMENT INDEX": "第 02 部分 / 实验目录",
    "SECTION 03 / THE WORKBENCH": "第 03 部分 / 工作台",
    "SECTION 04 / SOURCE REGISTRY": "第 04 部分 / 数据来源目录",
    "SECTION 05 / NOTES ON METHOD": "第 05 部分 / 方法笔记",
    "SECTION 06 / CONTACT": "第 06 部分 / 联系",
    "01 / QUANTUM": "01 / 量子随机性",
    "02 / QUANTUM": "02 / 量子随机性",
    "03 / SOLAR WIND": "03 / 太阳风",
    "04 / SOLAR WIND": "04 / 太阳风",
    "EXPERIMENT 001": "实验 001",
    "EXP. 001 ↗": "实验 001 ↗",
}


def _translate_nodes(source: str, locale: str) -> str:
    """Replace complete text nodes, preserving their surrounding whitespace."""

    def replace(match: re.Match[str]) -> str:
        value = match.group(1)
        key = value.strip()
        if not key:
            return value
        if key in TEXT:
            translated = TEXT[key][0 if locale == "en" else 1]
        elif locale == "zh-CN" and key in CHINESE_LABELS:
            translated = CHINESE_LABELS[key]
        else:
            translated = key
        start = value[: len(value) - len(value.lstrip())]
        end = value[len(value.rstrip()):]
        return start + escape(translated, quote=False) + end

    return re.sub(r"(?<=>)([^<>]+)(?=<)", replace, source)


def _translate_attributes(source: str, locale: str) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(2)
        if key not in TEXT:
            return match.group(0)
        translated = TEXT[key][0 if locale == "en" else 1]
        return match.group(1) + escape(translated, quote=True) + match.group(3)

    return re.sub(r'(\b(?:aria-label|alt|content)=")([^"]*)(")', replace, source)


def _page_path(locale: str, filename: str, current: str) -> str:
    if locale == current:
        return filename
    if current == "en":
        return f"{locale}/{filename}"
    if locale == "en":
        return f"../{filename}"
    return f"../{locale}/{filename}"


def _language_switch(filename: str, locale: str) -> str:
    labels = (("en", "EN"), ("ru", "RU"), ("zh", "中文"))
    items = []
    for target, label in labels:
        active = ' aria-current="page"' if target == locale else ""
        href = _page_path(target, filename, locale)
        items.append(f'<a href="{href}" hreflang="{target if target != "zh" else "zh-CN"}"{active}>{label}</a>')
    description = {"en": "Language", "ru": "Язык", "zh": "语言"}[locale]
    return f'<nav class="language-switch" aria-label="{description}">{"".join(items)}</nav>'


def _alternate_links(filename: str, locale: str) -> str:
    links = []
    for target, hreflang in (("en", "en"), ("ru", "ru"), ("zh", "zh-CN")):
        links.append(f'  <link rel="alternate" hreflang="{hreflang}" href="{_page_path(target, filename, locale)}">')
    links.append(f'  <link rel="alternate" hreflang="x-default" href="{_page_path("en", filename, locale)}">')
    return "\n".join(links)


def _render(source: str, filename: str, locale: str) -> str:
    html = source.replace('<html lang="ru">', f'<html lang="{locale if locale != "zh" else "zh-CN"}">')
    if locale != "ru":
        html = _translate_nodes(html, "en" if locale == "en" else "zh-CN")
        html = _translate_attributes(html, "en" if locale == "en" else "zh-CN")
    html = html.replace("__LANG_SWITCH__", _language_switch(filename, locale))
    if locale != "en":
        html = html.replace('href="style.css"', 'href="../style.css"')
        html = html.replace('href="assets/rift-mark.svg"', 'href="../assets/rift-mark.svg"')
        html = html.replace('src="assets/rift-mark.svg"', 'src="../assets/rift-mark.svg"')
    html = html.replace('  <link rel="stylesheet"', _alternate_links(filename, locale) + '\n  <link rel="stylesheet"', 1)
    return html


def build_locales(root: Path, filenames: list[str]) -> None:
    source_pages = {filename: (root / filename).read_text(encoding="utf-8") for filename in filenames}
    for locale in ("en", "ru", "zh"):
        target = root if locale == "en" else root / locale
        target.mkdir(exist_ok=True)
        for filename, source in source_pages.items():
            page = _render(source, filename, locale)
            if locale != "ru" and re.search(r"[А-Яа-яЁё]", page):
                raise ValueError(f"Untranslated Cyrillic in {locale}/{filename}")
            (target / filename).write_text(page, encoding="utf-8")
