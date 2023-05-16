from index import *

bucket_name = 'JigsawTxQuery'

bucket = s3.create_bucket(Bucket = bucket_name)

# pull data and 
# coerce to line separate list of dictionaries
name = 'HONDURAS MAYA CAFE & BAR LLC'
receipts = find_receipts(name)

in_mem_text = build_in_mem_file(receipts)

# upload to s3 object in our bucket
file_name = cleaned_name(name)

# s3.put_object(
#         Body=in_mem_text,
#         Bucket=bucket_name,
#         Key=file_name
#     )

# create bucket for results

# bucket_name = 'JigsawTxResults'

# results_bucket = s3.create_bucket(Bucket = bucket_name)