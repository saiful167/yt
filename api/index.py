from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# আপনার দেওয়া কুকিগুলো প্রসেস করার ফাংশন
def get_cookies():
    # এখানে আপনার দেওয়া প্রধান সেশন কুকিগুলো সাজানো হয়েছে
    return {
        "VISITOR_PRIVACY_METADATA": "CgJCRBIEGgAgMg%3D%3D",
        "__Secure-3PSID": "g.a0005wizLu87rqnmnHWeGPFWuyRbMpp_NvFvpuiKaBVyCncm6UZJDEE5NAyKk5wWAbZS64MPQAACgYKAZoSARUSFQHGX2Mi7QFkle3FWCJKymO0UReAERoVAUF8yKoNeS6TcR-zlwnscNrtrknr0076",
        "GPS": "1",
        "__Secure-1PSIDTS": "sidts-CjUB7I_69AiGFlWCIF_xdNig6LGS04ZMHN9Jr6FDWWWzyeuV8XwhgUga-3xkNqqab4Y5Jt538xAA",
        "__Secure-3PAPISID": "eoIxgQ98jlpKnGS4/AlzrXyA2NmkLW4sk0",
        "__Secure-3PSIDCC": "AKEyXzWyB6mNnqjdBctx27egrimEfRxFupKmIia84W6A_XT0nKA9LtxDa0q8hG-uFdK7QEiA",
        "__Secure-3PSIDTS": "sidts-CjUB7I_69AiGFlWCIF_xdNig6LGS04ZMHN9Jr6FDWWWzyeuV8XwhgUga-3xkNqqab4Y5Jt538xAA",
        "PREF": "tz=America.Tegucigalpa",
        "VISITOR_INFO1_LIVE": "jSlN01zseJs"
    }

@app.route('/')
def home():
    return jsonify({"developer": "Saiful Islam", "status": "Online"})

@app.route('/api/video')
def get_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided", "developer": "Saiful Islam"}), 400

    try:
        # yt-dlp অপশন সেটআপ
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            # সরাসরি কুকি ডাটা পাস করা
            'http_headers': {
                'Cookie': "; ".join([f"{k}={v}" for k, v in get_cookies().items()]),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('url'):
                    formats.append({
                        "quality": f.get('format_note') or f.get('height'),
                        "ext": f.get('ext'),
                        "url": f.get('url')
                    })

            return jsonify({
                "success": True,
                "developer": "Saiful Islam",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "direct_links": formats[:8] # সেরা ৮টি ফরম্যাট
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "developer": "Saiful Islam"}), 500

app = app
