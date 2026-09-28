from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

AYURVEDA_PATH = (
    BASE_DIR
    / "data"
    / "ayurvedic_knowledge.csv"
)


class AyurvedaKnowledgeEngine:

    def __init__(self):

        if not AYURVEDA_PATH.exists():

            raise FileNotFoundError(
                f"Ayurveda knowledge file not found: "
                f"{AYURVEDA_PATH}"
            )

        self.df = pd.read_csv(
            AYURVEDA_PATH,
            encoding="utf-8"
        )

        self.df.columns = [
            str(column).strip()
            for column in self.df.columns
        ]

    @staticmethod
    def normalize(value):

        return str(
            value
        ).strip().lower()

    def search(
        self,
        query,
        top_n=5
    ):

        if not query:
            return self.df.head(
                top_n
            ).copy()

        query = self.normalize(
            query
        )

        scores = []

        for _, row in self.df.iterrows():

            row_text = " ".join(
                str(value)
                for value in row.values
            ).lower()

            score = 0

            for word in query.split():

                if word in row_text:
                    score += 1

            scores.append(score)

        result = self.df.copy()

        result["_score"] = scores

        result = result[
            result["_score"] > 0
        ]

        result = result.sort_values(
            "_score",
            ascending=False
        )

        return result.drop(
            columns=["_score"]
        ).head(
            top_n
        ).reset_index(
            drop=True
        )

    def get_by_condition(
        self,
        condition,
        top_n=5
    ):

        return self.search(
            condition,
            top_n
        )

    def get_all(self):

        return self.df.copy()