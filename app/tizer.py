import jp2iser
from flask import Flask, request, jsonify
import logging
import sys


logging.basicConfig(stream=sys.stderr)

application = Flask(__name__)
app = application
app.config.from_object(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    result = {"status": "working"}
    return jsonify(result)

@app.route("/convert", methods=["POST"])
def convert():

    data = request.get_json()
    job_id = data.get("jobId")
    operation = data.get("operation")
    if operation is None:
        operation = "ingest"
    source = data.get("source")
    destination = data.get("destination")
    thumb_dir = data.get("thumbDir")
    optimisation = data.get("optimisation")
    image_id = data.get("imageId")
    if thumb_dir and thumb_dir[-1] != "/":
        thumb_dir += "/"
    thumb_sizes = data.get("thumbSizes")
    origin = data.get("origin")

    # TODO check rest for Noneness
    if source is not None:
        # currently no idea how this really went as no return value
        result = jp2iser.process(source, destination=destination, bounded_sizes=thumb_sizes, bounded_folder=thumb_dir,
                                 optimisation=optimisation, jpeg_info_id=image_id, operation=operation)
        result["source"] = source

    else:
        result = {"status": "Job failed"}

    result["jobId"] = job_id
    result["origin"] = origin
    result["imageId"] = image_id

    return jsonify(result)

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
