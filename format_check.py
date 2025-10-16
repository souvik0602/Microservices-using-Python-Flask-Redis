# service_type_check.py
from flask import Flask, request, jsonify
from PIL import Image
import io, redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#redis_client = redis.Redis(host='redis', port=6379, db=0)
@app.route('/check', methods=['POST'])
def check_type():
    data = request.get_json()
    image_id = data.get("image_id")
    print(image_id)
    if not image_id:
        return jsonify({"status": "FAIL", "reason": "No image ID"}), 400

    image_bytes = redis_client.get(image_id)
    if not image_bytes:
        return jsonify({"status": "FAIL", "reason": "Image not in Redis"}), 400

    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.format != "JPEG":
            return jsonify({"status": "FAIL", "reason": "Not a JPG"})
        return jsonify({"status": "PASS"})
    except:
        return jsonify({"status": "FAIL", "reason": "Invalid image format"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
