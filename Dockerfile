FROM tensorflow/tensorflow
WORKDIR /app
COPY . /app
RUN pip install --ignore-installed flask PyWavelets
EXPOSE 6002
CMD ["python", "server.py"]
