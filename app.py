import yt_dlp
import os
import json
from datetime import datetime
from mutagen.id3 import ID3, TCON, TDRC, COMM

def verificar_ffmpeg(diretorio):
    """Verifica se os executáveis do FFmpeg estão na pasta."""
    ffmpeg_exe = os.path.join(diretorio, 'ffmpeg.exe')
    if not os.path.exists(ffmpeg_exe):
        print("\n" + "!"*50)
        print(f"{'ERRO: FFMPEG NÃO ENCONTRADO':^50}")
        print(f"{'Coloque ffmpeg.exe em:':^50}")
        print(f"{diretorio:^50}")
        print("!"*50)
        return False
    return True

def sincronizar_metadados_avancados(caminho_arquivo, info):
    """Refina as tags ID3 para organização nível Spotify."""
    try:
        try:
            audio = ID3(caminho_arquivo)
        except:
            audio = ID3()

        # Gênero
        genero = info.get('genre', 'Geral')
        audio.add(TCON(encoding=3, text=genero))
        
        # Ano
        data_up = info.get('upload_date', '00000000')
        ano = str(info.get('release_year') or data_up[:4])
        audio.add(TDRC(encoding=3, text=ano))
        
        # Comentário com Link
        url_fonte = info.get('webpage_url', 'N/A')
        audio.add(COMM(encoding=3, lang='por', desc='desc', text=f"Fonte: {url_fonte}"))
        
        audio.save(caminho_arquivo)
        print(f" [TAGS] Gênero: {genero} | Ano: {ano} sincronizados.")
    except Exception as e:
        print(f" [!] Erro nas tags: {e}")

def progresso_hook(d):
    """Barra de progresso dinâmica com ETA e Velocidade."""
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%')
        v = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        
        try:
            percent_num = float(p.replace('%','').strip())
            preenchido = int(percent_num // 5)
            barra = '#' * preenchido
            vazio = '-' * (20 - preenchido)
            print(f"\r [BAIXANDO] [{barra}{vazio}] {p} | Vel: {v} | ETA: {eta}", end='')
        except:
            print(f"\r [BAIXANDO] {p}...", end='')
    elif d['status'] == 'finished':
        print(f"\n [SISTEMA] Download concluído! Convertendo...")

def salvar_no_historico(titulo, url, destino):
    """Registra a atividade no banco JSON."""
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    arquivo_log = os.path.join(diretorio_base, "historico.json")
    
    registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "titulo": titulo, "url": url, "pasta": destino
    }

    historico = []
    if os.path.exists(arquivo_log):
        with open(arquivo_log, 'r', encoding='utf-8') as f:
            try: historico = json.load(f)
            except: historico = []

    historico.append(registro)
    with open(arquivo_log, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

def escolher_qualidade(apenas_audio):
    """Submenu padronizado de qualidade."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    titulo = "QUALIDADE DE ÁUDIO" if apenas_audio else "QUALIDADE DE VÍDEO"
    print(f"{titulo:^50}")
    print("="*50)
    
    if apenas_audio:
        print(" [1] Alta Fidelidade (320kbps)")
        print(" [2] Padrão (192kbps)")
        print(" [3] Econômica (128kbps)")
        print("-" * 50)
        q = input(" Escolha: ")
        return '320' if q == '1' else '128' if q == '3' else '192'
    else:
        print(" [1] Full HD (1080p)")
        print(" [2] HD (720p)")
        print(" [3] SD (480p)")
        print("-" * 50)
        q = input(" Escolha: ")
        return '1080' if q == '1' else '480' if q == '3' else '720'

def baixar_conteudo(url, apenas_audio=True, modo_playlist=None, qualidade=None):
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    if not verificar_ffmpeg(diretorio_base): return

    if qualidade is None: qualidade = escolher_qualidade(apenas_audio)
    if modo_playlist is None: modo_playlist = 'playlist' in url.lower()

    subpasta = "Playlists" if modo_playlist else ("Musicas" if apenas_audio else "Videos")
    pasta_destino = os.path.join(diretorio_base, "Downloads", subpasta)
    if not os.path.exists(pasta_destino): os.makedirs(pasta_destino)

    config = {
        'ffmpeg_location': diretorio_base,
        'outtmpl': os.path.join(pasta_destino, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s") if modo_playlist else os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        'noplaylist': not modo_playlist,
        'writethumbnail': True,
        'download_archive': os.path.join(diretorio_base, "archive.txt"),
        'progress_hooks': [progresso_hook],
        'quiet': True,
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
            info = ydl.extract_info(url, download=True)
            if info:
                titulo = info.get('title', 'Desconhecido')
                if apenas_audio:
                    arq = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
                    if os.path.exists(arq): sincronizar_metadados_avancados(arq, info)
                salvar_no_historico(titulo, url, pasta_destino)
                print(f"\n [✔] CONCLUÍDO: {titulo}")
            else:
                print(f"\n [➡] PULADO: Arquivo já existe no histórico.")
    except Exception as e:
        print(f"\n [!] ERRO: {e}")

def ver_historico():
    """Tabela de histórico padronizada."""
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    arq_log = os.path.join(diretorio_base, "historico.json")
    if not os.path.exists(arq_log):
        print("\n [!] Histórico vazio.")
        return
    with open(arq_log, 'r', encoding='utf-8') as f:
        log = json.load(f)
        print("\n" + "="*95)
        print(f"{'DATA':<18} | {'TÍTULO':<35} | {'LINK'}")
        print("-" * 95)
        for item in log[-10:]:
            t = (item['titulo'][:32] + '..') if len(item['titulo']) > 32 else item['titulo']
            l = item['url'][:40] + "..."
            print(f" {item['data']:<17} | {t:<35} | {l}")
        print("="*95)

def menu_lote():
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_lote = os.path.join(diretorio_base, "links.txt")
    if not os.path.exists(caminho_lote):
        open(caminho_lote, 'w').close()
        print("\n [!] 'links.txt' criado. Adicione os links e tente novamente.")
        return
    with open(caminho_lote, 'r') as f:
        links = [l.strip() for l in f if l.strip()]
    if not links:
        print("\n [!] O arquivo está vazio!")
        return
    
    print(f"\n [LOTE] {len(links)} links encontrados.")
    tipo = input(" Baixar como [1] Música ou [2] Vídeo? ")
    apenas_audio = (tipo == '1')
    qualidade_lote = escolher_qualidade(apenas_audio)

    for i, link in enumerate(links, 1):
        print(f"\n [{i}/{len(links)}] Processando link...")
        baixar_conteudo(link, apenas_audio, None, qualidade_lote)

def exibir_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print(f"{'BAIXADOR MULTIMÍDIA PRO v4.6':^50}")
        print("="*50)
        print(" [1] Música Única")
        print(" [2] Vídeo Único")
        print(" [3] Playlist (Manual)")
        print(" [4] Lote Inteligente (links.txt)")
        print(" [5] Ver Histórico de Downloads")
        print(" [6] Sair")
        print("-" * 50)
        
        op = input(" Escolha uma opção: ")
        if op == '6': break
        if op == '5':
            ver_historico()
            input("\nPressione Enter para voltar...")
        elif op == '4':
            menu_lote()
            input("\nLote finalizado. Pressione Enter...")
        elif op in ['1', '2', '3']:
            link = input("\n Cole o link: ")
            if op == '1': baixar_conteudo(link, True, False)
            elif op == '2': baixar_conteudo(link, False, False)
            elif op == '3': baixar_conteudo(link, True, True)
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    exibir_menu()