from flask import Flask, request, render_template, jsonify
import requests, re

app = Flask(__name__)

def get_sold_quantity(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        match = re.search(r'(\d[\d,]*)\s+sold', html, re.IGNORECASE)
        if match:
            return match.group(1).replace(',', '')
        else:
            return "Không tìm thấy"
    else:
        return f"Lỗi: {response.status_code}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    url = data.get("ebay_url")
    sold = get_sold_quantity(url)
    return jsonify({"sold": sold})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

