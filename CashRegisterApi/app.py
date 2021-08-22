import boto3
import json
from chalice import Chalice, Response

app = Chalice(app_name='CashRegisterApi')
app.log.setLevel("DEBUG")
awslambda = boto3.client("lambda")

@app.route('/cashregister/change', methods=['POST'], api_key_required=True)
def handler():

    request = app.current_request.json_body
    
    request["billCounts"] = str(request["billCounts"])

    register_payload = json.dumps(request).encode()

    response = awslambda.invoke(
        FunctionName="CashRegister-calculate_change",
        InvocationType="RequestResponse",
        Payload=register_payload
    )

    response = json.loads(response["Payload"].read())

    change = response

    return Response(
            body=change,
            status_code=200
        )



