
import os
import threading
import time
import uuid

import yt_dlp
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DOWNLOAD_DIR = os.path.abspath("downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Konfigurasi penyimpanan job
JOB_RETENTION_SECONDS = 3600  # 1 jam

jobs = {}
jobs_lock = threading.Lock()


def cleanup_jobs():
    """Menghapus job selesai/gagal yang sudah lebih dari 1 jam."""
    now = time.time()

    with jobs_lock:
        expired_jobs = [
            job_id
            for job_id, job in jobs.items()
            if job.get("status") in ["completed", "error"]
            and now - job.get("finished_at", now) > JOB_RETENTION_SECONDS
        ]

        for job_id in expired_jobs:
            jobs.pop(job_id, None)


def run_conversion(job_id, url, format_type, resolution):

    def progress_hook(data):
        if data["status"] == "downloading":
            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate", 0)
            )
            downloaded = data.get("downloaded_bytes", 0)

            percent = (
                round(downloaded / total * 100, 1)
                if total else 0
            )

            with jobs_lock:
                jobs[job_id].update({
                    "status": "processing",
                    "progress": min(percent, 99),
                    "message": "Mengunduh media..."
                })

        elif data["status"] == "finished":
            with jobs_lock:
                jobs[job_id].update({
                    "progress": 99,
                    "message": "Memproses hasil konversi..."
                })

    try:
        unique_id = job_id[:8]

        # Penamaan file berdasarkan format dan kualitas
        if format_type == "mp3":
            filename = (
                f"%(title)s [MP3-192kbps] [{unique_id}].%(ext)s"
            )

        else:
            quality_label = (
                "Best" if resolution == "best"
                else f"{resolution}p"
            )

            filename = (
                f"%(title)s [MP4-{quality_label}] "
                f"[{unique_id}].%(ext)s"
            )

        options = {
            "outtmpl": os.path.join(DOWNLOAD_DIR, filename),
            "progress_hooks": [progress_hook],
            "noplaylist": True,
            "quiet": True,
        }

        if format_type == "mp3":
            options.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            })

        else:
            if resolution == "best":
                video_format = "bestvideo+bestaudio/best"
            else:
                video_format = (
                    f"bestvideo[height<={resolution}]"
                    f"+bestaudio/best[height<={resolution}]"
                )

            options.update({
                "format": video_format,
                "merge_output_format": "mp4",
            })

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        with jobs_lock:
            jobs[job_id].update({
                "status": "completed",
                "progress": 100,
                "message": "Konversi berhasil!",
                "finished_at": time.time()
            })

    except Exception as e:
        with jobs_lock:
            jobs[job_id].update({
                "status": "error",
                "message": str(e),
                "finished_at": time.time()
            })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    cleanup_jobs()

    url = request.form.get("url", "").strip()
    format_type = request.form.get("format")
    resolution = request.form.get("resolution")

    if not url:
        return jsonify({
            "error": "URL tidak boleh kosong"
        }), 400

    if format_type not in ["mp3", "mp4"]:
        return jsonify({
            "error": "Format tidak valid"
        }), 400

    if resolution not in ["best", "1080", "720", "480", "360"]:
        return jsonify({
            "error": "Resolusi tidak valid"
        }), 400

    job_id = str(uuid.uuid4())

    with jobs_lock:
        jobs[job_id] = {
            "status": "starting",
            "progress": 0,
            "message": "Menyiapkan konversi..."
        }

    thread = threading.Thread(
        target=run_conversion,
        args=(job_id, url, format_type, resolution),
        daemon=True
    )
    thread.start()

    return jsonify({
        "job_id": job_id
    })


@app.route("/progress/<job_id>")
def progress(job_id):

    cleanup_jobs()

    with jobs_lock:
        job = jobs.get(job_id)

        if not job:
            return jsonify({
                "error": "Job tidak ditemukan atau sudah kedaluwarsa"
            }), 404

        return jsonify(job.copy())


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
