import os, yt_dlp
from flask import Flask, request, send_file, render_template

# This ensures Flask knows exactly where the templates folder is
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    # We save to /tmp/ because Hugging Face has open write permissions there
    download_path = '/tmp'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        # NEW FIXES FOR ERRNO -5:
        'source_address': '0.0.0.0', # Forces IPv4
        'nocheckcertificate': True,
        'geo_bypass': True,
        'quiet': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Find the path of the downloaded file
            temp_path = ydl.prepare_filename(info)
            # Ensure the extension is .mp3 in our reference
            final_filename = os.path.splitext(temp_path)[0] + ".mp3"

        if os.path.exists(final_filename):
            return send_file(final_filename, as_attachment=True)
        else:
            return "File conversion failed - file not found.", 500

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Using 7860 for Hugging Face
    app.run(host='0.0.0.0', port=7860, debug=True)
