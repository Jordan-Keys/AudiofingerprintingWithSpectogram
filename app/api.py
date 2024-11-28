from flask import Flask, request, jsonify, send_file
import os
import logging
from audiofingerprintingandmatchingwithvisualisationFinal import fingerprint_audio, compare_fingerprints, visualize_fingerprints

# Configure logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Define directories used by the application
IMAGE_DIR = '/tmp/images'
TEMP_DIR = '/tmp/audio_files'
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/compare', methods=['POST'])
def compare():
    try:
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if not file1 or not file2:
            return jsonify({'error': 'Both files must be provided'}), 400

        # Save uploaded files to the TEMP_DIR
        filepath1 = os.path.join(TEMP_DIR, file1.filename)
        filepath2 = os.path.join(TEMP_DIR, file2.filename)
        file1.save(filepath1)
        file2.save(filepath2)

        fingerprint1 = fingerprint_audio(filepath1)
        fingerprint2 = fingerprint_audio(filepath2)

        # Ensure fingerprints are processed correctly
        if fingerprint1 is None or fingerprint2 is None:
            os.remove(filepath1)
            os.remove(filepath2)
            return jsonify({'error': 'Could not process fingerprint for provided files'}), 500

        score = compare_fingerprints(fingerprint1, fingerprint2)
        score = float(score)  # Ensure the score is a float

        # Save visualization to IMAGE_DIR
        visualize_fingerprints(fingerprint1, fingerprint2, file1.filename, file2.filename, IMAGE_DIR)

        # Clean up temporary files
        os.remove(filepath1)
        if os.path.exists(filepath2):
             os.remove(filepath2)
        else:
             print(f"Cannot remove file {filepath2}, it does not exist.")

        return jsonify({'similarity_score': score, 'image_path': '/download_image'})

    except Exception as e:
        logging.error(f"Error during comparison: {e}")
        return jsonify({'error': f"An error occurred during processing: {e}"}), 500

@app.route('/download_image', methods=['GET'])
def download_image():
    image_path = os.path.join(IMAGE_DIR, 'audio_comparison.png')
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png', as_attachment=True, download_name='audio_comparison.png')
    else:
        return jsonify({'error': 'Image not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

