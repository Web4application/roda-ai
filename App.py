from flask import Flask, request, jsonify
from flask_cors import CORS
from models import HealthcareModel, FinanceModel, EducationModel, EntertainmentModel
from utils import preprocess_data, setup_logging

# Setup Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
setup_logging()

@app.route('/healthcare/predict', methods=['POST'])
def healthcare_predict():
    # Same content as your script

if __name__ == '__main__':
    app.run(debug=True)
