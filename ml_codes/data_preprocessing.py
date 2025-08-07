import pandas as pd
from sklearn.impute import KNNImputer

targeted_fields = {
    "Q1": "Custom Age",
    "Q2": "Sex",
    "Q3": "In what grade are you",
    "Q10": "Fast food eating",
    "Q11": "Tooth brushing",
    "Q12": "Hand washing before eating",
    "Q13": "Hand washing after toilet",
    "Q14": "Hand washing with soap",
    "Q15": "Physically attacked",
    "Q20": "Bullied",
    "Q22": "Felt lonely",
    "Q23": "Could not sleep",
    "Q24": "Considered suicide",
    "Q25": "Made a suicide plan",
    "Q26": "Attempted suicide",
    "Q27": "Close friends",
    "Q28": "Initiation of cigarette use",
    "Q29": "Current cigarette use",
    "Q35": "Current alcohol use",
    "Q40": "Initiation of drug use",
    "Q44": "Ever sexual intercourse",
    "Q49": "Physical activity >= 5 days",
    "Q53": "Miss school no permission",
    "Q54": "Other students kind and helpful",
    "Q56": "Parents understand problems",
    "Q57": "Parents know about free time",
}


def dataset_stats(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Total Elements": df.count().sum(),
        "Missing Cells": df.isnull().sum().sum(),
    }


def load_and_preprocess_data(filepath, return_stats=False):
    df = pd.read_csv(filepath)
    df = df[list(targeted_fields.keys())]
    print(len(df.columns))
    print(df.select_dtypes(exclude=['number']).columns
)
    pre_stats = dataset_stats(df)
    print(pre_stats)
    imputer = KNNImputer(n_neighbors=len(df) - 1)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    post_stats = dataset_stats(df)

    df["suicide"] = df.apply(
        lambda row: 1 if (row["Q24"] == 1 or row["Q25"] == 1 or row["Q26"] != 1) else 0,
        axis=1,
    )
    df = df.drop(columns=["Q24", "Q25", "Q26"])

    if return_stats:
        return df, pre_stats, post_stats
    return df
