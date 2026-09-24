# Changelog

## 2.2.1 — 2026-09-24

### Corrigido
- Corrige falso positivo da **verificação profunda de integridade** observado em arquivos reais no Windows.
- A versão 2.2.0 usava FFmpeg com `-c copy -f hash`, comparando a representação comprimida dos pacotes do primeiro stream de áudio. Alguns contêineres/arquivos podem reescrever detalhes de empacotamento ao salvar metadados sem alterar as amostras audíveis, levando ao cancelamento seguro porém desnecessário.
- A verificação profunda agora decodifica o primeiro stream e o converte deterministicamente para `pcm_s32le` antes do SHA-256 (`-f hash`), comparando o **conteúdo de áudio decodificado** e ignorando timestamps/metadados.
- A escolha de PCM s32 preserva mais precisão que o padrão s16 do muxer `hash` do FFmpeg, cobrindo adequadamente fontes lossless de 24/32 bits sem reduzir a verificação para 16 bits.
- Mantida a função pública `audio_stream_hash()` como alias compatível para não quebrar integrações 2.x; sua semântica passa a ser o hash do conteúdo PCM decodificado.
- Mensagens da GUI foram atualizadas para explicar que a comparação é do áudio decodificado, não dos bytes do stream/contêiner.
- Timeout da verificação profunda ganhou piso mais conservador para arquivos longos/de baixo bitrate, preservando um teto finito contra travamentos.

### Validação
- Suíte ampliada para **70 testes automatizados**.
- Nova regressão garante que a verificação profunda não volte a usar `-c copy` e exige `pcm_s32le`.
- Nova regressão confirma que áudio realmente diferente continua produzindo hash diferente.
- Nova regressão confirma compatibilidade da API legada `audio_stream_hash()`.
- Nova regressão prova que duas codificações FLAC lossless diferentes do mesmo PCM têm hashes comprimidos distintos, mas o novo hash decodificado permanece idêntico.

## 2.2.0 — 2026-09-23

### Identificação e consenso
- Adicionada confirmação local por idioma e amostra vocal com `faster-whisper` opcional; o áudio permanece local nessa etapa.
- Amostragem adaptativa de aproximadamente 28–30 s em regiões internas da faixa, com até três tentativas e parada antecipada quando há evidência suficiente.
- Integração LRCLIB sem chave para confirmar o candidato por letra normal ou sincronizada.
- LRCLIB tenta primeiro `/api/get` e, quando não há correspondência exata, usa `/api/search` com ranking por título, artista, álbum e duração.
- Comparação de letra com janela deslizante e reforço por timestamps quando disponíveis.
- Discogs opcional como segunda opinião de release via `PYMETAUDIO_DISCOGS_TOKEN`.
- Relação explícita MusicBrainz → Discogs (`url-rels`) é preferida ao lookup textual quando disponível, reduzindo ambiguidade e requests.
- Confiança separada para identidade, título/artista, recording, release, capa, idioma e letra.
- Corrigida atualização da confiança por campo no modo manual após confirmação acústica posterior.
- Busca manual de uma música específica por título/artista, com confirmação acústica independente quando Chromaprint/AcoustID está disponível; conflitos reduzem a confiança em vez de trocar silenciosamente o candidato.
- Preservada a semântica de confiança 2.1.x quando as novas fontes não participam.

### Lote, cache e desempenho
- Nova aba de identificação em lote com subpastas, cancelamento e progresso.
- Autoaplicação desligada por padrão e protegida por confirmação do usuário.
- Autoaplicação exige limiar de identidade e limiar independente de release.
- Capas de fallback com confiança inferior ao limiar são preservadas para revisão, sem impedir a aplicação de metadados seguros.
- Resultado do lote exibe confiança de música, edição, capa, idioma e letra.
- Cache SQLite WAL de fingerprint e transcrição curta produzidos localmente, com fechamento explícito das conexões para evitar vazamento de handles em lotes longos.
- Schema do cache evoluído para v2 com migração não destrutiva e assinatura do modelo/algoritmo de transcrição para invalidar apenas transcrições incompatíveis, preservando fingerprints úteis.
- Invalidação de cache quando o arquivo muda, pruning por idade/quantidade e nenhum armazenamento de token ou letra remota completa.

