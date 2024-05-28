import json
import pandas as pd
import matplotlib.pyplot as plt

json_file = "_encoded_chat.json"
labels = ["erin", "rine", "opi", "inaba", "touho", "reimu", "marisa"]


def load_json(json_file):
    """
    Jsonファイルを読み込む

    Args:
        json_file (str): JSONファイルのパス

    Returns:
        dict: JSONデータ
    """
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def json_to_dataframe(data):
    """
    JSONデータをDataFrameに変換する

    Args:
        data (dict): JSONデータ

    Returns:
        pandas.DataFrame: DataFrame (message, time_in_seconds, label)
    """
    records = [
        {
            "message": item["message"],
            "time_in_seconds": item["time_in_seconds"],
            "label": item["label"],
        }
        for item in data
    ]
    return pd.DataFrame.from_records(records)


def dataframe_to_time_seconds(df):
    """
    DataFrameのtime_in_secondsをint型に変換する

    Args:
        df (pandas.DataFrame): DataFrame

    Returns:
        pandas.DataFrame: DataFrame
    """
    df["time_in_seconds"] = df["time_in_seconds"].apply(lambda x: int(x))
    return df


def plot_label_distribution(
    df, selected_labels=labels, flag=False, filename="label_distribution.png"
):
    """
    ラベルの分布を円グラフで表示する

    Args:
        df (pandas.DataFrame): DataFrame
        selected_labels (list): 選択したラベル
        flag (bool): 選択していないラベルをotherにまとめるかどうか
        filename (str): 保存するファイル名
    """
    label_counts = df["label"].value_counts()
    if flag:
        other = label_counts[~label_counts.index.isin(selected_labels)].sum()
        new_label_counts = label_counts[label_counts.index.isin(selected_labels)]
        new_label_counts["other"] = other
        label_counts = pd.Series(new_label_counts, index=selected_labels + ["other"])
    else:
        label_counts = pd.Series(label_counts, index=selected_labels)
    plt.pie(
        label_counts,
        labels=label_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
    )
    plt.savefig(filename)
    plt.show()


def plot_label_over_time(df, selected_labels, filename="label_count_over_time.png"):
    """
    ラベルの時間経過による分布を折れ線グラフで表示する

    Args:
        df (pandas.DataFrame): DataFrame
        selected_labels (list): 選択したラベル
        filename (str): 保存するファイル名
    """
    df = dataframe_to_time_seconds(df)
    plt.figure(figsize=(10, 6))
    for label in selected_labels:
        label_data = df[df["label"] == label]
        if not label_data.empty:
            label_counts_over_time = label_data.groupby("time_in_seconds").size()
            label_counts_over_time.plot(label=label)

    plt.title("Label Count Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Count")
    plt.legend(title="Label")
    plt.savefig(filename)
    plt.show()


def main():
    data = load_json(json_file)
    df = json_to_dataframe(data)

    print("データ数:", len(df))
    print(" えーりんを含むメッセージ数:", len(df[df["label"] == "erin"]))
    print(" えーりん以外を含むメッセージ数:", len(df[df["label"] != "erin"]))
    print("各ラベルのメッセージ数")
    for label in labels + ["other"]:
        print(f" {label}を含むメッセージ数:", len(df[df["label"] == label]))

    plot_label_distribution(
        df, selected_labels=["erin"], flag=True, filename="label_distribution_erin.png"
    )
    plot_label_distribution(
        df,
        selected_labels=labels[1:] + ["other"],
        flag=False,
        filename="label_distribution_others.png",
    )

    plot_label_over_time(df, labels + ["other"])


if __name__ == "__main__":
    main()
