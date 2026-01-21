from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "developer": "Saiful Islam",
        "message": "YouTube Multi-Quality Downloader API with Cookie Auth"
    })

@app.route('/api/video', methods=['GET'])
def get_video_data():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({
            "success": False, 
            "developer": "Saiful Islam", 
            "error": "URL is required"
        }), 400

    try:
        # Vercel-এ কুকি ফাইলের সঠিক পাথ নির্ধারণ
        # এটি মেইন ফোল্ডারে থাকা cookies.txt ফাইলটিকে খুঁজে বের করবে
        cookie_path = os.path.join(os.path.dirname(__file__), '..', 'cookies.txt')

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'cookiefile': cookie_path, # কুকি ফাইল ব্যবহার
            'format': 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর তথ্য সংগ্রহ করা
            info = ydl.extract_info(video_url, download=False)
            
            # ডাটা ফিল্টারিং করে ফরম্যাটগুলো সাজানো
            formats = []
            for f in info.get('formats', []):
                # শুধুমাত্র যেগুলোর ডাউনলোড লিঙ্ক (url) আছে সেগুলো নেওয়া
                if f.get('url'):
                    formats.append({
                        "quality": f.get('format_note') or f.get('height'),
                        "extension": f.get('ext'),
                        "size": f.get('filesize') or f.get('filesize_approx'),
                        "download_url": f.get('url')
                    })

            # ফাইনাল রেসপন্স ডাটা
            response_data = {
                "success": True,
                "developer": "Saiful Islam",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "direct_links": formats[:10] # সেরা ১০টি ডাউনলোড লিঙ্ক
            }
            
            return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "success": False, 
            "developer": "Saiful Islam", 
            "error": str(e)
        }), 500

# Vercel-এর জন্য app অবজেক্ট এক্সপোজ করা
app = app
