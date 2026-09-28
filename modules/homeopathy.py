from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "homeopathy_knowledge.csv"


class HomeopathyKnowledgeEngine:

    def __init__(self):

        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"File not found: {DATA_PATH}"
            )

        self.df = pd.read_csv(
            DATA_PATH,
            encoding="utf-8"
        )

        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

    def search(self, query="", top_n=10):

        if not query or not str(query).strip():
            return self.df.head(top_n).copy()

        query = str(query).strip().lower()

        scores = []

        for _, row in self.df.iterrows():

            text = " ".join(
                str(value).lower()
                for value in row.values
            )

            score = sum(
                1
                for word in query.split()
                if word in text
            )

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
        ).head(top_n).reset_index(drop=True)

    def get_by_condition(
        self,
        condition,
        top_n=10
    ):
        return self.search(
            condition,
            top_n
        )

    def get_all(self):
        return self.df.copy()