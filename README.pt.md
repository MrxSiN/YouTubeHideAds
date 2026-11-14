<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · **Português** · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**Um módulo Xposed que remove os anúncios do YouTube, com cada decisão escrita em Brainfuck e o resto em XAX.**

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](README.md#install)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-EA4AAA?logo=githubsponsors&logoColor=fff&style=for-the-badge)](https://github.com/sponsors/MrxSiN)

<img src="docs/images/settings-ads.png" width="240" alt="Ads and SponsorBlock settings">
<img src="docs/images/settings-player.png" width="240" alt="Player settings">
<img src="docs/images/settings-feed.png" width="240" alt="Feed and blacklist settings">

</div>

## Recursos

- **Anúncios removidos antes de aparecerem:** anúncios de vídeos e Shorts, anúncios do feed e da pesquisa, promoções do Premium e em tela cheia. Sem espaços em branco.
- **SponsorBlock integrado**, com segmentos coloridos na barra de progresso e um botão no player para pular manualmente, votar e enviar segmentos.
- **Player:** velocidade e qualidade padrão, idiomas de legenda preferidos, reprodução em segundo plano, áudio original, lembrar a posição na transmissão ao vivo, tocar para avançar, repetição, um botão de velocidade e a contagem do Return YouTube Dislike.
- **Gestos:** deslize para o brilho à esquerda e para o volume à direita em tela cheia, nunca sobre o chat ao vivo, os painéis ou a folha Mais vídeos.
- **Feed:** oculte prateleiras de Shorts, posts, prévias, Playables e canais de IA, lista negra de canais e palavras-chave, e miniaturas do DeArrow.
- **Shorts:** oculte botões e painéis individuais e pule Shorts ao vivo.
- **Uma única página de configurações** em **Você → Configurações → YouTube Hide Ads**, no idioma do YouTube (10 idiomas).

Os novos extras vêm desativados por padrão. Todas as configurações e seus padrões estão na [documentação](docs/README.md#settings-and-defaults).

## Instalação

1. Baixe o APK em [Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) ou em [modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Ative-o no [Vector](https://github.com/JingMatrix/Vector) ou no LSPosed (API libxposed 102) com o YouTube no escopo.
3. Force a parada do YouTube e abra-o de novo.

Requer Android 9 ou mais recente em arm64, e root para o framework. O módulo em si não pede nenhuma permissão.

## Compatibilidade

| YouTube | Módulo | Status |
|---|---|---|
| 21.45.88 | 1.3.0 (build 157) | ✅ Funcionando |
| 21.43.523 | 1.2.0 | ✅ Funcionando |
| 21.42.243 | 1.1.0 | ✅ Funcionando |

Testado em um Pixel 8 Pro com Android 17 e Vector 2.2. O YouTube renomeia suas classes internas na maioria das
atualizações. O módulo encontra seus alvos de novo pela estrutura e desativa um recurso em vez de adivinhar
quando não consegue. Histórico: [registro de alterações](CHANGELOG.md) · detalhes: [compatibilidade](docs/COMPATIBILITY.md).

## Limites conhecidos

- Apps que filtram HTTPS, como o AdGuard, podem bloquear o SponsorBlock, a verificação de atualizações, a contagem de dislikes e o DeArrow; veja [abaixo](README.md#sponsorblock-or-update-check-never-connects).
- O DeArrow substitui as miniaturas, não os títulos. O menu de velocidade do próprio YouTube continua mostrando 1x depois que uma velocidade padrão é aplicada.
- A qualidade padrão em dados móveis, os Shorts ao vivo e o bloqueio de legendas automáticas não foram testados em um celular.
- Verificado apenas no tema escuro e em um único celular. O texto novo da 1.3.0 está em inglês.

Tudo o que foi testado e o que não foi: [cobertura de recursos](docs/FEATURE_COVERAGE.md).

## Solução de problemas

| Problema | Tente |
|---|---|
| Nenhuma linha `YouTubeHideAds:` no log do framework | Verifique se o YouTube está no escopo e depois force a parada dele. |
| Uma chave do feed parece ignorada | Recarregue o feed. |
| Parou de funcionar depois de uma atualização do YouTube | Use **Sobre → Compatibilidade e diagnóstico → Relatar um problema**. |

### O SponsorBlock ou a verificação de atualizações nunca se conecta

Isso também vale para a contagem de dislikes e o DeArrow. O log mostra `NOT_ENOUGH_SCTS`. Um app que filtra HTTPS está reassinando a conexão, e a
verificação de transparência de certificados do YouTube a recusa. No AdGuard, adicione isto em **Filtragem HTTPS → Exclusões**:
`sponsor.ajay.app`, `github.com`, `returnyoutubedislikeapi.com`, `dearrow-thumb.ajay.app`. Depois reinicie o YouTube.

## Como funciona

O Brainfuck decide e o XAX age. Nove políticas em Brainfuck decidem, por exemplo, se um componente é um
anúncio, se um salto pode pular um segmento ou se um toque é um deslize. Elas são compiladas antecipadamente para
AArch64 pelo [BBC](https://github.com/MrxSiN/BBC). Hooks, descoberta, configurações e rede formam um único
repositório [XAX](https://github.com/MrxSiN/XAX), compilado para DEX. O repositório não tem código-fonte de aplicativo em Java, Kotlin ou C.

[Arquitetura](docs/ARCHITECTURE_BRAINFUCK_XAX.md) · [build](docs/BUILD.md) · [toda a documentação](docs/README.md) · [evidências](evidence/README.md)

## Apoio

Se o módulo é útil para você, pode [patrocinar o desenvolvimento](https://github.com/sponsors/MrxSiN).

## Créditos e licença

[DexKit](https://github.com/LuckyPray/DexKit), [libxposed](https://github.com/libxposed/api),
[Vector](https://github.com/JingMatrix/Vector), [SponsorBlock](https://sponsor.ajay.app),
[Return YouTube Dislike](https://returnyoutubedislike.com), [DeArrow](https://dearrow.ajay.app),
[AiSList](https://github.com/Override92/AiSList) (CC BY-NC 4.0, não incluído) e
[Morphe Patches](https://github.com/MorpheApp/morphe-patches), usado como referência de comportamento
([aviso](LICENSES/Morphe-NOTICE.txt)).

GPL-3.0-or-later. Veja [NOTICE](NOTICE) e a [origem do código upstream](docs/UPSTREAM_PROVENANCE.md).
Este projeto não é afiliado ao Google nem ao YouTube.
