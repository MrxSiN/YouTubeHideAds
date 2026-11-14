<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **Español** · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**Un módulo Xposed que elimina los anuncios de YouTube, con cada decisión escrita en Brainfuck y el resto en XAX.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## Características

- **Anuncios eliminados antes de que se muestren:** anuncios de vídeos y Shorts, anuncios del feed y de la búsqueda, promociones de Premium y a pantalla completa. Sin huecos en blanco.
- **SponsorBlock integrado**, con segmentos de colores en la barra de progreso y un botón en el reproductor para saltar a mano, votar y enviar segmentos.
- **Reproductor:** velocidad y calidad por defecto, idiomas de subtítulos preferidos, reproducción en segundo plano, audio original, recordar la posición en directo, tocar para avanzar, bucle, un botón de velocidad y el recuento de Return YouTube Dislike.
- **Gestos:** desliza para el brillo a la izquierda y para el volumen a la derecha en pantalla completa, nunca sobre el chat en directo, los paneles ni la hoja Más vídeos.
- **Feed:** oculta los estantes de Shorts, publicaciones, vistas previas, Playables y canales de IA, lista negra de canales y palabras clave, y miniaturas de DeArrow.
- **Shorts:** oculta botones y paneles concretos, y salta los Shorts en directo.
- **Una sola página de ajustes** en **Tú → Configuración → YouTube Hide Ads**, en el idioma de YouTube (10 idiomas).

Los nuevos extras están desactivados por defecto. Todos los ajustes y sus valores por defecto están en la [documentación](docs/README.md#settings-and-defaults).

## Instalación

1. Descarga el APK desde [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) o [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Actívalo en [Vector](https://github.com/JingMatrix/Vector) o LSPosed (API libxposed 102) con YouTube en el ámbito.
3. Fuerza la detención de YouTube y ábrelo de nuevo.

Requiere Android 9 o posterior en arm64, y root para el framework. El módulo en sí no pide ningún permiso.

## Compatibilidad

| YouTube | Módulo | Estado |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ Funciona |
| 21.43.523 | 1.2.0 | ✅ Funciona |
| 21.42.243 | 1.1.0 | ✅ Funciona |

Probado en un Pixel 8 Pro con Android 17 y Vector 2.2. YouTube cambia el nombre de sus clases internas en la mayoría de las
actualizaciones. El módulo vuelve a encontrar sus objetivos por su estructura y desactiva una función en lugar de adivinar
cuando no puede. Historial: [registro de cambios](CHANGELOG.md) · detalles: [compatibilidad](docs/COMPATIBILITY.md).

## Límites conocidos

- Las apps que filtran HTTPS, como AdGuard, pueden bloquear SponsorBlock, la búsqueda de actualizaciones, el recuento de dislikes y DeArrow; consulta [más abajo](README.md#sponsorblock-or-update-check-never-connects).
- DeArrow sustituye las miniaturas, no los títulos. El menú de velocidad de YouTube sigue mostrando 1x después de aplicar una velocidad por defecto.
- La calidad por defecto con datos móviles, los Shorts en directo y el bloqueo de subtítulos automáticos no se han probado en un teléfono.
- Comprobado solo en tema oscuro y en un único teléfono. El texto nuevo de la 1.3.0 está en inglés.

Todo lo probado y lo no probado: [cobertura de funciones](docs/FEATURE_COVERAGE.md).

## Solución de problemas

| Problema | Prueba |
|---|---|
| No hay líneas `YouTubeHideAds:` en el registro del framework | Comprueba que YouTube esté en el ámbito y luego fuerza su detención. |
| Un interruptor del feed parece ignorado | Recarga el feed. |
| Deja de funcionar tras una actualización de YouTube | Usa **Acerca de → Compatibilidad y diagnóstico → Informar de un problema**. |

### SponsorBlock o la búsqueda de actualizaciones nunca se conecta

Esto también afecta al recuento de dislikes y a DeArrow. El registro muestra `NOT_ENOUGH_SCTS`. Una app que filtra HTTPS está volviendo a firmar la conexión, y la
comprobación de transparencia de certificados de YouTube la rechaza. En AdGuard, añade esto a **Filtrado HTTPS → Exclusiones**:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. Después reinicia YouTube.

## Cómo funciona

Brainfuck decide y XAX actúa. Nueve políticas de Brainfuck deciden, por ejemplo, si un componente es un
anuncio, si un salto puede omitir un segmento o si un toque es un deslizamiento. [BBC](https://github.com/MrxSiN/BBC) las compila por adelantado a
AArch64. Los hooks, el descubrimiento, los ajustes y la red forman un único almacén
[XAX](https://github.com/MrxSiN/XAX), compilado a DEX. El repositorio no tiene código fuente de aplicación en Java, Kotlin ni C.

[Arquitectura](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [compilación](docs/BUILD.md) · [toda la documentación](docs/README.md) · [evidencia](evidence/README.md)

## Apoyo

Si el módulo te resulta útil, puedes [patrocinar su desarrollo](https://github.com/sponsors/MrxSiN).

## Créditos y licencia

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList) (CC BY-NC 4.0, no incluido) y
[Morphe Patches](https://github.com/MorpheApp/morphe-patches), usado como referencia de comportamiento
([aviso](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. Consulta [NOTICE](NOTICE) y el [origen del código upstream](docs/UPSTREAM_PROVENANCE.md).
Este proyecto no está afiliado a Google ni a YouTube.
