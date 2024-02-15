import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from rich import print
from sqlalchemy.engine import create_engine
import os


DRUIDQ_URL = os.environ.get("DRUIDQ_URL", "druid://localhost:8887/")


def main(query):
    print("Query:")
    print(query)

    engine = create_engine(DRUIDQ_URL)
    df = pd.read_sql(query, engine)

    print()
    print("Out:")
    print(df)


def app():
    import sys
    try:
        with open(sys.argv[1], "r") as f:
            query = f.read()
    except FileNotFoundError:
        query = sys.argv[1]
    main(query)


if __name__ == "__main__":
    app()
