# Auditoria técnica — PyMetaAudio v2.2.1

Data: 2026-09-24

## Motivo da release

Foi reportado em Windows um cancelamento durante **Salvar com proteção** com a mensagem de que o hash do fluxo de áudio havia mudado. A proteção funcionou corretamente ao preservar o original, porém a condição podia ser um falso positivo da própria estratégia de verificação profunda.

## Causa raiz

Na v2.2.0, `SafeFileEditor.audio_stream_hash()` executava FFmpeg com `-c copy -f hash`. Isso mede os pacotes comprimidos entregues ao muxer de hash. Alterações legítimas de metadados/estrutura do contêiner podem, em determinados arquivos reais, mudar representação/empacotamento sem mudar as amostras de áudio reproduzidas.

Para um editor de metadados, a propriedade de segurança correta é: **o conteúdo de áudio decodificado deve permanecer idêntico**, não necessariamente todos os bytes comprimidos/empacotados usados pelo contêiner.

## Correção

A verificação profunda passou a:

1. selecionar somente o primeiro stream de áudio (`-map 0:a:0`);
2. decodificar o áudio com FFmpeg;
3. converter para PCM assinado de 32 bits (`pcm_s32le`);
4. calcular SHA-256 com o muxer `hash`;
5. comparar o digest antes, no temporário e depois do `os.replace`.

Timestamps e metadados não participam do digest. A validação estrutural de handler, duração, sample rate e canais continua independente. Backup SHA-256, verificação de concorrência, commit atômico e rollback seguro permanecem inalterados.

A função pública histórica `audio_stream_hash()` foi preservada como alias para a nova implementação, evitando quebra de integrações/tests externos.

## Segurança preservada

A mudança não relaxa a proteção contra alteração real do som. Se as amostras decodificadas mudarem, o SHA-256 muda e o commit continua sendo cancelado. Também permanecem:

- backup versionado verificado;
- temporário no mesmo filesystem;
- `fsync`;
- `os.replace`;
- validação pós-commit;
- proteção contra edição concorrente;
- rollback condicionado ao digest esperado;
- limites de espaço/tempo;
- validação de formatos e capas.

## Mensagens externas observadas

`GoogleDriveFSPipe...UNAVAILABLE_RESOURCE` é emitido pela integração de shell do Google Drive/Explorer do Windows e não participa do mecanismo de salvamento do PyMetaAudio. O aviso do Hugging Face sobre requisições não autenticadas pode aparecer ao baixar modelos públicos do faster-whisper; `HF_TOKEN` é opcional para modelos públicos e não é uma credencial exigida pelo PyMetaAudio.

## Validação

- 70 testes automatizados;
- regressão que proíbe `-c copy` na verificação profunda;
- regressão que exige conversão `pcm_s32le`;
- teste de áudio realmente diferente produzindo hashes diferentes;
- teste de compatibilidade do alias `audio_stream_hash()`;
- teste lossless demonstrando que representações FLAC comprimidas diferentes do mesmo PCM convergem para o mesmo hash de conteúdo;
- round-trip protegido continua cobrindo MP3, FLAC, OGG, OPUS, M4A, WAV e WMA;
- `compileall` e suíte rigorosa com warnings como erro são executados antes do empacotamento final.

## Conclusão

A v2.2.1 corrige a causa raiz do falso cancelamento sem desabilitar a verificação profunda e sem reduzir a proteção transacional. A validação passa a medir a propriedade que realmente importa para um editor de metadados: **as amostras de áudio decodificadas continuam idênticas**.
