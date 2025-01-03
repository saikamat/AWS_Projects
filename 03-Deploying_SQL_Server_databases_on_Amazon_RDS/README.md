# Deploying SQL Server databases on Amazon RDS
> Swich to `assets` branch for illustrated Readme.
## Table of Contents
- [Deploying SQL Server databases on Amazon RDS](#deploying-sql-server-databases-on-amazon-rds)
  - [Table of Contents](#table-of-contents)
  - [High Level Architecture](#high-level-architecture)
  - [Workflow](#workflow)
  - [Deploy VPC](#deploy-vpc)
    - [Create VPC](#create-vpc)
<<<<<<< HEAD
    - [Create Internet Gateway](#create-internet-gateway)
    - [Create Routing Table](#create-routing-table)
  - [Create Security Group](#create-security-group)
    - [Create Inbound Rule](#create-inbound-rule)
    - [Create Outbound Rule](#create-outbound-rule)
  - [Create RDS](#create-rds)
  - [Connect to RDS Database](#connect-to-rds-database)
    - [Install Azure Data Studio](#install-azure-data-studio)
    - [Configure Connections](#configure-connections)
    - [Establish Connection](#establish-connection)
=======
    - [Create Subnet](#create-subnet)
    - [Create Internet Gateway](#create-internet-gateway)
    - [Create Routing Table](#create-routing-table)
    - [Enable DNS Hostnames (Optional)](#enable-dns-hostnames-optional)
  - [Create Security Group](#create-security-group)
    - [Inbound and Outbound Rules](#inbound-and-outbound-rules)
  - [Create RDS](#create-rds)
    - [Install Azure Data Studio](#install-azure-data-studio)
    - [Configure Connections](#configure-connections)
>>>>>>> assets
    - [Play with database](#play-with-database)
      - [Run SQL queries to interact with your database.](#run-sql-queries-to-interact-with-your-database)
      - [Create tables, insert data, and manage your database schema.](#create-tables-insert-data-and-manage-your-database-schema)
      - [Monitor and optimize database performance using tools like Performance Insights in the RDS Dashboard.](#monitor-and-optimize-database-performance-using-tools-like-performance-insights-in-the-rds-dashboard)
  - [Appendix](#appendix)
    - [Troubleshooting](#troubleshooting)

## High Level Architecture
Here, I've created a DB instance and understood important concepts relating to backups, security, scaling, optimizing, and monitoring my DB instance.

I need the following to deploy a SQL Server on RDS.
|Service|Role|
|---|---|
|Amazon RDS|managed DB service to simplify setup, operation, scaling of SQL server databases|
|VPC|secure network environment for DB|
|Security Groups|Virtual firewalls to control in & outbound traffic|
|Cloudwatch|Monitor and track RDS instance's health|
|Client Application|Used by end-user to connect to SQL Server database and send queries|

<<<<<<< HEAD
![image](./images/)
=======
![image](./assets/03-arch-diag.png)
>>>>>>> assets

## Workflow
```mermaid
graph LR

A(User sends request)

A --> B(Request routed through VPC)
B --> C{Authorized by SG?}
C -->|No| E(Blocked)
C -->|Yes| D(RDS Instance)
D -->|Process Request|F(Microsoft SQL Server)
F --> B
B --> A
```
## Deploy VPC
<<<<<<< HEAD
### Create VPC
### Create Internet Gateway
### Create Routing Table
## Create Security Group
### Create Inbound Rule
### Create Outbound Rule
## Create RDS
## Connect to RDS Database
### Install Azure Data Studio
Since I use Mac, SSML isn't natively available to me.
Therefore I use Azure Data Studio available from [here](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?tabs=macOS-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall#download-azure-data-studio)

### Configure Connections
### Establish Connection
### Play with database
#### Run SQL queries to interact with your database.
#### Create tables, insert data, and manage your database schema.
#### Monitor and optimize database performance using tools like Performance Insights in the RDS Dashboard.
## Appendix
### Troubleshooting
Often, stopping and restarting the RDS Instance helps most connection issues.
Enable Public Access while creating RDS Instance.
| Error | Error Type | Cause | Resolution |
|---|---|---|---|
||||
=======
I started with deploying a virtual private cloud which will host the setup.
### Create VPC
![image](./assets/Screenshot%202024-12-09%20at%2021.13.28.png)
Go to [AWS Console](https://console.aws.amazon.com/console/home), and look for `VPC`
Set configurations as illustrated in above picture.
### Create Subnet
![image](./assets/Screenshot%202024-12-09%20at%2021.14.30.png)

Head to VPC Dashboard and choose `Subnets` and `Create Subnet`
![image](./assets/Screenshot%202024-12-09%20at%2021.17.06.png)

Choose the VPC you created before. We create two subnets operating in two regions -> `10.0.1.0/24` having 256 IP addresses in one availability zone, 
![image](./assets/Screenshot%202024-12-09%20at%2021.19.25.png)
and `10.0.2.0/24` with another set of 256 IP Addresses in a different availability zone.
### Create Internet Gateway
When your RDS instances from inside the VPC wish to communicate with the Internet, you can use the `Internet Gateway`. 
![image](./assets/Screenshot%202024-12-09%20at%2021.22.47.png)
Head to VPC Dashboard, and choose `Internet gateways` and create one.
![image](./assets/Screenshot%202024-12-09%20at%2021.24.44.png)
Name it
![image](./assets/Screenshot%202024-12-09%20at%2021.25.31.png)
and attach it to the VPC you created before.
### Create Routing Table
The Route Table determines how traffic is routed to your VPC. This is crucial especially if your route your traffic to the internet. 
![image](./assets/Screenshot%202024-12-09%20at%2021.26.49.png)
In the VPC dashboard, head to `Route Tables` on the left, and select the route table associated with the VPC you created above.
![image](./assets/Screenshot%202024-12-09%20at%2021.27.59.png)
Edit the routes, 
![image](./assets/Screenshot%202024-12-09%20at%2021.29.25.png)
and choose the destination as `0.0.0.0/0` and target as the internet gateway that you already created before. This means all IPv4 traffic will be routed to the gateway.
![image](./assets/Screenshot%202024-12-09%20at%2021.31.36.png)
### Enable DNS Hostnames (Optional)
![image](./assets/Screenshot%202024-12-09%20at%2021.32.06.png)
If you want to use DNS hostnames to access resources inside your VPC, you enable this feature by heading to your VPC and editing the settings
![image](./assets/Screenshot%202024-12-09%20at%2021.32.50.png)
and mark `Enable DNS hostnames` and `resolution` as shown above.
## Create Security Group
Configuring Security Groups (SG) is crucial since it acts as a firewall that controls in and outbound traffic to your RDS instance.
![image](./assets/Screenshot%202024-12-09%20at%2021.34.52.png)
Head to EC2 in your AWS console, and choose `Security Groups` in the left tab. Choose `Create Security Group`.

### Inbound and Outbound Rules
Inbound Rules dictate what traffic is allowed to connect to your database, while Outbound Rules dictate what traffic, the database is allowed to send out. 

The inbound traffic could be SQL queries while outbound could be response to those queries.
![image](./assets/Screenshot%202024-12-09%20at%2021.40.59.png)
For inbound rules, select `MSSQL` as the type. Set the source to `My IP`  if you're connecting to the databasse from your local machine. AWS automatically detects and adds your current IP address.

However if you're connecting from an application server, enter the private IP or the CIDR block of the server (e.g. `10.0.2.0./24`)

For the outbound, set it to `0.0.0.0/0` so that RDS instance can send traffic to any destination.
## Create RDS
Navigate to AWS Console and type in `RDS` and create RDS database.
|Setting Key|Value|
|---|---|
|Database Creation|Standard Creation|
|Engine Option|Microsoft SQL Server|
|Edition|SQL Server Express*|
|Deployment|Multi A-Z|
|DB Instance Class|db.t3.micro|
|Storage Type|gp2|
|Allocated Storage|Default 20GB|
|DB Instance Identifer|My-RDS-SQL-Server|
|Master username|`admin`|
|Master password|configure strong username|
|VPC|select the RDS you created before|
|Subnet Group|select the subnet group you created before|
|Public Access|Enable|

*Free tier, suitable for small workloads
![image](./assets/Screenshot%202024-12-09%20at%2022.21.43.png)

### Install Azure Data Studio
Since I use Mac, SSML isn't natively available to me.
Therefore I use Azure Data Studio available from [here](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?tabs=macOS-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall#download-azure-data-studio)
![image](./assets/Screenshot%202024-12-09%20at%2022.02.01.png)
Click on `Create a connection`.
### Configure Connections
![image](./assets/Screenshot%202024-12-09%20at%2022.22.09.png)
Once the RDS is ready, copy the endpoint from `Connectivity and Security` tab,
![image](./assets/Screenshot%202024-12-09%20at%2022.23.28.png)
to the Connections Config of Azure Data Studio.
In the `Advanced` tab, add port no as `1433`.
### Play with database
![image](./assets/Screenshot%202024-12-10%20at%2010.12.03.png)
Once connected, you'll see above visuals.
![image](./assets/Screenshot%202024-12-10%20at%2010.27.01.png)
And on the left tab, you'll see list of databases.
#### Run SQL queries to interact with your database.
![image](./assets/Screenshot%202024-12-10%20at%2010.27.11.png)
To create a New Query to your database, tap `File`>>`New Query`
![image](./assets/Screenshot%202024-12-10%20at%2010.28.13.png)
In the query tab, try an SQL query
```sql
SELECT @@VERSION;
```
![image](./assets/Screenshot%202024-12-10%20at%2010.28.37.png)
You should see results as above. As expected, you can see the Microsoft SQL Server created in previous steps.
#### Create tables, insert data, and manage your database schema.
You can continue exploring RDS, by creating a new database.
![image](./assets/Screenshot%202024-12-10%20at%2010.29.27.png)
Create new employees information.
```sql
INSERT INTO Employees (EmployeeID, FirstName, LastName, HireDate)  
VALUES (1, 'John', 'Doe', '2024-01-01');  
```
![image](./assets/Screenshot%202024-12-10%20at%2010.36.24.png)
```sql
UPDATE Employees  
SET LastName = 'Smith'  
WHERE EmployeeID = 1;  
```
Update Employee information.
![image](./assets/Screenshot%202024-12-10%20at%2010.37.00.png)

![image](./assets/Screenshot%202024-12-10%20at%2011.03.59.png)
You can preview the created database in the left tab.
#### Monitor and optimize database performance using tools like Performance Insights in the RDS Dashboard.
You can monitor and optimise performance of your SQL server database. With performance insights, you can see real-time and historical performance metrics of your database.
![image](./assets/Screenshot%202024-12-10%20at%2010.43.54.png)
Head to RDS Dashboard and tap on `Performance insights`
![image](./assets/Screenshot%202024-12-10%20at%2010.45.32.png)
View metrics such as database load.
![image](./assets/Screenshot%202024-12-10%20at%2010.46.01.png)
Top SQL queries show the most resource intensive queries.
![image](./assets/Screenshot%202024-12-10%20at%2010.46.40.png)
Wait events highlight bottlenecks in query execution.
- RESOURCE_SEMAPHORE wait type occurs when SQL Server queries are waiting for memory grants to execute. Indicates memory pressure. At 0.15 seconds, it is not critical but worth monitoring.
- PAGEIOLATCH_SH wait type occurs when SQL Server is waiting to read data pages from disk into memory. 
- The CPU wait type indicates the time spent by SQL Server executing queries on the CPU.

![image](./assets/Screenshot%202024-12-10%20at%2010.51.00.png)
CloudWatch provides detailed metrics for your RDS instance, such as CPU utilization, memory usage, disk I/O, and network traffic. 
![image](./assets/Screenshot%202024-12-10%20at%2010.51.24.png)
Head to AWS Dashboard, look for Cloudwatch. Click on Service, `RDS`.


![image](./assets/chrome-capture-2024-12-10.gif)
- CPU Utilization: Indicates how much processing power your database is using.
- Free Storage Space: Ensures your database has enough storage to operate efficiently.
- Read/Write Latency: Measures the time it takes to read/write data to the database.
## Appendix
![image](./assets/Screenshot%202024-12-10%20at%2011.15.44.png)
`NT AUTHORITY\SYSTEM` is a built-in Windows system account that SQL Server uses for certain internal tasks and maintenance operations. It is a highly privileged account that is part of the Windows operating system and is often used by services running on Windows-based systems, including SQL Server.

### Troubleshooting
Often, stopping and restarting the RDS Instance helps most connection issues.

| Error Log | Cause | Resolution |
|---|---|---|
|The server was not found or was not accessible. Verify that the instance name is correct and that SQL Server is configured to allow remote connections. (provider: TCP Provider, error: 35 - An internal exception was caught)|Azure Data Studio client is unable to establish a connection to your Amazon RDS SQL Server instance. This is a common issue and can be caused by several factors, such as network configuration, security group rules, or incorrect connection details.|Enable Public Access while creating RDS Instance.|
>>>>>>> assets
