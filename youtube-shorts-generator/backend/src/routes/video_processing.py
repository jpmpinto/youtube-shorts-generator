from flask import Blueprint, request, jsonify, send_file
import os
import tempfile
import subprocess
from moviepy.editor import VideoFileClip
import yt_dlp
import uuid

video_processing_bp = Blueprint('video_processing', __name__)

@video_processing_bp.route('/process-video', methods=['POST'])
def process_video():
    """Processar vídeo do YouTube e criar shorts"""
    try:
        data = request.get_json()
        url = data.get('url')
        segments = data.get('segments', [])
        max_duration = data.get('max_duration', 60)
        
        if not url:
            return jsonify({'error': 'URL é obrigatório'}), 400
        
        # Criar diretório temporário
        temp_dir = tempfile.mkdtemp()
        video_id = str(uuid.uuid4())
        
        # Download do vídeo
        ydl_opts = {
            'format': 'best[height<=720]',  # Limitar qualidade para economizar espaço
            'outtmpl': os.path.join(temp_dir, f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Encontrar o ficheiro descarregado
            downloaded_file = None
            for file in os.listdir(temp_dir):
                if file.startswith(video_id):
                    downloaded_file = os.path.join(temp_dir, file)
                    break
            
            if not downloaded_file:
                return jsonify({'error': 'Falha no download do vídeo'}), 500
            
            # Se não foram fornecidos segmentos, gerar automaticamente
            if not segments:
                video_duration = info.get('duration', 0)
                segments = generate_auto_segments(video_duration, max_duration)
            
            # Processar cada segmento
            shorts_info = []
            for i, segment in enumerate(segments):
                short_path = create_short(
                    downloaded_file, 
                    segment['start'], 
                    segment['end'], 
                    temp_dir, 
                    f'short_{i+1}'
                )
                
                if short_path:
                    shorts_info.append({
                        'id': f'short_{i+1}',
                        'path': short_path,
                        'start_time': segment['start'],
                        'end_time': segment['end'],
                        'duration': segment['end'] - segment['start'],
                        'title': f"Short {i+1} - {info.get('title', 'Sem título')[:30]}...",
                        'status': 'ready'
                    })
            
            return jsonify({
                'success': True,
                'video_info': {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail')
                },
                'shorts': shorts_info,
                'total_shorts': len(shorts_info)
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_processing_bp.route('/download-short/<short_id>', methods=['GET'])
def download_short(short_id):
    """Fazer download de um short específico"""
    try:
        # Em produção, você armazenaria o caminho do ficheiro numa base de dados
        # Por agora, vamos simular
        return jsonify({'message': 'Download endpoint - implementar com armazenamento persistente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_auto_segments(video_duration, max_duration=60):
    """Gerar segmentos automaticamente baseado na duração do vídeo"""
    segments = []
    
    if video_duration <= max_duration:
        # Se o vídeo é menor que o máximo, usar o vídeo inteiro
        segments.append({'start': 0, 'end': video_duration})
    else:
        # Dividir o vídeo em segmentos
        num_segments = min(5, video_duration // max_duration + 1)  # Máximo 5 shorts
        segment_duration = min(max_duration, video_duration / num_segments)
        
        for i in range(int(num_segments)):
            start = i * segment_duration
            end = min(start + segment_duration, video_duration)
            if end - start >= 10:  # Mínimo 10 segundos
                segments.append({'start': int(start), 'end': int(end)})
    
    return segments

def create_short(input_path, start_time, end_time, output_dir, filename):
    """Criar um short a partir de um vídeo"""
    try:
        output_path = os.path.join(output_dir, f'{filename}.mp4')
        
        # Usar ffmpeg para criar o short com formato 9:16
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-ss', str(start_time),
            '-t', str(end_time - start_time),
            '-vf', 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',  # Sobrescrever ficheiro se existir
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
        else:
            print(f"Erro no ffmpeg: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Erro ao criar short: {str(e)}")
        return None

@video_processing_bp.route('/add-watermark', methods=['POST'])
def add_watermark():
    """Adicionar marca d'água a um vídeo"""
    try:
        data = request.get_json()
        video_path = data.get('video_path')
        watermark_text = data.get('watermark_text', '@YourBrand')
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Caminho do vídeo inválido'}), 400
        
        # Criar novo ficheiro com marca d'água
        output_path = video_path.replace('.mp4', '_watermarked.mp4')
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"drawtext=text='{watermark_text}':fontcolor=white:fontsize=24:x=10:y=h-th-10",
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'watermarked_path': output_path
            })
        else:
            return jsonify({'error': 'Falha ao adicionar marca d\'água'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

