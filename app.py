import os
import yt_dlp
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    
    # Template for Title + .mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Get the actual filename generated
        temp_filename = ydl.prepare_filename(info)
        # Since we converted to mp3, ensure extension is correct
        final_filename = os.path.splitext(temp_filename)[0] + ".mp3"

    # Send the file to the user
    response = send_file(final_filename, as_attachment=True)

    # DELETE the file after sending so Render's disk doesn't fill up
    @response.call_on_close
    def cleanup():
        if os.path.exists(final_filename):
            os.remove(final_filename)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)