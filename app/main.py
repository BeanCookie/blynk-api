from flask import request, Flask, jsonify
from multiprocessing import Value

import os

image_dir = "images"
counter_file = "counter.db"

if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        counter = Value('i', int(f.readline()))
else:
    counter = Value('i', 0)


if not os.path.exists(image_dir):
    os.mkdir(image_dir)

app = Flask(__name__)
app.debug = True

@app.route('/upload', methods=['POST'])
def upload():
    with counter.get_lock():
        counter.value += 1
        count = counter.value
        with open(counter_file, "w") as f:
            f.write("%d\n" % int(count))
        image_path = os.path.join(image_dir, "image_" + str(count) + ".jpg")
        with open(image_path, "wb") as f:
            f.write(request.data)
    return jsonify({"code": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)