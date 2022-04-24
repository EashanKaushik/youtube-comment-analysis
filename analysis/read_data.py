import os
import pandas as pd


def combine_all():
    final_df = None
    for current_dir in os.listdir("mr_beast"):
        if final_df is not None:
            final_df = pd.concat(
                [
                    final_df,
                    pd.read_csv(
                        os.path.join("mr_beast", current_dir), lineterminator="\n"
                    ),
                ]
            )
        else:
            final_df = pd.read_csv(
                os.path.join("mr_beast", current_dir), lineterminator="\n"
            )

    for current_dir in os.listdir("mr_beast_gaming"):
        if final_df is not None:
            final_df = pd.concat(
                [
                    final_df,
                    pd.read_csv(
                        os.path.join("mr_beast_gaming", current_dir),
                        lineterminator="\n",
                    ),
                ]
            )
        else:
            final_df = pd.read_csv(
                os.path.join("mr_beast_gaming", current_dir), lineterminator="\n"
            )

    return final_df


def combine_category(mr_beast=False, mr_beast_gaming=False):

    if mr_beast:
        mr_beast_df = None
        for current_dir in os.listdir("mr_beast"):
            if mr_beast_df is not None:
                mr_beast_df = pd.concat(
                    [mr_beast_df, pd.read_csv(os.path.join("mr_beast", current_dir), lineterminator='\n')]
                )
            else:
                mr_beast_df = pd.read_csv(os.path.join("mr_beast", current_dir), lineterminator='\n')

        return mr_beast_df

    if mr_beast_gaming:
        mr_beast_gaming_df = None

        for current_dir in os.listdir("mr_beast_gaming"):
            if mr_beast_gaming_df is not None:
                mr_beast_gaming_df = pd.concat(
                    [
                        mr_beast_gaming_df,
                        pd.read_csv(os.path.join("mr_beast_gaming", current_dir), lineterminator='\n'),
                    ]
                )
            else:
                mr_beast_gaming_df = pd.read_csv(
                    os.path.join("mr_beast_gaming", current_dir), lineterminator='\n'
                )

        return mr_beast_gaming_df


def read_data(name):

    if name in os.listdir("mr_beast"):
        return pd.read_csv(os.path.join("mr_beast", name))
    elif name in os.listdir("mr_beast_gaming"):
        return pd.read_csv(os.path.join("mr_beast_gaming", name))
    else:
        return f"No Data with {name} found!!"


if __name__ == "__main__":
    combine_all()
