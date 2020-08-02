from flask import Flask, request, jsonify
import requests as req
app = Flask(__name__)

def retrieveData(imageURL, videoURL):
    image = req.get(imageURL)
    video = req.get(videoURL)
    print('Done')

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    imageURL = request.args.get("image", None)
    videoURL = request.args.get("video", None)

    # For debugging
    print(f"got image {imageURL}")
    print(f"got video {videoURL}")

    response = {}

    # Check if user sent a name at all
    if not imageURL or not videoURL:
        response["ERROR"] = "Please send a valid video and image"
    # Check if the user entered a number not a name
    elif str(imageURL).isdigit() or str(imageURL).isdigit():
        response["ERROR"] = "URLs can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Received correct video and image output"
        retrieveData(imageURL, videoURL)

    # Return the response in json format
    return jsonify(response)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our image finding server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)