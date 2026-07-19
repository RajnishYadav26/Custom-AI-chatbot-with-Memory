from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_pages(
        self,
        pages,
        document_name
    ):

        chunks = []

        chunk_id = 0

        for page in pages:

            raw_chunks = self.splitter.split_text(
                page["text"]
            )

            for chunk in raw_chunks:

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "document": document_name,
                        "page": page["page"],
                        "text": chunk,
                        "length": len(chunk)
                    }
                )

                chunk_id += 1

        return chunks