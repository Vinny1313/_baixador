import yt_dlp
import os

def baixar_conteudo(url, apenas_audio=True):
    # Detecta a pasta onde o app.py está
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    config = {
        # Aponta para onde você moveu o ffmpeg.exe e ffprobe.exe
        'ffmpeg_location': diretorio_atual,
        'outtmpl': os.path.join(diretorio_atual, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    if apenas_audio:
        # Configuração para MP3
        print("\n[MODO] Música (MP3)")
        config.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Configuração para Vídeo (MP4)
        print("\n[MODO] Vídeo (MP4)")
        config.update({
            # 'best' garante que ele baixe o vídeo com áudio em um único arquivo
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    try:
        with yt_dlp.YoutubeDL(config) as ydl:
            print("[PROCESSO] Iniciando download... Aguarde.")
            ydl.download([url])
            print(f"\n[✔] SUCESSO! Arquivo salvo em: {diretorio_atual}")
    except Exception as e:
        print(f"\n[!] ERRO: {e}")

def exibir_menu():
    while True:
        # Limpa a tela para o menu ficar organizado
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*40)
        print("      MEU BAIXADOR MULTIMÍDIA")
        print("="*40)
        print(" [1] Baixar Música (MP3)")
        print(" [2] Baixar Vídeo (MP4)")
        print(" [3] Sair")
        print("="*40)
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            link = input("Cole o link da música: ")
            baixar_conteudo(link, apenas_audio=True)
            input("\nAperte Enter para voltar ao menu...")
            
        elif opcao == '2':
            link = input("Cole o link do vídeo: ")
            baixar_conteudo(link, apenas_audio=False)
            input("\nAperte Enter para voltar ao menu...")
            
        elif opcao == '3':
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!")
            input("Aperte Enter...")

if __name__ == "__main__":
    exibir_menu()