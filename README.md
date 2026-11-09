# Final Project

Emotion Detector — an AI-based web application using the IBM Watson NLP EmotionPredict API with a Flask interface.

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 test_emotion_detection.py
python3 server.py
```

Open http://localhost:5000 to analyze English text. Live detection requires access to IBM's training endpoint.

## Static code analysis

```bash
python3 -m pylint server.py
```

The unit tests use mocked API responses; a passing test run does not establish availability of the external Watson service.
