from flask import Flask, jsonify, request, make_response
from PIL import Image
import numpy as np
import logging, math, os
from sap.cf_logging import flask_logging

app = Flask(__name__)

#Iitialize logging
flask_logging.init(app, logging.INFO)

cf_port = os.getenv('PORT')

# Only get method by default
@app.route('/', methods=["GET", "POST"])
def hello():
    logger = logging.getLogger('my.logger')

    logger.info(request.files)

    image = Image.open(request.files['sampleImage'].stream)
    logger.info(image)

    #Calculate resize ratio
    ratio = math.sqrt(image.width * image.height / 400)

    #If need to make image file smaller
    if ratio > 1:
        image.thumbnail((int(image.width / ratio), int(image.height / ratio)))

    logger.info(image)

    (im_width, im_height) = image.size

    #Change file format for general TensorFlow format
    image_np = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
    image_list = image_np.tolist()
    return make_response(jsonify(image_list))

if __name__ == '__main__':
    if cf_port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)
