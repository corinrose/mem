import psutil, math, os, time, sys
from rich.panel import Panel
from rich.live import Live

def get_memory_usage():
    app_memory = {}

    for p in psutil.process_iter():
        try:
            exe = p.exe()
            if not exe:
                continue
            app_name = exe.split("/")[-1]
            pss = p.memory_full_info().pss
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

        app_memory[app_name] = app_memory.get(app_name, 0) + pss
    return app_memory

def get_top(mem, n = 10):
    top = dict(sorted(mem.items(), key=lambda item: item[1], reverse=True)[:n])
    total = sum(mem.values())
    return top, total

def bytes2human(n):
    """
    Convert bytes to human-readable format
    """
    try:
        symbols = [' ', 'K' , 'M', 'G']
        digits = math.floor(math.log10(n)) + 1
        order = math.floor(digits / 3)
        trunc = n / (1024 ** order)
        return str(round(trunc, 2)) + symbols[order]
    except ValueError:
        return "0B"

def tui(mem, rows = 24, columns = 80):
    top, total = get_top(mem, rows)

    mem_width = 10
    pct_width = 8
    title_width = max(10, columns - mem_width - pct_width - 8)

    output_lines = []
    for item in top.items():
        app = item[0]
        mem = bytes2human(item[1])
        pct = (item[1] / total) * 100

        # Rich markup for colors
        output_lines.append(f"[bold cyan]{app:<{title_width}}[/bold cyan] : [green]{mem:>{mem_width}}[/green] ({pct:5.1f}%)")

    panel = Panel(
        "\n".join(output_lines),
        title="[bold yellow]Memory Usage Breakdown (PSS)[/bold yellow]",
        expand=False
    )
    return panel

def main():
    mem = get_memory_usage()

    try:
         # Initialize Live display
        with Live(refresh_per_second=4, screen=True) as live:
            while True:
                rows = os.get_terminal_size()[1] - 2
                columns = os.get_terminal_size()[0]
                panel = tui(mem, rows, columns)

                # Update the live display panel in place without flashing
                live.update(panel)
                mem = get_memory_usage()
                time.sleep(2)
    finally:
        # Always restore the cursor when exiting (via Ctrl+C or completion)
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    # Exit cleanly and quietly with a standard Unix exit code (130 is standard for SIGINT)
    sys.exit(130)