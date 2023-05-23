import boto3
CLIENT = boto3.client("athena")
DATABASE_NAME = 'another-db'
TABLE_NAME = 'jigsaw_taylor_sample'
import time
RESULT_OUTPUT_LOCATION = "s3://jigsawtexasresults/"


def get_num_rows():
    query = f"select * from jigsaw_taylor_sample limit 3;"
    response = CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
    )

    return response["QueryExecutionId"]

def has_query_succeeded(execution_id):
    state = "RUNNING"
    max_execution = 5

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = CLIENT.get_query_execution(QueryExecutionId=execution_id)
        if (
            "QueryExecution" in response
            and "Status" in response["QueryExecution"]
            and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                return True

        time.sleep(30)

    return False

def get_query_results(execution_id):
    response = CLIENT.get_query_results(
        QueryExecutionId=execution_id
    )

    results = response['ResultSet']['Rows']
    return results



# execution_id = get_num_rows()
# query_status = has_query_succeeded(execution_id=execution_id)
# get_query_results(execution_id)
# https://www.learnaws.org/2022/01/16/aws-athena-boto3-guide/

# https://github.com/ramdesh/athena-python-examples/blob/main/athena_boto3_example.py