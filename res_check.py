# service_resolution_check.py
from flask import Flask, request, jsonify
from PIL import Image
import io, redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#redis_client = redis.Redis(host='redis', port=6379, db=0)
@app.route('/check', methods=['POST'])
def check_resolution():
    data = request.get_json()
    image_id = data.get("image_id")
    print(image_id)
    if not image_id:
        return jsonify({"status": "FAIL", "reason": "No image ID"}), 400

    image_bytes = redis_client.get(image_id)
    if not image_bytes:
        return jsonify({"status": "FAIL", "reason": "Image not in Redis"}), 400
    
    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size
    
    if width >= 640 and height >= 640:
        return jsonify({"status": "PASS"})
    else:
        return jsonify({"status": "FAIL", "reason": f"Resolution too low: {width}x{height}"})

if __name__ == '__main__':
    app.run(port=5002, debug=True)
