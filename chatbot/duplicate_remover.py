class DuplicateRemover:

    def __init__(self):
        pass

    def remove_duplicates(self, chunks):

        unique_chunks = []
        seen = set()

        for chunk in chunks:

            # Use the chunk ID if available
            chunk_id = chunk.get("chunk_id")

            if chunk_id is not None:

                if chunk_id in seen:
                    continue

                seen.add(chunk_id)

            else:
                # Fallback: remove duplicates by text
                text = chunk["text"].strip()

                if text in seen:
                    continue

                seen.add(text)

            unique_chunks.append(chunk)

        return unique_chunks