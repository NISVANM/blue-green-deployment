
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="Blue-Green Deployment Project")

VERSION = os.getenv("APP_VERSION", "Blue Version 1.0")
COLOR = os.getenv("APP_COLOR", "blue")

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blue-Green Deployment</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                text-align: center;
                padding: 60px 20px;
            }}
            .container {{
                background: white;
                max-width: 650px;
                margin: auto;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 5px 20px #cbd5e1;
            }}
            .status {{
                display: inline-block;
                background: {COLOR};
                color: white;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 22px;
                margin: 20px;
            }}
            h1 {{ color: #172554; }}
            p {{ color: #475569; font-size: 17px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Blue-Green Deployment System</h1>
            <p>Automated deployment using Jenkins, Docker and Kubernetes</p>
            <div class="status">{COLOR.upper()} ENVIRONMENT</div>
            <h2>{VERSION}</h2>
            <p>Application is running successfully!</p>
            <p>Deployment strategy: Blue-Green</p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": VERSION,
        "environment": COLOR
    }
