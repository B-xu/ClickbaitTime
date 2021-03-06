from flask import Flask, request, jsonify
from rq import Queue
from rq.job import Job
from getVideoURL import findVideo
from worker import conn
import redis
from def_find_frame import find_frame

app = Flask(__name__)
q = Queue(connection=conn)

def retrieveData(imageURL, videoURL, id):
    return find_frame(imageURL,videoURL, id)

@app.route('/getmsg/', methods=['GET'])
def respond():
    from app import retrieveData
    # Retrieve the name from url parameter
    imageURL = request.args.get("image", None)
    id = request.args.get("id", None)

    response = {}

    # Check if user sent a name at all
    if not id or not imageURL:
        response["ERROR"] = "Please send a valid id and image"
    # Check if the user entered a number not a name
    # elif str(imageURL).isdigit() or str(imageURL).isdigit():
    #     response["ERROR"] = "URLs can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Received correct video and image output"
        videoURL = findVideo(id)
        job = q.enqueue(retrieveData, args=(imageURL,videoURL,id), result_ttl=5000)
        response["id"] = job.get_id()
        print(job.get_id())


    # Return the response in json format
    return jsonify(response)

@app.route('/getTime/<job_key>', methods=['GET'])
def getTime(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:        
        response = {}
        result = job.result
        response["time"] = result
        return jsonify(response)
    else:
        return "Nay!", 202

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our image finding server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)