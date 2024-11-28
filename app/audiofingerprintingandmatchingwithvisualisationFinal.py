import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

def compare_fingerprints(fingerprint1, fingerprint2):
    """Compares two audio fingerprints and returns a similarity score."""
    if fingerprint1 is None or fingerprint2 is None:
        return 0  # where fingerprinting failed
    min_length = min(fingerprint1.shape[1], fingerprint2.shape[1])
    fingerprint1 = fingerprint1[:, :min_length]
    fingerprint2 = fingerprint2[:, :min_length]
    similarity = np.dot(fingerprint1.flatten(), fingerprint2.flatten()) / (
        np.linalg.norm(fingerprint1.flatten()) * np.linalg.norm(fingerprint2.flatten())
    )
    return similarity

def fingerprint_audio(file_path):
    """Generates a fingerprint for an audio file using librosa."""
    try:
        if os.path.exists(file_path):
            y, sr = librosa.load(file_path)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            return chroma
        else:
            print(f"File not found: {file_path}")
            return None
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def visualize_fingerprints(fingerprint1, fingerprint2, file1, file2, image_dir='/tmp/images'):
    """Visualizes the given fingerprints."""
    if fingerprint1 is not None and fingerprint2 is not None:
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        librosa.display.specshow(fingerprint1, sr=22050, x_axis='time', y_axis='chroma')
        plt.title(f'Fingerprint of {file1}')
        plt.colorbar()
        plt.subplot(2, 1, 2)
        librosa.display.specshow(fingerprint2, sr=22050, x_axis='time', y_axis='chroma')
        plt.title(f'Fingerprint of {file2}')
        plt.colorbar()
        plt.tight_layout()
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, 'audio_comparison.png')
        plt.savefig(image_path)
        plt.close()
    else:
        print("Visualization skipped due to failed processing of one or both files.")

