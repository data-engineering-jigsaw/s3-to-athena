from index import *
import pandas as pd
bucket_name = 'jigsawtexasquery'

bucket = s3.create_bucket(Bucket = bucket_name)


# pull data and 
# coerce to line separate list of dictionaries
name = 'HONDURAS MAYA CAFE & BAR LLC'
receipts = find_receipts(name)
receipts_df = pd.DataFrame(receipts)
file_name = f'{cleaned_name(name)}.csv'
receipts_df.to_csv(file_name, index = False)

df = pd.read_csv(file_name)

# s3.upload_file(file_name, bucket_name, file_name)

# obj = s3.get_object(Bucket=bucket_name, Key=file_name)
# text = obj['Body'].read()

# bucket_name = 'jigsawtexasresults'

# results_bucket = s3.create_bucket(Bucket = bucket_name)