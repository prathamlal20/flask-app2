from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db = mysql.connector.connect(
    host= '172.31.93.171',
    user= 'user',
    password= 'password',
    database= 'mysql_python'
)

# Route to fetch data from MySQL
@app.route('/', methods=['GET'])
def get_data():
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM sample_data')
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # HTML template string
        html = '''
        <html>
            <head>
                <title>MySQL Data</title>
                <style>
                    table {
                        width: 70%%;
                        border-collapse: collapse;
                        margin: 20px auto;
                        font-family: Arial, sans-serif;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }
                    th {
                        background-color: #f2f2f2;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <h2 style="text-align: center;">Data from MySQL Table</h2>
                <table>
                    <tr>
                        {% for col in columns %}
                            <th>{{ col }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in rows %}
                        <tr>
                            {% for item in row %}
                                <td>{{ item }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </table>
            </body>
        </html>
        '''

        return render_template_string(html, columns=column_names, rows=data)

    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
