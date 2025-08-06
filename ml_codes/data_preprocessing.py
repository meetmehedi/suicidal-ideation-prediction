# data_preprocessing.py
import pandas as pd
from scipy.__config__ import show
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
targeted_fields2 = {
    "Q1": "Custom Age",
    "Q2": "Sex",
    "Q3": "In what grade are you",
    "Q4": "How tall are you",
    "Q5": "How much do you weigh",
    "Q6": "How often went hungry",
    "Q7": "No fruit eating",
    "Q8": "No vegetable eating",
    "Q9": "Soft drinks",
    "Q10": "Fast food eating",
    "Q11": "Tooth brushing",
    "Q12": "Hand washing before eating",
    "Q13": "Hand washing after toilet",
    "Q14": "Hand washing with soap",
    "Q15": "Physically attacked",
    "Q16": "Physical fighting",
    "Q17": "Seriously injured",
    "Q18": "Serious injury broken bone",
    "Q20": "Bullied",
    "Q22": "Felt lonely",
    "Q23": "Could not sleep",
    "Q24": "Considered suicide",
    "Q25": "Made a suicide plan",
    "Q26": "Attempted suicide",
    "Q27": "Close friends",
    "Q28": "Initiation of cigarette use",
    "Q29": "Current cigarette use",
    "Q30": "Other tobacco use",
    "Q31": "Smoking cessation",
    "Q32": "Smoking in their presence",
    "Q33": "Parental tobacco use",
    "Q34": "Initiation of alcohol use",
    "Q35": "Current alcohol use",
    "Q36": "Drank 2+ drinks",
    "Q37": "Source of alchohol",
    "Q38": "Really drunk",
    "Q39": "Trouble from drinking",
    "Q40": "Initiation of drug use",
    "Q41": "Ever marijuana use",
    "Q42": "Current marijuana use",
    "Q43": "Amphethamine or methamphetamine use",
    "Q44": "Ever sexual intercourse",
    "Q45": "Sex before 14 years",
    "Q47": "Condom use",
    "Q48": "Birth control used",
    "Q49": "Physical activity >= 5 days",
    "Q50": "Walk or bike to school",
    "Q51": "PE attendance",
    "Q52": "Sitting activities",
    "Q53": "Miss school no permission",
    "Q54": "Other students kind and helpful",
    "Q55": "Parents check homework",
    "Q56": "Parents understand problems",
    "Q57": "Parents know about free time"
}


def load_and_preprocess_data(filepath):
    # Load the dataset
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print("Data loaded successfully.")

    # Keep only target columns
    df = df[list(targeted_fields.keys())]


    print("\nBefore imputation:")
    # showing loaded dataset information
    show_dataset_info(df)

    # KNN imputation
    imputer = KNNImputer(n_neighbors=len(df) - 1)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    print("\nAfter imputation:")
    # showing imputed dataset information
    show_dataset_info(df)

    # Create "suicide" label
    df["suicide"] = df.apply(
        lambda row: 1 if (row["Q24"] == 1 or row["Q25"] == 1 or row["Q26"] != 1) else 0, axis=1
    )

    # Drop the original suicide-related columns
    df = df.drop(columns=["Q24", "Q25", "Q26"])

    return df

def show_dataset_info(df):
    """
    Displays detailed information about the dataset.
    
    Parameters:
    - df: pandas DataFrame
    """
    print("--- Dataset Basic Info ---")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\nTotal number of data = {df.count().sum()}")

    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"Total missing values in dataset: {total_missing}")



