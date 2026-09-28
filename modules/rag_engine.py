from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


class RAGEngine:

    def __init__(
        self,
        knowledge_directory=KNOWLEDGE_DIR
    ):

        self.knowledge_directory = Path(
            knowledge_directory
        )

        self.documents = []

        self._load_documents()

    def _load_documents(self):

        if not self.knowledge_directory.exists():
            return

        for file_path in self.knowledge_directory.rglob("*"):

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in [
                ".txt",
                ".md"
            ]:
                continue

            try:

                content = file_path.read_text(
                    encoding="utf-8"
                )

            except Exception:

                continue

            chunks = self._chunk_text(content)

            for chunk in chunks:

                self.documents.append(
                    {
                        "source": str(
                            file_path.relative_to(
                                BASE_DIR
                            )
                        ),
                        "content": chunk
                    }
                )

    @staticmethod
    def _chunk_text(
        text,
        chunk_size=800
    ):

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if not text:
            return []

        words = text.split()

        chunks = []

        current = []
        current_length = 0

        for word in words:

            current.append(word)

            current_length += (
                len(word) + 1
            )

            if current_length >= chunk_size:

                chunks.append(
                    " ".join(current)
                )

                current = []
                current_length = 0

        if current:

            chunks.append(
                " ".join(current)
            )

        return chunks

    @staticmethod
    def _score(
        query,
        content
    ):

        query_words = set(
            query.lower().split()
        )

        content_words = set(
            content.lower().split()
        )

        if not query_words:
            return 0

        return len(
            query_words.intersection(
                content_words
            )
        )

    def retrieve(
        self,
        query,
        top_k=5
    ):

        if not query:
            return []

        scored = []

        for document in self.documents:

            score = self._score(
                query,
                document["content"]
            )

            if score > 0:

                scored.append(
                    {
                        "source": document["source"],
                        "content": document["content"],
                        "score": score
                    }
                )

        scored.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return scored[:top_k]

    def build_context(
        self,
        query,
        top_k=5
    ):

        results = self.retrieve(
            query,
            top_k
        )

        if not results:

            return {
                "context": "",
                "sources": []
            }

        context_parts = []
        sources = []

        for result in results:

            context_parts.append(
                result["content"]
            )

            sources.append(
                result["source"]
            )

        return {
            "context": "\n\n".join(
                context_parts
            ),
            "sources": list(
                dict.fromkeys(sources)
            )
        }

    def document_count(self):

        return len(
            self.documents
        )