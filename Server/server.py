from flask import Flask, request, jsonify
import util

app = Flask(__name__)
util.load_saved_artifacts()

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        # Use .get to avoid KeyErrors and provide meaningful defaults or raise custom errors
        total_sqft = request.form.get('total_sqft')
        location = request.form.get('location')
        bhk = request.form.get('bhk')
        bath = request.form.get('bath')

        # Check if all required fields are present
        if not total_sqft or not location or not bhk or not bath:
            return jsonify({'error': 'Missing one or more required fields: total_sqft, location, bhk, bath'}), 400

        # Convert to appropriate types
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except ValueError:
        return jsonify({'error': 'Invalid value type for total_sqft, bhk, or bath'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting Python Flask server for Real Estate Price Prediction")
    app.run(debug=True)
