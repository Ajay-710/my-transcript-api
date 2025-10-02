from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript_route():
    # Get the video ID from the URL parameter (e.g., ?videoId=...)
    video_id = request.args.get('videoId')

    # If no videoId is provided, return an error
    if not video_id:
        return jsonify({"success": False, "error": "videoId parameter is required"}), 400

    try:
        # This is the standard, most reliable way to call the library.
        # We explicitly ask for an English transcript.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Join all the text parts into a single string
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # Return the successful response
        return jsonify({"success": True, "transcript": full_transcript})

    except NoTranscriptFound:
        return jsonify({"success": False, "error": "No English transcript was found for this video."}), 404
    except TranscriptsDisabled:
        return jsonify({"success": False, "error": "Transcripts are disabled for this video."}), 403
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    return "YouTube Transcript API is running."
