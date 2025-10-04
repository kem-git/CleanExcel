import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ModernDataCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner")
        self.root.geometry("1050x700")  # upscale window
        self.root.configure(bg="#000000")  # True black
        self.root.resizable(False, False)

        self.file_path = None
        self.df = None
        self.cleaned_df = None

        # -------- TITLE --------
        tk.Label(root, text="Automated Data Cleaner",
                 bg="#000000", fg="#FFFFFF",
                 font=("Helvetica", 24, "bold")).pack(pady=20)

        # -------- FILE SELECTION --------
        self.load_btn = tk.Button(root, text="📂 Load File",
                                  command=self.load_file,
                                  font=("Helvetica", 14, "bold"),
                                  padx=22, pady=12,
                                  relief="flat", bd=0,
                                  bg="#1C1C1C", fg="#FFFFFF",
                                  activebackground="#2C2C2C", activeforeground="#FFFFFF")
        self.load_btn.pack(pady=15)

        self.make_hover(self.load_btn)

        # -------- CLEANING OPTIONS --------
        options_frame = tk.LabelFrame(root, text=" Cleaning Options ",
                                      bg="#0D0D0D", fg="#FFFFFF",
                                      font=("Helvetica", 14, "bold"),
                                      bd=2, relief="groove", padx=20, pady=12)
        options_frame.pack(pady=20, padx=20, fill="x")

        self.remove_dupes_var = tk.BooleanVar(value=True)
        self.fill_missing_var = tk.BooleanVar(value=True)
        self.trim_text_var = tk.BooleanVar(value=True)
        self.standardize_cols_var = tk.BooleanVar(value=True)

        opts = [
            ("Remove Duplicates (ignore whitespace/case)", self.remove_dupes_var, 0, 0),
            ("Fill Missing Values (median for numeric, empty for text)", self.fill_missing_var, 1, 0),
            ("Trim Text Columns", self.trim_text_var, 0, 1),
            ("Standardize Column Names", self.standardize_cols_var, 1, 1)
        ]

        for text, var, r, c in opts:
            chk = tk.Checkbutton(options_frame, text=text, variable=var,
                                 bg="#0D0D0D", fg="#FFFFFF", selectcolor="#1C1C1C",
                                 activebackground="#1C1C1C",
                                 font=("Helvetica", 13))
            chk.grid(row=r, column=c, sticky="w", padx=15, pady=10)

        # -------- BUTTON FRAME --------
        btn_frame = tk.Frame(root, bg="#000000")
        btn_frame.pack(pady=20)

        self.clean_btn = self.make_button(btn_frame, "🧹 Clean Data", self.clean_data_action, 0, 0)
        self.preview_btn = self.make_button(btn_frame, "👁 Preview Cleaned Data", self.preview_data, 0, 1)
        self.save_btn = self.make_button(btn_frame, "💾 Save Cleaned File", self.save_data, 0, 2)

        # -------- TABLE FRAME --------
        self.table_frame = tk.Frame(root, bg="#000000")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree = None

        # -------- STYLES --------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#0D0D0D",
                        foreground="white",
                        fieldbackground="#0D0D0D",
                        rowheight=32,
                        font=("Helvetica", 12))
        style.configure("Treeview.Heading",
                        background="#1C1C1C",
                        foreground="white",
                        font=("Helvetica", 13, "bold"))
        style.map("Treeview",
                  background=[("selected", "#333333")],
                  foreground=[("selected", "#FFFFFF")])

    # -------- HOVER EFFECTS --------
    def make_button(self, parent, text, command, row, col):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Helvetica", 14, "bold"),
                        padx=22, pady=12,
                        relief="flat", bd=0,
                        bg="#1C1C1C", fg="#FFFFFF",
                        activebackground="#2C2C2C", activeforeground="#FFFFFF")
        btn.grid(row=row, column=col, padx=20)
        self.make_hover(btn)
        return btn

    def make_hover(self, widget):
        def on_enter(e):
            widget["bg"] = "#2C2C2C"
        def on_leave(e):
            widget["bg"] = "#1C1C1C"
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # -------- FILE LOADING --------
    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv")
        ])
        if self.file_path:
            try:
                if self.file_path.endswith(".xlsx"):
                    temp_df = pd.read_excel(self.file_path, header=None)
                else:
                    temp_df = pd.read_csv(self.file_path, header=None)

                first_row = temp_df.iloc[0]
                if first_row.apply(lambda x: isinstance(x, str)).sum() >= len(first_row) / 2:
                    header = 0
                else:
                    header = None

                if self.file_path.endswith(".xlsx"):
                    self.df = pd.read_excel(self.file_path, header=header)
                else:
                    self.df = pd.read_csv(self.file_path, header=header)

                if header is None:
                    self.df.columns = [f"column_{i+1}" for i in range(self.df.shape[1])]

                messagebox.showinfo("File Loaded", f"Loaded file: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    # -------- CLEANING --------
    def clean_data(self):
        if self.df is None:
            return None
        df = self.df.copy()

        if self.trim_text_var.get():
            text_cols = df.select_dtypes(include='object').columns
            for col in text_cols:
                df[col] = df[col].astype(str).str.strip()

        if self.standardize_cols_var.get():
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        if self.fill_missing_var.get():
            numeric_cols = df.select_dtypes(include='number').columns
            for col in numeric_cols:
                df[col] = df[col].fillna(df[col].median())
            text_cols = df.select_dtypes(include='object').columns
            for col in text_cols:
                df[col] = df[col].fillna("")

        if self.remove_dupes_var.get():
            df = self.remove_duplicates(df)

        return df

    def clean_data_action(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a file first.")
            return
        self.cleaned_df = self.clean_data()
        messagebox.showinfo("Cleaned", "Data cleaned successfully! Preview or save now.")

    @staticmethod
    def remove_duplicates(df):
        df_copy = df.copy()
        for col in df_copy.select_dtypes(include='object').columns:
            df_copy[col] = df_copy[col].astype(str).str.strip().str.lower()
        df_clean = df_copy.drop_duplicates(ignore_index=True)
        return df_clean

    # -------- PREVIEW --------
    def preview_data(self):
        if self.cleaned_df is None:
            messagebox.showwarning("Not Cleaned", "Please clean the data first.")
            return

        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(self.table_frame)
        self.tree.pack(fill="both", expand=True)

        self.tree["columns"] = list(self.cleaned_df.columns)
        self.tree["show"] = "headings"
        for col in self.cleaned_df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160)

        for _, row in self.cleaned_df.head(50).iterrows():
            self.tree.insert("", "end", values=list(row))

    # -------- SAVE --------
    def save_data(self):
        if self.cleaned_df is None:
            messagebox.showwarning("No Data", "Please clean the data first.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("CSV files", "*.csv")])
        if save_path:
            try:
                if save_path.endswith(".xlsx"):
                    self.cleaned_df.to_excel(save_path, index=False)
                else:
                    self.cleaned_df.to_csv(save_path, index=False)
                messagebox.showinfo("Success", f"Cleaned file saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDataCleaner(root)
    root.mainloop()
