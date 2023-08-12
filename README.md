# Serverless Dad Joke Website Hosted on AWS

![alt text](https://github.com/theitguycj/dad-jokes/blob/main/Serverless%20Dad%20Jokes(2).png)

## Overview
Here’s an overview of my completed AWS project. This is a randomized joke website that allows a joke to be generated and shown on the button press. A user will be able to insert their email address before pressing “Tell Me A Joke” to get the next joke and the previous 5 jokes that were generated sent to their email. This blog post is a bit involved so most steps will be straight to the point to keep it from being too long. You’ll need an AWS account to use the following technologies: Route 53, CloudFront, S3, Lambda, and DynamoDB. You’ll need an API Ninjas account for random joke generation. You’ll also need an email account for sending jokes to users.

## Step 0: Prereqs
**API**: Create a free [API Ninjas](https://api-ninjas.com/) account. It gives you 50,000 API calls per month (plenty for this project environment). You’ll need to pick the API that you’ll want to use. For this project, it’ll be dad jokes.

**Email address**: I recommend that you create a project/test email account to send the jokes to users. You can use Amazon SES (not recommended for reasons I will state later), a custom email account you’ve already set up, or a Gmail/Outlook.com account.

**AWS account**: Sign up for an AWS account. Almost everything I’m using works within the Free Tier (except Route 53). If you already have an AWS account and no longer have access to the “free tier for a year” of services, this project shouldn’t cost more than a few dollars a month to run 24/7.

**Code Editor/IDE**: Install Visual Studio Code. We’ll use it for HTML, CSS, JavaScript, and Python scripting. You can optionally use Cloud9 on AWS for a development environment.

## Step 1: HTML, CSS, & JavaScript
Here’s the source files to this project to clone or download: https://github.com/theitguycj/dad-jokes. You’ll need the “index.html”, “index.js”, and “style.css” files. You can keep these files as is but I suggest that you make changes to these files. It’s a great way to learn the programming languages and comfortably speak to the challenges of putting your project together. I go over the files in more detail in the video but I’ll note a few things here:
- The “index.html” file is the base webpage that users see and it links to the other 2 files for processing and styling.
- In the “index.js” file, you need to replace the API URL and API Key with the ones that you get from API-Ninjas. You’ll also need to input the Lambda Function URL. You create that upfront or wait until we get that point then go back and edit the file.
- When passing the user’s email address and jokes to Lambda for data processing, I have “$$$” in the place of a single space because spaces can’t be used in a URL. We will use Lambda to convert it back.
- I kept a bunch of the console log lines that helped with my debugging. Hopefully it helps with yours.

## Step 2: Hosting, CDN, and Domain Name
Route 53 handles the domain name and DNS management. CloudFront is a delivery network that will cache your website around the world for quick user access. Amazon S3 will host your website that includes all the files needed to make the frontend work and look as intended. The end result will look like this: a user will navigate to the domain name that you chose for the project. That will direct to a CloudFront distribution that has cached a version of your website that’s located an S3 bucket.

1. S3: Use defaults unless specified
    - Create a new S3 bucket.
    - Name the bucket and choose the region.
    - Keep all defaults (We don’t need public access because we only want someone to access it via CloudFront, not directly).
    - Upload the 3 files to S3.
2. CloudFront: Use defaults unless specified
    - Choose your S3 bucket as the origin.
    - Origin access: Origin access control settings.
    - Origin access control: Create control settings. Keep defaults then create.
    - (Optional) Redirect HTTP to HTTPS
    - No WAF.
    - Use CNAME as the domain that you want for the website.
    - (Optional) Choose an existing SSL cert or request a new one
    - Request public cert
    - Type a single domain name or use a wildcard.
    - Validate cert
    - Default root object: index.html
    - Once it’s created, copy the CloudFront policy statement to your S3 bucket’s policy to allow CloudFront read access.
3. Route 53
    - Use my [previous guide](https://theitguycj.com/using-amazon-route-53-for-dns/) to create a hosted zone.
    - Navigate to hosted zone and create new record.
    - Name the subdomain. Record type: A. Choose “alias”
    - Route traffic to the CloudFront distribution you just created.

## Step 3: DynamoDB
DynamoDB will store all the jokes in a NoSQL database (DB). Create a new database and name it. We’ll use the partition key “jokepartition” as a string and the sort key “order” as a number. Keep all other defaults.

## Step 4: 1st Lambda Function
This Lambda function will do the initial processing of the joke and user email address. We pass the values in using Lambda’s function URL. This allows a remote call to execute the function and eliminates the need for an API Gateway. This Python code then stores the joke and the user’s email address (optional) in the DB, and increments the order number by one.

Create a Lambda function. Name it, use the Python runtime, enable function URL, select NONE for Auth type, and enable CORS. The function URL will be needs to be added to the JavaScript file in Step 1 to invoke the Lambda function. The function permissions needs to have a policy that allows for DynamoDB read and write access. I just used full access for this project. Copy my 1st Lambda function located in GitHub. My code comments make things pretty self-explanatory; you’ll just need to replace my values with your DynamoDB key names and variable names if you changed them.

## Step 5: 2nd Lambda Function
This Lambda function is triggered when a new item is inserted into the database. It 1st looks to see if an email address is present. If not, it does nothing. It there’s one, it grabs the email address, joke, and order number. It then grabs the 5 jokes that came before it and writes them out to a few lines to be sent to the user.

Create another Lambda function but no need for a Function URL. Name it and use the Python runtime. Use the created DynamoDB table as a trigger. It’ll need a policy for DynamoDB read access (and, if used, Amazon SES). I tried to use Amazon SES for sending emails but Amazon didn’t approve me to leave the “sandbox environment” that only allows you to send emails to pre-approved senders as “we believe that your use case would impact the deliverability of our service and would affect your reputation as a sender” ????. Since that was the case, I just used my own “no-reply” email address and SMTP settings to send emails. I have had a few issues with my custom email not sending to ALL recipients but most major email providers have received the jokes with no issues. You could also use a Gmail address (use SMTP) and that should give you no issues. Copy the 2nd Lambda function that you need (SES or SMTP) from my GitHub and insert your own settings for the SMTP (or SES), DB, and email address.

## Step 6: Verify
Make sure that you are doing various console log outputs, JSON returns, and print messages during your projects to ensure that the right data is being returned. After that attempt to send yourself a test emails from the project to different email providers to see if there are formatting or deliverability issues. Other than that, good luck!
