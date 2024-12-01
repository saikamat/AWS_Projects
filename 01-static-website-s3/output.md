# How to Run a Static Website Hosted on S3 using AWS

![image](./images/01-Static-Website.png)

## 1.Register Domain on Route 53
![image](./images/Screenshot%202024-11-28%20at%2021.14.43.png)

### In Route 53 Dashboard, click on Registered Domains
![image](./images/Screenshot%202024-11-28%20at%2021.15.40.png)

### Add the Domain name you want and Click 'Register Domain' in left menu
![image](./images/Screenshot%202024-11-28%20at%2021.23.06.png)
Once  the domain is available, add to your cart and proceed to checkout.
Provide the required contact information and complete the registration process. Once domain registered, Route 53 will automatically create a `Hosted Zone` for your domain. This is where you manage the DNS Records.
---
## 2.Set up Amazon S3 Bucket to host the Static Website
Navigate to AWS Mangemnt Console and search for `S3` and open the service.
![image](./images/Screenshot%202024-11-28%20at%2021.33.02.png)

### Create an S3 Bucket
Enter a unique bucket name that matches your domain name. Here I've used `projects-saikamat.com`.
Choose the bucket closest to the target audience in terms of region.
![image](./images/Screenshot%202024-11-28%20at%2021.53.02.png)

### Configure the bucket
After creating the bucket, click on `Properties` tab to scroll to `Static Website Hosting`. Click on `Edit` to enable static website hosting. Specify the following:-
- `index.html` as the index document, or the main HTML file.
- `error.html` for custom error pages. This is an optional step.
![image](./images/Screenshot%202024-11-28%20at%2021.54.10.png)

### Create a sample `index.html` and `style.css` files on local machine
You can use the sample ones provided in the github source code.
![image](./images/Screenshot%202024-11-28%20at%2021.57.26.png)

### Head to S3 Bucket, and uplaod these files
![image](./images/Screenshot%202024-11-28%20at%2021.59.23.png)

![image](./images/Screenshot%202024-11-28%20at%2022.00.20.png)

## Configure S3 Bucket Policy
By default, the `Make Public by ACL` in the `Actions` tab is disabled by default, because `Block Public Access` settings are enabled for the Bucket.

AWS blocks public access to S3 buckets and objects for security purposes. To resolve this, you need to adjust the bucket's public access settings and permissions.
![image](./images/Screenshot%202024-11-28%20at%2022.03.00.png)



### Head to S3 Permissions
![image](./images/Screenshot%202024-11-28%20at%2022.05.14.png)

### Untick `Block all public access` and Save changes
![image](./images/Screenshot%202024-11-28%20at%2022.06.16.png)

### Scroll Down further to edit `Bucket Policy`
![image](./images/Screenshot%202024-11-28%20at%2022.07.34.png)

### Use the following Bucket Policy and Save changes
![image](./images/Screenshot%202024-11-28%20at%2022.09.09.png)

### Test Public Access
![image](./images/Screenshot%202024-11-28%20at%2022.11.44.png)
Go to `Objects` tab of S3 bucket, and select the `index.html` file. Tap on `Copy URL` and open it in the Browser Window.

### Verify whether you can access the S3 static Web page
![image](./images/Screenshot%202024-11-28%20at%2022.13.15.png)

---
## 3. Configure Cloudfront to Distribute Website Content
![image](./images/Screenshot%202024-11-28%20at%2022.14.17.png)
Click on `Create Distribution`

### Configure Cloudfront Origin Settings
![image](./images/Screenshot%202024-11-28%20at%2022.15.47.png)
Under `Origin Domain`, select the S3 bucket from the drop-down

![image](./images/Screenshot%202024-11-28%20at%2022.17.52.png)
Under `Origin Access Control`, enable OAC to restrict direct access to the S3 Bucket.

> NOTE: Though this is optional, OAC is recommended for higher security.

## OAC Settings
OAC is modern and recommended way to allow Cloudfront to access your S3 Bucket while ensuring the Bucket isn't publicly accessible.

In the OAC Creation Dialog, enter name for the OAC, and choose `Sign Requests` as the signing behaviour. THis ensures that Cloudfront signs off requests to your S3 Bucket.
![image](./images/Screenshot%202024-11-28%20at%2022.19.26.png)

## Update S3 Bucket Policy
Once OAC is created, you need to update the S3 policy of your bucket. This will allow access originating only from Cloudfront using the OAC and not public.
![image](./images/Screenshot%202024-11-28%20at%2022.21.28.png)

Head back to S3 Bucket, permissions and `Edit Policy`.

### Use the following Bucket Policy
S3-Bucket Policy for Cloudfront OAC:-
```json
{
    "Version": "2021-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontAccess",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            }
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3::::projects-saikamat.com/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT_ID:distribution/YOUR_DISTRIBUTION_ID"
                }
            }
        }
    ]
}
```

Cloudfront Distributions take 10 to 20 mintures to deploy changes.

## Configure Cloudfront Cache behaviour
- Under `Viewer Protocol Policy`, set to `Redirect HTTP to HTTPS`

- Allowed HTTP Methods, choose `GET`, `HEAD` for static websites.
![image](./images/Screenshot%202024-11-28%20at%2022.22.15.png)

## Update Route 53 DNS Records
Go back to `Route 53` and open the `Hosted Zones` and choose your domain. 

- Click on `Settings`, and add an `Alternate domain name (CNAME)` to your domain.

