from flask import Flask, request, jsonify
from ecgdetectors import Detectors

app = Flask(__name__)
detectors = Detectors(125)


@app.route('/analyze', methods=['POST'])
def calculate_sum():
    try:
        data = request.get_json()
        r_peaks = detectors.engzee_detector(data)
        return jsonify({
            'r_peaks': r_peaks
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=6003, host='0.0.0.0')
