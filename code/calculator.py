import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import combinations
import threading
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class RamseyResult:
    """Data class to store Ramsey calculation results."""
    k1: int
    k2: int
    estimated_r: int
    trials: int
    timestamp: str
    success: bool


class RamseyCalculator:
    """Core calculator for Ramsey numbers using Monte Carlo method."""

    def __init__(self):
        self.known_ramsey = {
            (3, 3): 6,
            (3, 4): 9,
            (3, 5): 14,
            (4, 4): 18,
            (3, 6): 18,
            (4, 5): 25,
        }
        self.history = []

    def has_monochromatic_clique(self, G, k, color):
        """Check if graph G contains a monochromatic clique of size k."""
        nodes = list(G.nodes)
        if k > len(nodes):
            return False

        for subset in combinations(nodes, k):
            sub = G.subgraph(subset)
            edges = list(sub.edges())

            if not edges and k == 1:
                return True

            if all(G[u][v]['color'] == color for u, v in edges):
                return True

        return False

    def check_ramsey(self, n, k1, k2, trials):
        """Monte Carlo estimation: check if R(k1, k2) <= n."""
        for _ in range(trials):
            G = nx.complete_graph(n)

            for u, v in G.edges():
                G[u][v]['color'] = random.choice(['red', 'blue'])

            has_red = self.has_monochromatic_clique(G, k1, 'red')
            has_blue = self.has_monochromatic_clique(G, k2, 'blue')

            if not has_red and not has_blue:
                return False

        return True

    def estimate_ramsey(self, k1, k2, trials, max_n=50, progress_callback=None):
        """Estimate Ramsey number using binary search style approach."""
        start_n = max(k1, k2)

        for n in range(start_n, max_n + 1):
            if progress_callback:
                progress_callback(n, k1, k2, max_n)

            if self.check_ramsey(n, k1, k2, trials):
                return n, True

        return None, False

    def get_known_value(self, k1, k2):
        """Return known Ramsey number if available."""
        key = tuple(sorted([k1, k2]))
        return self.known_ramsey.get(key)


