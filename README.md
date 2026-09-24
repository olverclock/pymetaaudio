<div align="center">

# 🎵 PyMetaAudio

### Editor profissional de metadados, identificação musical e processamento de áudio

**Edite, identifique, confirme e organize músicas com proteção contra corrupção, identificação em múltiplas camadas e processamento em lote.**

[![Versão](https://img.shields.io/badge/vers%C3%A3o-2.2.1-2ea44f)](https://github.com/olverclock/PyMetaAudio)
[![Python](https://img.shields.io/badge/Python-3.10%20%E2%80%93%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/olverclock/PyMetaAudio/actions/workflows/ci.yml/badge.svg)](https://github.com/olverclock/PyMetaAudio/actions/workflows/ci.yml)
[![Testes](https://img.shields.io/badge/testes-70%20automatizados-success)](./CHANGELOG.md)
[![Plataformas](https://img.shields.io/badge/plataformas-Windows%20%7C%20Linux%20%7C%20macOS-informational)](#compatibilidade)

**Desenvolvido por [olverclock](https://github.com/olverclock)**

</div>

---

## 🧭 Navegação

- [Sobre o projeto](#-sobre-o-projeto)
- [Principais recursos](#-principais-recursos)
- [Formatos suportados](#-formatos-suportados)
- [Identificação inteligente](#-identificação-inteligente)
- [Proteção contra corrupção](#-proteção-contra-corrupção)
- [Identificação em lote](#-identificação-em-lote)
- [Vídeo → áudio](#-vídeo--áudio)
- [YouTube → MP3](#️-youtube--mp3)
- [Instalação](#-instalação)
- [Configuração](#️-configuração)
- [Privacidade](#-privacidade)
- [Diagnóstico e logs](#-diagnóstico)
- [Windows `.exe`](#-windows-exe--instalador)
- [Linux `.deb`](#-linux-deb)
- [Testes](#-desenvolvimento-e-testes)
- [Compatibilidade](#-compatibilidade)
- [Histórico](#️-histórico-de-versões)

---

## 📌 Sobre o projeto

O **PyMetaAudio 2.2.1** é uma evolução completa do editor original de metadados. Além de editar título, artista, álbum, ano, gênero, número de faixa, compositor, comentários e capas, o projeto agora inclui:

- proteção transacional contra corrupção;
- identificação acústica por **Chromaprint + AcoustID**;
- metadados e identidade musical pelo **MusicBrainz**;
- confirmação opcional de release pelo **Discogs**;
- busca de capa pelo **Cover Art Archive**;
- identificação de idioma e transcrição local com **faster-whisper**;
- confirmação por letra utilizando **LRCLIB**;
- motor de evidências com confiança separada por campo;
- identificação manual e em lote;
- extração de áudio de vídeos locais;
- conversão autorizada de vídeos do YouTube para MP3;
- cache local SQLite;
- logs estruturados e ferramenta de diagnóstico.

O objetivo é melhorar a qualidade dos metadados **sem alterar desnecessariamente o conteúdo de áudio** e sem depender de APIs pagas no núcleo do projeto.

> [!IMPORTANT]
> Informações encontradas online não são consideradas automaticamente “100% corretas”. O PyMetaAudio separa a confiança da **música/gravação**, do **release/álbum** e da **capa**, porque uma mesma gravação pode existir em singles, coletâneas, remasters e edições diferentes.

---

## 🖼️ Interface

<p align="center">
  <img src="https://github.com/olverclock/PyMetaAudio/blob/main/PyMetaAudio.png?raw=true" alt="Interface do PyMetaAudio" width="850">
</p>

> A captura acima pode representar uma versão anterior da interface. A série 2.2.x possui novas áreas de identificação, mídia e processamento em lote.

---

## ✨ Principais recursos

| Área | Recursos |
|---|---|
| 🏷️ **Metadados** | título, artista, álbum, artista do álbum, ano, gênero, faixa, total de faixas, compositor e comentário |
| 🖼️ **Capas** | visualizar, adicionar, remover, preservar artes secundárias e buscar capa online |
| 🧠 **Identificação** | Chromaprint, AcoustID, MusicBrainz, Discogs opcional, idioma, letra e consenso |
| 🎤 **Letra/idioma** | faster-whisper local + LRCLIB, com amostragem vocal adaptativa |
| 📂 **Lote** | identificar pastas/subpastas, progresso, cancelamento, cache e revisão por confiança |
| 🎬 **Vídeo local** | extrair áudio para MP3, FLAC, M4A, OPUS e WAV |
| ▶️ **YouTube** | conversão para MP3 via yt-dlp + FFmpeg para conteúdo autorizado |
| 🔒 **Integridade** | backup SHA-256, temporário, validação, troca segura e rollback |
| 🧰 **Diagnóstico** | `pymetaaudio-doctor`, logs JSON Lines e detecção de dependências |
| 📦 **Distribuição** | infraestrutura de build para Windows `.exe`/Setup e Linux `.deb` |

---

## 🎵 Formatos suportados

| Formato | Extensão | Metadados | Capa | Situação |
|---|---|---:|---:|---|
| MP3 | `.mp3` | ✅ ID3 | ✅ APIC | leitura e escrita |
| FLAC | `.flac` | ✅ Vorbis Comments | ✅ FLAC Picture | leitura e escrita |
| OGG Vorbis | `.ogg` | ✅ Vorbis Comments | ✅ | leitura e escrita |
| OPUS | `.opus` | ✅ Vorbis Comments | ✅ | leitura e escrita |
| M4A / MP4 | `.m4a`, `.mp4` | ✅ MP4 atoms | ✅ `covr` | leitura e escrita |
| WAV | `.wav` | ✅ ID3 quando suportado | ✅ quando disponível | leitura e escrita |
| WMA / ASF | `.wma` | ✅ ASF | ✅ `WM/Picture` | leitura e escrita |
| AAC bruto | `.aac` | ⚠️ leitura | — | somente leitura quando tagging seguro não é suportado |

O projeto tenta preservar tags que não são gerenciadas diretamente pelo PyMetaAudio e também preserva ID3v2.4 existente quando possível.

---

# 🧠 Identificação inteligente

## Como funciona

```text
Arquivo de áudio
      │
      ▼
Mutagen
(tags já existentes)
      │
      ▼
Chromaprint / fpcalc
(fingerprint acústico local)
      │
      ▼
AcoustID
(fingerprint + duração)
      │
      ▼
MusicBrainz
(gravação, artista, release, faixa, ano...)
      │
      ├──────────────► Discogs opcional
      │                (segunda opinião do release)
      │
      ▼
faster-whisper local
(idioma + amostra vocal)
      │
      ▼
LRCLIB
(letra do candidato)
      │
      ▼
Motor de evidências
      │
      ▼
Cover Art Archive
(capa do release/release-group)
```

### Fingerprint acústico

Quando `fpcalc` e uma chave AcoustID estão disponíveis, o PyMetaAudio calcula a impressão acústica **localmente**. Para a consulta normal ao AcoustID são enviados o fingerprint e a duração — não o arquivo de áudio completo.

### MusicBrainz

O MusicBrainz é a principal referência para:

- título;
- artista;
- gravação;
- álbum/release;
- artista do álbum;
- data/ano;
- número da faixa;
- total de faixas;
- gênero quando disponível;
- release-group e relações externas.

### Discogs opcional

O Discogs funciona como **segunda opinião**, principalmente para confirmar o release. Se o MusicBrainz já possuir uma relação explícita com um release do Discogs, esse vínculo é preferido à pesquisa textual.

O Discogs não é obrigatório para o restante do programa.

### Idioma e letra

Com o extra opcional de letras instalado, o PyMetaAudio pode usar `faster-whisper` localmente para:

1. analisar regiões internas da música;
2. detectar o idioma e sua probabilidade;
3. transcrever uma amostra vocal de aproximadamente **28–30 segundos**;
4. comparar o trecho com a letra do candidato obtida no LRCLIB;
5. adicionar essa evidência ao resultado final.

O programa pode testar até três regiões da música e encerrar antecipadamente quando já possui evidência suficiente.

---

## 📊 Confiança por evidência

O PyMetaAudio evita transformar evidências diferentes em um único “número mágico”. O resultado pode apresentar separadamente:

- **música / identidade**;
- **artista**;
- **título**;
- **gravação**;
- **álbum / release**;
- **ano**;
- **capa**;
- **idioma**;
- **similaridade da letra**.

Exemplo conceitual:

```text
Música / identidade      99%
Artista                  99%
Título                   99%
Gravação                 98%
Álbum / release          92%
Capa                     88%
Idioma                   97%
Letra                    95%
```

Uma música pode estar praticamente confirmada e ainda haver dúvida sobre qual **edição física/digital** ou qual **capa específica** é a correta. Nesses casos o PyMetaAudio sinaliza a ambiguidade em vez de sobrescrever informações com falsa certeza.

---

# 🔒 Proteção contra corrupção

A gravação de metadados utiliza um fluxo transacional.

Ao salvar, o PyMetaAudio:

1. registra o estado inicial do arquivo;
2. calcula digests de proteção;
3. cria backup versionado;
4. verifica o SHA-256 do backup;
5. cria um temporário no mesmo sistema de arquivos;
6. grava os metadados somente no temporário;
7. reabre e valida o arquivo modificado;
8. opcionalmente compara o conteúdo de áudio decodificado;
9. verifica se outro programa alterou o original durante a operação;
10. substitui o original com `os.replace` quando seguro;
11. valida novamente após a troca;
12. executa rollback somente quando isso não apagaria alterações externas.

## Verificação profunda da v2.2.1

A partir da **v2.2.1**, o hash profundo é calculado sobre o áudio **decodificado em PCM `s32le`**, em vez dos pacotes comprimidos do contêiner.

Isso corrige falsos positivos em casos nos quais os bytes internos do stream mudam, mas as amostras reproduzidas continuam idênticas.

```text
Original   → FFmpeg → PCM s32le → SHA-256
Temporário → FFmpeg → PCM s32le → SHA-256
                              │
                              ▼
                         comparação
```

Se o áudio decodificado realmente mudar, a operação continua sendo bloqueada.

Os backups ficam, por padrão, em uma pasta `.pymetaaudio-backups` ao lado do arquivo original.

---

# 📂 Identificação em lote

A aba **Identificação em lote** permite selecionar uma pasta e processar também suas subpastas.

Recursos:

- fila controlada;
- progresso por arquivo;
- cancelamento;
- cache local;
- reaproveitamento de fingerprint/transcrição;
- rate limits centralizados;
- confiança separada para identidade, release e capa;
- resultados incertos marcados para revisão;
- autoaplicação **desativada por padrão**.

Quando a autoaplicação é habilitada, os limiares de identidade e release são avaliados separadamente. Uma capa de baixa confiança pode ser preservada para revisão sem impedir a aplicação de metadados considerados seguros.

---

# 🔍 Identificação manual

Além do reconhecimento automático, é possível pesquisar uma música específica por título/artista e comparar o candidato com o arquivo local.

Quando disponíveis, entram na comparação:

- fingerprint;
- duração;
- MusicBrainz;
- Discogs;
- idioma;
- transcrição;
- letra.

Nada é gravado no arquivo apenas porque uma busca online encontrou um resultado. A edição continua dependendo da aplicação/confirmacão do usuário e do fluxo **Salvar com proteção**.

---

# 🎬 Vídeo → áudio

O PyMetaAudio utiliza FFmpeg para extrair áudio de vídeos locais.

Formatos de saída disponíveis:

- MP3;
- FLAC;
- M4A;
- OPUS;
- WAV.

As conversões utilizam temporários exclusivos e não sobrescrevem silenciosamente arquivos já existentes.

---

# ▶️ YouTube → MP3

O módulo utiliza **yt-dlp + FFmpeg** e detecta runtimes JavaScript compatíveis com as versões modernas do yt-dlp.

Runtimes suportados pelo projeto:

- Deno;
- Node.js compatível;
- QuickJS compatível.

> [!CAUTION]
> Utilize esse recurso somente para conteúdo próprio, licenciado, em domínio público ou para o qual você possua autorização de download/uso. O PyMetaAudio não remove DRM nem mecanismos de proteção de conteúdo.

---

# 🚀 Instalação

## Requisitos principais

- **Python 3.10 a 3.14**;
- `pip`;
- Windows, Linux ou macOS.

Para funções multimídia e identificação completa, também são recomendados:

- FFmpeg + ffprobe;
- Chromaprint / fpcalc.

---

## Instalação pelo código-fonte

```bash
git clone https://github.com/olverclock/PyMetaAudio.git
cd PyMetaAudio
python -m pip install -r requirements.txt
python PyMetaAudio.py
```

Também é possível instalar o projeto como pacote:

```bash
python -m pip install .
pymetaaudio
```

---

## Confirmação por idioma e letra

Esse recurso é opcional.

```bash
python -m pip install -r requirements-lyrics.txt
```

ou:

```bash
python -m pip install ".[lyrics]"
```

O `faster-whisper` baixa o modelo configurado quando necessário.

O modelo padrão do PyMetaAudio é:

```text
modelo: small
dispositivo: cpu
compute_type: int8
```

---

# ⚙️ Configuração

## AcoustID

Para identificação acústica pelo próprio áudio, configure uma chave de aplicação AcoustID:

### Windows PowerShell

```powershell
$env:PYMETAUDIO_ACOUSTID_KEY="SUA_CHAVE"
python .\PyMetaAudio.py
```

A chave também pode ser informada temporariamente na própria interface.

## Discogs opcional

```powershell
$env:PYMETAUDIO_DISCOGS_TOKEN="SEU_TOKEN"
```

ou, no Linux/macOS:

```bash
export PYMETAUDIO_DISCOGS_TOKEN="SEU_TOKEN"
```

O token não é armazenado no cache do PyMetaAudio.

## Whisper

```text
PYMETAUDIO_LYRICS_CONFIRMATION=1
PYMETAUDIO_WHISPER_MODEL=small
PYMETAUDIO_WHISPER_DEVICE=cpu
PYMETAUDIO_WHISPER_COMPUTE_TYPE=int8
```

Em máquinas NVIDIA compatíveis é possível optar por `cuda`, desde que a instalação local do faster-whisper/CTranslate2 seja compatível.

## Cache

Opcionalmente:

```text
PYMETAUDIO_CACHE_DIR=...
```

Locais padrão:

- Windows: `%LOCALAPPDATA%\PyMetaAudio\Cache`;
- Linux/macOS: `$XDG_CACHE_HOME/pymetaaudio` ou `~/.cache/pymetaaudio`.

> [!TIP]
> O arquivo `.env.example` documenta as variáveis aceitas, mas contém apenas placeholders. Nunca publique chaves reais no repositório.

---

# 🌐 Serviços utilizados

| Serviço | Função | Obrigatório | Pago no núcleo? |
|---|---|---:|---:|
| Chromaprint / fpcalc | fingerprint local | não | não |
| AcoustID | reconhecimento do fingerprint | não | não para o fluxo público compatível com seus termos |
| MusicBrainz | identidade e metadados | identificação online | não |
| Cover Art Archive | capas | não | não |
| Discogs | segunda opinião do release | não | não para o fluxo configurado pelo usuário, sujeito aos termos do serviço |
| faster-whisper | idioma/transcrição local | não | não |
| LRCLIB | confirmação por letra | não | não |
| AudD | — | não usado | **não faz parte do núcleo** |

O projeto foi desenhado para não depender de uma API paga para sua identificação principal.

---

# 🔐 Privacidade

- O `faster-whisper` processa a amostra de áudio **localmente**.
- No fluxo AcoustID, o programa envia fingerprint e duração, não o arquivo completo.
- Chaves AcoustID e tokens Discogs não são gravados no cache SQLite.
- Respostas completas do Discogs não são persistidas no cache.
- A letra remota completa não é mantida como histórico permanente pelo mecanismo de cache.
- Logs estruturados não adicionam automaticamente tokens como campos.

Consulte também [`SECURITY.md`](./SECURITY.md).

---

# 💾 Cache local

O cache utiliza **SQLite em modo WAL** para reaproveitar análises locais mais caras, como fingerprint e transcrição curta.

Características:

- invalidação quando o arquivo muda;
- migrações não destrutivas;
- retenção limitada;
- reutilização entre operações;
- assinatura do modelo/algoritmo de transcrição;
- nenhuma credencial armazenada.

---

# 🩺 Diagnóstico

Depois de instalar como pacote, execute:

```bash
pymetaaudio-doctor
```

Ou diretamente pelo módulo:

```bash
python -m pymetaaudio.doctor
```

O diagnóstico informa a disponibilidade de:

- Python;
- PyMetaAudio;
- Mutagen;
- Pillow;
- CustomTkinter;
- yt-dlp;
- FFmpeg;
- ffprobe;
- fpcalc / Chromaprint;
- faster-whisper;
- runtime JavaScript;
- identificação acústica;
- confirmação por letra;
- Discogs.

Valores de tokens não são exibidos.

---

# 📜 Logs

Os logs rotativos ficam em:

```text
~/.pymetaaudio/logs/pymetaaudio.log
```

Formato: **JSON Lines**.

Podem incluir:

- timestamp;
- nível;
- módulo;
- função;
- linha;
- mensagem;
- contexto de exceção.

Antes de publicar logs em uma Issue, remova caminhos pessoais e outros dados privados.

---

# 🪟 Windows `.exe` / instalador

A infraestrutura está em:

```text
packaging/windows/
```

Inclui:

- `PyMetaAudio.spec` — configuração PyInstaller `onedir`;
- `build.ps1` — build Windows;
- `installer.iss` — instalador Inno Setup.

Para incluir ferramentas externas no build, `PYMETAUDIO_BUNDLE_TOOLS_DIR` pode apontar para uma pasta contendo:

```text
ffmpeg.exe
ffprobe.exe
fpcalc.exe
```

> PyInstaller não é cross-compiler. O `.exe` final deve ser construído e testado no Windows.

---

# 🐧 Linux `.deb`

O projeto contém:

```text
packaging/linux/build-deb.sh
```

Execute em Debian/Ubuntu na arquitetura desejada:

```bash
chmod +x packaging/linux/build-deb.sh
./packaging/linux/build-deb.sh
```

A saída será semelhante a:

```text
dist-deb/pymetaaudio_2.2.1_amd64.deb
```

ou, em uma máquina ARM64:

```text
dist-deb/pymetaaudio_2.2.1_arm64.deb
```

O `.deb` deve ser construído/testado nativamente na arquitetura de destino.

---

# 🧪 Desenvolvimento e testes

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute:

```bash
python -m pytest
python -m compileall -q .
python -m ruff check .
```

Validação registrada para a **v2.2.1**:

- **70 testes automatizados**;
- `python -W error -m pytest`;
- `python -X dev -W error -m pytest`;
- `compileall`;
- regressões de GUI;
- round-trip de formatos;
- rollback;
- concorrência;
- cache/migrações;
- rede/retries;
- redirects/SSRF;
- identificação e letras;
- lote/cancelamento;
- verificação PCM da integridade do áudio.

A CI está configurada para Windows, Linux e macOS, cobrindo versões modernas do Python usadas pelo projeto.

---

# ✅ Compatibilidade

| Ambiente | Código-fonte / CI | Distribuição nativa |
|---|---:|---:|
| Windows 10/11 x64 | ✅ | 🧰 infraestrutura `.exe`/Setup pronta para build nativo |
| Linux amd64 | ✅ | 🧰 gerador `.deb` disponível |
| Linux ARM64 | código compatível | 🧰 `.deb` pode ser gerado nativamente em ARM64 |
| macOS | ✅ CI | código-fonte/pacote Python; sem instalador nativo incluído |
| Python 3.10–3.14 | ✅ alvo do projeto | depende das wheels das bibliotecas no sistema usado |

---

# ⚠️ Avisos comuns no Windows

## `GoogleDriveFSPipe...UNAVAILABLE_RESOURCE`

Essa mensagem pode vir da extensão de shell do **Google Drive para computador** quando um diálogo nativo do Windows consulta integrações do Explorer.

Ela não é gerada pelo mecanismo de gravação do PyMetaAudio.

## `You are sending unauthenticated requests to the HF Hub`

Pode aparecer ao obter um modelo público usado pelo faster-whisper.

Um `HF_TOKEN` não é necessário para modelos públicos, embora uma conta autenticada possa oferecer limites maiores de download conforme as regras do serviço.

---

# 🛡️ Uso responsável e limitações

- O PyMetaAudio não remove DRM.
- Identificação musical não é infalível.
- Releases diferentes podem compartilhar a mesma gravação.
- A capa correta depende da confiança no release identificado.
- APIs e serviços externos podem ficar temporariamente indisponíveis.
- O processamento em lote não deve aplicar automaticamente resultados de baixa confiança.
- YouTube → MP3 deve ser usado somente quando o usuário tiver direito de baixar/converter o conteúdo.

---

# 🗂️ Estrutura do projeto

```text
PyMetaAudio/
├── PyMetaAudio.py
├── pymetaaudio/
│   ├── batch.py
│   ├── cache.py
│   ├── config.py
│   ├── discogs.py
│   ├── doctor.py
│   ├── gui.py
│   ├── image_utils.py
│   ├── logging_config.py
│   ├── lyrics.py
│   ├── media_tools.py
│   ├── metadata_engine.py
│   ├── models.py
│   ├── online_metadata.py
│   ├── safety.py
│   └── transcription.py
├── tests/
├── packaging/
│   ├── windows/
│   └── linux/
├── .github/workflows/ci.yml
├── requirements.txt
├── requirements-lyrics.txt
├── requirements-dev.txt
├── pyproject.toml
├── SECURITY.md
├── THIRD_PARTY_NOTICES.md
├── CHANGELOG.md
└── README.md
```

---

# 📝 Histórico de versões

## v2.2.1

- Corrigida a verificação profunda de integridade para comparar o **áudio decodificado em PCM s32le**.
- Eliminado falso cancelamento provocado por diferenças de empacotamento/compressão sem alteração sonora.
- Mantida compatibilidade da API `audio_stream_hash()`.
- Suíte ampliada para **70 testes automatizados**.

## v2.2.0

- identificação por idioma e letra;
- LRCLIB;
- Discogs opcional;
- processamento em lote;
- cache SQLite;
- motor de evidências;
- builds Windows/Linux;
- retries e logs estruturados.

## v2.1.x

- identificação MusicBrainz/AcoustID;
- capas online;
- correções de concorrência;
- correções Tkinter/Python 3.14;
- endurecimento da gravação segura.

## v2.0.0

- arquitetura modular;
- escrita transacional;
- handlers explícitos por formato;
- vídeo → áudio;
- YouTube → MP3;
- testes, CI e diagnóstico.

Para o histórico completo, consulte [`CHANGELOG.md`](./CHANGELOG.md).

---

# 🔐 Segurança

Problemas de segurança devem ser tratados com cuidado para não expor arquivos pessoais, tokens ou dados privados.

Leia [`SECURITY.md`](./SECURITY.md) antes de publicar informações sensíveis em uma Issue.

---

# 📚 Documentação adicional

- [`CHANGELOG.md`](./CHANGELOG.md) — histórico detalhado;
- [`SECURITY.md`](./SECURITY.md) — modelo de segurança;
- [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) — componentes de terceiros;
- [`AUDITORIA-PyMetaAudio-v2.2.1.md`](./AUDITORIA-PyMetaAudio-v2.2.1.md) — auditoria técnica da versão;
- [`packaging/README.md`](./packaging/README.md) — geração de `.exe`, Setup e `.deb`.

---

# 🤝 Contribuindo

Contribuições, correções e sugestões são bem-vindas.

Antes de enviar um Pull Request:

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest
python -m compileall -q .
```

Ao relatar um problema, inclua quando possível:

- versão do PyMetaAudio;
- versão do Python;
- sistema operacional;
- saída relevante do `pymetaaudio-doctor`;
- traceback/log sem tokens, caminhos pessoais ou dados sensíveis.

[📝 Abrir uma Issue](https://github.com/olverclock/PyMetaAudio/issues)

---

<div align="center">

## ⭐ PyMetaAudio

**Metadados, identificação e integridade de áudio em uma única aplicação.**

Desenvolvido com ❤️ por **olverclock**

Se o projeto foi útil, considere deixar uma ⭐ no repositório.

</div>
