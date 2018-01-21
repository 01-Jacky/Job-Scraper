# Job-Scraper

Scrap jobs from job boards and insert into DynamoDB

App that uses these data: 

http://internship-watch.herokuapp.com/

Repo - https://github.com/01-Jacky/Internship-Watch

## Getting Started 

Clone repo, setup virtualenv with prerequisites, and run the scraper script(s). Schedule CRON job for periodic scraps. 

### Prerequisites

1. Python 3.6

2. Boto3 for talking with DynamoDB

3. Beautifulsoup 4 

### Configuration

To talk to your DynamoDB instance, provide your AWS keys in environment variables under:
 
    AWS_ACCESS_KEY_ID 
    
    AWS_SECRET_ACCESS_KEY. 

Boto3 by default looks for those key names.

### Running

cd to root folder and run from shell

    ```
    set FLASK_APP=web_result.py
    flask run
    ```
    
Alternatively schedule schedule CRON or deploy to AWS Lambda





