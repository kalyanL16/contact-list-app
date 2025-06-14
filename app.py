from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

def get_data_from_db():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="NewStrongPassword123!",
        database="sample"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name, phone, email, website, address FROM json_import LIMIT 500")
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

@app.route('/')
def home():
    data = get_data_from_db()
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Contact List</title>
      <style>
        body {
          font-family: Verdana, sans-serif;
          background-color: #f0f4f8;
          margin: 40px;
        }
        h1 {
          text-align: center;
          color: #2c3e50;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          background-color: white;
          box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        th, td {
          padding: 12px 15px;
          border: 1px solid #ddd;
          text-align: left;
          vertical-align: top;
        }
        th {
          background-color: #2980b9;
          color: white;
        }
        tr:nth-child(even) {
          background-color: #ecf0f1;
        }
        a {
          color: #2980b9;
          text-decoration: none;
        }
        a:hover {
          text-decoration: underline;
        }
      </style>
    </head>
    <body>
      <h1>Contact List</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Website</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          {% for row in data %}
          <tr>
            <td>{{ row.name }}</td>
            <td>{{ row.phone }}</td>
            <td><a href="mailto:{{ row.email }}">{{ row.email }}</a></td>
            <td><a href="{{ row.website }}" target="_blank">{{ row.website }}</a></td>
            <td>{{ row.address | replace('\n', '<br>') | safe }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

if __name__ == '__main__':
    app.run(debug=True)
