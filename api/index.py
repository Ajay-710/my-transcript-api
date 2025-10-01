from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript_route():
    video_id = request.args.get('videoId')

    if not video_id:
        return jsonify({"error": "videoId parameter is required"}), 400

    try:
        # This is the simplest and most direct way to get a transcript.
        # The library will automatically find an available English transcript.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        return jsonify({"success": True, "transcript": full_transcript})

    except NoTranscriptFound:
        # This error is now more specific if no English transcript is found.
        return jsonify({"success": False, "error": "No English transcript was found for this video."}), 404
    except TranscriptsDisabled:
        return jsonify({"success": False, "error": "Transcripts are disabled for this video."}), 403
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    return "YouTube Transcript API is running."
