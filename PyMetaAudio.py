"""
Editor Profissional de Metadados de Áudio
Suporta: MP3, FLAC, OGG, M4A, WAV, WMA, OPUS, AAC
Edição sem perda de qualidade - Apenas metadados são modificados
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import mutagen
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TCON, TPE2, TRCK, COMM, ID3NoHeaderError
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
import os
import shutil
from pathlib import Path
import io

class AudioMetadataEditor:
    def __init__(self):
        # Configuração da janela principal
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Editor Profissional de Metadados de Áudio")
        self.root.geometry("900x700")
        
        self.current_file = None
        self.backup_file = None
        self.audio = None
        self.cover_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(main_frame, text="Editor de Metadados de Áudio", 
                            font=("Arial", 24, "bold"))
        title.pack(pady=10)
        
        # Frame de seleção de arquivo
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        self.file_label = ctk.CTkLabel(file_frame, text="Nenhum arquivo selecionado",
                                       font=("Arial", 12))
        self.file_label.pack(side="left", padx=10, pady=10)
        
        select_btn = ctk.CTkButton(file_frame, text="Selecionar Arquivo",
                                   command=self.select_file, width=150)
        select_btn.pack(side="right", padx=10, pady=10)
        
        # Frame principal de edição (scrollable)
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para capa do álbum
        cover_frame = ctk.CTkFrame(scroll_frame)
        cover_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(cover_frame, text="Capa do Álbum:", 
                    font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.cover_display = ctk.CTkLabel(cover_frame, text="Sem capa", 
                                         width=200, height=200)
        self.cover_display.pack(pady=10)
        
        cover_btn_frame = ctk.CTkFrame(cover_frame)
        cover_btn_frame.pack(pady=5)
        
        ctk.CTkButton(cover_btn_frame, text="Adicionar Capa", 
                     command=self.add_cover, width=120).pack(side="left", padx=5)
        ctk.CTkButton(cover_btn_frame, text="Remover Capa", 
                     command=self.remove_cover, width=120).pack(side="left", padx=5)
        
        # Campos de metadados
        fields_frame = ctk.CTkFrame(scroll_frame)
        fields_frame.pack(fill="x", pady=10)
        
        # Dicionário de campos
        self.entries = {}
        metadata_fields = [
            ("Título", "title"),
            ("Artista", "artist"),
            ("Álbum", "album"),
            ("Artista do Álbum", "albumartist"),
            ("Ano", "year"),
            ("Gênero", "genre"),
            ("Número da Faixa", "track"),
            ("Total de Faixas", "tracktotal"),
            ("Compositor", "composer"),
            ("Comentário", "comment")
        ]
        
        for label, key in metadata_fields:
            field_frame = ctk.CTkFrame(fields_frame)
            field_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(field_frame, text=label + ":", 
                        font=("Arial", 12), width=150, anchor="w").pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(field_frame, width=400)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            self.entries[key] = entry
        
        # Frame de botões de ação
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(action_frame, text="Salvar Alterações", 
                     command=self.save_metadata, width=150, 
                     fg_color="green", hover_color="darkgreen").pack(side="left", padx=10)
        
        ctk.CTkButton(action_frame, text="Restaurar Backup", 
                     command=self.restore_backup, width=150,
                     fg_color="orange", hover_color="darkorange").pack(side="left", padx=10)
        
        ctk.CTkButton(action_frame, text="Limpar Campos", 
                     command=self.clear_fields, width=150).pack(side="left", padx=10)
        
    def select_file(self):
        """Seleciona arquivo de áudio com validação"""
        filetypes = (
            ("Arquivos de Áudio", "*.mp3 *.flac *.ogg *.m4a *.wav *.wma *.opus *.aac"),
            ("MP3", "*.mp3"),
            ("FLAC", "*.flac"),
            ("OGG", "*.ogg"),
            ("M4A/AAC", "*.m4a *.aac"),
            ("Todos os arquivos", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo de áudio",
            filetypes=filetypes
        )
        
        if filename:
            try:
                # Criar backup antes de qualquer operação
                self.create_backup(filename)
                
                # Carregar arquivo
                self.current_file = filename
                self.audio = mutagen.File(filename)
                
                if self.audio is None:
                    raise ValueError("Formato não suportado ou arquivo corrompido")
                
                # Atualizar interface
                self.file_label.configure(text=os.path.basename(filename))
                self.load_metadata()
                
                messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!\nBackup criado automaticamente.")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}")
                self.current_file = None
                self.audio = None
    
    def create_backup(self, filename):
        """Cria backup automático do arquivo original"""
        try:
            backup_path = filename + ".backup"
            shutil.copy2(filename, backup_path)
            self.backup_file = backup_path
        except Exception as e:
            raise Exception(f"Erro ao criar backup: {str(e)}")
    
    def load_metadata(self):
        """Carrega metadados do arquivo para a interface"""
        if not self.audio:
            return
        
        # Limpar campos primeiro
        self.clear_fields()
        
        try:
            # Carregar metadados de forma segura
            if isinstance(self.audio, MP4):
                self.load_mp4_metadata()
            elif isinstance(self.audio, FLAC):
                self.load_flac_metadata()
            elif isinstance(self.audio, OggVorbis):
                self.load_ogg_metadata()
            else:  # ID3 (MP3, etc)
                self.load_id3_metadata()
            
            # Carregar capa
            self.load_cover()
            
        except Exception as e:
            messagebox.showwarning("Aviso", f"Alguns metadados não puderam ser carregados:\n{str(e)}")
    
    def load_id3_metadata(self):
        """Carrega metadados ID3 (MP3)"""
        try:
            if hasattr(self.audio, 'tags') and self.audio.tags:
                self.entries['title'].insert(0, str(self.audio.tags.get('TIT2', '')))
                self.entries['artist'].insert(0, str(self.audio.tags.get('TPE1', '')))
                self.entries['album'].insert(0, str(self.audio.tags.get('TALB', '')))
                self.entries['albumartist'].insert(0, str(self.audio.tags.get('TPE2', '')))
                self.entries['year'].insert(0, str(self.audio.tags.get('TDRC', '')))
                self.entries['genre'].insert(0, str(self.audio.tags.get('TCON', '')))
                self.entries['track'].insert(0, str(self.audio.tags.get('TRCK', '')).split('/')[0])
                self.entries['composer'].insert(0, str(self.audio.tags.get('TCOM', '')))
                
                # Comentário
                comm = self.audio.tags.get('COMM::eng')
                if comm:
                    self.entries['comment'].insert(0, str(comm))
        except Exception as e:
            print(f"Erro ao carregar ID3: {e}")
    
    def load_mp4_metadata(self):
        """Carrega metadados MP4/M4A"""
        mapping = {
            'title': '\xa9nam',
            'artist': '\xa9ART',
            'album': '\xa9alb',
            'albumartist': 'aART',
            'year': '\xa9day',
            'genre': '\xa9gen',
            'composer': '\xa9wrt',
            'comment': '\xa9cmt'
        }
        
        for key, tag in mapping.items():
            if tag in self.audio.tags:
                self.entries[key].insert(0, str(self.audio.tags[tag][0]))
        
        if 'trkn' in self.audio.tags:
            track = self.audio.tags['trkn'][0]
            self.entries['track'].insert(0, str(track[0]))
            if len(track) > 1:
                self.entries['tracktotal'].insert(0, str(track[1]))
    
    def load_flac_metadata(self):
        """Carrega metadados FLAC"""
        simple_mapping = {
            'title': 'title',
            'artist': 'artist',
            'album': 'album',
            'albumartist': 'albumartist',
            'year': 'date',
            'genre': 'genre',
            'track': 'tracknumber',
            'tracktotal': 'tracktotal',
            'composer': 'composer',
            'comment': 'comment'
        }
        
        for key, tag in simple_mapping.items():
            if tag in self.audio:
                self.entries[key].insert(0, str(self.audio[tag][0]))
    
    def load_ogg_metadata(self):
        """Carrega metadados OGG Vorbis"""
        self.load_flac_metadata()  # OGG usa formato similar ao FLAC
    
    def load_cover(self):
        """Carrega e exibe capa do álbum"""
        try:
            cover_data = None
            
            if isinstance(self.audio, MP4):
                if 'covr' in self.audio.tags:
                    cover_data = bytes(self.audio.tags['covr'][0])
            elif isinstance(self.audio, FLAC):
                if self.audio.pictures:
                    cover_data = self.audio.pictures[0].data
            elif hasattr(self.audio, 'tags') and self.audio.tags:
                # ID3
                for tag in self.audio.tags.values():
                    if isinstance(tag, APIC):
                        cover_data = tag.data
                        break
            
            if cover_data:
                self.display_cover(cover_data)
                self.cover_image = cover_data
            else:
                self.cover_display.configure(text="Sem capa", image=None)
                self.cover_image = None
                
        except Exception as e:
            print(f"Erro ao carregar capa: {e}")
    
    def display_cover(self, image_data):
        """Exibe imagem de capa"""
        try:
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.cover_display.configure(image=photo, text="")
            self.cover_display.image = photo  # Manter referência
        except Exception as e:
            print(f"Erro ao exibir capa: {e}")
    
    def add_cover(self):
        """Adiciona capa do álbum"""
        if not self.audio:
            messagebox.showwarning("Aviso", "Selecione um arquivo de áudio primeiro!")
            return
        
        filename = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=(("Imagens", "*.jpg *.jpeg *.png"), ("Todos", "*.*"))
        )
        
        if filename:
            try:
                with open(filename, 'rb') as f:
                    self.cover_image = f.read()
                self.display_cover(self.cover_image)
                messagebox.showinfo("Sucesso", "Capa carregada! Clique em 'Salvar Alterações' para aplicar.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{str(e)}")
    
    def remove_cover(self):
        """Remove capa do álbum"""
        self.cover_image = None
        self.cover_display.configure(text="Capa será removida", image=None)
        messagebox.showinfo("Info", "Capa marcada para remoção. Clique em 'Salvar Alterações' para aplicar.")
    
    def save_metadata(self):
        """Salva metadados de forma segura sem alterar qualidade de áudio"""
        if not self.audio or not self.current_file:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado!")
            return
        
        try:
            # Salvar de acordo com o formato
            if isinstance(self.audio, MP4):
                self.save_mp4_metadata()
            elif isinstance(self.audio, FLAC):
                self.save_flac_metadata()
            elif isinstance(self.audio, OggVorbis):
                self.save_ogg_metadata()
            else:
                self.save_id3_metadata()
            try:
                self.audio.save(v2_version=3)
            except TypeError:
                # Alguns formatos (como FLAC/MP4) não usam v2_version, então faz o save normal
                self.audio.save()
            
            messagebox.showinfo("Sucesso", "Metadados salvos com sucesso!\nÁudio preservado sem alterações.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{str(e)}\n\nUse 'Restaurar Backup' para recuperar o arquivo original.")
    
    def save_id3_metadata(self):
        """Salva metadados ID3 - CORRIGIDO PARA CAPAS"""
        # Tags de texto normais usando self.audio (como já estava)
        if not hasattr(self.audio, 'tags') or self.audio.tags is None:
            self.audio.add_tags()

        self.audio.tags['TIT2'] = TIT2(encoding=3, text=self.entries['title'].get())
        self.audio.tags['TPE1'] = TPE1(encoding=3, text=self.entries['artist'].get())
        self.audio.tags['TALB'] = TALB(encoding=3, text=self.entries['album'].get())
        self.audio.tags['TPE2'] = TPE2(encoding=3, text=self.entries['albumartist'].get())
        self.audio.tags['TDRC'] = TDRC(encoding=3, text=self.entries['year'].get())
        self.audio.tags['TCON'] = TCON(encoding=3, text=self.entries['genre'].get())

        track = self.entries['track'].get()
        tracktotal = self.entries['tracktotal'].get()
        if track:
            track_str = f"{track}/{tracktotal}" if tracktotal else track
            self.audio.tags['TRCK'] = TRCK(encoding=3, text=track_str)

        if self.entries['comment'].get():
            self.audio.tags['COMM'] = COMM(
                encoding=3, lang='eng', desc='',
                text=self.entries['comment'].get()
            )

        # ===== CORREÇÃO DA CAPA MP3 AQUI =====
        # Reabre só para manipular APIC, sem tentar criar tags de novo
        audio_mp3 = MP3(self.current_file, ID3=ID3)

        # NÃO chamar add_tags se já existe; só cria se não tiver
        if audio_mp3.tags is None:
            audio_mp3.add_tags()

        # Remove todas as capas antigas
        audio_mp3.tags.delall('APIC')

        # Se tiver nova capa, adiciona de forma compatível
        if self.cover_image:
            # aqui é melhor fixar como jpeg; se sua imagem for png, troque o mime
            audio_mp3.tags.add(APIC(
                encoding=0,              # Latin1, mais compatível com players [web:15]
                mime='image/jpeg',
                type=3,                  # capa frontal [web:11]
                desc='Cover',
                data=self.cover_image
            ))

        # Salva como ID3v2.3 (bem suportado) [web:18]
        audio_mp3.save(v2_version=3)
    
    def save_mp4_metadata(self):
        """Salva metadados MP4"""
        mapping = {
            'title': '\xa9nam',
            'artist': '\xa9ART',
            'album': '\xa9alb',
            'albumartist': 'aART',
            'year': '\xa9day',
            'genre': '\xa9gen',
            'composer': '\xa9wrt',
            'comment': '\xa9cmt'
        }
        
        for key, tag in mapping.items():
            value = self.entries[key].get()
            if value:
                self.audio.tags[tag] = [value]
        
        # Track number
        track = self.entries['track'].get()
        tracktotal = self.entries['tracktotal'].get()
        if track:
            try:
                track_num = int(track)
                total_num = int(tracktotal) if tracktotal else 0
                self.audio.tags['trkn'] = [(track_num, total_num)]
            except ValueError:
                pass
        
        # Capa
        if 'covr' in self.audio.tags:
            del self.audio.tags['covr']
        if self.cover_image:
            self.audio.tags['covr'] = [MP4Cover(self.cover_image, 
                                        imageformat=MP4Cover.FORMAT_JPEG)]
    
    def save_flac_metadata(self):
        """Salva metadados FLAC"""
        mapping = {
            'title': 'title',
            'artist': 'artist',
            'album': 'album',
            'albumartist': 'albumartist',
            'year': 'date',
            'genre': 'genre',
            'track': 'tracknumber',
            'tracktotal': 'tracktotal',
            'composer': 'composer',
            'comment': 'comment'
        }
        
        for key, tag in mapping.items():
            value = self.entries[key].get()
            if value:
                self.audio[tag] = value
        
        # Capa
        self.audio.clear_pictures()
        if self.cover_image:
            picture = Picture()
            picture.type = 3  # Cover (front)
            picture.mime = 'image/jpeg'
            picture.data = self.cover_image
            self.audio.add_picture(picture)
    
    def save_ogg_metadata(self):
        """Salva metadados OGG"""
        self.save_flac_metadata()
    
    def restore_backup(self):
        """Restaura arquivo do backup"""
        if not self.backup_file or not os.path.exists(self.backup_file):
            messagebox.showwarning("Aviso", "Nenhum backup disponível!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja restaurar o arquivo original do backup?"):
            try:
                shutil.copy2(self.backup_file, self.current_file)
                self.audio = mutagen.File(self.current_file)
                self.load_metadata()
                messagebox.showinfo("Sucesso", "Arquivo restaurado do backup!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{str(e)}")
    
    def clear_fields(self):
        """Limpa todos os campos de entrada"""
        for entry in self.entries.values():
            entry.delete(0, 'end')
        self.cover_display.configure(text="Sem capa", image=None)
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


# Iniciar aplicação
if __name__ == "__main__":
    app = AudioMetadataEditor()
    app.run()
