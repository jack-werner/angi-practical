import pandas as pd
from datetime import datetime

df = pd.read_csv("outputs/roofing.csv")


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


def get_score(df):
    # days_accredited + bbb_rating + customer_rating_avg + days_in_operation - complaints_l12m - complaints_l36m
    current_date = datetime.now()
    df["days_accredited"] = (
        current_date - pd.to_datetime(df["accredited_date"])
    ).dt.days
    df["numeric_bbb"] = df["bbb_ranking"].apply(numeric_ranking)
    df["days_in_operation"] = (
        current_date - pd.to_datetime(df["business_start_date"])
    ).dt.days
