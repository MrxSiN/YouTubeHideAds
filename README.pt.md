<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · **Português** · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**Um módulo Xposed que remove anúncios do YouTube, com cada decisão escrita em Brainfuck e o resto em XAX. Sim, é sério.**

Anúncios, Shorts patrocinados e promoções são removidos antes de o YouTube exibi-los, e os segmentos do SponsorBlock são pulados.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#requisitos)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> O YouTube renomeia suas classes ofuscadas em quase toda atualização. O módulo reencontra seus alvos pela estrutura a cada inicialização. Quando um papel está ausente ou é ambíguo, ele deixa o recurso como está em vez de adivinhar. Veja a tabela de [compatibilidade](#compatibilidade) para o que foi realmente testado.

## Por que Brainfuck? E o que é XAX?

- **Brainfuck decide.** Se um componente é anúncio, se o marketing do Premium pode sair, se o player pode pular para o fim de um segmento patrocinado, se um deslize muda o brilho. Brainfuck não pode chamar Android, Xposed, DexKit nem JNI: ele lê e escreve bytes, e o host só age diante de uma resposta exata e bem-sucedida.
- **XAX faz todo o resto.** Hooks, busca com DexKit, reflexão, a página de configurações e o HTTPS/JSON do SponsorBlock formam um único armazenamento semântico canônico do [XAX](https://github.com/MrxSiN/XAX). O compilador externo do XAX o transforma em DEX e assina o APK. Não há código de aplicativo em Java, Kotlin, C, Python ou shell neste repositório.

Também não é lento. As nove políticas são compiladas antecipadamente para bibliotecas compartilhadas AArch64 pelo [BBC](https://github.com/MrxSiN/BBC). O APK não tem interpretador.

|  | |
|---|---|
| 🧹 **Removido, não escondido** | Componentes de anúncio são substituídos antes de o YouTube montá-los, e Shorts patrocinados saem do feed antes de o player existir: sem espaços vazios nem clipes travados. |
| ⏭️ **SponsorBlock integrado** | Consultas por prefixo com repetição e cache limitados, modos e cores por categoria, pular e desfazer manuais, criação de segmentos e votos, exclusões, estatísticas e transferência de configurações. |
| 🔎 **Resiste a renomeações** | O DexKit encontra cada hook pela estrutura a cada inicialização. Um papel ausente ou ambíguo não instala nada para aquele recurso. |
| 🧠 **Políticas em Brainfuck, compiladas** | Nove programas escritos à mão e compilados para código nativo; políticas e controles do SponsorBlock são verificados a cada inicialização. |
| 🛟 **Falha de forma segura** | Se uma verificação falha, o recurso fica desligado. Erros de rede e tipos de reprodução desconhecidos nunca causam saltos. |
| ⚙️ **Configurações com visual nativo** | Uma seção própria **YouTubeHideAds** em **Você → Configurações**, acima de Conta, com as linhas do próprio YouTube, cada chave independente e uma página de Compatibilidade e diagnóstico. |
| 🎛️ **SponsorBlock dentro do player** | Um ícone do SponsorBlock ao lado da reprodução automática abre o mesmo menu flutuante da engrenagem de configurações; os segmentos ficam coloridos na barra de progresso. |
| 📱 **Shorts mais limpos** | Oculte botões e painéis específicos dos Shorts e pule transmissões ao vivo no feed de Shorts. |
| 👆 **Controles de deslize fáceis de ler** | Brilho à esquerda, volume à direita, numa cápsula com ícone, nível e valor. |
| 🌐 **Seu idioma** | Segue o idioma do YouTube: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia e Bahasa Melayu. |

---

## O que é removido

| Grupo | Configuração | Padrão |
|---|---|---|
| Anúncios | Anúncios em vídeo e nos Shorts · Anúncios do feed e da pesquisa · Promoções do Premium · Promoções em tela cheia | Ativado, sob a chave geral **Ocultar anúncios** |
| SponsorBlock | Patrocínios, autopromoção | Ativado |
| SponsorBlock | Lembretes de interação, introduções, encerramentos, prévias, enrolação, trechos sem música | Desativado |
| Conteúdo | Playables (seções de jogos, cards, entrada Explorar) | Oculto |
| Feed | Vídeos de prévia · Explorar mais temas · Postagens | Oculto |
| Feed | Shorts nos feeds | Visível |
| Feed | Canais de IA · Prováveis canais de IA ([AiSList](https://github.com/Override92/AiSList)) | Desativado |
| Player | Brilho por deslize (esquerda) · Volume por deslize (direita), só em tela cheia | Ativado |
| Player | Forçar o áudio original em vídeos com vários idiomas | Ativado |
| Player | Reprodução em segundo plano, incluindo vídeos para crianças | Ativado |
| Shorts | Gostei, comentários, compartilhar, remix, salvar, som, inscrever-se, título, sugestões e painéis de informações, botões ao pausar | Visível (cada um pode ser ocultado) |
| Shorts | Pular Shorts ao vivo | Desativado |

Desligar **Ocultar anúncios** não desliga os recursos de conteúdo e do player. Recarregue o feed depois de mudar suas chaves. O áudio original vale a partir da próxima lista de faixas e respeita uma escolha manual. Tabela completa: [configurações e padrões](docs/README.md#settings-and-defaults). A reprodução em segundo plano independe de Ocultar anúncios e do SponsorBlock; reinicie o YouTube depois de mudá-la. [Implementação e limites testados](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 Onde cada remoção acontece</b></summary>
<br>

| Superfície | Onde | O que faz |
|---|---|---|
| **Anúncios em vídeo** | ativação e layout de anúncios do player | Suprime o espaço de anúncio quando o Brainfuck confirma um sinal estrutural e uma transição segura. |
| **Anúncios do feed, da pesquisa e de compras** | o analisador de componentes, encontrado pelo DexKit | Substitui um componente pago confirmado pelo componente vazio do próprio YouTube. |
| **Shorts patrocinados** | resposta, inserção e dados iniciais do player de Shorts | Remove entradas de anúncio em vídeo ou imagem com seus dados de rastreamento antes de o player existir. |
| **Premium, tela cheia, painéis** | visão da oferta, diálogo em tela cheia, painel de engajamento por identificador tipado | Oculta superfícies de marketing sem mexer em benefícios ou no gerenciamento de assinatura. |
| **Seções do feed, Playables, canais de IA, componentes dos Shorts** | o mesmo hook de componentes | Remove só a seção, o card ou o botão correspondente; linhas de canal e playlists ficam. |
| **SponsorBlock** | pontes de salto/duração do player e barra de progresso nativa | Consultas por prefixo limitadas, modos por categoria, marcas coloridas, controles manuais e ações explícitas da comunidade. |

</details>

---

## Status

**v1.1.0** (versionCode 153) é a primeira versão desde a 1.0.0. Ela adiciona reprodução em segundo plano, uma seção própria nas Configurações do YouTube, uma página de Compatibilidade e diagnóstico, controles do SponsorBlock no estilo do YouTube, Ocultar componentes dos Shorts, Pular Shorts ao vivo, controles de deslize redesenhados e mais nove idiomas. Também está bem mais leve no telefone: as políticas em Brainfuck não reabrem mais o APK e os resultados do DexKit ficam em cache, então o YouTube abre cerca de 0,35 s mais rápido depois da primeira abertura. [Verificações no dispositivo](evidence/device_perf_20261028/README.md).

As versões de desenvolvimento entre as duas versões (111 a 153) estão no [registro de alterações](CHANGELOG.md), com as evidências de cada uma em [evidence](evidence/README.md).

### Compatibilidade

Testado em um Pixel 8 Pro com Android 17 e Vector 2.2 (libxposed API 102). Testou outra configuração? Abra um pull request adicionando uma linha.

| YouTube | Módulo | Status |
|---|---|---|
| 21.42.243 | 1.1.0 | ✅ Funciona |
| 21.41.525 | 1.0.0 | ✅ Funciona |

### Limites conhecidos

- Promoções do Premium, em tela cheia e de painéis só foram removidas em testes controlados dos hooks; casos reais ainda não apareceram.
- As seções de vídeos de prévia e de “Explorar mais temas” só são reconhecidas pelos títulos em inglês.
- As listas de canais de IA são mantidas pela comunidade e podem classificar canais errado; por isso vêm desligadas.
- A reprodução em segundo plano exige reiniciar o YouTube após mudar a opção e deixa os Shorts com o YouTube. Controles Bluetooth e chamadas recebidas não foram testados.
- Envio e votação do SponsorBlock não foram testados no servidor real. Veja [funções e limites](docs/SPONSORBLOCK_API_RESEARCH.md).
- Pular Shorts ao vivo ainda não encontrou um Short ao vivo real; essa função, a pílula de deslize e a troca de idioma do YouTube foram verificadas com sondas de desenvolvimento.
- As páginas do módulo só foram verificadas no tema escuro. Tema claro, tablets e layouts da direita para a esquerda não foram testados.
- A primeira abertura após atualizar o YouTube ou o módulo reconstrói o cache de hooks e demora cerca de 0,4 s a mais.
- Somente arm64-v8a. Só a configuração e as versões do YouTube acima foram testadas; o LSPatch não.

Detalhes: [cobertura de recursos](docs/FEATURE_COVERAGE.md) e [compatibilidade](docs/COMPATIBILITY.md).

## Requisitos

| | |
|---|---|
| **Android** | 9.0 (API 28) ou mais recente, arm64 |
| **App** | YouTube (`com.google.android.youtube`) |
| **Framework** | [Vector](https://github.com/JingMatrix/Vector) ou LSPosed com libxposed API 102 |
| **Root** | Exigido pelo Vector/LSPosed; o módulo não pede nenhuma permissão |

## Instalação

```
1. Instale o APK pelos Releases ou pelo repositório de módulos do Xposed
2. Ative o YouTubeHideAds no Vector ou LSPosed com o YouTube no escopo
3. Force a parada do YouTube uma vez e abra-o
```

Baixe em [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) ou em [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads). As configurações ficam em **YouTube → Você → Configurações → YouTubeHideAds**. Preferências e caches de IA ficam nos dados do próprio YouTube; limpar esses dados as redefine.

O registro do framework mostra o que aconteceu em linhas que começam com `YouTubeHideAds:`:

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## Como funciona

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

Uma única regra decide onde fica o código: **se mexe com YouTube, Android, rede ou JNI, o XAX faz; se decide agir sobre o que o XAX encontrou, o Brainfuck decide.** Detalhes das bibliotecas de políticas, do layout de bytes e da busca de hooks estão em [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md) e [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md).

A busca automática de segmentos envia só um prefixo SHA-256 de quatro dígitos hexadecimais do ID do vídeo. Resposta, número de registros e tempos limite são restritos, e redirecionamentos ficam desativados. Envios e votos manuais mandam ao servidor escolhido os dados necessários e a identidade privada; relatórios de visualização vêm desligados e exportações excluem o ID privado por padrão.

---

## Compilação

Este repositório não tem script de compilação. As versões são compiladas com ferramentas externas:

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

Cada entrada é fixada com BLAKE3 no armazenamento, então uma entrada diferente faz a compilação falhar. Para recompilar, use o [XAX](https://github.com/MrxSiN/XAX) com o perfil Android libxposed (commit `3cca599` ou o snapshot compatível branding-v2). Os passos estão em [`docs/BUILD.md`](docs/BUILD.md).

## Solução de problemas

| Problema | Tente |
|---|---|
| Nenhuma linha do módulo no registro | Confira se o módulo está ativo com o YouTube no escopo e force a parada do YouTube. |
| `UnsatisfiedLinkError` logo após atualizar | Espere a instalação terminar, force a parada e abra o YouTube de novo. |
| Uma verificação indica `false` | Esse recurso fica desligado. Envie as linhas `YouTubeHideAds:` do registro. |
| Uma chave do feed parece ignorada | Recarregue o feed; remoções valem para componentes carregados de novo. |
| Parou de funcionar após atualizar o YouTube | O YouTube pode ter mudado classes internas. Envie o registro com a versão do YouTube ou copie o relatório de Compatibilidade e diagnóstico. |

## Créditos

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed), [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BBC](https://github.com/MrxSiN/BBC), [SponsorBlock](https://sponsor.ajay.app), [Override92/AiSList](https://github.com/Override92/AiSList) e [Morphe Patches](https://github.com/MorpheApp/morphe-patches) ([aviso preservado](LICENSES/Morphe-NOTICE.txt)). O material novo do projeto é GPL-3.0-or-later; veja [NOTICE](NOTICE) para os termos de terceiros.

## Aviso legal

Sem afiliação, endosso ou patrocínio do Google LLC ou do YouTube. Fornecido para uso educacional e pessoal. Atualizações do YouTube podem quebrar os hooks sem aviso.
