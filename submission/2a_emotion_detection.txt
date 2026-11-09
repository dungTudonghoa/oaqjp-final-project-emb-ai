"""Detect emotions in English text using the IBM Watson NLP service."""

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return scores for five emotions and the strongest emotion.

    Empty input or an HTTP 400 response produces a dictionary of None values.
    Other HTTP errors propagate so deployment problems are not hidden.
    """
    empty_result = {emotion: None for emotion in EMOTIONS}
    empty_result["dominant_emotion"] = None

    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result

    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(
        API_URL, json=payload, headers=HEADERS, timeout=30
    )

    if response.status_code == 400:
        return empty_result

    response.raise_for_status()
    response_body = response.json()
    emotion_scores = response_body["emotionPredictions"][0]["emotion"]
    result = {emotion: emotion_scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(EMOTIONS, key=result.get)
    return result
