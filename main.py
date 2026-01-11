from flask import Flask, render_template_string
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

QUERIES = {
    "order_status": {
        "title": "Order Status Distribution",
        "subtitle": "Operational health of order processing",
        "color": "#fde2e4",
        "sql": """
            SELECT status, COUNT(order_id) AS order_count
            FROM `cloudcourseworkb-481017.thelook.orders`
            GROUP BY status
            ORDER BY order_count DESC
        """
    },
    "avg_order_value": {
        "title": "Average Order Value by Department",
        "subtitle": "Pricing strength across departments",
        "color": "#e8f8f0",
        "sql": """
            SELECT
              p.department,
              ROUND(AVG(oi.sale_price), 2) AS avg_order_value
            FROM `cloudcourseworkb-481017.thelook.order_items` oi
            JOIN `cloudcourseworkb-481017.thelook.products` p
            ON oi.product_id = p.id
            GROUP BY p.department
            ORDER BY avg_order_value DESC
        """
    },
    "top_categories": {
        "title": "Top Categories by Revenue",
        "subtitle": "Product portfolio performance",
        "color": "#efe9ff",
        "sql": """
            SELECT
              p.category,
              ROUND(SUM(oi.sale_price), 2) AS total_revenue
            FROM `cloudcourseworkb-481017.thelook.order_items` oi
            JOIN `cloudcourseworkb-481017.thelook.products` p
            ON oi.product_id = p.id
            GROUP BY p.category
            ORDER BY total_revenue DESC
            LIMIT 10
        """
    }
}

@app.route("/")
def home():
    return render_template_string(HOME_HTML, queries=QUERIES)

@app.route("/query/<key>")
def run_query(key):
    q = QUERIES[key]
    results = list(client.query(q["sql"]).result())

    headers = results[0].keys() if results else []
    rows = [list(r.values()) for r in results]

    return render_template_string(
        RESULT_HTML,
        title=q["title"],
        subtitle=q["subtitle"],
        headers=headers,
        rows=rows
    )

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
  margin: 0;
  font-family: "Segoe UI Variable","Segoe UI",Inter,Arial,sans-serif;
  background: #f4f7fb;
}
.container {
  max-width: 1100px;
  margin: auto;
  padding: 60px 30px;
}
h1 {
  text-align: center;
  font-size: 42px;
}
.subtitle {
  text-align: center;
  color: #555;
  margin-bottom: 50px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 25px;
}
.card {
  padding: 28px;
  border-radius: 18px;
  box-shadow: 0 14px 30px rgba(0,0,0,0.15);
  transition: transform .2s ease, box-shadow .2s ease;
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 38px rgba(0,0,0,0.25);
}
.card h3 {
  margin: 0 0 8px 0;
}
.card p {
  font-size: 14px;
  opacity: .8;
}
.card a {
  display: inline-block;
  margin-top: 16px;
  padding: 10px 20px;
  background: white;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  color: #333;
}
</style>
</head>
<body>
<div class="container">
  <h1>Business Analytics Dashboard</h1>
  <div class="subtitle">Executive insights powered by Cloud Run & BigQuery</div>

  <div class="grid">
    {% for key, q in queries.items() %}
      <div class="card" style="background: {{ q.color }};">
        <h3>{{ q.title }}</h3>
        <p>{{ q.subtitle }}</p>
        <a href="/query/{{ key }}">View Analysis →</a>
      </div>
    {% endfor %}
  </div>
</div>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
  font-family: "Segoe UI Variable","Segoe UI",Inter,Arial,sans-serif;
  background: #f4f7fb;
}
.container {
  max-width: 1000px;
  margin: auto;
  padding: 40px;
}
h1 {
  margin-bottom: 5px;
}
.subtitle {
  color: #555;
  margin-bottom: 25px;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}
th, td {
  padding: 14px 16px;
  border-bottom: 1px solid #eee;
}
th {
  background: #eef3ff;
  text-align: left;
}
a {
  display: inline-block;
  margin-top: 25px;
  text-decoration: none;
  font-weight: 600;
}
</style>
</head>
<body>
<div class="container">
  <h1>{{ title }}</h1>
  <div class="subtitle">{{ subtitle }}</div>

  <table>
    <tr>
      {% for h in headers %}<th>{{ h }}</th>{% endfor %}
    </tr>
    {% for r in rows %}
    <tr>
      {% for c in r %}<td>{{ c }}</td>{% endfor %}
    </tr>
    {% endfor %}
  </table>

  <a href="/">← Back to Dashboard</a>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
