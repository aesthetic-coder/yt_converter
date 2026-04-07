FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app
COPY --chown=user . .

# Force the latest yt-dlp version
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -U yt-dlp

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app", "--timeout", "120"]