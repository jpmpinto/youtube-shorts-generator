# YouTube to Shorts Generator & Publisher

Uma aplicação web full-stack que permite aos utilizadores inserir um URL do YouTube e gerar automaticamente clips de vídeo curtos (shorts) de até 60 segundos, com funcionalidades de edição, pré-visualização, download e publicação direta no TikTok e YouTube Shorts.

## Funcionalidades

### 🔽 Input
- Campo de entrada para URL do YouTube
- Obtenção automática de metadados do vídeo (título, duração, etc.)

### ✂️ Geração de Shorts
- Auto-geração de clips de até 60 segundos
- Opções para:
  - Dividir em múltiplos shorts
  - Selecionar intervalo de tempo
  - Editar manualmente com editor visual
  - Auto-gerar legendas (subtítulos)
  - Marca d'água opcional com marca/logo
  - Sugestão automática de título para cada short (baseado em resumo AI do conteúdo do vídeo)

### 📲 Autenticação & Upload
- Login OAuth para TikTok e YouTube
- Integração com APIs:
  - TikTok: video.upload, user.info.basic
  - YouTube: youtube.upload, youtube.force-ssl

### 🚀 Opções de Upload
- Upload manual ou em massa de múltiplos shorts para TikTok e YouTube
- Indicadores de status para:
  - Sucesso do upload
  - Modo rascunho
  - Mensagens de falha

### 📦 Exportação & Download
- Download de short em formato .mp4
- Download em lote de shorts em .zip

### 🔐 Autenticação de Utilizador
- Login via Google ou TikTok
- Opcionalmente guardar histórico de shorts por utilizador

## Stack Tecnológico

### Frontend
- **React** com **Tailwind CSS**
- **shadcn/ui** para componentes
- **Lucide Icons** para ícones
- **Vite** como bundler

### Backend
- **Flask** (Python)
- **yt-dlp** para download de vídeos do YouTube
- **ffmpeg** para processamento de vídeo
- **moviepy** para manipulação de vídeo
- **Google API Client** para integração com YouTube
- **OAuth** para autenticação

### Processamento de Vídeo
- **ffmpeg** para corte e conversão
- Formato 9:16 (vertical) compatível com TikTok e YouTube Shorts
- Compressão otimizada para plataformas móveis

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- ffmpeg instalado no sistema

### Backend

1. Navegar para o diretório backend:
```bash
cd backend
```

2. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

3. Instalar dependências:
```bash
pip install -r requirements.txt
```

4. Configurar variáveis de ambiente:
```bash
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
export TIKTOK_CLIENT_ID="your-tiktok-client-id"
export TIKTOK_CLIENT_SECRET="your-tiktok-client-secret"
```

5. Executar o servidor:
```bash
python src/main.py
```

### Frontend

1. Navegar para o diretório frontend:
```bash
cd frontend
```

2. Instalar dependências:
```bash
pnpm install
```

3. Executar o servidor de desenvolvimento:
```bash
pnpm run dev
```

## Configuração OAuth

### Google (YouTube)
1. Aceder à [Google Cloud Console](https://console.cloud.google.com/)
2. Criar um novo projeto ou selecionar existente
3. Ativar a YouTube Data API v3
4. Criar credenciais OAuth 2.0
5. Adicionar `http://localhost:5000/api/auth/google/callback` aos URIs de redirecionamento

### TikTok
1. Aceder ao [TikTok for Developers](https://developers.tiktok.com/)
2. Criar uma nova aplicação
3. Solicitar acesso às APIs de upload de vídeo
4. Configurar URI de redirecionamento: `http://localhost:5000/api/auth/tiktok/callback`

**Nota:** A API do TikTok requer aprovação especial para upload de vídeos. Para testes, use a funcionalidade de download manual.

## Estrutura do Projeto

```
youtube-shorts-generator/
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── auth.py          # Autenticação OAuth
│   │   │   ├── youtube.py       # APIs do YouTube
│   │   │   ├── video_processing.py  # Processamento de vídeo
│   │   │   ├── upload.py        # Upload para plataformas
│   │   │   └── user.py          # Gestão de utilizadores
│   │   ├── models/
│   │   ├── static/              # Ficheiros estáticos
│   │   └── main.py              # Ponto de entrada
│   ├── venv/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   └── package.json
└── README.md
```

## APIs Disponíveis

### YouTube
- `POST /api/youtube/video-info` - Obter informações do vídeo
- `POST /api/youtube/download-video` - Download do vídeo
- `POST /api/youtube/generate-shorts` - Gerar shorts

### Processamento de Vídeo
- `POST /api/video/process-video` - Processar vídeo e criar shorts
- `POST /api/video/add-watermark` - Adicionar marca d'água
- `GET /api/video/download-short/<id>` - Download de short

### Autenticação
- `GET /api/auth/google/login` - Iniciar login Google
- `GET /api/auth/tiktok/login` - Iniciar login TikTok
- `GET /api/auth/status` - Verificar status de autenticação
- `POST /api/auth/logout` - Logout

### Upload
- `POST /api/upload/youtube` - Upload para YouTube
- `POST /api/upload/tiktok` - Upload para TikTok
- `POST /api/upload/bulk` - Upload em massa

## Limitações e Considerações

1. **API do TikTok**: Requer aprovação especial para upload de vídeos
2. **Quotas do YouTube**: Limitadas pela Google API
3. **Processamento de Vídeo**: Requer recursos computacionais significativos
4. **Armazenamento**: Ficheiros temporários são criados durante o processamento

## Deployment

### Opção 1: Vercel (Recomendado)
1. Fazer build do frontend
2. Copiar ficheiros para o diretório static do Flask
3. Fazer deploy do backend no Vercel

### Opção 2: Heroku
1. Configurar Procfile
2. Adicionar buildpacks para Python e Node.js
3. Configurar variáveis de ambiente

### Opção 3: Docker
1. Criar Dockerfile para backend e frontend
2. Usar docker-compose para orquestração
3. Configurar volumes para armazenamento temporário

## Contribuição

1. Fork o projeto
2. Criar branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit das alterações (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - ver o ficheiro [LICENSE](LICENSE) para detalhes.

## Suporte

Para suporte, abra uma issue no GitHub ou contacte a equipa de desenvolvimento.

---

**Nota**: Esta aplicação é para fins educacionais e de demonstração. Certifique-se de cumprir os termos de serviço do YouTube e TikTok ao usar suas APIs.

