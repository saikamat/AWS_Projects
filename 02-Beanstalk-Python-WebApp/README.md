# RUNNING A WEB APP USING AWS BEANSTALK
## Introduction
Elastic Beanstalk is a Platform-as-a-Service (PaaS) that abstracts infrastructure management. It automatically provisions and manages resources like EC2 instances, load balancers, and auto-scaling groups.

Here's how it converses with various components

TODO-IMAGE


### Components
| Component Name | Purpose |
|---|---|
|Elastic Beanstalk|Hosts and manages your Python web application.  It automatically provisions and manages resources like EC2 instances, load balancers, and auto-scaling groups.|
|Application Code|Web application (e.g., built with Flask or Django) is the core of your deployment|
|EC2 Instances| virtual servers execute your Python application|
|Load Balancer|Ensures your application can handle traffic spikes and provides redundancy|
|Auto-Scaling Group|Ensures your application scales up during high demand and scales down during low demand|
|Environment Variables|rovide dynamic configuration to your application without hardcoding sensitive information|

### Workflow
1. User Requests: Users send HTTP requests to your application via a domain name or IP address.
2. Load Balancer: The load balancer receives the requests and forwards them to one of the EC2 instances running your application.
3. EC2 Instances: The EC2 instances process the requests using your Python application and return responses to the load balancer.
4. Environment Variables: The application running on EC2 instances uses environment variables for configuration (e.g., database connection strings).


## I. Python Web Application
1. Create Python Web App - `applications.py`
2. Run it as simple Flask application and see if accessible on `127.0.0.1:5000`

![image](Screenshot%202024-12-08%20at%2017.44.36.png)

## II. AWS Configuration using CLI
1. `aws configure`
2. AWS Console >> Login with IAM Credentials >> Account >> Security Credentials >> Create Access Key >> For CLI
3. Copy Access Key ID and Access Secret Key ID from console and enter in configure
4. Choose `us-east-1` region
5. Test whether it's working with this command
```bash
aws s3 ls  
```

## III. AWS Beanstalk Configuration
Elastic Beanstalk is a PaaS which auto-creates EC2, database, load balancer, auto scaling group
   1. `eb init`
   2. By default, AWS Elastic Beanstalk creates an Auto Scaling Launch Configuration, which has been deprecated for new AWS accounts created after June 1, 2023, and fully phased out as of October 1, 2024. Instead, AWS now requires the use of Launch Templates for Auto Scaling groups. To resolve this issue, you need to configure your Elastic Beanstalk environment to use Launch Templates instead of the deprecated Launch Configurations.
   3. Create a `.ebextensions` Directory:
      1. In your project directory, create a folder named `.ebextensions`.
      2. Add a Configuration File, inside the `.ebextensions` folder, named `autoscaling.config` with the following content:
      ```yaml
          option_settings:  
              aws:autoscaling:launchconfiguration:  
                  DisableIMDSv1: true  
                  RootVolumeType: gp3  
      ```
        This configuration ensures that Elastic Beanstalk uses a Launch Template instead of a Launch Configuration.
    
## IV. Launching the App
1. Create the Beanstalk
```
   eb create <<name of web app>>
```
    
Wait till you see that Elastic Beanstalk create and launch succesfully
```bash
2024-12-08 12:41:15    INFO    Successfully launched environment: 02-Beanstalk-Python-WebApp-2
```
2. Check status
```bash
eb status
```
Use the `CNAME` from the status and add it to the browser.

![image](Screenshot%202024-12-08%20at%2023.23.36.png)

## V. Make changes to your application
1. Open `applications.py`
2. Make small edits in the return method, e.g. 
```python3
...
...
@app.route('/')  
def home():  
    return "Hello AWS Beanstalk, change 2!!!"
...
...
```
3. Deploy the existing environment and wait for setting to take hold
```bash
eb deploy
```
4. Verify on browser

## VI. Edit Environment Configurations
Configuring environment variables in AWS Elastic Beanstalk is an important step, especially if your application relies on sensitive information (e.g., API keys, database credentials, or configuration settings) or needs specific runtime configurations. 

Environment variables are key-value pairs that are passed to your application at runtime. They are commonly used to:
- Store sensitive information securely (e.g., API keys, database credentials).
- Configure application behavior (e.g., DEBUG mode, FLASK_ENV).
- Avoid hardcoding values in your application code.

### 1. Configure Environment Variables in Elastic Beanstalk using AWS Console
1. Open the Elastic Beanstalk Console and Select your application and environment.
![image](Screenshot%202024-12-09%20at%2010.43.28.png)
2. In the left-hand menu, click on Configuration.
3. Scroll all the way down till you see `Environment Variables`. This is where you add your own variables

![image](Screenshot%202024-12-09%20at%2012.24.45.png)

4. Save Changes
![image](Screenshot%202024-12-09%20at%2012.26.42.png)
### 2. Access Environment Variables in Your Application
1. Once the environment variables are configured, your application can access them using the `os` module in Python. 

Things to watch out for:-
- Never hardcode sensitive information like database credentials or API keys in your codebase. Use environment variables instead.
- Provide default values in your code to handle cases where an environment variable is not set.

Here’s an example of how to use environment variables in a Flask application:

```python3
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
```
2. Deploy the existing environment and wait for setting to take hold
```bash
eb deploy
```
3. Verify on browser
   
![image](Screenshot%202024-12-09%20at%2012.32.18.png)

## Troubleshooting
If you can't access the elastic beanstalk URL, here are the steps to diagnose the error.
1. Check status
    ```bash
    eb status
    ```
2. Check logs
   ```bash
   eb logs
   ```

|Error| Error Type | Cause | Resolution |
|---|---|---|---|
|502 Bad Gateway|Failed to find attribute 'application' in 'application'|**Gunicorn**, the application server Elastic Beanstalk uses to run your Python app, is unable to find the WSGI application object it needs to serve your app.|Ensure your application contains a WSGI application object named `application` (see code below)|
```python3
# Application code 
# ...
# ...
@app.route('/')  
def home():  
    return "Hello, AWS Elastic Beanstalk!"  

# Gunicorn looks for 'application' by default  
application = app  <---- RESOLUTION STEP

# Application code 
# ...
# ...
```

|Error| Error Type | Cause | Resolution |
|---|---|---|---|
|502 Bad Gateway|Connection refused) while connecting to upstream|By default, **Gunicorn** listens on port `8000`. However the **Gunicorn** used by Elastic Beanstalk expects the application to listen on port `8080`|Modify your application code to ensure it binds to port `8080`|
```python3
if __name__ == "__main__":  
    application.run(host='0.0.0.0', port=8080)  
```
---
## Saving Costs
AWS Elastic Beanstalk costs more because the EC2 instances it props up are charged by the hour. 

Therefore the easiest way to avoid downtime costs is to terminate the beanstalk environment and create a new one.

1. Create a backup config of existing Beanstalk environmnent
```bash
eb config save
```
2. Terminate the Environment
```bash
eb terminate
```
3. When you want to re-create the same environmnent again
```bash
eb create
```