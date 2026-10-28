<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **Español** · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**Un módulo de Xposed que quita los anuncios de YouTube, con cada decisión escrita en Brainfuck y el resto en XAX. Sí, de verdad.**

Los anuncios, los Shorts patrocinados y las promociones se eliminan antes de que YouTube los muestre, y los segmentos de SponsorBlock se saltan.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#requisitos)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube cambia el nombre de sus clases ofuscadas en casi cada actualización. El módulo vuelve a encontrar sus objetivos por su estructura en cada inicio. Si un rol falta o es ambiguo, deja esa función tal cual en vez de adivinar. Consulta la tabla de [compatibilidad](#compatibilidad) para ver lo que se ha probado de verdad.

## ¿Por qué Brainfuck? ¿Y qué es XAX?

- **Brainfuck decide.** Si un componente es un anuncio, si se puede quitar el marketing de Premium, si el reproductor puede saltar al final de un segmento patrocinado, si un deslizamiento cambia el brillo. Brainfuck no puede llamar a Android, Xposed, DexKit ni JNI: lee bytes y escribe bytes, y el host solo actúa ante una respuesta exacta y correcta.
- **XAX hace todo lo demás.** Los hooks, la búsqueda con DexKit, la reflexión, la página de configuración y el HTTPS/JSON de SponsorBlock forman un único almacén semántico canónico de [XAX](https://github.com/MrxSiN/XAX). El compilador externo de XAX lo convierte en DEX y firma el APK. En este repositorio no hay código de aplicación en Java, Kotlin, C, Python ni shell.

Tampoco es lento. Las nueve políticas se compilan por adelantado a bibliotecas compartidas AArch64 con [BrainfuckCC](https://github.com/MrxSiN/BrainfuckCC). El APK no lleva intérprete.

|  | |
|---|---|
| 🧹 **Eliminados, no ocultos** | Los componentes publicitarios se sustituyen antes de que YouTube los coloque, y los Shorts patrocinados salen del feed antes de crear el reproductor: sin huecos ni clips congelados. |
| ⏭️ **SponsorBlock integrado** | Consultas por prefijo con reintentos y caché limitados, modos y colores por categoría, salto y deshacer manuales, creación de segmentos y votos, exclusiones, estadísticas y transferencia de configuración. |
| 🔎 **Resiste los cambios de nombre** | DexKit localiza cada hook por su estructura en cada inicio. Un rol ausente o ambiguo no instala nada para esa función. |
| 🧠 **Políticas en Brainfuck, compiladas** | Nueve programas escritos a mano y compilados a código nativo; las políticas y los controles de SponsorBlock se comprueban en cada inicio. |
| 🛟 **Falla de forma segura** | Si una autocomprobación falla, esa función queda desactivada. Los errores de red y los tipos de reproducción desconocidos nunca provocan saltos. |
| ⚙️ **Configuración con aspecto nativo** | Su propia sección **YouTubeHideAds** en **Tú → Configuración**, encima de Cuenta, con las filas de YouTube, cada interruptor independiente y una página de Compatibilidad y diagnóstico. |
| 🎛️ **SponsorBlock integrado en el reproductor** | Un icono de SponsorBlock junto a la reproducción automática abre el mismo menú flotante que el engranaje de ajustes; los segmentos se colorean en la barra de progreso. |
| 📱 **Shorts más limpios** | Oculta botones y paneles concretos de Shorts y pasa de largo las emisiones en directo del feed de Shorts. |
| 👆 **Controles de deslizamiento claros** | Brillo a la izquierda y volumen a la derecha, en una cápsula con icono, nivel y valor. |
| 🌐 **Tu idioma** | Sigue el idioma de YouTube: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia y Bahasa Melayu. |

---

## Qué elimina

| Grupo | Ajuste | Por defecto |
|---|---|---|
| Anuncios | Anuncios de vídeo y de Shorts · Anuncios del feed y la búsqueda · Promociones de Premium · Promociones a pantalla completa | Activado, bajo el interruptor general **Ocultar anuncios** |
| SponsorBlock | Patrocinios, autopromoción | Activado |
| SponsorBlock | Recordatorios de interacción, introducciones, cierres, avances, relleno, segmentos sin música | Desactivado |
| Contenido | Playables (secciones de juegos, tarjetas, entrada de Explorar) | Oculto |
| Feed | Vídeos de vista previa · Explorar más temas · Publicaciones | Oculto |
| Feed | Shorts en los feeds | Visible |
| Feed | Canales de IA · Posibles canales de IA ([AiSList](https://github.com/Override92/AiSList)) | Desactivado |
| Reproductor | Brillo deslizando (izquierda) · Volumen deslizando (derecha), solo a pantalla completa | Activado |
| Reproductor | Forzar el audio original en vídeos con varios idiomas | Activado |
| Reproductor | Reproducción en segundo plano, incluidos los vídeos para niños | Activado |
| Shorts | Me gusta, comentarios, compartir, remix, guardar, sonido, suscribirse, título, sugerencias y paneles de información, botones al pausar | Visible (cada uno se puede ocultar) |
| Shorts | Saltar Shorts en directo | Desactivado |

Desactivar **Ocultar anuncios** no desactiva las funciones de contenido y del reproductor. Recarga el feed después de cambiar sus interruptores. El audio original se aplica a la siguiente lista de pistas y respeta una elección manual. Tabla completa: [ajustes y valores predeterminados](docs/README.md#settings-and-defaults). La reproducción en segundo plano no depende de Ocultar anuncios ni de SponsorBlock; reinicia YouTube después de cambiarla. [Implementación y límites probados](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 Dónde ocurre cada eliminación</b></summary>
<br>

| Superficie | Dónde | Qué hace |
|---|---|---|
| **Anuncios de vídeo** | activación y diseño de anuncios del reproductor | Suprime el espacio publicitario cuando Brainfuck confirma un indicio estructural de anuncio y una transición segura. |
| **Anuncios del feed, la búsqueda y compras** | el analizador de componentes, encontrado por DexKit | Sustituye un componente de pago confirmado por el componente vacío de YouTube. |
| **Shorts patrocinados** | respuesta, inserción y datos iniciales del reproductor de Shorts | Elimina las entradas de anuncios de vídeo o imagen junto con sus datos de seguimiento antes de que exista el reproductor. |
| **Premium, pantalla completa, paneles** | vista de oferta, diálogo a pantalla completa, panel de interacción por identificador tipado | Oculta superficies de marketing sin tocar derechos ni la gestión de suscripciones. |
| **Secciones del feed, Playables, canales de IA, elementos de Shorts** | el mismo hook de componentes | Quita solo la sección, la tarjeta o el botón coincidente; las filas de canales y las listas se mantienen. |
| **SponsorBlock** | puentes de salto/duración del reproductor y barra de progreso nativa | Consultas por prefijo limitadas, modos por categoría, marcas de color, controles manuales y acciones explícitas de la comunidad. |

</details>

---

## Estado

**v1.1.0** (versionCode 153) es la primera versión desde la 1.0.0. Añade reproducción en segundo plano, una sección propia en la Configuración de YouTube, una página de Compatibilidad y diagnóstico, controles de SponsorBlock con el estilo de YouTube, Ocultar elementos de Shorts, Saltar Shorts en directo, controles de deslizamiento rediseñados y nueve idiomas más. También es mucho más ligera en el teléfono: las políticas de Brainfuck ya no vuelven a abrir el APK y los resultados de DexKit se guardan en caché, así que YouTube se abre unos 0,35 s antes después del primer inicio. [Pruebas en el dispositivo](evidence/device_perf_20261028/README.md).

Las versiones de desarrollo entre ambas versiones (111 a 153) están en el [registro de cambios](CHANGELOG.md), con las pruebas de cada una en [evidence](evidence/README.md).

### Compatibilidad

Cada fila es una configuración que alguien ha usado de verdad. Si pruebas otra, abre un pull request para añadir una fila.

| Dispositivo | Android | Framework | YouTube | Módulo | Resultado | Probado por | Fecha |
|---|---|---|---|---|---|---|---|
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | 1.1.0 | Anuncios, eliminación de anuncios de Shorts, SponsorBlock, audio original, reproducción en segundo plano desde el feed y desde un enlace (Inicio, pantalla apagada, interruptor desactivado); 11 comprobaciones de inicio | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 132 | Sección de ajustes, diagnóstico, elementos de Shorts, icono/menú de SponsorBlock, saltos reales; 11 comprobaciones de inicio + 64 de interfaz | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 127 | Deslizadores modernos; tema oscuro/claro, táctil, teclado, guardar/reabrir; 636 + 64 comprobaciones | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.42.243 | dev 123 | Interfaz nativa de SponsorBlock, selector de color, 636 + 28 comprobaciones | @MrxSiN | 2026-10 |

### Límites conocidos

- Las promociones de Premium, a pantalla completa y de paneles superaron pruebas controladas de los hooks; todavía no se han visto casos reales.
- Los encabezados de vídeos de vista previa y de «Explorar más temas» solo se reconocen en inglés.
- Las listas de IA las mantiene la comunidad y pueden clasificar mal un canal; por eso vienen desactivadas.
- Los controles de SponsorBlock están en el icono de SponsorBlock de la barra superior del reproductor y en los ajustes del módulo. Consulta [funciones y límites](docs/SPONSORBLOCK_API_RESEARCH.md).
- Saltar Shorts en directo aún no se ha encontrado con un Short en directo real en el teléfono de pruebas; su comprobación de página se verificó con una sonda de desarrollo.
- Solo arm64-v8a. No se han probado otras versiones de YouTube, dispositivos ni LSPatch.

Detalles: [cobertura de funciones](docs/FEATURE_COVERAGE.md) y [compatibilidad](docs/COMPATIBILITY.md).

## Requisitos

| | |
|---|---|
| **Android** | 9.0 (API 28) o superior, arm64 |
| **App** | YouTube (`com.google.android.youtube`) |
| **Framework** | [Vector](https://github.com/JingMatrix/Vector) o LSPosed con libxposed API 102 |
| **Root** | Lo requiere Vector/LSPosed; el módulo no pide ningún permiso |

## Instalación

```
1. Instala el APK desde Releases o el repositorio de módulos de Xposed
2. Activa YouTubeHideAds en Vector o LSPosed con YouTube como ámbito
3. Fuerza la detención de YouTube una vez y ábrelo
```

Descárgalo en [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) o en [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads). Los ajustes están en **YouTube → Tú → Configuración → YouTubeHideAds**. Las preferencias y las cachés de IA se guardan en los datos de YouTube, así que borrarlos los restablece.

El registro del framework muestra lo ocurrido en líneas que empiezan por `YouTubeHideAds:`:

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## Cómo funciona

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

Una sola regla decide dónde va el código: **si toca YouTube, Android, la red o JNI, lo hace XAX; si decide si actuar sobre lo que XAX encontró, lo decide Brainfuck.** Los detalles de las bibliotecas de políticas, la disposición de bytes y la búsqueda de hooks están en [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) y [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md).

La obtención automática de segmentos solo envía un prefijo SHA-256 de cuatro dígitos hexadecimales del ID del vídeo. La respuesta, el número de registros y los tiempos de espera están limitados, y las redirecciones desactivadas. Los envíos y votos manuales mandan al servidor elegido los datos necesarios y la identidad privada; los informes de visualización vienen desactivados y las exportaciones excluyen el ID privado por defecto.

---

## Compilación

Este repositorio no tiene script de compilación. Las versiones se compilan con herramientas externas:

```text
BrainfuckCC  source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

Cada entrada está fijada con BLAKE3 en el almacén, de modo que una entrada distinta hace fallar la compilación. Para recompilar se usa [XAX](https://github.com/MrxSiN/XAX) con su perfil de Android libxposed (commit `3cca599` o la instantánea compatible branding-v2). Los pasos están en [`docs/BUILD.md`](docs/BUILD.md).

## Solución de problemas

| Problema | Prueba |
|---|---|
| No hay líneas del módulo en el registro | Comprueba que el módulo esté activado con YouTube en su ámbito y fuerza la detención de YouTube. |
| `UnsatisfiedLinkError` justo después de actualizar | Espera a que termine la instalación y vuelve a abrir YouTube tras forzar su detención. |
| Una autocomprobación indica `false` | Esa función queda desactivada. Comparte las líneas `YouTubeHideAds:` del registro. |
| Un interruptor del feed no parece funcionar | Recarga el feed; las eliminaciones se aplican a componentes cargados de nuevo. |
| Deja de funcionar tras actualizar YouTube | YouTube puede haber cambiado sus clases internas. Comparte el registro con la versión de YouTube o copia el informe de Compatibilidad y diagnóstico. |

## Créditos

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed), [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BrainfuckCC](https://github.com/MrxSiN/BrainfuckCC), [SponsorBlock](https://sponsor.ajay.app), [Override92/AiSList](https://github.com/Override92/AiSList) y [Morphe Patches](https://github.com/MorpheApp/morphe-patches) ([aviso conservado](LICENSES/Morphe-NOTICE.txt)). El material nuevo del proyecto es GPL-3.0-or-later; consulta [NOTICE](NOTICE) para los términos de terceros.

## Aviso legal

No está afiliado a Google LLC ni a YouTube, ni cuenta con su respaldo o patrocinio. Se ofrece para uso educativo y personal. Las actualizaciones de YouTube pueden romper los hooks sin previo aviso.
