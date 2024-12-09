# application.py  
from flask import Flask
import os

app = Flask(__name__)  

# access environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
flask_env = os.getenv("FLASK_ENV", "development") # default to 'development' if not set

@app.route('/')  
def home():  
    return f"DB_USER: {db_user}, Flask Environment: {flask_env}" 

# Gunicorn looks for 'application' by default  
application = app  


if __name__ == "__main__":  
    # app.run(debug=True)  
    app.run(host='0.0.0.0', port=8080) 