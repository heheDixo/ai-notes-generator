import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def sentence_split(text: str):

    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences


def semantic_chunks(text: str, max_chars=1200):
    sentences = sentence_split(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_text(text: str):

    sem_chunks = semantic_chunks(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    final_chunks = []
    for chunk in sem_chunks:
        final_chunks.extend(splitter.split_text(chunk))

    return final_chunks

