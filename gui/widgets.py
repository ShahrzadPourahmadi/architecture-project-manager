import tkinter as tk
from tkinter import ttk


def make_tree(parent, columns, height=8):
    """ساخت Treeview با اسکرول. columns: [(key, title, width), ...]"""
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns],
                        show="headings", height=height, selectmode="browse")
    for key, title, width in columns:
        tree.heading(key, text=title)
        tree.column(key, width=width, anchor="center")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return frame, tree


def labeled_entry(parent, text, row, col=0, width=20):
    ttk.Label(parent, text=text).grid(row=row, column=col, padx=4, pady=3, sticky="e")
    var = tk.StringVar()
    ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=col + 1, padx=4, pady=3)
    return var


def fmt_money(x):
    return f"{x:,.0f}"


def selected_id(tree):
    sel = tree.selection()
    return sel[0] if sel else None