- Choose `Custom SSL Certificate`
![image](./images/Screenshot%202024-11-28%20at%2022.26.43.png)

## SSL Certificate
Request a Free Certificate from AWS Certificate Manager (ACM)
![image](./images/Screenshot%202024-11-28%20at%2022.27.49.png)


### Validation
ACM will ask you to validate that you own the domain. You can choose either of the two methods.

It is recommended to use `DNS Validation` , where ACM provides a DNS record that you add to your domain's DNS Settings in Route 53.
![image](./images/Screenshot%202024-11-28%20at%2022.30.49.png)

### DNS Validation
ACM will provide a CNAME record. Go to Route 53 and hosted zones
![image](./images/Screenshot%202024-11-28%20at%2022.32.24.png)

Choose your domain
![image](./images/Screenshot%202024-11-28%20at%2022.32.58.png)

Add a `CNAME` record provided by ACM to your domain's DNS Settings. The validation process takes from a few minutes to an hour.
![image](./images/Screenshot%202024-11-28%20at%2022.34.39.png)


### After creating CNAME records in ACM, you can simply create those records in route 53.
![image](./images/Screenshot%202024-11-28%20at%2022.45.34.png)

### Add SSL Certificate in Cloudfront
Go to AWS Conosle, and choose Cloudfront ad head to the distribution created before. Choose the Certificate created in ACM
![image](./images/Screenshot%202024-11-28%20at%2022.49.41.png)

## Update S3 Bucket Policy
Adding new custom SSL certificate, will update the S3 bucket policy. Update it accordingly.
![image](./images/Screenshot%202024-11-28%20at%2022.54.11.png)

##  Update Alias Record
Head back to Route 53, to the hosted zone. 

Create a new record, of type A-IPv4 Address

Enable Alias, select your created Cloudfront distribution and save the Record.
![image](./images/Screenshot%202024-11-29%20at%2011.10.00.png)

## Troubleshooting
I witnessed one tiny hiccup when lauching the website. When seemingly everything was said and done on the Cloudfront Distribution, I saw this error. 
![image](./images/Screenshot%202024-11-29%20at%2011.29.34.png)

Turns out, the "Access Denied" error you're seeing indicates that your CloudFront distribution is unable to access the content in your S3 bucket. This is a common issue when hosting a static website on AWS, and it usually happens because of one of the following reasons:

1. S3 Bucket Permissions: The S3 bucket is not configured to allow CloudFront to access its content.
2. Origin Access Control (OAC) or Origin Access Identity (OAI): If you're using OAC or OAI, the bucket policy might not be properly configured to allow CloudFront access.

---
## Key Takeaways

### 1. Domain Management with Amazon Route 53
Purpose: Route 53 is used to register and manage your domain (e.g., projects-saikamat.com).

Key Steps:
- Register a domain or transfer an existing one to Route 53.
- Create a hosted zone and configure DNS records (e.g., A or CNAME) to point to your CloudFront distribution.
> Takeaway: Route 53 ensures your domain resolves to the correct resources (CloudFront in this case).

### 2. Static Website Hosting with Amazon S3
Purpose: S3 is used to store and serve your static website files (HTML, CSS, JavaScript, images, etc.).

Key Steps:
- Create an S3 bucket with the same name as your domain (e.g., projects-saikamat.com).
- Enable static website hosting in the bucket settings.
Upload your website files to the bucket.
Configure bucket policies to allow access (either public or via CloudFront OAC).
> Takeaway: S3 provides a cost-effective and scalable solution for hosting static websites.

### 3. Content Delivery with Amazon CloudFront
Purpose: CloudFront acts as a Content Delivery Network (CDN) to distribute your website globally with low latency.

Key Steps:
- Create a CloudFront distribution with your S3 bucket as the origin.
- Configure the Default Root Object (e.g., index.html) to ensure proper routing.
- Use Origin Access Control (OAC) to securely access your S3 bucket.
Optionally enable caching, compression, and HTTPS for better performance and security.
> Takeaway: CloudFront improves website performance and security by caching content at edge locations worldwide.

<!--
## 37.
![image](./images/Screenshot%202024-11-29%20at%2012.18.49.png)


 ## 38.
![image](./images/Screenshot%202024-11-29%20at%2012.25.32.png)

## 39.
![image](./images/Screenshot%202024-11-29%20at%2012.27.45.png)

## 40.
![image](./images/Screenshot%202024-11-29%20at%2012.30.53.png)

## 41.
![image](./images/Screenshot%202024-11-29%20at%2012.35.02.png)

## 42.
![image](./images/Screenshot%202024-11-29%20at%2014.26.49.png)

## 43.
![image](./images/Screenshot%202024-11-29%20at%2014.35.53.png)

## 44.
![image](./images/Screenshot%202024-11-29%20at%2014.37.08.png)

## 45.
![image](./images/Screenshot%202024-11-29%20at%2014.38.29.png)

## 46.
![image](./images/Screenshot%202024-11-29%20at%2014.40.03.png)

## 47.
![image](./images/Screenshot%202024-11-29%20at%2014.41.17.png)

## 48.
![image](./images/Screenshot%202024-11-29%20at%2014.43.46.png)

## 49.
![image](./images/Screenshot%202024-11-29%20at%2014.51.36.png)

## 50.
![image](./images/Screenshot%202024-11-29%20at%2014.54.20.png) -->

