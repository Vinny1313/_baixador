📥 Baixador Multimídia Profissional (v4.6)

Ferramenta avançada em Python para download e gerenciamento de mídias de centenas de plataformas (YouTube, Instagram, TikTok, SoundCloud, etc.). Este projeto evoluiu de um script simples para uma ferramenta robusta com foco em metadados de alta fidelidade, automação e UX de terminal.
✨ Funcionalidades Principais

    Metadados Avançados: Injeção cirúrgica de Gênero, Ano e Link da fonte via biblioteca Mutagen.

    Download em Lote: Processamento automático de múltiplos links via arquivo links.txt.

    Seletor de Qualidade: Menus padronizados para escolha de bitrate (até 320kbps) e resolução (até 1080p).

    Organizador Inteligente: Separação automática em pastas Musicas, Videos e Playlists.

    Histórico & Archive: Registro em JSON e sistema que pula arquivos já baixados automaticamente.

    Interface Dinâmica: Barra de progresso visual com velocidade e tempo restante (ETA).

🛠️ Como usar em qualquer computador
1. Pré-requisitos

    Ter o Python 3.x instalado.

    Possuir os executáveis do FFmpeg (ffmpeg.exe e ffprobe.exe) na pasta raiz.

2. Instalação
Bash

pip install -r requirements.txt

3. Execução
Bash

python app.py

📜 Histórico de Versões
v1.0 a v3.5 - Fundação e Metadados

    Scripts básicos, suporte a playlists, organização de pastas e inclusão de capas básicas.

v4.0 a v4.5 - Automação e Interface

    Implementação de downloads em lote, histórico JSON, modo Archive e Barra de Progresso.

v4.6 (Atual) - Refinamento Profissional

    Sincronização ID3: Uso do Mutagen para tags de gênero, ano e comentários.

    Padronização Visual: Menus centralizados com limpeza de tela (CLS) entre ações.

    Estabilidade: Otimização do fluxo de download para evitar arquivos temporários órfãos.

📂 Estrutura do Repositório

    app.py: O "coração" do programa com toda a lógica integrada.

    .gitignore: Protege o repositório contra arquivos pesados, logs e mídias pessoais.

    requirements.txt: Dependências necessárias (yt-dlp, mutagen).

    README.md: Documentação técnica completa.

Desenvolvido por Vinny1313