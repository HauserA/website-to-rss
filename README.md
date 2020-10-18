# Website to RSS

Use AWS to create a RSS feed from a website.
I made this project to get push notifications for all changes on the bulletin board of my university.

This project will use:
1. [**AWS Lambda**](https://aws.amazon.com/lambda/) to read and parse the website, create the RSS feed and save the feed to AWS S3.
2. [**AWS S3**](https://aws.amazon.com/s3/) to provide a public link to the RSS feed.
3. [**AWS Eventbridge**](https://aws.amazon.com/eventbridge/) to trigger the lambda function which will update the RSS feed.
4. [**AWS IAM**](https://aws.amazon.com/iam/) to handle permissions of every service.
5. [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) to create all needed resources.

The architecture of the project will look like this:

![Architecture](https://a-h.io/images/website-to-rss/architecture.png)

More here: [https://a-h.io/blog/website-to-rss/](https://a-h.io/blog/website-to-rss/)
