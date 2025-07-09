from flask import Blueprint, request, jsonify
import yt_dlp
import os
import tempfile
import json

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/video-info', methods=['POST'])
def get_video_info():
    """Obter informações de um vídeo do YouTube"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL é obrigatório'}), 400
        
        # Configurar yt-dlp para obter apenas informações
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extrair informações relevantes
            video_info = {
                'id': info.get('id'),
                'title': info.get('title'),
                'description': info.get('description'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'uploader': info.get('uploader'),
                'upload_date': info.get('upload_date'),
                'view_count': info.get('view_count'),
                'formats': []
            }
            
            # Obter formatos de vídeo disponíveis
            if info.get('formats'):
                for fmt in info['formats']:
                    if fmt.get('vcodec') != 'none':  # Apenas formatos com vídeo
                        video_info['formats'].append({
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('quality'),
                            'height': fmt.get('height'),
                            'width': fmt.get('width'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url')
                        })
            
            return jsonify(video_info)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@youtube_bp.route('/download-video', methods=['POST'])
def download_video():
    """Fazer download de um vídeo do YouTube"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_id = data.get('format_id', 'best')
        
        if not url:
            return jsonify({'error': 'URL é obrigatório'}), 400
        
        # Criar diretório temporário para downloads
        temp_dir = tempfile.mkdtemp()
        
        # Configurar yt-dlp para download
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Encontrar o ficheiro descarregado
            downloaded_file = None
            for file in os.listdir(temp_dir):
                if file.endswith(('.mp4', '.webm', '.mkv')):
                    downloaded_file = os.path.join(temp_dir, file)
                    break
            
            if downloaded_file:
                return jsonify({
                    'success': True,
                    'file_path': downloaded_file,
                    'title': info.get('title'),
                    'duration': info.get('duration')
                })
            else:
                return jsonify({'error': 'Falha no download do vídeo'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@youtube_bp.route('/generate-shorts', methods=['POST'])
def generate_shorts():
    """Gerar shorts a partir de um vídeo"""
    try:
        data = request.get_json()
        video_path = data.get('video_path')
        segments = data.get('segments', [])
        max_duration = data.get('max_duration', 60)
        
        if not video_path:
            return jsonify({'error': 'Caminho do vídeo é obrigatório'}), 400
        
        if not os.path.exists(video_path):
            return jsonify({'error': 'Ficheiro de vídeo não encontrado'}), 404
        
        # Se não foram fornecidos segmentos, gerar automaticamente
        if not segments:
            # Lógica para gerar segmentos automaticamente
            # Por agora, vamos criar um segmento do início do vídeo
            segments = [{'start': 0, 'end': min(max_duration, 60)}]
        
        shorts_info = []
        for i, segment in enumerate(segments):
            short_info = {
                'id': f'short_{i+1}',
                'start_time': segment.get('start', 0),
                'end_time': segment.get('end', max_duration),
                'duration': segment.get('end', max_duration) - segment.get('start', 0),
                'title': f"Short {i+1}",
                'status': 'ready'
            }
            shorts_info.append(short_info)
        
        return jsonify({
            'success': True,
            'shorts': shorts_info,
            'total_shorts': len(shorts_info)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

