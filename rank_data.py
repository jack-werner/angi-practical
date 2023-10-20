import pandas as pd
from datetime import datetime


def numeric_ranking(rank):
    grade_values = {
        "A+": 12,
        "A": 11,
        "A-": 10,
        "B+": 9,
        "B": 8,
        "B-": 7,
        "C+": 6,
        "C": 5,
        "C-": 4,
        "D+": 3,
        "D": 2,
        "D-": 1,
        "F": 0,
        "NR": -1,
    }

    return grade_values[rank]


def min_max_scaler(col: pd.Series):
    min_val = col.min()
    max_val = col.max()
    return (col - min_val) / (max_val - min_val)


def calc_score(df: pd.DataFrame):
    for col in df.columns:
        df[col] = min_max_scaler(df[col])

    return (
        df["numeric_bbb"].fillna(0) * 6
        + df["customer_rating_avg"].fillna(0) * 5
        + df["days_accredited"].fillna(0) * 4
        + df["days_in_operation"].fillna(0) * 3
        - df["complaints_l12m"].fillna(0) * 2
        - df["complaints_l36m"].fillna(0) * 1
    )


def get_score(df: pd.DataFrame):
    df["bbb_rating"] = df["bbb_rating"].str.strip()

    current_date = datetime.now()
    df["days_accredited"] = (
        current_date - pd.to_datetime(df["accredited_date"])
    ).dt.days
    df["numeric_bbb"] = df["bbb_rating"].apply(numeric_ranking)
    df["days_in_operation"] = (
        current_date - pd.to_datetime(df["business_start_date"])
    ).dt.days

    # get numerical data
    numerical_cols = [
        "days_accredited",
        "numeric_bbb",
        "customer_rating_avg",
        "days_in_operation",
        "complaints_l12m",
        "complaints_l36m",
    ]

    df_calc = df[numerical_cols]

    df["score"] = calc_score(df_calc)

    return df


if __name__ == "__main__":
    df = get_score(df=pd.read_csv("outputs/roofing.csv"))
    df = df.sort_values(by="score", ascending=False)

    df.to_csv("outputs/rankings.csv", index=False)
