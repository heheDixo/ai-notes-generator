FLASHCARD_PROMPT = """
You are a great teacher.

From the study notes below, create revision flashcards.

Rules:
- Create 12–18 flashcards
- Each flashcard must be short
- Format strictly as:

Q: question
A: answer

Make questions clear and answers concise.

Notes:
"""


def generate_flashcards(llm, notes: str) -> str:
    response = llm.invoke(FLASHCARD_PROMPT + notes)
    return response.content