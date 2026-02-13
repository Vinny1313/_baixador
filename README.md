Markdown

# 📥 Baixador Multimídia CLI (v3.5)

Este é um programa robusto em Python para download de mídias de diversas plataformas (YouTube, Instagram, TikTok, Twitter, etc.). O projeto evoluiu de um script simples para uma ferramenta automatizada com foco em **organização inteligente**, **preservação de metadados** e **portabilidade**.

## ✨ Funcionalidades Principais
* **Multisites:** Suporte a centenas de redes sociais através do motor `yt-dlp`.
* **Organizador Inteligente:** Separa downloads automaticamente nas pastas `Downloads/Musicas`, `Downloads/Videos` e `Downloads/Playlists`.
* **Preservação de Álbuns:** Mantém a ordem original das playlists numerando as faixas (ex: 01, 02...).
* **Tags & Capas:** Embuti automaticamente a capa do álbum (Thumbnail), nome do artista e álbum nos arquivos MP3.
* **Verificação de Dependências:** Sistema que detecta a ausência do FFmpeg e orienta o usuário sobre a instalação.

---

## 🛠️ Como usar em qualquer computador

### 1. Pré-requisitos
* Ter o **Python 3.x** instalado.
* Baixar os executáveis do **FFmpeg** (`ffmpeg.exe` e `ffprobe.exe`).

### 2. Instalação
Clone o repositório e instale a biblioteca necessária:
```bash
pip install -r requirements.txt

3. Configuração

Coloque o ffmpeg.exe e o ffprobe.exe na mesma pasta do arquivo app.py.
4. Execução
Bash

python app.py

📜 Histórico de Versões
v1.0 - O Início

    Script básico para download de vídeos e áudios individuais.

    Desafios iniciais com caminhos de sistema e conversão de formatos.

v2.0 - Suporte a Playlists

    Implementação da lógica de loops para baixar álbuns completos.

    Ajuste de caminhos absolutos para garantir portabilidade entre pastas.

v3.0 - Organizador Inteligente

    Implementação da estrutura automática de diretórios para separar tipos de mídia.

    Lógica de subpastas para manter playlists agrupadas por título.

v3.5 (Atual) - Metadados & Portabilidade

    Upgrade Visual: Inclusão de capas de álbum (Thumbnails) nos arquivos.

    Upgrade de Informação: Inclusão de metadados (Artista, Álbum, Ano) via post-processamento.

    Upgrade de Ordem: Numeração automática de faixas seguindo a ordem original da fonte.

    Sistema de Diagnóstico: Verificação proativa da presença do motor FFmpeg.

📂 Estrutura do Repositório

    app.py: Código fonte principal com a lógica de download e interface CLI.

    .gitignore: Configurado para ignorar binários pesados, bibliotecas e mídias baixadas.

    requirements.txt: Lista de dependências necessárias.

    README.md: Documentação completa do projeto.

Desenvolvido por Vinny1313


---

### Como aplicar no seu GitHub:
1. Abra o arquivo **README.md** no seu editor.
2. Apague o que estiver lá e cole este conteúdo.
3. No terminal, execute:
   ```powershell
   git add README.md
   git commit -m "Documentação final: Detalhamento das funcionalidades e versões"
   git push origin main