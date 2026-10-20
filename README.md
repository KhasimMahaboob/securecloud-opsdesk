cat << 'EOF' > README.md
# 🛡️ SecureCloud OpsDesk — Cloud Incident Management Platform

SecureCloud OpsDesk is a production-ready incident management web application built with Python Flask and hosted on Amazon Web Services (AWS). It provides a secure, decoupled cloud architecture for logging system incidents, uploading log files, and monitoring compute metrics in real-time.

---

## 🏗️ Architecture Overview

The application integrates key AWS core services:

* **Amazon EC2:** Runs the Flask web application and handles user HTTP requests.
* **AWS IAM:** Uses keyless, role-based access control (`SecureCloudEC2S3Role`) attached to the EC2 instance to safely interact with S3 without hardcoding API keys.
* **Amazon S3:** Dedicated object storage bucket (`securecloud-opsdesk-attachments-2026`) that stores uploaded log files and diagnostic attachments via `boto3`.
* **Amazon RDS (MySQL):** Managed relational database tier (`cloud-devops-rds`) that persists incident metadata, timestamps, severity levels, and attachment references via `pymysql`.
* **Amazon CloudWatch:** Provides real-time server observability and operational metrics tracking (such as EC2 `CPUUtilization`).

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, `boto3` (AWS SDK), `pymysql`
* **Frontend:** HTML5, CSS3, Responsive Dashboard UI
* **Cloud Infrastructure:** AWS (EC2, IAM, S3, RDS MySQL, CloudWatch)

---

## 🔑 Key Features

1. **Role-Based AWS Security:** Zero credentials stored in source code. S3 uploads rely strictly on dynamic IAM instance profile permissions.
2. **Decoupled Architecture:** Structured data persists in Amazon RDS while unstructured attachment files stream to Amazon S3.
3. **Database Schema Management:** Applied SQL table alterations to support file attachment references smoothly.
4. **Cloud Performance Monitoring:** Live metrics tracking via Amazon CloudWatch to monitor web server health.
EOF

# 2. Stage, commit, and push the README
git add README.md
git commit -m "Add professional project README.md"
git push origin main
