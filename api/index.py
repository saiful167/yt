from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"developer": "Saiful Islam", "status": "Online"})

@app.route('/api/video', methods=['GET'])
def get_video_data():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL is required", "developer": "Saiful Islam"}), 400

    # Vercel-এর রাইট-অ্যাক্সেস ফোল্ডার (/tmp) ব্যবহার করা
    cookie_src = os.path.join(os.path.dirname(__file__), '..', 'cookies.txt')
    cookie_dest = '/tmp/cookies.txt'

    try:
        # কুকি ফাইলটি রিড-অনলি জায়গা থেকে /tmp ফোল্ডারে কপি করা
        if os.path.exists(cookie_src):
            shutil.copy2(cookie_src, cookie_dest)

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'cookiefile': cookie_dest, # /tmp ফোল্ডারের ফাইলটি ব্যবহার করা
            'format': 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('url'):
                    formats.append({
                        "quality": f.get('format_note') or f.get('height'),
                        "extension": f.get('ext'),
                        "download_url": f.get('url')
                    })

            return jsonify({
                "success": True,
                "developer": "Saiful Islam",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "direct_links": formats[:8]
            }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "developer": "Saiful Islam"}), 500

app = app
