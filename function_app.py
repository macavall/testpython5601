import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="http1", auth_level=func.AuthLevel.ANONYMOUS)
def http1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# An HTTP-Triggered Function with a Durable Functions Client binding
@app.route(route="orchestrators/{functionName}")
@app.durable_client_input(client_name="client")
async def durable1_starter(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)
    response = client.create_check_status_response(req, instance_id)
    return response


# Orchestrator
@app.orchestration_trigger(context_name="context")
def durable1_orchestrator(context):
    result1 = yield context.call_activity("durable1_activity", "Seattle")
    result2 = yield context.call_activity("durable1_activity", "Tokyo")
    result3 = yield context.call_activity("durable1_activity", "London")

    return [result1, result2, result3]

# Activity
@app.activity_trigger(input_name="city")
def durable1_activity(city: str):
    return "Hello " + city 