<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · **Русский** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**Модуль Xposed, который убирает рекламу из YouTube: каждое решение написано на Brainfuck, всё остальное на XAX.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## Возможности

- **Реклама убирается до показа:** реклама в видео и Shorts, в ленте и поиске, промо Premium и полноэкранные акции. Никаких пустых мест.
- **Встроенный SponsorBlock**: цветные сегменты на полосе перемотки и кнопка в плеере для ручного пропуска, голосования и отправки сегментов.
- **Плеер:** скорость и качество по умолчанию, предпочитаемые языки субтитров, фоновое воспроизведение, оригинальная дорожка, запоминание позиции в трансляции, перемотка касанием, повтор, кнопка скорости и счётчик Return YouTube Dislike.
- **Жесты:** в полноэкранном режиме свайп слева меняет яркость, справа громкость; не срабатывает над чатом трансляции, панелями и списком «Другие видео».
- **Лента:** скрытие полок Shorts, постов, превью, Playables и ИИ-каналов, чёрный список каналов и ключевых слов, миниатюры DeArrow.
- **Shorts:** скрытие отдельных кнопок и панелей, пропуск прямых трансляций в Shorts.
- **Одна страница настроек** в **Вы → Настройки → YouTube Hide Ads**, на языке YouTube (10 языков).

Новые дополнения по умолчанию выключены. Все настройки и их значения по умолчанию перечислены в [документации](docs/README.md#settings-and-defaults).

## Установка

1. Скачайте APK из [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) или с [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Включите его в [Vector](https://github.com/JingMatrix/Vector) или LSPosed (libxposed API 102), указав YouTube в области действия.
3. Принудительно остановите YouTube и откройте его снова.

Нужен Android 9 или новее на arm64 и root для фреймворка. Сам модуль не запрашивает никаких разрешений.

## Совместимость

| YouTube | Модуль | Статус |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ Работает |
| 21.43.523 | 1.2.0 | ✅ Работает |
| 21.42.243 | 1.1.0 | ✅ Работает |

Проверено на Pixel 8 Pro с Android 17 и Vector 2.2. YouTube переименовывает внутренние классы почти в каждом
обновлении. Модуль заново находит нужные цели по структуре и отключает функцию, а не гадает,
если не может. История: [журнал изменений](CHANGELOG.md) · подробности: [совместимость](docs/COMPATIBILITY.md).

## Известные ограничения

- Приложения с фильтрацией HTTPS, например AdGuard, могут блокировать SponsorBlock, проверку обновлений, счётчик дизлайков и DeArrow; см. [ниже](README.md#sponsorblock-or-update-check-never-connects).
- DeArrow заменяет миниатюры, но не заголовки. Собственное меню скорости YouTube по-прежнему показывает 1x после применения скорости по умолчанию.
- Качество по умолчанию при мобильном интернете, прямые трансляции в Shorts и блокировка автоматических субтитров не проверялись на телефоне.
- Проверено только в тёмной теме и только на одном телефоне. Новые тексты 1.3.0 на английском.

Всё проверенное и непроверенное: [покрытие функций](docs/FEATURE_COVERAGE.md).

## Устранение неполадок

| Проблема | Что сделать |
|---|---|
| В журнале фреймворка нет строк `YouTubeHideAds:` | Проверьте, что YouTube указан в области действия, затем принудительно остановите его. |
| Переключатель ленты как будто не работает | Обновите ленту. |
| Перестало работать после обновления YouTube | Откройте **О модуле → Совместимость и диагностика → Сообщить о проблеме**. |

### SponsorBlock или проверка обновлений не подключается

Это относится и к счётчику дизлайков, и к DeArrow. В журнале видно `NOT_ENOUGH_SCTS`. Приложение с фильтрацией HTTPS подменяет сертификат соединения, а проверка
прозрачности сертификатов в YouTube его отклоняет. В AdGuard добавьте в **Фильтрация HTTPS → Исключения**:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. Затем перезапустите YouTube.

## Как это работает

Brainfuck решает, XAX действует. Девять политик на Brainfuck решают, например, является ли компонент
рекламой, можно ли при перемотке пропустить сегмент и является ли касание свайпом. Их заранее компилирует в
AArch64 [BBC](https://github.com/MrxSiN/BBC). Хуки, поиск, настройки и сеть собраны в одно хранилище
[XAX](https://github.com/MrxSiN/XAX), которое компилируется в DEX. В репозитории нет исходного кода приложения на Java, Kotlin или C.

[Архитектура](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [сборка](docs/BUILD.md) · [вся документация](docs/README.md) · [свидетельства](evidence/README.md)

## Поддержка

Если модуль вам полезен, можно [поддержать его разработку](https://github.com/sponsors/MrxSiN).

## Благодарности и лицензия

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList) (CC BY-NC 4.0, не входит в сборку) и
[Morphe Patches](https://github.com/MorpheApp/morphe-patches), использованный как образец поведения
([уведомление](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. См. [NOTICE](NOTICE) и [происхождение кода из upstream](docs/UPSTREAM_PROVENANCE.md).
Проект не связан с Google или YouTube.
