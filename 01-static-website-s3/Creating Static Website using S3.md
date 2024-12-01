# Creating Static Website using S3

<!-- ## 1. Route 53
Select Route 53 in IAM Search
![image](./images/Screenshot%202024-11-28%20at%2021.03.39.png) -->
![images](./images/01-Static-Website.png)

## 1. Domain Management with Amazon Route 53
Purpose: Route 53 is used to register and manage your domain (e.g., projects-saikamat.com).

Key Steps:
- Register a domain or transfer an existing one to Route 53.
- Create a hosted zone and configure DNS records (e.g., A or CNAME) to point to your CloudFront distribution.
> Takeaway: Route 53 ensures your domain resolves to the correct resources (CloudFront in this case).

## 2. Static Website Hosting with Amazon S3
Purpose: S3 is used to store and serve your static website files (HTML, CSS, JavaScript, images, etc.).

Key Steps:
- Create an S3 bucket with the same name as your domain (e.g., projects-saikamat.com).
- Enable static website hosting in the bucket settings.
- Upload your website files to the bucket.
- Configure bucket policies to allow access (either public or via CloudFront OAC).
> Takeaway: S3 provides a cost-effective and scalable solution for hosting static websites.

## 3. Content Delivery with Amazon CloudFront
Purpose: CloudFront acts as a Content Delivery Network (CDN) to distribute your website globally with low latency.

Key Steps:
- Create a CloudFront distribution with your S3 bucket as the origin.
- Configure the Default Root Object (e.g., index.html) to ensure proper routing.
- Use Origin Access Control (OAC) to securely access your S3 bucket.
- Optionally enable caching, compression, and HTTPS for better performance and security.
> Takeaway: CloudFront improves website performance and security by caching content at edge locations worldwide.

