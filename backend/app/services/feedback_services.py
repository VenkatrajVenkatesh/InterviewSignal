def generate_mock_feedback(answer_text: str) -> dict:
    text_length = len(answer_text.strip())

    if text_length < 30:
        return {
            "score": 4,
            "feedback_text": "Your answer is too short. Add more detail, structure, and examples."
        }
    elif text_length < 100:
        return {
            "score": 6,
            "feedback_text": "Decent start, but your answer could be clearer and more complete. Try explaining your reasoning in more depth."
        }
    elif text_length < 250:
        return {
            "score": 8,
            "feedback_text": "Good answer. It has reasonable detail and structure. To improve further, include trade-offs or a practical example."
        }
    else:
        return {
            "score": 9,
            "feedback_text": "Strong answer. Well explained with good depth. Consider tightening the structure slightly for even better clarity."
        }