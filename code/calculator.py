import tkinter as tk
from tkinter import ttk,messagebox
import networkx as nx
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import combinations
import threading
import time
from dataclasses import dataclass

@dataclass
class graph_statistics:
    """Store graph analysis statistics."""
    vertices: int
    edges: int
    red_edges: int
    blue_edges: int
    cliques_found: dict

class ramsey_calculator:
    """Core calculator for Ramsey numbers using Monte Carlo method."""
    def __init__(self):
        self.cancel_flag=False
    def has_monochromatic_clique(self,G,k,color):
        """Check if graph G contains a monochromatic clique of size k."""
        nodes=list(G.nodes)
        if k > len(nodes):
            return False
        if k == 1:
            return True
        for subset in combinations(nodes,k):
            sub=G.subgraph(subset)
            edges=list(sub.edges())
            if not edges and k <= 1:
                continue
            if len(edges) == k * (k - 1) // 2:
                if all(G[u][v]['color'] == color for u,v in edges):
                    return True
        return False
    def check_ramsey(self,n,k1,k2,trials):
        """Monte Carlo estimation: check if R(k1,k2) <= n."""
        for trial in range(trials):
            if self.cancel_flag:
                return False
            G=nx.complete_graph(n)
            for u,v in G.edges():
                G[u][v]['color']=random.choice(['red','blue'])
            has_red=self.has_monochromatic_clique(G,k1,'red')
            has_blue=self.has_monochromatic_clique(G,k2,'blue')
            if not has_red and not has_blue:
                return False
        return True
    def estimate_ramsey(self,k1,k2,trials,max_n=50,progress_callback=None):
        """Estimate Ramsey number using binary search style approach."""
        start_n=max(k1,k2)
        for n in range(start_n,max_n + 1):
            if self.cancel_flag:
                return None,False
            if progress_callback:
                progress_callback(n,max_n)
            if self.check_ramsey(n,k1,k2,trials):
                return n,True
        return None,False
    def get_graph_statistics(self,G):
        """Extract statistics from a graph."""
        red_edges=sum(1 for u,v,d in G.edges(data=True) if d.get('color') == 'red')
        blue_edges=sum(1 for u,v,d in G.edges(data=True) if d.get('color') == 'blue')
        return graph_statistics(
            vertices=G.number_of_nodes(),
            edges=G.number_of_edges(),
            red_edges=red_edges,
            blue_edges=blue_edges,
            cliques_found={}
        )
