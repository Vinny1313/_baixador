import yt_dlp
import os

def verificar_ffmpeg(diretorio):
    """Verifica se os executáveis estão na pasta principal."""
    ffmpeg_exe = os.path.join(diretorio, 'ffmpeg.exe')
    if not os.path.exists(ffmpeg_exe):
        print("\n" + "!"*50)
        print("ERRO: ffmpeg.exe não encontrado!")
        print(f"Certifique-se de que ele está em: {diretorio}")
        print("!"*50)
        return False
    return True

def baixar_conteudo(url, apenas_audio=True, modo_playlist=False):
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Verificação de segurança inicial
    if not verificar_ffmpeg(diretorio_base):
        input("\nAperte Enter para voltar ao menu...")
        return

    # 2. Definição inteligente de pastas (Organizador)
    if modo_playlist:
        pasta_destino = os.path.join(diretorio_base, "Downloads", "Playlists")
        # Mantém a ordem original usando o índice da playlist
        template_nome = os.path.join(pasta_destino, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        pasta_destino = os.path.join(diretorio_base, "Downloads", "Musicas" if apenas_audio else "Videos")
        template_nome = os.path.join(pasta_destino, "%(title)s.%(ext)s")

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # 3. Configuração do motor de download
    config = {
        'ffmpeg_location': diretorio_base,
        'outtmpl': template_nome,
        'noplaylist': not modo_playlist,
        'writethumbnail': True,  # Necessário para a capa do álbum
        'quiet': False,
    }

    if apenas_audio:
        config.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail', # Insere a capa no arquivo
                },
                {
                    'key': 'FFmpegMetadata', # Insere Artista, Álbum e Título
                }
            ],
        })
    else:
        config.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'postprocessors': [{'key': 'FFmpegMetadata'}]
        })

    # 4. Execução do Download
    try:
        with yt_dlp.YoutubeDL(config) as ydl:
            print(f"\n[SISTEMA] Destino: {pasta_destino}")
            print("[SISTEMA] Processando metadados e mídia...")
            ydl.download([url])
            print("\n[✔] Concluído! Arquivo organizado e tagueado.")
    except Exception as e:
        print(f"\n[!] ERRO: {e}")

def exibir_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*45)
        print("      BAIXADOR ORGANIZADO v3.5")
        print("="*45)
        print(" [1] Música Individual (MP3)")
        print(" [2] Vídeo Individual (MP4)")
        print(" [3] Playlist Completa (Músicas)")
        print(" [4] Playlist Completa (Vídeos)")
        print(" [5] Sair")
        print("="*45)
        
        op = input("\nEscolha: ")
        if op == '5': break
        if op in ['1','2','3','4']:
            link = input("Link: ")
            if op == '1': baixar_conteudo(link, True, False)
            elif op == '2': baixar_conteudo(link, False, False)
            elif op == '3': baixar_conteudo(link, True, True)
            elif op == '4': baixar_conteudo(link, False, True)
            input("\nEnter para voltar...")

if __name__ == "__main__":
    exibir_menu()