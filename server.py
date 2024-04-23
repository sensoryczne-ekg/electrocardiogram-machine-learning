from flask import Flask, request, jsonify
from ecgdetectors import Detectors

app = Flask(__name__)
detectors = Detectors(125)


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        r_peaks = detectors.engzee_detector(data)
        return jsonify({
            'r_peaks': r_peaks
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        
        # TODO(kSuroweczka): Implement predictor from tensorflow. data is a list of readings in 125Hz manner. Keep in mind that length of data is variable. Please fill following dict with probabilities of each class. Sum of all values should be equal to 1.
        return jsonify({
            'n': 0,
            's': 0,
            'v': 0,
            'f': 0,
            'q': 0,
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=6003, host='0.0.0.0')