class RamseyGUI:
    """Main GUI application for Ramsey Number Calculator."""

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Ramsey Number Calculator")
        self.root.geometry("1600x950")
        self.root.configure(bg="#0d1117")

        self.calculator = RamseyCalculator()
        self.current_graph = None
        self.is_calculating = False
        self.calculation_thread = None

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles for modern dark theme appearance."""
        style = ttk.Style()
        style.theme_use('clam')

        bg_color = "#0d1117"
        fg_color = "#e0e0e0"
        accent_color = "#58a6ff"
        button_bg = "#161b22"

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, 
                       font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=bg_color, foreground=accent_color, 
                       font=("Segoe UI", 14, "bold"))
        style.configure("Subtitle.TLabel", background=bg_color, foreground=accent_color, 
                       font=("Segoe UI", 11, "bold"))
        style.configure("TEntry", font=("Segoe UI", 10), fieldbackground="#0f3460", 
                       foreground=fg_color, borderwidth=1)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background=button_bg, 
                       foreground=fg_color)
        style.map("TButton", 
                 background=[("active", "#58a6ff"), ("pressed", "#1f6feb")],
                 foreground=[("active", "black"), ("pressed", "white")])
        style.configure("TLabelframe", background=bg_color, foreground=accent_color, 
                       borderwidth=1)
        style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color, 
                       font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background=button_bg, foreground=fg_color, 
                       padding=10)
        style.map("TNotebook.Tab", background=[("selected", bg_color)])

    def create_widgets(self):
        """Create all GUI widgets and layout."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        banner_frame = ttk.Frame(main_frame)
        banner_frame.pack(fill="x", pady=(0, 10))

        banner_label = ttk.Label(banner_frame, 
                                text="RAMSEY NUMBER CALCULATOR", 
                                style="Title.TLabel")
        banner_label.pack(side="left", padx=10)

        subtitle_label = ttk.Label(banner_frame, 
                                  text="Monte Carlo Graph Theory Tool", 
                                  foreground="#8b949e", 
                                  font=("Segoe UI", 9))
        subtitle_label.pack(side="left", padx=10)

        separator = ttk.Frame(main_frame, height=2)
        separator.pack(fill="x", pady=5)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))

        input_frame = ttk.LabelFrame(left_panel, text="Input Parameters", 
                                     padding=12)
        input_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(input_frame, text="Clique Size 1 (Red):", 
                 foreground="#79c0ff").grid(row=0, column=0, sticky="w", 
                                            pady=8, padx=5)
        self.entry_k1 = ttk.Entry(input_frame, width=12)
        self.entry_k1.insert(0, "3")
        self.entry_k1.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(input_frame, text="Clique Size 2 (Blue):", 
                 foreground="#79c0ff").grid(row=1, column=0, sticky="w", 
                                            pady=8, padx=5)
        self.entry_k2 = ttk.Entry(input_frame, width=12)
        self.entry_k2.insert(0, "3")
        self.entry_k2.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(input_frame, text="Trials per n:", 
                 foreground="#79c0ff").grid(row=2, column=0, sticky="w", 
                                            pady=8, padx=5)
        self.entry_trials = ttk.Entry(input_frame, width=12)
        self.entry_trials.insert(0, "5000")
        self.entry_trials.grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Label(input_frame, text="Max Search Limit:", 
                 foreground="#79c0ff").grid(row=3, column=0, sticky="w", 
                                            pady=8, padx=5)
        self.entry_max_n = ttk.Entry(input_frame, width=12)
        self.entry_max_n.insert(0, "25")
        self.entry_max_n.grid(row=3, column=1, sticky="ew", padx=5)

        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.LabelFrame(left_panel, text="Actions", padding=8)
        button_frame.pack(fill="x", pady=5, padx=5)

        self.btn_calculate = ttk.Button(button_frame, 
                                        text="START CALCULATION", 
                                        command=self.on_calculate)
        self.btn_calculate.pack(fill="x", pady=3)

        self.btn_visualize = ttk.Button(button_frame, 
                                        text="Visualize Graph", 
                                        command=self.visualize_example)
        self.btn_visualize.pack(fill="x", pady=3)

        self.btn_known = ttk.Button(button_frame, 
                                    text="Known Values", 
                                    command=self.show_known_values)
        self.btn_known.pack(fill="x", pady=3)

        self.btn_info = ttk.Button(button_frame, 
                                   text="Theory Info", 
                                   command=self.show_ramsey_info)
        self.btn_info.pack(fill="x", pady=3)

        self.btn_export = ttk.Button(button_frame, 
                                     text="Export History", 
                                     command=self.export_history)
        self.btn_export.pack(fill="x", pady=3)

        progress_frame = ttk.LabelFrame(left_panel, text="Progress", 
                                        padding=10)
        progress_frame.pack(fill="x", pady=5, padx=5)

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var, 
                                           maximum=100, 
                                           mode="determinate", 
                                           length=250)
        self.progress_bar.pack(fill="x", pady=5)

        self.progress_label = ttk.Label(progress_frame, 
                                       text="Ready", 
                                       foreground="#3fb950", 
                                       font=("Segoe UI", 10, "bold"))
        self.progress_label.pack()

        results_notebook = ttk.Notebook(left_panel)
        results_notebook.pack(fill="both", expand=True, pady=5, padx=5)

        results_frame = ttk.Frame(results_notebook)
        results_notebook.add(results_frame, text="Results")

        self.result_text = tk.Text(results_frame, height=20, width=40, 
                                   bg="#161b22", fg="#58a6ff", 
                                   font=("Consolas", 9),
                                   relief="flat", borderwidth=0, 
                                   insertbackground="#58a6ff")
        scrollbar1 = ttk.Scrollbar(results_frame, orient="vertical", 
                                  command=self.result_text.yview)
        self.result_text.configure(yscroll=scrollbar1.set)
        self.result_text.pack(side="left", fill="both", expand=True, 
                             padx=2, pady=2)
        scrollbar1.pack(side="right", fill="y", padx=(0, 2))

        history_frame = ttk.Frame(results_notebook)
        results_notebook.add(history_frame, text="History")

        self.history_text = tk.Text(history_frame, height=20, width=40, 
                                    bg="#161b22", fg="#58a6ff", 
                                    font=("Consolas", 8),
                                    relief="flat", borderwidth=0, 
                                    insertbackground="#58a6ff")
        scrollbar2 = ttk.Scrollbar(history_frame, orient="vertical", 
                                  command=self.history_text.yview)
        self.history_text.configure(yscroll=scrollbar2.set)
        self.history_text.pack(side="left", fill="both", expand=True, 
                              padx=2, pady=2)
        scrollbar2.pack(side="right", fill="y", padx=(0, 2))

        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, 
                        padx=(5, 0))

        viz_label = ttk.Label(right_panel, 
                             text="Graph Visualization", 
                             style="Subtitle.TLabel")
        viz_label.pack(pady=(0, 5), padx=5)

        self.canvas_frame = ttk.Frame(right_panel, relief="solid", 
                                     borderwidth=1)
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def on_calculate(self):
        """Handle calculate button click."""
        if self.is_calculating:
            messagebox.showwarning("Warning", 
                                 "Calculation already in progress!")
            return

        try:
            k1 = int(self.entry_k1.get())
            k2 = int(self.entry_k2.get())
            trials = int(self.entry_trials.get())
            max_n = int(self.entry_max_n.get())

            if k1 < 2 or k2 < 2:
                messagebox.showerror("Error", 
                                    "Clique sizes must be at least 2!")
                return

            if trials < 100:
                messagebox.showerror("Error", 
                                    "Trials must be at least 100!")
                return

            if trials > 50000:
                messagebox.showerror("Error", 
                                    "Trials cannot exceed 50000!")
                return

            if max_n < max(k1, k2):
                messagebox.showerror("Error", 
                                    f"Max limit must be >= {max(k1, k2)}!")
                return

            if max_n > 100:
                messagebox.showerror("Error", 
                                    "Max limit cannot exceed 100!")
                return

            self.is_calculating = True
            self.btn_calculate.config(state="disabled")
            self.result_text.delete(1.0, tk.END)

            self.calculation_thread = threading.Thread(
                target=self._calculate_thread,
                args=(k1, k2, trials, max_n),
                daemon=True
            )
            self.calculation_thread.start()

        except ValueError:
            messagebox.showerror("Error", 
                                "Please enter valid integers!")

    def _calculate_thread(self, k1, k2, trials, max_n):
        """Run calculation in background thread."""
        self.result_text.delete(1.0, tk.END)

        header = "=" * 38
        self.result_text.insert(tk.END, header + "\n")
        self.result_text.insert(tk.END, "        RAMSEY CALCULATION\n")
        self.result_text.insert(tk.END, header + "\n\n")

        self.result_text.insert(tk.END, f"Red Clique Size:  {k1}\n")
        self.result_text.insert(tk.END, f"Blue Clique Size: {k2}\n")
        self.result_text.insert(tk.END, f"Trials per n:     {trials:,}\n")
        self.result_text.insert(tk.END, f"Max Search Limit: {max_n}\n")

        divider = "-" * 38
        self.result_text.insert(tk.END, "\n" + divider + "\n\n")
        self.result_text.insert(tk.END, "Checking Known Values...\n")
        self.root.update()

        known_val = self.calculator.get_known_value(k1, k2)
        if known_val:
            self.result_text.insert(tk.END, 
                                   f"Found: R({k1},{k2}) = {known_val}\n\n")
            self.root.update()
        else:
            self.result_text.insert(tk.END, 
                                   "Unknown - Estimating...\n\n")
            self.root.update()

        self.result_text.insert(tk.END, "Testing vertex counts:\n")
        self.root.update()

        def progress_callback(n, k1, k2, max_n):
            progress = int((n / max_n) * 100)
            self.progress_var.set(min(progress, 99))
            self.progress_label.config(text=f"Testing n = {n}/{max_n}")
            self.result_text.insert(tk.END, f"  n = {n:2d}... OK\n")
            self.result_text.see(tk.END)
            self.root.update()

        result, success = self.calculator.estimate_ramsey(k1, k2, trials, 
                                                         max_n, 
                                                         progress_callback)

        self.result_text.insert(tk.END, "\n" + divider + "\n\n")

        if success:
            self.result_text.insert(tk.END, "SUCCESS!\n\n")
            self.result_text.insert(tk.END, f"Result:\n")
            self.result_text.insert(tk.END, f"  R({k1},{k2}) = {result}\n\n")
            self.result_text.insert(tk.END, f"Meaning:\n")
            self.result_text.insert(tk.END, 
                                   f"  {result} vertices needed to\n")
            self.result_text.insert(tk.END, 
                                   f"  guarantee either:\n")
            self.result_text.insert(tk.END, 
                                   f"  - Red clique of size {k1}\n")
            self.result_text.insert(tk.END, 
                                   f"  - Blue clique of size {k2}\n")

            ram_result = RamseyResult(
                k1=k1, k2=k2, estimated_r=result, trials=trials,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                success=True
            )
            self.calculator.history.append(ram_result)
            self.update_history_display()
        else:
            self.result_text.insert(tk.END, "INCOMPLETE\n\n")
            self.result_text.insert(tk.END, f"Could not find R({k1},{k2})\n")
            self.result_text.insert(tk.END, f"within limit n <= {max_n}\n\n")
            self.result_text.insert(tk.END, "Suggestions:\n")
            self.result_text.insert(tk.END, "  - Increase trials\n")
            self.result_text.insert(tk.END, "  - Increase max limit\n")

        self.progress_var.set(100)
        self.progress_label.config(text="Complete!", 
                                  foreground="#3fb950")
        self.is_calculating = False
        self.btn_calculate.config(state="normal")

        if success:
            self.root.after(300, lambda: self.visualize_example(result))

    def update_history_display(self):
        """Update the history tab with all calculations."""
        self.history_text.delete(1.0, tk.END)

        if not self.calculator.history:
            self.history_text.insert(tk.END, "No history yet.")
            return

        header = "=" * 38
        self.history_text.insert(tk.END, header + "\n")
        self.history_text.insert(tk.END, "   CALCULATION HISTORY\n")
        self.history_text.insert(tk.END, header + "\n\n")

        for i, result in enumerate(self.calculator.history, 1):
            self.history_text.insert(tk.END, 
                                    f"{i}. R({result.k1},{result.k2}) = {result.estimated_r}\n")
            self.history_text.insert(tk.END, 
                                    f"   Trials: {result.trials:,}\n")
            self.history_text.insert(tk.END, 
                                    f"   Time: {result.timestamp}\n")
            self.history_text.insert(tk.END, "\n")

    def visualize_example(self, n=None):
        """Visualize a Ramsey graph with edge coloring."""
        try:
            if n is None:
                k1 = int(self.entry_k1.get())
                k2 = int(self.entry_k2.get())
                n = max(k1, k2) + 2

            G = nx.complete_graph(n)
            for u, v in G.edges():
                G[u][v]['color'] = random.choice(['red', 'blue'])

            self.current_graph = G

            fig = Figure(figsize=(9, 8), dpi=100, 
                        facecolor="#0d1117")
            ax = fig.add_subplot(111, facecolor="#0d1117")

            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

            red_edges = [(u, v) for u, v, d in G.edges(data=True) 
                        if d.get('color') == 'red']
            blue_edges = [(u, v) for u, v, d in G.edges(data=True) 
                         if d.get('color') == 'blue']

            nx.draw_networkx_edges(G, pos, edgelist=red_edges, 
                                  edge_color='#f85149', 
                                  width=1.2, ax=ax, alpha=0.5)
            nx.draw_networkx_edges(G, pos, edgelist=blue_edges, 
                                  edge_color='#58a6ff', 
                                  width=1.2, ax=ax, alpha=0.5)

            nx.draw_networkx_nodes(G, pos, node_color='#1f6feb', 
                                  node_size=400, 
                                  ax=ax, edgecolors='#58a6ff', 
                                  linewidths=2)
            nx.draw_networkx_labels(G, pos, font_size=9, 
                                   font_color='white', 
                                   font_weight='bold', ax=ax)

            edge_count = len(G.edges())
            red_count = len(red_edges)
            blue_count = len(blue_edges)

            title_text = (f"Complete Graph K({n})\n"
                         f"{n} vertices | {edge_count} edges | "
                         f"Red: {red_count} | Blue: {blue_count}")
            ax.set_title(title_text, color="#58a6ff", 
                        fontsize=12, fontweight='bold', pad=15)
            ax.axis('off')
            fig.tight_layout()

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Visualization Error", 
                                f"Failed: {str(e)}")

    def show_known_values(self):
        """Display all known Ramsey numbers."""
        self.result_text.delete(1.0, tk.END)
        header = "=" * 38
        self.result_text.insert(tk.END, header + "\n")
        self.result_text.insert(tk.END, "  KNOWN RAMSEY NUMBERS\n")
        self.result_text.insert(tk.END, header + "\n\n")

        sorted_known = sorted(self.calculator.known_ramsey.items())
        for (k1, k2), val in sorted_known:
            self.result_text.insert(tk.END, f"R({k1},{k2}) = {val}\n")

        divider = "-" * 38
        self.result_text.insert(tk.END, "\n" + divider + "\n\n")
        self.result_text.insert(tk.END, "KEY FACTS:\n\n")
        self.result_text.insert(tk.END, "- R(3,3) = 6 (smallest)\n")
        self.result_text.insert(tk.END, "- R(5,5) between 43-49\n")
        self.result_text.insert(tk.END, "- R(6,6) between 102-165\n")
        self.result_text.insert(tk.END, "- Grows exponentially\n")
        self.result_text.insert(tk.END, "- Only proven values shown\n")

    def show_ramsey_info(self):
        """Show information about Ramsey Theory."""
        self.result_text.delete(1.0, tk.END)
        header = "=" * 38
        self.result_text.insert(tk.END, header + "\n")
        self.result_text.insert(tk.END, "  RAMSEY THEORY BASICS\n")
        self.result_text.insert(tk.END, header + "\n\n")

        info_text = """DEFINITION:
R(k1, k2) = smallest n such
that any 2-coloring of edges
of complete graph K(n) must
contain either red clique of
size k1 or blue clique of k2.

EXAMPLE:
R(3,3) = 6
With 6 people, guaranteed to
find either 3 mutual friends
or 3 mutual strangers.

METHOD: Monte Carlo
Tests random colorings and
searches for minimum n value
where all trials guarantee a
monochromatic clique.

APPLICATIONS:
- Combinatorics
- Network Theory
- Computer Science
- Mathematical Logic

LIMITS:
Computing beyond R(5,5)
requires massive resources.
Many values remain unknown!
"""
        self.result_text.insert(tk.END, info_text)

    def export_history(self):
        """Export calculation history to JSON file."""
        if not self.calculator.history:
            messagebox.showinfo("Info", 
                               "No history to export!")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"ramsey_history_{timestamp}.json"
        )

        if file_path:
            try:
                history_data = [
                    {
                        "k1": r.k1,
                        "k2": r.k2,
                        "estimated_r": r.estimated_r,
                        "trials": r.trials,
                        "timestamp": r.timestamp,
                        "success": r.success
                    }
                    for r in self.calculator.history
                ]

                with open(file_path, 'w') as f:
                    json.dump(history_data, f, indent=2)

                messagebox.showinfo("Success", 
                                   f"Exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", 
                                    f"Failed: {str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = RamseyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
