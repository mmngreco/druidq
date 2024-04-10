# ignore warnings from sqlalchemy and pandas
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
from rich import print
from sqlalchemy.engine import create_engine
import os


DRUIDQ_URL = os.environ.get("DRUIDQ_URL", "druid://localhost:8887/")


def get_query(args):
    query_in = args.query
    try:
        with open(query_in, "r") as f:
            out = f.read()
    except FileNotFoundError:
        out = query_in
    return out


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description="Druid Query")
    parser.add_argument("query", help="Druid query or filename")
    parser.add_argument(
        "-e",
        "--eval-df",
        help="Evaluate 'df' using string or filename",
        default="",
    )
    parser.add_argument(
        "-n",
        "--no-cache",
        help="Do not use cache",
        action="store_true",
    )
    return parser.parse_args()


def get_eval_df(args):
    eval_df_in = args.eval_df
    try:
        with open(eval_df_in, "r") as f:
            out = f.read()
    except FileNotFoundError:
        out = eval_df_in
    return out


def get_temp_file(query):
    from hashlib import sha1
    from pathlib import Path

    qhash = sha1(query.encode()).hexdigest()
    temp_file = Path(f"/tmp/druidq/{qhash}.parquet")
    if not temp_file.parent.exists():
        temp_file.parent.mkdir(parents=True, exist_ok=True)

    return temp_file


def execute(query, engine, no_cache=False):
    if no_cache:
        return pd.read_sql(query, engine)

    # cache {{
    temp_file = get_temp_file(query)
    if temp_file.exists():
        print(f"Loading cache: {temp_file}")
        return pd.read_parquet(temp_file)
    # }}

    df = pd.read_sql(query, engine)

    # cache {{
    print(f"Saving cache: {temp_file}")
    df.to_parquet(temp_file)
    # }}

    return df


def app():
    args = get_args()
    query = get_query(args)
    print("In[query]:")
    print(query)

    engine = create_engine(DRUIDQ_URL)
    df = execute(query, engine, args.no_cache)

    print()
    print("Out[df]:")
    print(df)

    if args.eval_df:
        eval_df = get_eval_df(args)
        print()
        print("In[eval]:")
        print(eval_df)

        print("Out[eval]:")
        exec(eval_df, globals(), locals())


if __name__ == "__main__":
    app()
