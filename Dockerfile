FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask py-ecg-detectors
EXPOSE 6002
CMD ["python", "server.py"]
