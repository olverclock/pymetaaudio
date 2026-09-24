# Segurança — PyMetaAudio 2.2.1

## Modelo de confiança

O PyMetaAudio trata arquivos de mídia, imagens e respostas remotas como entradas não confiáveis. Dados online nunca são gravados no áudio sem passar pela interface/limiares configurados e pelo editor transacional.

## Arquivos e corrupção

- backups versionados com SHA-256;
- temporários no mesmo filesystem;
- `fsync` antes da troca;
- `os.replace` somente após validação;
- validação estrutural pós-commit;
- SHA-256 opcional do conteúdo de áudio decodificado em PCM s32, sem incluir metadados/bytes do contêiner;
- rollback condicionado ao digest esperado para não apagar alterações de terceiros;
- retenção limitada de backups;
- capas limitadas por bytes e pixels.

## Rede

Clientes internos usam HTTPS, timeout, limite de tamanho de resposta e host allowlist. Redirects de LRCLIB, Discogs, MusicBrainz e capas são validados antes de serem seguidos/aceitos. Credenciais embutidas em URLs são rejeitadas e retries são finitos, restritos a condições transitórias. Não são usados URLs remotos fornecidos diretamente pelo usuário nesses clientes.

## Credenciais

Aceitas somente por variável de ambiente ou campo temporário da GUI:

- `PYMETAUDIO_ACOUSTID_KEY`;
- `PYMETAUDIO_DISCOGS_TOKEN`.

Nenhuma chave é escrita no SQLite, arquivos de configuração ou logs. `.env.example` contém apenas placeholders.

## Transcrição local

`faster-whisper` é opcional e roda localmente. O modo manual também pode usar AcoustID para confirmar ou contradizer o candidato textual sem substituí-lo silenciosamente. O cache armazena no máximo uma transcrição curta/normalizada necessária para evitar recomputação; não armazena a letra completa recebida do LRCLIB.

## Lote

Gravação automática é opt-in. Mesmo ativada, exige confiança mínima de identidade e de release e usa o mesmo `SafeFileEditor` da edição manual. Uma capa abaixo do limiar de confiança não substitui automaticamente a capa existente; fica marcada para revisão.

## YouTube

URLs são restritas a hosts YouTube suportados; lives/agendamentos são rejeitados e o fluxo possui cancelamento e staging temporário.

## Logs e diagnóstico

O log rotativo usa JSON Lines com campos conhecidos e não serializa automaticamente dados arbitrários/segredos. `pymetaaudio-doctor` reporta capacidades sem imprimir os valores das credenciais.

## Reporte

Ao relatar um bug, remova tokens, caminhos pessoais e metadados privados dos logs antes de publicar a issue.
