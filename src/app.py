from flask import Flask, request, Response
from flask_restful import Resource, Api
from flasgger import Swagger
import os
from io import StringIO
import sys
from uploader import StockPriceReader
from predictor import PricePredictor
import random


SWAGGER_URL="/ui"
SWAGGER_CONFIG="/static/swagger.yml"
UPLOAD_FOLDER="/uploaded"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
ELEMENTS_NUM = 10
NUM_PREDICTIONS = 3

class BaseHandler(Resource):
    def processCsv(self):
        file = ""
        try:
            file = request.files['csv_file']
        except Exception as ex:
            print(f"BaseHandler {ex} - csv_file not uploaded", file=sys.stdout)
            return Response( "The response body goes here", status=400)

        if file== "":
            print("BaseHandler - no file uploaded!", file=sys.stdout)
            return Response( "The response body goes here", status=400)
        
        reader = StockPriceReader()
        print("Processed data", file=sys.stdout)
        newdata = reader.read(StringIO(file.read().decode("utf-8")))

        errors = newdata["errors"]
        if len(errors):
            # for row in errors:
            #     print(row, file=sys.stdout)
            return {'errors': f"{errors}"}

        rows = newdata["rows"]
        
        # return 10 elements starting from a random index
        total_rows = len(rows)
        startint_index = 0

        if total_rows > ELEMENTS_NUM:
            startint_index = random.randint(0, total_rows - ELEMENTS_NUM)
        end_index = min(total_rows, startint_index+ELEMENTS_NUM)
        return [rows, rows[startint_index:end_index]]

class UploadStockCsv(BaseHandler):
    def post(self):
        print("UploadStockCsv", file=sys.stdout)

        response = self.processCsv()
        if (isinstance(response, Response)):
            return response
        
        if "errors" in response:
            return response

        return {'message': f"{response[1]}"}

class PredictNextStockPrices(BaseHandler):
    def post(self):
        print("PredictNextStockPrices", file=sys.stdout)

        response = self.processCsv()
        if (isinstance(response, Response)):
            return response
        
        if "errors" in response:
            return response
        
        predictor = PricePredictor()
        predictions = predictor.predict(response[1], NUM_PREDICTIONS)

        return {'message': f"{predictions}"}
 
api.add_resource(UploadStockCsv, '/upload')
api.add_resource(PredictNextStockPrices, '/predict') 

swagger_config = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": "Predicting prices",
                "route": SWAGGER_CONFIG,
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": f"{SWAGGER_URL}/"
    }

# # create swagger UI
swagger = Swagger(app=app, config = swagger_config, template_file='static/swagger.yml')
 
 
if __name__ == '__main__':

    app.run(debug=True)