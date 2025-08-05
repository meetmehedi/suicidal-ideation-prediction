# data_preprocessing.py
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
    "Q57": "Parents know about free time"
}

def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)

    # Keep only target columns
    df = df[list(targeted_fields.keys())]

    print("Before imputation:\n", df.isnull().sum())

    # KNN imputation
    imputer = KNNImputer(n_neighbors=len(df) - 1)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    print("After imputation:\n", df.isnull().sum())

    # Create "suicide" label
    df["suicide"] = df.apply(
        lambda row: 1 if (row["Q24"] == 1 or row["Q25"] == 1 or row["Q26"] != 1) else 2, axis=1
    )

    # Drop the original suicide-related columns
    df = df.drop(columns=["Q24", "Q25", "Q26"])

    return df
