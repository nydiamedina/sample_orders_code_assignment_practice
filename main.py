import pandas as pd
import gzip
import json
from transformations.user_agent_parser import parse_user_agent


# Read the gzipped JSON lines file into a pandas DataFrame
def read_data(file_name):
    with gzip.open(file_name, "rt", encoding="utf-8") as f:
        data = pd.DataFrame([json.loads(line) for line in f])
    return data


def preprocess_data(data):
    pd.set_option("display.max_colwidth", None)
    data["USER_AGENT"].fillna("Unknown", inplace=True)
    data["USER_AGENT"].replace('""', "Unknown", inplace=True)
    return data


def main():
    data = read_data("sample_orders.json.gz")
    data = preprocess_data(data)

    # Apply the parse_user_agent function to the USER_AGENT column
    data[["DEVICE_TYPE", "BROWSER_TYPE", "BROWSER_VERSION"]] = data.apply(
        lambda row: parse_user_agent(row["USER_AGENT"]), axis=1, result_type="expand"
    )

    unique_browser_rows = data.groupby("BROWSER_TYPE").first().reset_index()
    for index, row in unique_browser_rows.iterrows():
        print(row[["USER_AGENT", "DEVICE_TYPE", "BROWSER_TYPE", "BROWSER_VERSION"]])


if __name__ == "__main__":
    main()