class graph_visualizer:
    """Handles graph visualization."""
    def __init__(self,canvas_frame,bg_color="#0a0e27"):
        self.canvas_frame=canvas_frame
        self.bg_color=bg_color
        self.fig=None
        self.canvas=None
    def create_static_visualization(self,G):
        """Create static graph visualization."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        pos=nx.spring_layout(G,k=2.5,iterations=50,seed=42)
        self.fig=Figure(figsize=(8,6),dpi=100,facecolor=self.bg_color)
        ax=self.fig.add_subplot(111,facecolor=self.bg_color)
        red_edges=[(u,v) for u,v,d in G.edges(data=True) if d.get('color') == 'red']
        blue_edges=[(u,v) for u,v,d in G.edges(data=True) if d.get('color') == 'blue']
        nx.draw_networkx_edges(G,pos,edgelist=red_edges,
                               edge_color='#ff4757',width=2.5,ax=ax,alpha=0.8)
        nx.draw_networkx_edges(G,pos,edgelist=blue_edges,
                               edge_color='#00d9ff',width=2.5,ax=ax,alpha=0.8)
        nx.draw_networkx_nodes(G,pos,node_color='#1a2847',
                               node_size=600,ax=ax,
                               edgecolors='#00d9ff',linewidths=3)
        nx.draw_networkx_labels(G,pos,font_size=11,
                                font_color='#ffffff',
                                font_weight='bold',ax=ax)
        ax.axis('off')
        self.fig.tight_layout()
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both",expand=True)
        return self.fig
class ramsey_gui:
    """Main GUI application for Ramsey Number Calculator."""
    def __init__(self,root):
        self.root=root
        self.root.title("Ramsey Number Calculator")
        self.root.geometry("1700x900")
        self.root.configure(bg="#0a0e27")
        self.calculator=ramsey_calculator()
        self.visualizer=graph_visualizer(None)
        self.current_graph=None
        self.is_calculating=False
        self.calculation_thread=None
        self.setup_styles()
        self.create_widgets()
    def setup_styles(self):
        """Configure ttk styles for premium dark theme."""
        style=ttk.Style()
        style.theme_use('clam')
        bg_color="#0a0e27"
        fg_color="#e8eef7"
        accent_color="#00d9ff"
        button_bg="#1a2847"
        style.configure("TFrame",background=bg_color)
        style.configure("TLabel",background=bg_color,foreground=fg_color,
                        font=("Segoe UI",10))
        style.configure("Title.TLabel",background=bg_color,foreground=accent_color,
                        font=("Segoe UI",24,"bold"))
        style.configure("Card.TFrame",background="#1a2847",relief="flat")
        style.configure("TEntry",font=("Segoe UI",12),fieldbackground="#1a2847",
                        foreground=fg_color,borderwidth=0)
        style.configure("TButton",font=("Segoe UI",11,"bold"),background=button_bg,
                        foreground=fg_color,borderwidth=0,padding=12)
        style.map("TButton",
                  background=[("active",accent_color),("pressed","#0099cc")],
                  foreground=[("active","#0a0e27"),("pressed","#0a0e27")])
    def create_widgets(self):
        """Create all GUI widgets with modern card-based layout."""
        main_container=ttk.Frame(self.root)
        main_container.pack(fill="both",expand=True,padx=20,pady=20)
        header_frame=ttk.Frame(main_container)
        header_frame.pack(fill="x",pady=(0,20))
        title=ttk.Label(header_frame,
                          text="RAMSEY NUMBER CALCULATOR",
                          style="Title.TLabel")
        title.pack()
        content_frame=ttk.Frame(main_container)
        content_frame.pack(fill="both",expand=True)
        left_panel=ttk.Frame(content_frame,width=480)
        left_panel.pack(side="left",fill="both",expand=False,padx=(0,15))
        left_panel.pack_propagate(False)
        self.left_container=ttk.Frame(left_panel)
        self.left_container.pack(fill="both",expand=True)
        self.input_section=ttk.Frame(self.left_container)
        self.input_section.pack(fill="both",expand=True)
        input_card=ttk.Frame(self.input_section,style="Card.TFrame",relief="flat",borderwidth=0)
        input_card.pack(fill="x",pady=(0,15))
        card_padding=ttk.Frame(input_card,style="Card.TFrame")
        card_padding.pack(fill="both",expand=True,padx=20,pady=20)
        card_title=tk.Label(card_padding,text="Configuration",
                              bg="#1a2847",fg="#00d9ff",
                              font=("Segoe UI",14,"bold"))
        card_title.pack(anchor="w",pady=(0,15))
        fields_frame=ttk.Frame(card_padding,style="Card.TFrame")
        fields_frame.pack(fill="x")
        input_configs=[
            ("Red Clique Size (k1)","3","entry_k1"),
            ("Blue Clique Size (k2)","3","entry_k2"),
            ("Monte Carlo Trials","5000","entry_trials"),
            ("Max Vertices (n)","20","entry_max_n")
        ]
        for i,(label_text,default_val,attr_name) in enumerate(input_configs):
            field_frame=ttk.Frame(fields_frame,style="Card.TFrame")
            field_frame.pack(fill="x",pady=8)
            label=tk.Label(field_frame,text=label_text,
                            bg="#1a2847",fg="#a0aaf0",
                            font=("Segoe UI",10))
            label.pack(anchor="w",pady=(0,5))
            entry=ttk.Entry(field_frame,font=("Segoe UI",12))
            entry.insert(0,default_val)
            entry.pack(fill="x",ipady=8)
            setattr(self,attr_name,entry)
        btn_frame=ttk.Frame(card_padding,style="Card.TFrame")
        btn_frame.pack(fill="x",pady=(20,0))
        self.btn_calculate=ttk.Button(btn_frame,
                                        text="START ESTIMATION",
                                        command=self.on_calculate)
        self.btn_calculate.pack(fill="x",ipady=5)
        status_card=ttk.Frame(self.input_section,style="Card.TFrame")
        status_card.pack(fill="x",pady=(0,0))
        status_padding=ttk.Frame(status_card,style="Card.TFrame")
        status_padding.pack(fill="both",expand=True,padx=20,pady=15)
        self.status_label=tk.Label(status_padding,
                                     text="● Ready",
                                     bg="#1a2847",fg="#00ff99",
                                     font=("Segoe UI",12,"bold"))
        self.status_label.pack()
        self.status_detail=tk.Label(status_padding,
                                      text="",
                                      bg="#1a2847",fg="#a0aaf0",
                                      font=("Segoe UI",9))
        self.status_detail.pack(pady=(5,0))
        self.results_section=ttk.Frame(self.left_container)
        results_card=ttk.Frame(self.results_section,style="Card.TFrame")
        results_card.pack(fill="both",expand=True)
        results_padding=tk.Frame(results_card,bg="#1a2847")
        results_padding.pack(fill="both",expand=True,padx=20,pady=20)
        results_title=tk.Label(results_padding,text="✓ ESTIMATION COMPLETE",
                                bg="#1a2847",fg="#00ff99",
                                font=("Segoe UI",16,"bold"))
        results_title.pack(anchor="w",pady=(0,15))
        self.result_value_label_panel=tk.Label(results_padding,
                                                 text="",
                                                 bg="#1a2847",fg="#00ff99",
                                                 font=("Segoe UI",44,"bold"))
        self.result_value_label_panel.pack(pady=(0,15))
        sep_canvas=tk.Canvas(results_padding,height=2,bg="#00d9ff",highlightthickness=0)
        sep_canvas.pack(fill="x",pady=(0,15))
        stats_label=tk.Label(results_padding,text="Graph Statistics",
                              bg="#1a2847",fg="#00d9ff",
                              font=("Segoe UI",11,"bold"))
        stats_label.pack(anchor="w",pady=(0,10))
        self.stats_container=tk.Frame(results_padding,bg="#1a2847")
        self.stats_container.pack(fill="x",pady=(0,20))
        back_btn=tk.Button(results_padding,
                            text="← Back to Settings",
                            bg="#1a2847",fg="#00d9ff",
                            font=("Segoe UI",10,"bold"),
                            relief="flat",
                            bd=0,
                            padx=20,
                            pady=8,
                            cursor="hand2",
                            activebackground="#00d9ff",
                            activeforeground="#0a0e27",
                            command=self.show_input_section)
        back_btn.pack(pady=(10,0))
        right_panel=ttk.Frame(content_frame)
        right_panel.pack(side="right",fill="both",expand=True)
        graph_card=ttk.Frame(right_panel,style="Card.TFrame")
        graph_card.pack(fill="both",expand=True)
        graph_padding=ttk.Frame(graph_card,style="Card.TFrame")
        graph_padding.pack(fill="both",expand=True,padx=20,pady=20)
        graph_title=tk.Label(graph_padding,text="Graph Visualization",
                              bg="#1a2847",fg="#00d9ff",
                              font=("Segoe UI",14,"bold"))
        graph_title.pack(anchor="w",pady=(0,15))
        self.canvas_frame=ttk.Frame(graph_padding,style="Card.TFrame")
        self.canvas_frame.pack(fill="both",expand=True,pady=(0,15))
        self.visualizer.canvas_frame=self.canvas_frame
        self.result_display_frame=tk.Frame(graph_padding,bg="#1a2847")
        self.result_display_frame.pack(fill="x")
        self.result_value_label_graph=tk.Label(self.result_display_frame,
                                                 text="Awaiting calculation...",
                                                 bg="#1a2847",fg="#888888",
                                                 font=("Segoe UI",32,"bold"),
                                                 pady=15)
        self.result_value_label_graph.pack()
    def show_input_section(self):
        """Switch to input section."""
        self.results_section.pack_forget()
        self.input_section.pack(fill="both",expand=True)
    def show_results_section(self):
        """Switch to results section."""
        self.input_section.pack_forget()
        self.results_section.pack(fill="both",expand=True)
    def on_calculate(self):
        """Handle calculation start."""
        if self.is_calculating:
            messagebox.showwarning("Warning","Calculation already in progress!")
            return
        try:
            k1=int(self.entry_k1.get())
            k2=int(self.entry_k2.get())
            trials=int(self.entry_trials.get())
            max_n=int(self.entry_max_n.get())
            if k1 < 2 or k2 < 2:
                messagebox.showerror("Error","Clique sizes must be >= 2!")
                return
            if trials < 100 or trials > 100000:
                messagebox.showerror("Error","Trials must be 100-100000!")
                return
            if max_n < max(k1,k2) or max_n > 100:
                messagebox.showerror("Error",f"Max n must be {max(k1,k2)}-100!")
                return
            self.is_calculating=True
            self.btn_calculate.config(state="disabled")
            self.status_label.config(text="● Computing...",fg="#ffaa00")
            self.status_detail.config(text="Please wait...")
            self.result_value_label_graph.config(text="Computing...",fg="#ffaa00")
            self.calculation_thread=threading.Thread(
                target=self._calculate_thread,
                args=(k1,k2,trials,max_n),
                daemon=True
            )
            self.calculation_thread.start()
        except ValueError:
            messagebox.showerror("Error","Please enter valid integers!")
    def _calculate_thread(self,k1,k2,trials,max_n):
        """Run calculation in background thread."""
        start_time=time.time()
        def progress_callback(n,max_n):
            elapsed=time.time() - start_time
            progress_percent=int((n / max_n) * 100)
            self.status_detail.config(text=f"Testing n={n}/{max_n} ({progress_percent}%)")
            self.root.update()
        result,success=self.calculator.estimate_ramsey(k1,k2,trials,
                                                          max_n,
                                                          progress_callback)
        elapsed=time.time() - start_time
        if success:
            G=nx.complete_graph(result)
            for u,v in G.edges():
                G[u][v]['color']=random.choice(['red','blue'])
            self.current_graph=G
            stats=self.calculator.get_graph_statistics(G)
            self.root.after(100,lambda: self.update_displays(k1,k2,result,stats,elapsed))
            self.status_label.config(text="● Complete",fg="#00ff99")
            self.status_detail.config(text=f"R({k1},{k2})={result}")
        else:
            self.result_value_label_graph.config(
                text=f"R({k1},{k2}) > {max_n}",
                fg="#ff6b6b",
                font=("Segoe UI",28,"bold")
            )
            self.status_label.config(text="● Incomplete",fg="#ff6b6b")
            self.status_detail.config(text=f"Tested up to n={max_n}")
        self.is_calculating=False
        self.btn_calculate.config(state="normal")
        self.calculator.cancel_flag=False
    def update_displays(self,k1,k2,result,stats,elapsed):
        """Update both left and right panel displays."""
        self.visualizer.create_static_visualization(self.current_graph)
        self.result_value_label_graph.config(
            text=f"R({k1},{k2})={result}",
            fg="#00ff99",
            font=("Segoe UI",36,"bold")
        )
        self.result_value_label_panel.config(
            text=f"R({k1},{k2})={result}"
        )
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        stats_items=[
            ("Vertices",str(stats.vertices)),
            ("Total Edges",str(stats.edges)),
            ("Red Edges",str(stats.red_edges)),
            ("Blue Edges",str(stats.blue_edges)),
            ("Computation Time",f"{elapsed:.2f}s"),
            ("Graph Density",f"{2*stats.edges/(stats.vertices*(stats.vertices-1)):.4f}")
        ]
        for label_text,value_text in stats_items:
            item_frame=tk.Frame(self.stats_container,bg="#1a2847")
            item_frame.pack(fill="x",pady=5)
            label=tk.Label(item_frame,
                            text=label_text + ":",
                            bg="#1a2847",fg="#a0aaf0",
                            font=("Segoe UI",10),
                            width=18,
                            anchor="w")
            label.pack(side="left")
            value=tk.Label(item_frame,
                            text=value_text,
                            bg="#1a2847",fg="#00d9ff",
                            font=("Segoe UI",10,"bold"),
                            anchor="w")
            value.pack(side="left",padx=(10,0))
        self.show_results_section()

def main():
    """Main entry point for the application."""
    root=tk.Tk()
    app=ramsey_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()