def transform_peleg_output(df_puzzle):
    id_col = df_puzzle.pop("id")
    df_puzzle.insert(0,"piece",id_col)
    df_puzzle = df_puzzle.loc[:,~df_puzzle.columns.str.match("Unnamed")]
    return df_puzzle


def save_puzzle_plot_as_naive(csvs,output_dir):
    pass