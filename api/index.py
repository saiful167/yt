from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import concurrent.futures

app = Flask(__name__)
CORS(app)

# Target APIs
INFO_API = "https://downr.org/.netlify/functions/video-info"
DOWNLOAD_API = "https://downr.org/.netlify/functions/youtube-download"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://downr.org/",
    "Origin": "https://downr.org"
}

def get_link(video_url, quality):
    """ডাউনলোড লিঙ্ক জেনারেট করার ফাংশন"""
    payload = {
        "url": video_url,
        "downloadMode": "video",
        "videoQuality": quality
    }
    try:
        res = requests.post(DOWNLOAD_API, json=payload, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            return {f"download_{quality}": res.json().get("url")}
    except:
        return {f"download_{quality}": None}
    return {f"download_{quality}": None}

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "developer": "Saiful Islam",
        "message": "Welcome to Video Downloader API"
    })

@app.route('/api/video', methods=['GET'])
def get_all_in_one():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL is required", "developer": "Saiful Islam"}), 400

    try:
        # ১. ভিডিওর সাধারণ তথ্য আনা
        info_res = requests.post(INFO_API, json={"url": video_url}, headers=HEADERS, timeout=10)
        if info_res.status_code != 200:
            return jsonify({"error": "Failed to fetch data", "developer": "Saiful Islam"}), 500
        
        video_info = info_res.json()
        
        # ২. ১০৮০পি এবং ৭২০পি এর সরাসরি ডাউনলোড লিঙ্ক বের করা (একসাথে)
        links = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_link, video_url, q) for q in ["720p", "1080p"]]
            for f in concurrent.futures.as_completed(futures):
                links.update(f.result())

        # ৩. সব তথ্য একসাথে সাজানো
        response_data = {
            "success": True,
            "developer": "Saiful Islam",
            "title": video_info.get("title"),
            "thumbnail": video_info.get("thumbnail"),
            "duration_seconds": video_info.get("duration"),
            "formats": video_info.get("medias"),
            "direct_links": links
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e), "developer": "Saiful Islam"}), 500

# Vercel deployment
app = app
      
