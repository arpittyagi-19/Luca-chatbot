from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper  # Ensure db_helper.py includes the get_order_status function

app = FastAPI()


@app.post("/")
async def handle_request(request: Request):
    try:
        # Retrieve JSON data from the request
        payload = await request.json()

        # Print the payload for debugging
        print("Received payload:", payload)  # Check your console for this output

        # Extract information from the Dialogflow webhook payload
        intent = payload.get('queryResult', {}).get('intent', {}).get('displayName', '')
        parameters = payload.get('queryResult', {}).get('parameters', {})

        # Handle the specific intent
        if intent == "track order - context:ongoing-tracking":
            # Call track_order function to process this intent
            response = track_order(parameters, payload.get("session", ""))
            return response
        else:
            # Return default response if intent is not recognized
            return JSONResponse(content={"fulfillmentText": "Intent not recognized"})

    except Exception as e:
        # Return error message if an exception occurs
        return JSONResponse(content={"fulfillmentText": f"Error: {str(e)}"})


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters.get('order_id', 0))  # Get order_id from parameters

    # Fetch the order status from the database
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    # Return JSON response to Dialogflow
    return JSONResponse(content={"fulfillmentText": fulfillment_text})
