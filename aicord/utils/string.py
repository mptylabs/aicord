from __future__ import annotations

def split_paragraph_chunks(text: str, max_length: int) -> list[str]:
    """
    Splits a large text into chunks by paragraphs, each chunk being less than the specified length.

    Parameters:
        text (str): The text to be split into chunks.
        max_length (int): The maximum length for each chunk.

    Returns:
        list: A list of chunks, each less than max_length. Each chunk may contain multiple paragraphs.
    """
    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # Calculate the new length if we add this paragraph and a separator
        new_length = len(current_chunk) + len(paragraph) + len("\n\n")

        if new_length <= max_length:
            # If the new chunk is within the limit, append the paragraph
            current_chunk += paragraph + "\n\n"
        else:
            # If the new chunk would be too large, finalize the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    # Don't forget to append the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks