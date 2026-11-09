async function RunSentimentAnalysis() {
  const text = document.getElementById('textToAnalyze').value;
  const output = document.getElementById('system_response');
  output.textContent = 'Analyzing...';
  try {
    const response = await fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    output.textContent = await response.text();
  } catch (error) {
    output.textContent = `Unable to analyze text: ${error.message}`;
  }
}
