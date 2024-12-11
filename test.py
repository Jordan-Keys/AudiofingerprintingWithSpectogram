import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths to the test audio files
file1_path = '/pathtofile/audio1.mp3'
file2_path = '/pathtofile/audio2.mp3'

# API endpoint for comparing audio files
api_url = 'http://172.17.0.2:5000/compare'

def test_compare_api(file1, file2):
    # Open files in binary mode and post them to the API
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        files = {
            'file1': f1,
            'file2': f2
        }
        response = requests.post(api_url, files=files)

    if response.status_code == 200:
        # Parse JSON response
        result = response.json()
        similarity_score = result.get('similarity_score')
        print(f"Similarity Score: {similarity_score}")

        # Add a comment based on the similarity score
        threshold = 0.8  # Example threshold
        if similarity_score >= threshold:
            print(f"The audio files are likely the same.")
        else:
            print(f"The audio files are likely different.")

        # Retrieve and download the image
        # Ensure JSON response includes correct path
        image_url = result.get('image_path')
        if image_url:
            fetch_and_display_image(f"http://localhost:5000{image_url}")
    else:
        print("Error:", response.status_code, response.text)

def fetch_and_display_image(image_url):
    # Send a request to download the image
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Raise exception for HTTP errors

    # Save the image locally
    image_path = '/Desktop/image.png'
    with open(image_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Image downloaded to: {image_path}')

    # Display the image using matplotlib
    img = mpimg.imread(image_path)
    plt.imshow(img)
    plt.axis('off')  # Turn off the axis
    plt.show()

# Run the test
test_compare_api(file1_path, file2_path)
