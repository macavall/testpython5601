import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="http1", auth_level=func.AuthLevel.ANONYMOUS)
def http1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    return func.HttpResponse(f"This HTTP triggered function executed successfully.")
