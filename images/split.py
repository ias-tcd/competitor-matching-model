import os

from sklearn.model_selection import train_test_split


def make_folders(company_name: str) -> None:
    os.mkdir(f"./{company_name}/training")
    os.mkdir(f"./{company_name}/validation")
    os.mkdir(f"./{company_name}/test")


def split_images(company_name: str) -> None:
    data: list[str] = os.listdir(f"./{company_name}")
    make_folders(company_name)

    # sklearn only has function to split data into two sets so we need to run it twice
    # to get our three sets
    # this will give us split of 70/20/10 for training/validation/test respectively
    X_train, X_test = train_test_split(data, test_size=0.1, random_state=42)
    X_train, X_val = train_test_split(X_train, test_size=0.22, random_state=42)

    for img in X_train:
        os.rename(f"./{company_name}/{img}", f"./{company_name}/training/{img}")

    for img in X_val:
        os.rename(f"./{company_name}/{img}", f"./{company_name}/validation/{img}")

    for img in X_test:
        os.rename(f"./{company_name}/{img}", f"./{company_name}/test/{img}")


def undo_split(company_name: str) -> None:
    train = os.listdir(f"./{company_name}/training")
    val = os.listdir(f"./{company_name}/validation")
    test = os.listdir(f"./{company_name}/test")

    for img in train:
        os.rename(f"./{company_name}/training/{img}", f"./{company_name}/{img}")

    for img in val:
        os.rename(f"./{company_name}/validation/{img}", f"./{company_name}/{img}")

    for img in test:
        os.rename(f"./{company_name}/test/{img}", f"./{company_name}/{img}")

    os.rmdir(f"./{company_name}/training")
    os.rmdir(f"./{company_name}/validation")
    os.rmdir(f"./{company_name}/test")


def main():
    os.chdir("./images")
    split_images("under_armour")


if __name__ == "__main__":
    main()
