import yt_dlp
from mutagen.easyid3 import EasyID3
import os

def search_alternative_video(title, channel=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    # Construimos la consulta de búsqueda
    search_query = title
    if channel:
        search_query = f"{title} {channel}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                # Verificamos que el resultado sea relevante
                for entry in result['entries']:
                    if entry:  # Aseguramos que la entrada no sea None
                        return entry['url']  # Devuelve la URL del primer resultado válido
        except Exception as e:
            print(f"⚠️ Error en búsqueda alternativa: {str(e)}")
    return None

def download_playlist(playlist_url, default_artist="Punky con u"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/playlist/%(title)s.%(ext)s',
        'extract_flat': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in info:
                playlist_title = info['title']
                num_canciones = len(info['entries'])
                print(f"🎵 Playlist encontrada: {playlist_title} ({num_canciones} canciones)")
                
                for video in info['entries']:
                    video_title = video.get('title', 'Sin título')
                    video_channel = video.get('uploader', None)
                    downloaded = False
                    
                    # Intento 1: Descargar el video original
                    try:
                        ydl.download([video['url']])
                        mp3_file = f"downloads/playlist/{video_title}.mp3"
                        audio = EasyID3(mp3_file)
                        audio["artist"] = default_artist
                        audio["title"] = video_title
                        audio.save()
                        print(f"✅ {video_title} descargada")
                        downloaded = True
                    except Exception as e:
                        print(f"⚠️ Error con {video_title} (original): {str(e)} - Buscando alternativa...")
                    
                    # Intento 2: Buscar alternativa con el mismo título y canal
                    if not downloaded and video_channel:
                        print(f"🔍 Buscando alternativa para '{video_title}' del canal '{video_channel}'")
                        alternative_url = search_alternative_video(video_title, video_channel)
                        if alternative_url:
                            try:
                                ydl.download([alternative_url])
                                mp3_file = f"downloads/playlist/{video_title}.mp3"
                                audio = EasyID3(mp3_file)
                                audio["artist"] = default_artist
                                audio["title"] = video_title
                                audio.save()
                                print(f"✅ {video_title} descargada (alternativa del mismo canal)")
                                downloaded = True
                            except Exception as e:
                                print(f"⚠️ Error con {video_title} (alternativa del canal): {str(e)}")
                    
                    # Intento 3: Buscar alternativa solo con el título (si falló la búsqueda con canal o no había canal)
                    if not downloaded:
                        print(f"🔍 Buscando alternativa genérica para '{video_title}'")
                        alternative_url = search_alternative_video(video_title)
                        if alternative_url:
                            try:
                                ydl.download([alternative_url])
                                mp3_file = f"downloads/playlist/{video_title}.mp3"
                                audio = EasyID3(mp3_file)
                                audio["artist"] = default_artist
                                audio["title"] = video_title
                                audio.save()
                                print(f"✅ {video_title} descargada (alternativa genérica)")
                                downloaded = True
                            except Exception as e:
                                print(f"❌ Error con {video_title} (alternativa genérica): {str(e)}")
                        else:
                            print(f"❌ No se encontró alternativa para {video_title}")
            else:
                print("⚠️ El enlace no es una playlist válida")

    except Exception as e:
        print(f"🚨 Error: {str(e)}")

if __name__ == "__main__":
    os.makedirs("downloads/playlist", exist_ok=True)
    playlist_url = "https://www.youtube.com/playlist?list=PLB5dEiAFAzhH3ZzLzmlyYMakhIv4mZqxA"
    download_playlist(playlist_url)
