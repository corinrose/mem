import subprocess, io, argparse, os
import pandas as pd

def get_memory_usage():
    # Run the smem command to get memory usage
    mem = subprocess.run(["smem", "-r"], capture_output=True, text=True, check=True)

    # Read the fixed-width formatted file into a pandas DataFrame
    df = pd.read_fwf(io.StringIO(mem.stdout))
    # Convert USS, PSS, and RSS columns from kilobytes to bytes
    df[["USS", "PSS", "RSS"]] = df[["USS", "PSS", "RSS"]].apply(lambda x: x * 1024)
    return df

def human2bytes(x):
    """
    Convert human-readable byte string to integer.
    """
    try:
        return int(x)
    except ValueError:
        symbols = [' ', 'K' , 'M', 'G']
        return int(float(x[:-1]) * (1024 ** symbols.index(x[-1])))


import math
import numpy as np

def bytes2human(n):
    """
    Convert bytes to human-readable format
    """
    symbols = [' ', 'K' , 'M', 'G']
    digits = math.floor(math.log10(n)) + 1
    order = math.floor(digits / 3)
    trunc = n / (1024 ** order)
    return str(round(trunc, 2)) + symbols[order]

def get_top(df, n = 10):
    """
    Get the top n applications by PSS memory usage.
    """
    # Classify rows by application name extracted from the Command column
    df["Application"] = df["Command"].astype(str).str.split('/').str[-1].str.split().str[0]
    grouped = df.groupby("Application", as_index=False)[["PSS"]].sum()
    top = grouped.sort_values(by="PSS", ascending=False).head(n)
    total = grouped["PSS"].sum()

    return df, top, total

def text_list(df, rows = 24, columns = 80):
    """
    Get the top n applications by PSS memory usage and return a formatted string.
    """
    _, top, total = get_top(df, rows)
    top["%"] = top["PSS"] / total * 100
    top["%"] = top["%"].apply(lambda x: f"{x:.1f}%")
    top["PSS"] = top["PSS"].apply(bytes2human)
    return top.to_string(index=False)


import matplotlib.pyplot as plt

def pie_chart(df, rows = 24, columns = 80):
    top = get_top(df, rows)[1]

    # Create a pie chart of the filtered applications' PSS values
    plt.pie(top["PSS"], labels=(top["Application"] + " " + top["PSS"].apply(bytes2human)), autopct='%1.1f%%')
    plt.show()

    return top

from rich import print
from rich.panel import Panel
#from rich.progress import BarColumn, Progress, TextColumn


def tui(df, rows = 24, columns = 80):
    _, top, total = get_top(df, rows)

    mem_width = 10
    pct_width = 8
    title_width = max(10, columns - mem_width - pct_width - 10)

    output_lines = []
    for _, row in top.iterrows():
        app = row["Application"]
        mem = bytes2human(row["PSS"])
        pct = (row["PSS"] / total) * 100
        
        # Rich markup for colors
        output_lines.append(f"[bold cyan]{app:<{title_width}}[/bold cyan] : [green]{mem:>{mem_width}}[/green] ({pct:5.1f}%)")

    panel = Panel(
        "\n".join(output_lines),
        title="[bold yellow]Memory Usage Breakdown (PSS)[/bold yellow]",
        expand=False
    )
    return panel


def main():
    parser = argparse.ArgumentParser(description="Analyze system memory usage via smem.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--tui', action='store_true', help='Display Rich TUI memory breakdown')
    group.add_argument('-p', '--pie', action='store_true', help='Generate graphical pie chart using matplotlib')
    group.add_argument('-l', '--list', action='store_true', help='Print text list breakdown')

    parser.add_argument('-n', '--number', type=int, default=10, help='Number of top applications to display (default: 10)')

    args = parser.parse_args()


    if args.tui:
        f = tui
    elif args.pie:
        f = pie_chart
    elif args.list:
        f = text_list
    else:
        f = tui  # Default to TUI if no argument is provided

    df = get_memory_usage()

    while True: 
        rows = os.get_terminal_size()[1] - 3
        columns = os.get_terminal_size()[0]
        panel = f(df, rows, columns)
        os.system('clear')
        print(panel)
        df = get_memory_usage()


if __name__ == "__main__":
    main()