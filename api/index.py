from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript_route():
    video_id = request.args.get('videoId')

    if not video_id:
        return jsonify({"error": "videoId parameter is required"}), 400

    try:
        # This is the correct way to call the function with the modern library version
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        return jsonify({"success": True, "transcript": full_transcript})

    except NoTranscriptFound:
        return jsonify({"success": False, "error": "Transcript not found for this video."}), 404
    except TranscriptsDisabled:
        return jsonify({"success": False, "error": "Transcripts are disabled for this video."}), 403
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    return "YouTube Transcript API is running."
