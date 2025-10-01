from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript_route():
    video_id = request.args.get('videoId')

    if not video_id:
        return jsonify({"error": "videoId parameter is required"}), 400

    try:
        # This is a more robust way to get a transcript.
        # It first lists available transcripts for the video.
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to find the English transcript specifically.
        transcript = transcript_list.find_transcript(['en'])
        
        # Fetch the actual transcript data.
        transcript_data = transcript.fetch()

        # Combine the text into a single string.
        full_transcript = " ".join([item['text'] for item in transcript_data])
        
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
