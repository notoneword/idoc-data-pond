My First Pipeline!
(small data, slow stream)

NOTES:
- Using pandas layer {"package": "pandas", "packageVersion": "1.4.1", "arn": "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pandas:2"}

DONE:
- Downloads population spreadsheets
- normalizes file names
- cleans data, checks for changing header names
- First steps to make serverless, store files to S3

TODO:
- Step Function to also process raw files, etc.
- process latest file for who we serve stats
