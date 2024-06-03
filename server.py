from flask import Flask, request, jsonify
# from ecgdetectors import Detectors
import pywt
from tensorflow import keras
import numpy as np

app = Flask(__name__)
# detectors = Detectors(125)


# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.get_json()
#         r_peaks = detectors.engzee_detector(data)
#         return jsonify({
#             'r_peaks': r_peaks
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        model = keras.models.load_model('model_cnn2.h5')

        predicted_class = predict_class(data, model)
        return jsonify(predicted_class)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def denoise_ecg(ecg_signal):
    wavelet = 'db4'
    level = 6
    coeffs = pywt.wavedec(ecg_signal, wavelet, level=level)

    threshold = np.std(coeffs[-1]) * np.sqrt(2 * np.log(len(ecg_signal)))
    coeffs_thresh = [pywt.threshold(
        c, threshold, mode='soft') if i == level else c for i, c in enumerate(coeffs)]

    ecg_denoised = pywt.waverec(coeffs_thresh, wavelet)

    return ecg_denoised


def normalize_data(data):
    data = np.array(data)
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return normalized_data


def predict_class(data, model):
    denoised_ecg_signal = denoise_ecg(data)
    normalized_data = normalize_data(denoised_ecg_signal)

    predictions_num = [0, 0, 0, 0, 0]
    labels = ['n', 's', 'v', 'f', 'q']
    windows_size = 186
    window_shift = 100
    total_windows = 0

    for i in range(0, normalized_data.shape[0] - windows_size + 1, window_shift):
        window = normalized_data[i:i + windows_size]
        window = window.reshape(1, window.shape[0], 1)
        predicted_probabilities = model.predict(window)
        predicted_class_index = np.argmax(predicted_probabilities)
        predictions_num[predicted_class_index] += 1
        total_windows += 1

    predicted_class_probabilities = [
        num / total_windows for num in predictions_num]
    sum_probabilities = sum(predicted_class_probabilities)
    predicted_class_probabilities = [
        round(prob / sum_probabilities, 2) for prob in predicted_class_probabilities]

    if sum(predicted_class_probabilities) != 1:
        diff = 1 - sum(predicted_class_probabilities)
        max_index = predicted_class_probabilities.index(
            max(predicted_class_probabilities))
        predicted_class_probabilities[max_index] += diff

    predicted_class_probabilities = {
        label: prob for label, prob in zip(labels, predicted_class_probabilities)}
    return predicted_class_probabilities


if __name__ == '__main__':
    app.run(debug=True, port=6003, host='0.0.0.0')
