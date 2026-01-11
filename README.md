# thelook-cloudrun-analytics

## Overview

This project implements a **serverless analytics web service** using **Google Cloud Run** and **BigQuery** to query and explore insights from the **thelook e-commerce dataset**.

The application provides a simple, user-friendly web interface that allows users to trigger predefined analytical queries and view results dynamically in tabular form. The solution demonstrates cloud-native deployment, scalable querying, and lightweight UI design for business analytics use cases.

This repository was developed as part of **Task B5** of a cloud computing coursework assignment.

---

## Architecture

The solution follows a **serverless architecture**:

```
User Browser
     ↓
Cloud Run (Flask Application)
     ↓
BigQuery (thelook dataset)
```

- **Cloud Run** hosts a containerised Python web application  
- **BigQuery** stores and processes the dataset  
- **Flask** handles HTTP routing and request handling  
- **HTML & CSS** provide a lightweight, responsive interface  

---

## Features

- Web-based interface with interactive query buttons  
- Executes multiple BigQuery SQL queries on demand  
- Displays query results in clean, formatted tables  
- Serverless deployment with automatic scaling  
- Simple, business-friendly user interface  

---

## Implemented Queries

The application currently supports the following analytical queries:

1. **Order Status Distribution**  
   Displays the number of orders grouped by order status to provide insight into operational order processing.

2. **Average Order Value by Department**  
   Calculates the average item-level sales value across product departments, enabling pricing comparison.

3. **Top Categories by Revenue**  
   Identifies the highest revenue-generating product categories.

These queries are executed only when requested, ensuring efficient use of cloud resources.

---

## Technologies Used

- Python 3  
- Flask  
- Google Cloud Run  
- Google BigQuery  
- Docker  
- HTML & CSS  

---

## Deployment

The application is containerised using Docker and deployed to Google Cloud Run.

### Build the Container Image
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/b5-cloudrun-minal
```

### Deploy to Cloud Run
```bash
gcloud run deploy b5-cloudrun-minal \
  --image gcr.io/PROJECT_ID/b5-cloudrun-minal \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

After deployment, Cloud Run provides a public HTTPS endpoint to access the application.

---

## Project Structure

```
thelook-cloudrun-analytics/
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## Learning Outcomes

This project demonstrates:

- Deployment of serverless applications using Cloud Run  
- Querying large-scale datasets using BigQuery  
- Containerisation with Docker  
- Cloud-based analytics workflows  
- Separation of application logic, data access, and presentation  

---

## Author

**Minal Honali Raghunandan**  
Cloud Computing Coursework – Task B5
