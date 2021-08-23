import boto3
import json
from chalice import Chalice, Response

app = Chalice(app_name='CashRegisterApi')
app.log.setLevel("DEBUG")
awslambda = boto3.client("lambda")

@app.route('/cashregister/change', methods=['POST'], cors=True)
def handler():

    # read in the current request body and extract the billCounts
    request = app.current_request.json_body
    request["billCounts"] = str(request["billCounts"])
    register_payload = json.dumps(request).encode()

    # invoke the CashRegister-calculate_change function synchronously
    response = awslambda.invoke(
        FunctionName="CashRegister-calculate_change",
        InvocationType="RequestResponse",
        Payload=register_payload
    )

    # parse the response and return to requester
    change_response = json.loads(response["Payload"].read())
    return Response(
        body=change_response,
        status_code=200
    )



