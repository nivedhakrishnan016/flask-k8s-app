from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
items = {
    1: {"name": "Laptop", "price": 50000},
    2: {"name": "Mouse",  "price": 500},
}
next_id = 3


# ── HOME PAGE ──────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Flask REST API</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }

    .container { max-width: 860px; width: 100%; }

    .header { text-align: center; margin-bottom: 3rem; }

    .badge {
      display: inline-block;
      background: #1a1f2e;
      border: 1px solid #2d3748;
      color: #68d391;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.35rem 1rem;
      border-radius: 99px;
      margin-bottom: 1.2rem;
    }

    h1 {
      font-size: 2.8rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.2;
      margin-bottom: 1rem;
    }

    .subtitle {
      color: #718096;
      font-size: 1.05rem;
      line-height: 1.7;
      max-width: 520px;
      margin: 0 auto;
    }

    .status-bar {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 2.5rem;
      font-size: 0.85rem;
      color: #68d391;
      font-weight: 500;
    }

    .dot {
      width: 8px; height: 8px;
      border-radius: 50%;
      background: #68d391;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50%       { opacity: 0.3; }
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .card {
      background: #1a1f2e;
      border: 1px solid #2d3748;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      transition: border-color 0.2s, transform 0.2s;
    }

    .card:hover { border-color: #4a5568; transform: translateY(-2px); }

    .card-top {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.6rem;
    }

    .method {
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      letter-spacing: 0.05em;
      min-width: 52px;
      text-align: center;
    }

    .method.get    { background: #1a3a2a; color: #68d391; }
    .method.post   { background: #1a2a3a; color: #63b3ed; }
    .method.put    { background: #3a2a1a; color: #f6ad55; }
    .method.delete { background: #3a1a1a; color: #fc8181; }

    .endpoint {
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
      color: #e2e8f0;
      font-weight: 600;
    }

    .card-desc { font-size: 0.82rem; color: #718096; }

    .info-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .info-box {
      background: #1a1f2e;
      border: 1px solid #2d3748;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
    }

    .info-box h3 {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #4a5568;
      margin-bottom: 0.75rem;
    }

    .info-box p {
      font-family: 'Courier New', monospace;
      font-size: 0.88rem;
      color: #a0aec0;
      line-height: 1.9;
    }

    .info-box p span { color: #68d391; }

    .footer {
      text-align: center;
      font-size: 0.78rem;
      color: #4a5568;
      border-top: 1px solid #2d3748;
      padding-top: 1.5rem;
    }

    .footer strong { color: #718096; }

    @media (max-width: 560px) {
      h1 { font-size: 2rem; }
      .info-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">

    <div class="header">
      <div class="badge">Prophaze Technologies — DevOps Engineer Assignment</div>
      <h1>Flask REST API</h1>
      <p class="subtitle">
        Production-grade REST API containerized with Docker and orchestrated
        on a self-hosted Kubernetes cluster via kubeadm on AWS EC2.
      </p>
    </div>

    <div class="status-bar">
      <div class="dot"></div>
      Server is live and running
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-top">
          <span class="method get">GET</span>
          <span class="endpoint">/items</span>
        </div>
        <div class="card-desc">Retrieve all items</div>
      </div>

      <div class="card">
        <div class="card-top">
          <span class="method get">GET</span>
          <span class="endpoint">/items/&lt;id&gt;</span>
        </div>
        <div class="card-desc">Retrieve a single item by ID</div>
      </div>

      <div class="card">
        <div class="card-top">
          <span class="method post">POST</span>
          <span class="endpoint">/items</span>
        </div>
        <div class="card-desc">Create a new item</div>
      </div>

      <div class="card">
        <div class="card-top">
          <span class="method put">PUT</span>
          <span class="endpoint">/items/&lt;id&gt;</span>
        </div>
        <div class="card-desc">Update an existing item</div>
      </div>

      <div class="card">
        <div class="card-top">
          <span class="method delete">DELETE</span>
          <span class="endpoint">/items/&lt;id&gt;</span>
        </div>
        <div class="card-desc">Delete an item by ID</div>
      </div>

      <div class="card">
        <div class="card-top">
          <span class="method get">GET</span>
          <span class="endpoint">/health</span>
        </div>
        <div class="card-desc">Kubernetes health check probe</div>
      </div>
    </div>

    <div class="info-row">
      <div class="info-box">
        <h3>Stack</h3>
        <p>
          <span>→</span> Python Flask<br/>
          <span>→</span> Docker<br/>
          <span>→</span> Kubernetes (kubeadm)<br/>
          <span>→</span> AWS EC2 Ubuntu
        </p>
      </div>
      <div class="info-box">
        <h3>Quick Test</h3>
        <p>
          <span>GET</span> /items<br/>
          <span>GET</span> /health<br/>
          <span>GET</span> /items/1
        </p>
      </div>
    </div>

    <div class="footer">
      Built by <strong>Nivedha K</strong> &nbsp;·&nbsp;
      DevOps Assignment &nbsp;·&nbsp; Prophaze Technologies
    </div>

  </div>
</body>
</html>
"""


# ── GET all items ──────────────────────────────────────────────
@app.route("/items", methods=["GET"])
def get_all():
    return jsonify(items)


# ── GET one item ───────────────────────────────────────────────
@app.route("/items/<int:item_id>", methods=["GET"])
def get_one(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


# ── POST – create new item ─────────────────────────────────────
@app.route("/items", methods=["POST"])
def create():
    global next_id
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    items[next_id] = data
    created_id = next_id
    next_id += 1
    return jsonify({"id": created_id, "item": data}), 201


# ── PUT – update existing item ─────────────────────────────────
@app.route("/items/<int:item_id>", methods=["PUT"])
def update(item_id):
    if item_id not in items:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    items[item_id] = data
    return jsonify({"updated": items[item_id]})


# ── DELETE – remove item ───────────────────────────────────────
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete(item_id):
    if item_id not in items:
        return jsonify({"error": "Item not found"}), 404
    del items[item_id]
    return jsonify({"deleted": item_id})


# ── Health check (used by Kubernetes readiness probe) ──────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)