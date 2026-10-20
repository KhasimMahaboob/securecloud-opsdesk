import os
import boto3
import pymysql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# --- RDS Database Configuration ---
DB_HOST = os.environ.get(
    'DB_HOST', 'cloud-devops-rds.c6fi4u2ecr4y.us-east-1.rds.amazonaws.com'
)
DB_USER = os.environ.get('DB_USER', 'cloudadmin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Khasim0710')
DB_NAME = os.environ.get('DB_NAME', 'cloudapp')

# --- S3 Configuration ---
S3_BUCKET = 'securecloud-opsdesk-attachments-2026'
s3 = boto3.client('s3', region_name='us-east-1')


def get_db_connection():
  return pymysql.connect(
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASSWORD,
      database=DB_NAME,
      cursorclass=pymysql.cursors.DictCursor,
  )


@app.route('/')
def index():
  connection = get_db_connection()
  incidents = []
  with connection.cursor() as cursor:
    # Auto-create table if it doesn't exist yet (includes attachment column)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                severity VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                attachment VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    connection.commit()

    cursor.execute(
        'SELECT * FROM incidents ORDER BY created_at DESC LIMIT 10'
    )
    incidents = cursor.fetchall()
  connection.close()
  return render_template('index.html', incidents=incidents)


@app.route('/add', methods=['POST'])
def add_incident():
  title = request.form['title']
  severity = request.form['severity']
  description = request.form['description']

  # Handle optional file upload to S3
  file = request.files.get('attachment')
  attachment_name = None

  if file and file.filename != '':
    attachment_name = file.filename
    # Upload file directly to S3 via EC2 IAM Role permissions
    s3.upload_fileobj(file, S3_BUCKET, attachment_name)

  connection = get_db_connection()
  with connection.cursor() as cursor:
    cursor.execute(
        'INSERT INTO incidents (title, severity, description, attachment) VALUES'
        ' (%s, %s, %s, %s)',
        (title, severity, description, attachment_name),
    )
    connection.commit()
  connection.close()
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
