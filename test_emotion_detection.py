"""Unit tests for the Watson NLP emotion detector."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Validate results for five emotions and invalid input."""

    def assert_dominant_emotion(self, text, expected):
        """Mock a response and check the computed dominant emotion."""
        scores = {
            "anger": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.05,
            "sadness": 0.05,
        }
        scores[expected] = 0.8
        fake_response = Mock(status_code=200)
        fake_response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=fake_response,
        ) as mock_post:
            result = emotion_detector(text)
            self.assertEqual(result["dominant_emotion"], expected)
            for emotion, score in scores.items():
                self.assertEqual(result[emotion], score)
            mock_post.assert_called_once()

    def test_joy(self):
        """Happy text maps to joy."""
        self.assert_dominant_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Angry text maps to anger."""
        self.assert_dominant_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Disgusted text maps to disgust."""
        self.assert_dominant_emotion("I feel disgusted by this", "disgust")

    def test_sadness(self):
        """Sad text maps to sadness."""
        self.assert_dominant_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Afraid text maps to fear."""
        self.assert_dominant_emotion("I am really afraid", "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input(self, mock_post):
        """Empty input does not contact the external service."""
        result = emotion_detector("  ")
        self.assertTrue(all(value is None for value in result.values()))
        mock_post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, mock_post):
        """The API's 400 status produces an empty-result dictionary."""
        mock_post.return_value.status_code = 400
        result = emotion_detector("invalid input")
        self.assertTrue(all(value is None for value in result.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
