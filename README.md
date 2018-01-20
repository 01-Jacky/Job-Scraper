# Job-Scraper

Scrap jobs from job boards and insert into DynamoDB

Front end that uses these info: 

http://internship-watch.herokuapp.com/

Repo - https://github.com/01-Jacky/Internship-Watch

### Prerequisites

1. Python 3.6

2. Python Lob API

    ```
    pip install lob
    ```

3. Create a config.ini in the root folder to include lob api key .  

    NOTE: For reviewing the coding challenge, can skip this step as I provided a default config.ini and test API keys. 
    Please behave :). config.ini is in .gitignore to prevent accidental comitting of keys. 
    Alternative is using enviornment variables but that's not possible when delivering this code challenge as a zip file.
    ```
    [main]
    lob_key = ...
    google_civic_key = ...
    ```


### Running

1. Unzip into a desirable path  

2. In inputs folder, edit the default provided inputs.json with FROM address infi. 
Alternatively create your own input file per format below.
   
    ```
    {
      "name": "Peter The Anteater",
      "address1": "University of California, Irvine",
      "address2": "",
      "city": "Irvine",
      "state": "CA",
      "zipcode": "92697",
      "message": "Why is tuition so expensive? How can I afford an iPhone X???"
    }
    ```

3. Running from shell.
    
    To use default inputs.json in root folder, just run:
    ```
    python send_letter.py
    ```
    
    Otherwise give it your own input file:
    ```
    python send_letter.py path/some_inputs.json
    ```

### Sample Output
```
Reading user input file...
Fetching Governer info from Google Civic API...
Generating letter via Lob API...
Letter generated susccessfully
View at: https://s3.us-west-2.amazonaws.com/assets.lob.com/ltr_1249ec8262921a71.pdf?AWSAccessKeyId=AKIAIILJUBJGGIBQDPQQ&Expires=1518640526&Signature=Poo5OJfRL429FzuCaSGn6zo3TbY%3D

```


## Author

Jacky Lee - hklee310@gmail.com
