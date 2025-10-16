from flask import Flask, request, jsonify
import requests, hashlib, redis, json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#redis_client = redis.Redis(host='redis', port=6379, db=0)

SERVICES = {
    "type_check": "http://localhost:5001/check",
    "resolution_check": "http://localhost:5002/check",
    "bw_check": "http://localhost:5003/check"
}

def call_service(name, url, image_id):
    try:
        res = requests.post(url, json={"image_id": image_id}).json()
        return name, res
    except Exception as e:
        return name, {"status": "FAIL", "reason": str(e)}

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file received"}), 400
    
    image = request.files['image']
    image_bytes = image.read()

    #  Hash-based ID
    image_id = hashlib.md5(image_bytes).hexdigest()
    if not redis_client.exists(image_id):
        redis_client.set(image_id, image_bytes)
        
    cached_result = redis_client.get(f"result:{image_id}")
    if cached_result:
        cached_result = json.loads(cached_result)  
        return jsonify(cached_result)
    
    # Parallel Execution Starts Here
    with ThreadPoolExecutor() as executor:
        tasks = [executor.submit(call_service, name, url, image_id) for name, url in SERVICES.items()]
        
        for future in as_completed(tasks):
            name, result = future.result()
            fail_result = {
            "final_status": "FAIL",
            "failed_at": name,
            "reason": result.get("reason")
            }

            if result.get("status") != "PASS":
                redis_client.set(f"result:{image_id}", json.dumps(fail_result))
                return jsonify(fail_result)
            
    redis_client.set(f"final_status:{image_id}", "PASS") 
    return jsonify({"final_status": "PASS", "image_id": image_id})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
