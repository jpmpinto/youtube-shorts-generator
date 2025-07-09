from flask import Blueprint, request, jsonify, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
import os
import json

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/youtube', methods=['POST'])
def upload_to_youtube():
    """Fazer upload de um short para o YouTube"""
    try:
        # Verificar se o utilizador está autenticado
        if 'google_credentials' not in session:
            return jsonify({'error': 'Utilizador não autenticado no Google'}), 401
        
        data = request.get_json()
        video_path = data.get('video_path')
        title = data.get('title', 'YouTube Short')
        description = data.get('description', 'Criado com YouTube to Shorts Generator')
        tags = data.get('tags', ['shorts', 'youtube'])
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Ficheiro de vídeo não encontrado'}), 400
        
        # Criar credenciais
        creds = Credentials.from_authorized_user_info(session['google_credentials'])
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Metadados do vídeo
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'  # Categoria "People & Blogs"
            },
            'status': {
                'privacyStatus': 'public',  # ou 'private', 'unlisted'
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload do vídeo
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = insert_request.execute()
        
        return jsonify({
            'success': True,
            'video_id': response['id'],
            'video_url': f"https://www.youtube.com/watch?v={response['id']}",
            'title': response['snippet']['title'],
            'status': response['status']['privacyStatus']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/tiktok', methods=['POST'])
def upload_to_tiktok():
    """Fazer upload de um short para o TikTok"""
    try:
        # Verificar se o utilizador está autenticado
        if 'tiktok_credentials' not in session:
            return jsonify({'error': 'Utilizador não autenticado no TikTok'}), 401
        
        data = request.get_json()
        video_path = data.get('video_path')
        title = data.get('title', 'TikTok Short')
        description = data.get('description', 'Criado com YouTube to Shorts Generator')
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Ficheiro de vídeo não encontrado'}), 400
        
        # Nota: A API do TikTok requer aprovação especial para upload de vídeos
        # Esta é uma implementação simulada
        
        # Em produção, você usaria algo como:
        # access_token = session['tiktok_credentials']['access_token']
        # 
        # # Primeiro, fazer upload do vídeo
        # upload_url = 'https://open-api.tiktok.com/share/video/upload/'
        # 
        # with open(video_path, 'rb') as video_file:
        #     files = {'video': video_file}
        #     data = {
        #         'access_token': access_token,
        #         'title': title,
        #         'description': description
        #     }
        #     response = requests.post(upload_url, files=files, data=data)
        
        # Por agora, retornar uma resposta simulada
        return jsonify({
            'success': True,
            'message': 'Upload simulado para o TikTok',
            'note': 'A API do TikTok requer aprovação especial para upload de vídeos',
            'alternative': 'Use a funcionalidade de download para fazer upload manual'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/bulk', methods=['POST'])
def bulk_upload():
    """Fazer upload em massa de shorts"""
    try:
        data = request.get_json()
        shorts = data.get('shorts', [])
        platforms = data.get('platforms', ['youtube'])  # ['youtube', 'tiktok']
        
        if not shorts:
            return jsonify({'error': 'Nenhum short fornecido'}), 400
        
        results = []
        
        for short in shorts:
            short_result = {
                'short_id': short.get('id'),
                'platforms': {}
            }
            
            # Upload para YouTube
            if 'youtube' in platforms and 'google_credentials' in session:
                try:
                    youtube_result = upload_single_to_youtube(short)
                    short_result['platforms']['youtube'] = youtube_result
                except Exception as e:
                    short_result['platforms']['youtube'] = {'error': str(e)}
            
            # Upload para TikTok
            if 'tiktok' in platforms and 'tiktok_credentials' in session:
                try:
                    tiktok_result = upload_single_to_tiktok(short)
                    short_result['platforms']['tiktok'] = tiktok_result
                except Exception as e:
                    short_result['platforms']['tiktok'] = {'error': str(e)}
            
            results.append(short_result)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def upload_single_to_youtube(short):
    """Helper para upload individual no YouTube"""
    creds = Credentials.from_authorized_user_info(session['google_credentials'])
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': short.get('title', 'YouTube Short'),
            'description': short.get('description', 'Criado com YouTube to Shorts Generator'),
            'tags': ['shorts', 'youtube'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(short['path'], chunksize=-1, resumable=True)
    
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = insert_request.execute()
    
    return {
        'success': True,
        'video_id': response['id'],
        'video_url': f"https://www.youtube.com/watch?v={response['id']}"
    }

def upload_single_to_tiktok(short):
    """Helper para upload individual no TikTok"""
    # Implementação simulada
    return {
        'success': True,
        'message': 'Upload simulado para o TikTok',
        'note': 'API do TikTok requer aprovação especial'
    }

@upload_bp.route('/status/<upload_id>', methods=['GET'])
def get_upload_status(upload_id):
    """Verificar o status de um upload"""
    try:
        # Em produção, você consultaria uma base de dados para o status
        return jsonify({
            'upload_id': upload_id,
            'status': 'completed',
            'message': 'Upload concluído com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

