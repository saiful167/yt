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
        "message": "Welcome to Saiful's Multi-Source Video API"
    })

@app.route('/api/video', methods=['GET'])
def get_video_data():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({
            "success": False,
            "developer": "Saiful Islam",
            "error": "Please provide a valid URL"
        }), 400

    try:
        # yt-dlp কনফিগারেশন
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'nocheckcertificate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ভিডিওর তথ্য সংগ্রহ করা
            info = ydl.extract_info(video_url, download=False)
            
            # ডাটা ফিল্টারিং করা
            formats = []
            for f in info.get('formats', []):
                # ভিডিও এবং অডিও লিঙ্কগুলো আলাদা করা
                if f.get('url'):
                    formats.append({
                        "quality": f.get('format_note') or f.get('height'),
                        "extension": f.get('ext'),
                        "size": f.get('filesize') or f.get('filesize_approx'),
                        "download_url": f.get('url')
                    })

            response = {
                "success": True,
                "developer": "Saiful Islam",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "direct_links": formats[:10] # সেরা ১০টি লিঙ্ক দেখাবে
            }
            
            return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "developer": "Saiful Islam",
            "error": str(e)
        }), 500

app = app

