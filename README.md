Markdown

# 📥 Baixador Profissional CLI (v4.5)

Ferramenta avançada em Python para gerenciamento e download de mídias de centenas de plataformas (YouTube, Instagram, TikTok, SoundCloud, etc.). Este projeto evoluiu para uma solução completa com foco em **automação em lote**, **qualidade personalizada** e **inteligência de arquivo**.

## ✨ Funcionalidades Principais
* **Download em Lote:** Processa múltiplos links automaticamente a partir do arquivo `links.txt`.
* **Seletor de Qualidade:** Escolha entre Alta (320kbps/1080p), Padrão ou Econômica antes de iniciar.
* **Organizador Inteligente:** Separa downloads automaticamente em `Musicas`, `Videos` e `Playlists`.
* **Histórico com Logs:** Registro detalhado em JSON com data, título, URL e local do arquivo.
* **Modo Archive:** O sistema "lembra" o que já foi baixado e pula arquivos repetidos automaticamente.
* **Tags & Capas:** Embuti capas de álbum (Thumbnail), artista e álbum nos arquivos MP3.
* **Barra de Progresso:** Visualização dinâmica no terminal com velocidade e tempo restante (ETA).

---

## 🛠️ Como usar em qualquer computador

### 1. Pré-requisitos
* Ter o **Python 3.x** instalado.
* Possuir os executáveis do **FFmpeg** (`ffmpeg.exe` e `ffprobe.exe`) na pasta raiz.

### 2. Instalação
```bash
pip install -r requirements.txt

3. Execução
Bash

python app.py

📜 Histórico de Versões
v1.0 a v3.5 - Fundação e Metadados

    Scripts básicos, suporte a playlists, organização de pastas e inclusão de capas/tags.

v4.0 - Automação em Lote

    Implementação da leitura de links.txt para downloads múltiplos sem intervenção manual.

v4.2 - Controle de Qualidade

    Adição de submenu para escolha de bitrate de áudio e resolução de vídeo.

v4.4 - Inteligência e Histórico

    Implementação do historico.json e do sistema de archive.txt para evitar duplicatas.

v4.5 (Atual) - Experiência Visual

    Inclusão de Barra de Progresso dinâmica e otimização do fluxo de logs no terminal.

📂 Estrutura do Repositório

    app.py: O "coração" do programa com toda a lógica integrada.

    .gitignore: Protege o repositório contra arquivos pesados, logs pessoais e mídias.

    requirements.txt: Dependência principal (yt-dlp).

    README.md: Documentação atualizada.

Desenvolvido por Vinny1313


---

### Comandos para finalizar no terminal:

Agora, execute estes três comandos para selar o projeto no GitHub:

```powershell
# 1. Adiciona o README e o código final
git add .

# 2. Faz o commit da grande atualização v4.5
git commit -m "Documentação v4.5: Suporte a lote, qualidade, histórico e barra de progresso"

# 3. Envia para o mundo
git push origin main