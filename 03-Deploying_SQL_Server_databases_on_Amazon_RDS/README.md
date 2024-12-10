# Deploying SQL Server databases on Amazon RDS
> Swich to `assets` branch for illustrated Readme.
## Table of Contents
- [Deploying SQL Server databases on Amazon RDS](#deploying-sql-server-databases-on-amazon-rds)
  - [Table of Contents](#table-of-contents)
  - [High Level Architecture](#high-level-architecture)
  - [Workflow](#workflow)
  - [Deploy VPC](#deploy-vpc)
    - [Create VPC](#create-vpc)
    - [Create Subnet](#create-subnet)
    - [Create Internet Gateway](#create-internet-gateway)
    - [Create Routing Table](#create-routing-table)
  - [Create Security Group](#create-security-group)
  - [Create RDS](#create-rds)
    - [Install Azure Data Studio](#install-azure-data-studio)
    - [Configure Connections](#configure-connections)
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

![image](./assets/03-arch-diag.png)

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
![image](./assets/Screenshot%202024-12-09%20at%2021.13.28.png)
### Create VPC
![image](./assets/Screenshot%202024-12-09%20at%2021.13.28.png)
### Create Subnet
![image](./assets/Screenshot%202024-12-09%20at%2021.14.30.png)
![image](./assets/Screenshot%202024-12-09%20at%2021.17.06.png)
![image](./assets/Screenshot%202024-12-09%20at%2021.19.25.png)
### Create Internet Gateway
![image](./assets/Screenshot%202024-12-09%20at%2021.22.47.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.24.44.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.25.31.png)
### Create Routing Table

![image](./assets/Screenshot%202024-12-09%20at%2021.26.49.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.27.59.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.29.25.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.31.36.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.32.06.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.32.50.png)
## Create Security Group
![image](./assets/Screenshot%202024-12-09%20at%2021.34.52.png)

![image](./assets/Screenshot%202024-12-09%20at%2021.40.59.png)
## Create RDS
![image](./assets/Screenshot%202024-12-09%20at%2022.21.43.png)

### Install Azure Data Studio
Since I use Mac, SSML isn't natively available to me.
Therefore I use Azure Data Studio available from [here](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?tabs=macOS-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall#download-azure-data-studio)
![image](./assets/Screenshot%202024-12-09%20at%2022.02.01.png)
### Configure Connections
![image](./assets/Screenshot%202024-12-09%20at%2022.22.09.png)
![image](./assets/Screenshot%202024-12-09%20at%2022.23.28.png)

### Play with database
![image](./assets/Screenshot%202024-12-10%20at%2010.12.03.png)
![image](./assets/Screenshot%202024-12-10%20at%2010.27.01.png)
#### Run SQL queries to interact with your database.
![image](./assets/Screenshot%202024-12-10%20at%2010.27.11.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.28.13.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.28.37.png)
#### Create tables, insert data, and manage your database schema.
![image](./assets/Screenshot%202024-12-10%20at%2010.29.27.png)
![image](./assets/Screenshot%202024-12-10%20at%2010.36.24.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.37.00.png)
![image](./assets/Screenshot%202024-12-10%20at%2011.03.59.png)
#### Monitor and optimize database performance using tools like Performance Insights in the RDS Dashboard.
![image](./assets/Screenshot%202024-12-10%20at%2010.43.54.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.45.32.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.46.01.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.46.40.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.51.00.png)

![image](./assets/Screenshot%202024-12-10%20at%2010.51.24.png)

## Appendix
![image](./assets/Screenshot%202024-12-10%20at%2011.15.44.png)
### Troubleshooting
Often, stopping and restarting the RDS Instance helps most connection issues.
Enable Public Access while creating RDS Instance.
| Error | Error Type | Cause | Resolution |
|---|---|---|---|
||||