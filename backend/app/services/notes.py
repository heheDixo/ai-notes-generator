from typing import List


# CHUNK_PROMPT = """
# You are a brilliant teacher creating revision notes from a lecture.

# From this transcript part, extract ONLY the core learning points.

# Rules:
# - Use bullet points, not paragraphs
# - Be very concise
# - Explain concepts in 1–2 lines
# - Define terms only when necessary
# - Capture examples used by the speaker
# - Do NOT write like an article
# - Write like exam revision notes
# """

# FINAL_PROMPT = """
# You are a brilliant teacher creating ultra-crisp revision notes.

# You are given rough notes from different parts of a lecture.

# Your job is to produce HIGH-QUALITY STUDY NOTES that are:
# - Extremely concise
# - Easy to skim
# - Easy to revise in 3 minutes
# - Written like a teacher’s blackboard notes

# STRICT RULES:
# - No paragraphs
# - Only bullets and sub-bullets
# - Each bullet max 12 words
# - No textbook language
# - No filler sentences
# - No repetition
# - Use simple, direct words
# - Add memory hooks where possible

# Structure EXACTLY as:

# ## Overview (6–8 bullets)

# ## Core Concepts
# For each concept:
# - One line: what it is
# - One line: why it matters
# - One simple example

# ## Key Terms (very short)

# ## Big Picture (5 bullets)

# ## 2-Minute Revision (10 bullets max)
# """

# def summarize_chunk(llm, chunk: str) -> str:
#     res = llm.invoke(CHUNK_PROMPT + chunk)
#     return res.content


# def generate_notes_from_chunks(llm, chunks: List[str]) -> str:
   
#     mini_notes = []
#     for chunk in chunks:
#         note = summarize_chunk(llm, chunk)
#         mini_notes.append(note)


#     combined = "\n".join(mini_notes)


#     final = llm.invoke(FINAL_PROMPT + combined)

#     return final.content


MASTER_PROMPT = """
You are an expert teacher.

Below is a large transcript from a lecture.

Extract ALL important concepts, explanations, and examples.
Write them as rough teaching notes in bullet points.

Transcript:
"""

FINAL_PROMPT = """
You are a brilliant teacher creating ultra-crisp revision notes.

Convert the following rough teaching notes into structured study notes.

Rules:
- Only bullets and sub-bullets
- Very concise
- No repetition
- Easy to revise in 3 minutes
- Keep entire output under 350 words

Structure exactly as:

## Overview
## Core Concepts
## Key Terms
## Big Picture
## Quick Revision

Notes:
"""


def generate_notes_from_chunks(llm, chunks):

    big_text = "\n".join(chunks[:8])


    MAX_CHARS = 15000
    if len(big_text) > MAX_CHARS:
        big_text = big_text[:MAX_CHARS]

    print(f"Sending {len(big_text)} characters to Gemini")

    rough_notes = llm.invoke(MASTER_PROMPT + big_text).content


    final_notes = llm.invoke(FINAL_PROMPT + rough_notes).content

    return final_notes