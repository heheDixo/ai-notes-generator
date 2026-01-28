QUIZ_PROMPT = """
You are a teacher creating a revision quiz from study notes.

Create 8 multiple choice questions.

Rules:
- 4 options per question (A, B, C, D)
- Mark the correct answer
- Questions should test understanding, not memory

Format exactly like:

Q1. Question text
A. option
B. option
C. option
D. option

Answer: B

Notes:
"""


def generate_quiz(llm, notes: str) -> str:
    response = llm.invoke(QUIZ_PROMPT + notes)
    return response.content