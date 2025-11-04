import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import random

def has_monochromatic_clique(G, k, color):
    """Check if graph G contains a monochromatic clique of size k for given color."""
    nodes = list(G.nodes)
    from itertools import combinations
    for subset in combinations(nodes, k):
        sub = G.subgraph(subset)
        if all(G[u][v]['color'] == color for u, v in sub.edges()):
            return True
    return False

def check_ramsey(n, k1, k2, trials):
    """Monte Carlo estimation: check if R(k1, k2) ≤ n."""
    for _ in range(trials):
        G = nx.complete_graph(n)
        for u, v in G.edges():
            G[u][v]['color'] = random.choice(['red', 'blue'])
        if not has_monochromatic_clique(G, k1, 'red') and not has_monochromatic_clique(G, k2, 'blue'):
            return False
    return True

def estimate_ramsey():
    try:
        k1 = int(entry_k1.get())
        k2 = int(entry_k2.get())
        trials = int(entry_trials.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers!")
        return
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Estimating R({k1},{k2})...\n\n")

    found = False
    for n in range(2, 20):  # limit for speed
        output_text.insert(tk.END, f"Testing n = {n}...\n")
        root.update()
        if check_ramsey(n, k1, k2, trials):
            output_text.insert(tk.END, f"\n✅ Estimated Ramsey Number R({k1},{k2}) ≈ {n}\n")
            found = True
            break
    
    if not found:
        output_text.insert(tk.END, "\n❌ Could not find an upper bound within n ≤ 20\n")

# === GUI Setup ===
root = tk.Tk()
root.title("Ramsey Number Calculator")
root.geometry("600x500")
root.configure(bg="#20232a")

style = ttk.Style()
style.configure("TLabel", background="#20232a", foreground="white", font=("Consolas", 12))
style.configure("TEntry", font=("Consolas", 12))
style.configure("TButton", font=("Consolas", 12, "bold"), padding=6)

frame = ttk.Frame(root)
frame.pack(pady=20)

ttk.Label(frame, text="Clique size 1 (red):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_k1 = ttk.Entry(frame, width=10)
entry_k1.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Clique size 2 (blue):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_k2 = ttk.Entry(frame, width=10)
entry_k2.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Monte Carlo Trials:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_trials = ttk.Entry(frame, width=10)
entry_trials.insert(0, "1000")
entry_trials.grid(row=2, column=1, padx=5, pady=5)

btn = ttk.Button(root, text="Estimate Ramsey Number", command=estimate_ramsey)
btn.pack(pady=10)

output_text = tk.Text(root, height=15, width=70, bg="#282c34", fg="#00ff99", font=("Consolas", 11))
output_text.pack(padx=10, pady=10)

root.mainloop()
