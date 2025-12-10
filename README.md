# PyMetaAudio 🎵 **Editor Profissional de Metadados de Áudio com Interface Gráfica**

PyMetaAudio - Editor profissional de metadados de áudio com interface gráfica moderna. Edite título, artista, álbum, capa e mais em MP3, FLAC, M4A, OGG sem alterar a qualidade do som. Backup automático, compatível com Windows Media Player. Desenvolvido por olverclock em Python com CustomTkinter.

---

## 📋 Descrição

PyMetaAudio é um editor completo e robusto de metadados para arquivos de áudio com interface gráfica moderna. Permite editar informações como título, artista, álbum, capa e muito mais, **sem alterar a qualidade do áudio original**.

### ✨ Características Principais

- 🎨 **Interface gráfica moderna** com CustomTkinter (tema dark)
- 🎵 **Suporte a múltiplos formatos**: MP3, FLAC, OGG, M4A, AAC, WAV, WMA, OPUS
- 🖼️ **Editor de capas de álbum** (adicionar/remover/visualizar)
- 💾 **Backup automático** antes de qualquer edição
- 🔒 **Proteção contra corrupção** do arquivo original
- 🎯 **Edição lossless** - apenas metadados são modificados
- ✅ **Compatibilidade máxima** - tags ID3v2.3 para Windows Media Player e outros players

---

## 🖼️ Capturas de Tela

![Interface Principal](https://github.com/olverclock/pymetaaudio/blob/main/PyMetaAudio.png)>

*Interface limpa e intuitiva para edição de metadados*

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Dependências

pip install mutagen customtkinter pillow

### Instalação Rápida

Clone o repositório

git clone https://github.com/olverclock/PyMetaAudio.git
Entre no diretório

cd PyMetaAudio
Instale as dependências

pip install -r requirements.txt
Execute o programa

python PyMetaAudio.py

---

## 📦 Formatos Suportados

| Formato | Extensão | Metadados | Capa |
|---------|----------|-----------|------|
| MP3 | `.mp3` | ✅ ID3v2.3 | ✅ APIC |
| FLAC | `.flac` | ✅ Vorbis Comments | ✅ Picture |
| M4A/AAC | `.m4a`, `.aac` | ✅ MP4 | ✅ covr |
| OGG | `.ogg` | ✅ Vorbis Comments | ✅ |
| WAV | `.wav` | ✅ | ❌ |
| WMA | `.wma` | ✅ | ✅ |
| OPUS | `.opus` | ✅ | ✅ |

---

## 🎯 Funcionalidades

### Metadados Editáveis

- **Título** da música
- **Artista** principal
- **Álbum**
- **Artista do Álbum**
- **Ano** de lançamento
- **Gênero** musical
- **Número da Faixa** e **Total de Faixas**
- **Compositor**
- **Comentário**

### Gerenciamento de Capas

- ✅ Visualização da capa atual
- ✅ Adicionar nova capa (JPEG/PNG)
- ✅ Remover capa existente
- ✅ Compatibilidade com Windows Explorer, Media Player, VLC, foobar2000

### Recursos de Segurança

- 🔄 **Backup automático** (.backup) antes de salvar
- 🔙 **Restaurar do backup** com um clique
- ⚠️ **Validação de arquivos** antes de carregar
- 🛡️ **Tratamento robusto de erros**

---

## 📖 Como Usar

### 1. Selecionar Arquivo
- Clique em **"Selecionar Arquivo"**
- Escolha um arquivo de áudio compatível
- Backup automático é criado

### 2. Visualizar Metadados
- Todos os campos são preenchidos automaticamente
- Capa é exibida (se existir)

### 3. Editar Informações
- Modifique qualquer campo desejado
- Adicione ou remova a capa do álbum

### 4. Salvar Alterações
- Clique em **"Salvar Alterações"**
- Arquivo é salvo em **ID3v2.3** (máxima compatibilidade)
- Áudio permanece **100% intacto**

### 5. Restaurar (opcional)
- Use **"Restaurar Backup"** para desfazer alterações
- Arquivo original é recuperado do backup

---

## ⚙️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** - Linguagem principal
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Interface gráfica moderna
- **[Mutagen](https://mutagen.readthedocs.io/)** - Biblioteca de metadados de áudio
- **[Pillow](https://python-pillow.org/)** - Processamento de imagens

---

## 📝 requirements.txt

mutagen>=1.47.0
customtkinter>=5.2.0
pillow>=10.0.0

---

## 🐛 Problemas Conhecidos e Soluções

### Capa não aparece no Windows Media Player
- ✅ Resolvido: PyMetaAudio salva em **ID3v2.3** automaticamente
- Renomeie o arquivo ou limpe o cache de miniaturas do Windows

### Erro "ID3 tag already exists"
- ✅ Resolvido: código atualizado verifica tags antes de criar

### Imagem muito grande
- Recomendação: use imagens de 500-800px para melhor compatibilidade

---

## 📊 Changelog

### v1.0.0 (10/12/2025)
- ✨ Lançamento inicial
- ✅ Suporte a 8 formatos de áudio
- ✅ Editor de capas integrado
- ✅ Backup automático
- ✅ Interface gráfica moderna
- ✅ Compatibilidade ID3v2.3

---

## 🔮 Roadmap

- [ ] Edição em lote (múltiplos arquivos)
- [ ] Busca automática de capas online
- [ ] Preset de metadados
- [ ] Histórico de edições
- [ ] Exportar/Importar metadados (JSON)
- [ ] Suporte a playlists

---

## ❓ FAQ

**P: O programa altera a qualidade do áudio?**  
R: Não! PyMetaAudio edita **apenas metadados**, o áudio permanece 100% intacto.

**P: Posso usar em arquivos protegidos por DRM?**  
R: Não. O programa não remove proteções DRM.

**P: Funciona no Linux/Mac?**  
R: Sim! Python e todas as bibliotecas são multiplataforma.

**P: O backup é automático?**  
R: Sim! Sempre que você abre um arquivo, um backup `.backup` é criado.

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão?

- Abra uma [Issue](https://github.com/olverclock/PyMetaAudio/issues)
- Entre em contato pelo GitHub

---

<div align="center">

**Desenvolvido com ❤️ por olverclock**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>

