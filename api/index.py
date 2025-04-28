from flask import Flask, request, render_template
from math import pow

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Render the HTML template (index.html)
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_bmi():
    try:
        # Get height (convert cm to meters) and weight from the form
        height = float(request.form['height']) / 100
        weight = float(request.form['weight'])
        
        # Calculate BMI
        bmi = round(weight / pow(height, 2), 1)

        # Determine BMI category
        if bmi < 18.5:
            result = f'BMI = {bmi} is Underweight'
        elif 18.5 <= bmi < 24.9:
            result = f'BMI = {bmi} is Normal'
        elif 24.9 <= bmi < 29.9:
            result = f'BMI = {bmi} is Overweight'
        else:
            result = f'BMI = {bmi} is Obesity'

        # Return result with updated template
        return render_template('index.html', result=result)
    except Exception as e:
        # In case of an error, return the error message
        return str(e)

# This function allows the app to work as a serverless function on Vercel
def handler(request, context):
    from werkzeug.test import EnvironBuilder
    from werkzeug.wrappers import Request

    # Build environment from the request
    builder = EnvironBuilder(
        method=request['method'],
        path=request['path'],
        query_string=request.get('queryString') or '',
        data=request.get('body') or {}
    )
    env = builder.get_environ()
    req = Request(env)

    # Dispatch the request and get the response
    with app.test_request_context(req.path, method=req.method, data=req.form):
        response = app.full_dispatch_request()

    # Return the response in the expected format for Vercel
    return {
        "statusCode": response.status_code,
        "headers": dict(response.headers),
        "body": response.get_data(as_text=True)
    }
