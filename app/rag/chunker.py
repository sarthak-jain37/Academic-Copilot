def find_last_period(chunk):
    last_index = -1

    for i in range(len(chunk)):
        if chunk[i] == ".":
            last_index = i

    return last_index


def chunk_document(text, chunk_size=500, overlap=50):
    local_chunks = []

    start = 0
    chunk_num = 1

    while start < len(text):
        try:
            end = start + chunk_size
            chunk = text[start:end]

            if end < len(text):
                last_period = find_last_period(chunk)

                if last_period > chunk_size * 0.7:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1

            local_chunks.append(chunk.strip())
            start = end - overlap
            chunk_num += 1

        except Exception as e:
            raise Exception(f"Chunking failed at chunk {chunk_num}: {e}")

    return local_chunks