### Rede, segurança e estabilidade
- LRCLIB implementa timeout, resposta máxima, throttling, retry controlado, `429 Retry-After` e redirect restrito ao host permitido.
- Discogs implementa timeout, resposta máxima, retry/backoff, `429 Retry-After` e redirect restrito.
- MusicBrainz/AcoustID ganharam retry central finito para `429`, `5xx` e falhas transitórias de rede, com `Retry-After` limitado/backoff e sem ampliar a allowlist SSRF.
- URLs de LRCLIB/Discogs rejeitam credenciais embutidas e normalizam hosts antes de qualquer request.
- Nenhuma credencial é embutida em código, cache ou log.
- Discogs não é persistido em cache por causa das regras próprias de dados/cache.
- AudD não foi adicionado ao núcleo; a identificação principal não depende de API paga.
- Logs rotativos passaram a JSON Lines estruturado e falhas inesperadas do lote ganham contexto de diagnóstico.

### Compatibilidade e distribuição
- Nova dependência opcional `[lyrics]` para `faster-whisper`.
- Pillow limitado a `>=10.4,<12` para conviver melhor com ambientes que ainda usam dependências de vídeo restritas a Pillow 11.x, sem perder APIs usadas pelo projeto.
- CI inclui Linux, Windows e macOS, além de Python 3.14 e smoke do extra de letras.
- Adicionados PyInstaller `onedir`, script Windows, Inno Setup e gerador `.deb` nativo da arquitetura.
- Build nativo continua obrigatório: PyInstaller não é cross-compiler.

### Validação
- **66 testes automatizados passando**.
- Suítes `python -W error -m pytest` e `python -X dev -W error -m pytest` passam sem ResourceWarnings.
- `python -m compileall -q .`, `bash -n packaging/linux/build-deb.sh` e `pymetaaudio-doctor` validados no ambiente local.
- Novas regressões cobrem fallback/ranking LRCLIB, migração de cache, vínculo MusicBrainz↔Discogs, credenciais embutidas em URL, refresh de confiança manual, retries HTTP e log estruturado.


## 2.1.2 - 2026-09-23

### Corrigido

- Corrige `_tkinter.TclError: image "pyimageN" doesn't exist` na prévia de capas em Windows/Python 3.14.
- Remove o uso de `CTkImage` apenas da prévia dinâmica de capa e passa a usar `ImageTk.PhotoImage` com `master=self.root` explícito.
- Mantém referência forte da imagem durante a exibição e limpa o handle Tk com `image=""`.
- Atualiza texto + imagem da prévia em uma única chamada ao widget, evitando estado intermediário com handle Tcl inválido.
- Adiciona 2 testes de regressão; suíte total passa para 48 testes.
- Smoke test Tcl/Tk executado com 200 ciclos de exibição/remoção de capa sem erro.

## 2.1.1 - 2026-09-23

### Corrigido

- Corrige `NameError: name 'entry' is not defined` ao usar **Identificar música e buscar capa**.
- Corrige o mesmo defeito latente em **Salvar com proteção**.
- Centraliza a leitura dos campos da GUI em `_collect_form_metadata()`, evitando divergência entre callbacks.
- Adiciona tratamento defensivo para campos ausentes/inválidos sem deixar a exceção escapar para o callback do Tkinter.
- Adiciona testes de regressão específicos para a coleta de metadados da interface.

## 2.1.0 — 2026-09-23

### Identificação inteligente e capas online
- Adiciona MusicBrainz para identificação e enriquecimento de metadados.
- Adiciona Cover Art Archive para capa frontal de release/release-group.
- Adiciona fingerprint acústico opcional via Chromaprint/fpcalc + AcoustID.
- O áudio permanece local; somente fingerprint/duração são enviados ao AcoustID.
- Fallback por título/artista e heurística segura `Artista - Título` no nome do arquivo.
- Ranking de releases usa status oficial, álbum/ano já existentes, tipo e data; compilações recebem menor prioridade quando não há evidência específica.
- Ambiguidade entre várias edições é explicitamente informada.
- Resultado online exige confirmação e nunca salva automaticamente no arquivo.
- Limite global de aproximadamente 1 requisição/s ao MusicBrainz e User-Agent identificável.
- Downloads de capa têm limite de 25 MB, validação Pillow e allowlist de hosts/redirecionamentos.
- Fingerprint acústico pode ser cancelado durante a execução do `fpcalc`; o subprocesso é encerrado com segurança.
- Cliente AcoustID possui limitador global interno para respeitar o teto público de 3 requisições/s.

### Segurança, concorrência e regressões
- Corrige risco de deadlock de FFmpeg unificando stdout/stderr no leitor de progresso.
- Restauração passa a ter rollback automático após falha pós-substituição.
- Detecta alterações externas durante a preparação do salvamento e durante restaurações, evitando sobrescrever mudanças concorrentes.
- Rollback pós-commit agora verifica o SHA-256 do destino e é bloqueado se outro programa tiver alterado o arquivo nessa janela, preservando a edição externa e o backup verificado.
- Redirecionamentos para subdomínios `archive.org` são aceitos somente na política de capas; APIs JSON permanecem restritas aos hosts exatos autorizados.
- Leitura de capa local verifica tamanho antes de carregar os bytes completos.
- Troca de capa preserva comentários ID3 descritos, artes ID3/FLAC não-frontais e dados não gerenciados.
- Runtime YouTube agora valida versão mínima real (Deno >= 2.3, Node >= 22, QuickJS compatível), em vez de apenas presença no PATH.
- Operações de identificação e salvamento do mesmo arquivo são mutuamente bloqueadas na GUI.
- Suíte ampliada para 44 testes automatizados.
- Faixa de Pillow relaxada para `>=10.4,<13`, evitando conflito desnecessário com aplicações que ainda dependem de Pillow 11.x sem perder as APIs utilizadas pelo projeto.

## 2.0.0 — 2026-09-23

### Segurança e integridade
- Salvamento transacional: o arquivo original não é editado diretamente.
- Backup versionado com SHA-256 e retenção configurável.
- Cópia temporária no mesmo filesystem e substituição final com `os.replace`.
- Rollback automático caso a validação final falhe depois da substituição.
- Validação estrutural de formato, duração, sample rate e canais.
- Verificação profunda opcional do fluxo de áudio via FFmpeg `-c copy` + SHA-256.
- Verificação de espaço livre antes de iniciar uma transação.
- Validação de capas JPEG/PNG, limite de tamanho e proteção contra imagens excessivamente grandes.

### Metadados
- Adaptadores explícitos para MP3, WAV, FLAC, OGG Vorbis, OPUS, M4A/MP4 e WMA/ASF.
- AAC bruto ADTS/ADIF detectado como somente leitura, evitando gravação enganosa/insegura.
- Capas corretas por formato: APIC, FLAC Picture, `metadata_block_picture`, `covr` e `WM/Picture`.
- MIME JPEG/PNG preservado corretamente.
- Campos vazios removem somente as tags controladas pelo aplicativo.
- Tags desconhecidas são preservadas.
- ID3v2.4 existente é preservado; arquivos novos/legados usam v2.3 por padrão.
- Compositor e comentário passam a ser gravados de forma consistente.

### Vídeo e YouTube
- Extração de áudio de vídeos locais para MP3, FLAC, M4A, OPUS e WAV.
- Conversão YouTube → MP3 com yt-dlp, FFmpeg e EJS; Deno é priorizado, com fallback para Node/QuickJS.
- Rejeição de lives/transmissões agendadas, `noplaylist`, timeout/retries, progresso e cancelamento.
- Metadados e thumbnail incorporados quando disponíveis.
- Nomes de saída não sobrescrevem silenciosamente arquivos existentes e temporários de conversão são exclusivos por operação.

### Arquitetura e qualidade
- Projeto dividido em motor de metadados, segurança, mídia, imagem, modelos e GUI.
- Trabalho pesado executado fora da thread principal.
- Comunicação de workers para Tk por `queue.Queue`, sem chamadas Tk diretas a partir dos workers.
- Log rotativo de diagnóstico em `~/.pymetaaudio/logs/pymetaaudio.log`.
- Pyproject, dependências de desenvolvimento, suíte pytest e workflow de CI.
- Comando `pymetaaudio-doctor` para diagnóstico estruturado do ambiente.
