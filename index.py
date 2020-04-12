from flask import *
import io
from modules.TinyDBController import TinyDBController
import numpy as np


# For nginx server...
# app = Flask(__name__)

# For local server...
app = Flask(__name__, static_url_path='', static_folder='.',)


def main():
    TinyDBObj = TinyDBController()
    TinyDBObj.load_tables(['user'])
    TinyDBObj.tables['user'].purge_tables()
    TinyDBObj.insert('user', {'name': 'a', 'age': 23})
    TinyDBObj.insert('user', {'name': 'b', 'age': 23})
    TinyDBObj.insert('user', {'name': 'c', 'age': 24})
    print(TinyDBObj.tables['user'].all())
    TinyDBObj.update('user', 'name', 'c', 'age', 99)


def handle_file_upload(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return (np.array([]), '')

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return (np.array([]), file.filename)

    if file and valid_file(file.filename):
        return (decode_img(file), file.filename)


def decode_img(file):
    in_memory_img = io.BytesIO()
    file.save(in_memory_img)
    imgbuf = np.fromstring(in_memory_img.getvalue(), np.uint8)
    img = cv.imdecode(imgbuf, cv.IMREAD_UNCHANGED)
    return img


def createErrorResponse(message, code):
    payload = {}
    payload["error_message"] = message
    payload["http_code"] = code
    return jsonify(payload), code


@app.route("/")
def homepage():
    return "Homepage"


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


@app.route("/api/v1/test", methods=["POST"])
def ocr_endpoint():
    payload = "lmao1"
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
    # image, filename = handle_file_upload(request)
    # if image.shape[0] == 0:
    #     return createErrorResponse("NO IMAGE UPLOADED", 400)
    #
    # # For a grayscale/single channel image that is uploaded
    # if len(image.shape) == 2:
    #     image = cv.merge((image, image, image))
    #
    # languages = request.form.get("lang")
    # if languages is None:
    #     return createErrorResponse("NO LANGUAGE(S) SPECIFIED", 400)
    #
    # (imageHeight, imageWidth) = image.shape[:2]
    # imageMeta = {}
    # imageMeta["ext"] = filename.split('.')[1]
    # imageMeta["width"] = imageWidth
    # imageMeta["height"] = imageHeight
    # imageMeta["filename"] = filename
    #
    # outputFileName = "{}_{}_texts".format(filename.split('.')[0], languages)
    # outputFileNameWithExt = outputFileName + '.' + imageMeta["ext"]
    #
    # boxes = textDetector.detectTexts(image, imageMeta, outputFileNameWithExt)
    # results = ocrEngine.performOCR(image, boxes, imageMeta, languages)
    #
    # origImgPath = outputImage(image, filename);
    #
    # payload = {}
    # payload["imageWidth"] = imageWidth;
    # payload["imageHeight"] = imageHeight;
    # payload["recognisedTexts"] = results
    # payload["filename"] = outputFileName
    # payload["originalImageURL"] = origImgPath;
    # payload["textDetectionsURL"] = textDetector.getOutputFilePath(
    #     outputFileNameWithExt)
    # response = jsonify(payload)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response, 200


@app.route("/api/v1/test2", methods=["POST"])
def color_separation_endpoint():
    payload = "lmao2"
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


if __name__ == "__main__":
    main()
    app.run()
