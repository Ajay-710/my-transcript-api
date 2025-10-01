from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    # Get the videoId from the query parameters (e.g., ?videoId=xyz)
    video_id = request.args.get('videoId')

    # If no videoId is provided, return an error
    if not video_id:
        return jsonify({"error": "videoId parameter is required"}), 400

    try:
        # Fetch the transcript using the library
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine the transcript text into a single string
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # Return the successful response
        return jsonify({"success": True, "transcript": full_transcript})

    except NoTranscriptFound:
        return jsonify({"success": False, "error": "Transcript not found for this video."}), 404
    except TranscriptsDisabled:
        return jsonify({"success": False, "error": "Transcripts are disabled for this video."}), 403
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

# This is a catch-all route for the root URL
@app.route('/', methods=['GET'])
def index():
    return "YouTube Transcript API is running."