import yt_dlp
import os
import json
from datetime import datetime

def verificar_ffmpeg(diretorio):
    """Garante que o FFmpeg está presente para conversão."""
    ffmpeg_exe = os.path.join(diretorio, 'ffmpeg.exe')
    if not os.path.exists(ffmpeg_exe):
        print("\n" + "!"*50)
        print("ERRO: ffmpeg.exe não encontrado!")
        print(f"Coloque o executável em: {diretorio}")
        print("!"*50)
        return False
    return True

def progresso_hook(d):
    """Cria uma barra de progresso visual no terminal."""
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%')
        v = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        total = d.get('_total_bytes_str', d.get('_total_bytes_estimate_str', 'N/A'))
        
        # Desenha a barra [##########----------]
        try:
            percent_num = float(p.replace('%','').strip())
            preenchido = int(percent_num // 5)
            barra = '#' * preenchido
            vazio = '-' * (20 - preenchido)
            print(f"\r[BAIXANDO] [{barra}{vazio}] {p} | Total: {total} | Vel: {v} | ETA: {eta}", end='')
        except:
            print(f"\r[BAIXANDO] {p} - Processando...", end='')
            
    elif d['status'] == 'finished':
        print(f"\n[SISTEMA] Download concluído! Finalizando arquivo...")

def salvar_no_historico(titulo, url, destino):
    """Registra o download no arquivo historico.json."""
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    arquivo_log = os.path.join(diretorio_base, "historico.json")
    
    novo_registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "titulo": titulo,
        "url": url,
        "pasta": destino
    }

    historico = []
    if os.path.exists(arquivo_log):
        with open(arquivo_log, 'r', encoding='utf-8') as f:
            try:
                historico = json.load(f)
            except:
                historico = []

    historico.append(novo_registro)
    with open(arquivo_log, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

def escolher_qualidade(apenas_audio):
    """Permite ao usuário definir a qualidade da mídia."""
    if apenas_audio:
        print("\n--- QUALIDADE DO ÁUDIO ---")
        print(" [1] Alta (320kbps) | [2] Padrão (192kbps) | [3] Econômica (128kbps)")
        q = input("Escolha: ")
        return '320' if q == '1' else '128' if q == '3' else '192'
    else:
        print("\n--- QUALIDADE DO VÍDEO ---")
        print(" [1] Full HD (1080p) | [2] HD (720p) | [3] SD (480p)")
        q = input("Escolha: ")
        return '1080' if q == '1' else '480' if q == '3' else '720'

def baixar_conteudo(url, apenas_audio=True, modo_playlist=None, qualidade=None):
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    if not verificar_ffmpeg(diretorio_base): return

    if qualidade is None: qualidade = escolher_qualidade(apenas_audio)
    if modo_playlist is None: modo_playlist = 'playlist' in url.lower()

    # Organizador inteligente
    subpasta = "Playlists" if modo_playlist else ("Musicas" if apenas_audio else "Videos")
    pasta_destino = os.path.join(diretorio_base, "Downloads", subpasta)
    if not os.path.exists(pasta_destino): os.makedirs(pasta_destino)

    config = {
        'ffmpeg_location': diretorio_base,
        'outtmpl': os.path.join(pasta_destino, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s") if modo_playlist else os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        'noplaylist': not modo_playlist,
        'writethumbnail': True,
        'download_archive': os.path.join(diretorio_base, "archive.txt"), # Modo apenas novos
        'progress_hooks': [progresso_hook],
        'quiet': True,
        'no_warnings': True,
    }

    if apenas_audio:
        config.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': qualidade},
                {'key': 'EmbedThumbnail'}, {'key': 'FFmpegMetadata'},
            ],
        })
    else:
        config.update({
            'format': f'bestvideo[height<={qualidade}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'postprocessors': [{'key': 'FFmpegMetadata'}]
        })

    try:
        with yt_dlp.YoutubeDL(config) as ydl:
            # Obtém informações antes do download
            info = ydl.extract_info(url, download=False)
            titulo = info.get('title', 'Desconhecido')
            print(f"\n[PROCESSO] Iniciando: {titulo}")
            
            # Baixa e registra
            ydl.download([url])
            salvar_no_historico(titulo, url, pasta_destino)
    except Exception as e:
        if "already been recorded in the archive" in str(e):
            print(f"\n[➡] PULADO: Este item já existe na sua pasta.")
        else:
            print(f"\n[!] ERRO: {e}")

def ver_historico():
    """Mostra os últimos downloads com links."""
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    arquivo_log = os.path.join(diretorio_base, "historico.json")
    if not os.path.exists(arquivo_log):
        print("\n[!] Histórico vazio.")
        return

    with open(arquivo_log, 'r', encoding='utf-8') as f:
        log = json.load(f)
        print("\n" + "="*95)
        print(f"{'DATA':<18} | {'TÍTULO':<35} | {'LINK'}")
        print("-" * 95)
        for item in log[-10:]:
            t_curto = (item['titulo'][:32] + '..') if len(item['titulo']) > 32 else item['titulo']
            l_curto = item['url'][:40] + "..."
            print(f"{item['data']:<18} | {t_curto:<35} | {l_curto}")
        print("="*95)

def menu_lote():
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_lote = os.path.join(diretorio_base, "links.txt")
    if not os.path.exists(caminho_lote):
        open(caminho_lote, 'w').close()
        print("\n[!] 'links.txt' criado. Adicione os links e tente novamente.")
        return

    with open(caminho_lote, 'r') as f:
        links = [l.strip() for l in f if l.strip()]

    if not links:
        print("\n[!] O arquivo links.txt está vazio.")
        return

    print(f"\n[LOTE] {len(links)} links encontrados.")
    tipo = input("Deseja baixar como [1] Música ou [2] Vídeo? ")
    apenas_audio = (tipo == '1')
    qualidade_lote = escolher_qualidade(apenas_audio)

    for i, link in enumerate(links, 1):
        print(f"\n[{i}/{len(links)}] Verificando link...")
        baixar_conteudo(link, apenas_audio, None, qualidade_lote)
    print("\n[✔] Lote concluído!")

def exibir_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*45)
        print("      BAIXADOR PROFISSIONAL v4.5")
        print("="*45)
        print(" [1] Música Individual")
        print(" [2] Vídeo Individual")
        print(" [3] Playlist (Manual)")
        print(" [4] Lote Inteligente (links.txt)")
        print(" [5] Ver Histórico Completo")
        print(" [6] Sair")
        print("="*45)
        
        op = input("\nEscolha: ")
        if op == '6': break
        if op == '5': ver_historico()
        elif op == '4': menu_lote()
        elif op in ['1','2','3']:
            link = input("Link: ")
            if op == '1': baixar_conteudo(link, True, False)
            elif op == '2': baixar_conteudo(link, False, False)
            elif op == '3': baixar_conteudo(link, True, True)
        
        if op != '6': input("\nAperte Enter para continuar...")

if __name__ == "__main__":
    exibir_menu()