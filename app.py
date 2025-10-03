import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ModernDataCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner")
        self.root.geometry("850x600")
        self.root.configure(bg="#f2f2f2")
        self.root.attributes("-alpha", 0.95)  # translucent
        self.root.resizable(False, False)

        self.file_path = None
        self.df = None
        self.cleaned_df = None  # store cleaned version

        # Title
        tk.Label(root, text="Automated Data Cleaner", bg="#f2f2f2", fg="#333",
                 font=("Helvetica", 18, "bold")).pack(pady=10)

        # File Selection
        tk.Button(root, text="📂 Load File", command=self.load_file,
                  bg="#fff", fg="#333", relief="groove", bd=2, font=("Helvetica", 12),
                  activebackground="#ddd").pack(pady=5)

        # Cleaning Options
        options_frame = tk.LabelFrame(root, text="Cleaning Options", bg="#f2f2f2", font=("Helvetica", 12))
        options_frame.pack(pady=10, padx=10, fill="x")

        self.remove_dupes_var = tk.BooleanVar(value=True)
        self.fill_missing_var = tk.BooleanVar(value=True)
        self.trim_text_var = tk.BooleanVar(value=True)
        self.standardize_cols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(options_frame, text="Remove Duplicates (ignore whitespace/case)", variable=self.remove_dupes_var,
                       bg="#f2f2f2").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(options_frame, text="Fill Missing Values (median for numeric, empty for text)", variable=self.fill_missing_var,
                       bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(options_frame, text="Trim Text Columns", variable=self.trim_text_var,
                       bg="#f2f2f2").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Checkbutton(options_frame, text="Standardize Column Names", variable=self.standardize_cols_var,
                       bg="#f2f2f2").grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#f2f2f2")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🧹 Clean Data", command=self.clean_data_action,
                  bg="#fff", fg="#333", relief="groove", bd=2, font=("Helvetica", 12),
                  activebackground="#ddd").grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="👁 Preview Cleaned Data", command=self.preview_data,
                  bg="#fff", fg="#333", relief="groove", bd=2, font=("Helvetica", 12),
                  activebackground="#ddd").grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="💾 Save Cleaned File", command=self.save_data,
                  bg="#fff", fg="#333", relief="groove", bd=2, font=("Helvetica", 12),
                  activebackground="#ddd").grid(row=0, column=2, padx=10)

        # Table Frame
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = None

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if self.file_path:
            try:
                # Read first row to detect headers
                if self.file_path.endswith(".xlsx"):
                    temp_df = pd.read_excel(self.file_path, header=None)
                else:
                    temp_df = pd.read_csv(self.file_path, header=None)

                first_row = temp_df.iloc[0]
                if first_row.apply(lambda x: isinstance(x, str)).sum() >= len(first_row)/2:
                    header = 0  # first row looks like headers
                else:
                    header = None

                if self.file_path.endswith(".xlsx"):
                    self.df = pd.read_excel(self.file_path, header=header)
                else:
                    self.df = pd.read_csv(self.file_path, header=header)

                # Assign default headers if none detected
                if header is None:
                    self.df.columns = [f"column_{i+1}" for i in range(self.df.shape[1])]

                messagebox.showinfo("File Loaded", f"Loaded file: {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def clean_data(self):
        if self.df is None:
            return None
        df = self.df.copy()

        # Trim text
        if self.trim_text_var.get():
            text_cols = df.select_dtypes(include='object').columns
            for col in text_cols:
                df[col] = df[col].astype(str).str.strip()

        # Standardize column names
        if self.standardize_cols_var.get():
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        # Fill missing values safely
        if self.fill_missing_var.get():
            numeric_cols = df.select_dtypes(include='number').columns
            for col in numeric_cols:
                df[col] = df[col].fillna(df[col].median())
            text_cols = df.select_dtypes(include='object').columns
            for col in text_cols:
                df[col] = df[col].fillna("")

        # Remove duplicates
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
            self.tree.column(col, width=120)

        for _, row in self.cleaned_df.head(50).iterrows():
            self.tree.insert("", "end", values=list(row))

    def save_data(self):
        if self.cleaned_df is None:
            messagebox.showwarning("No Data", "Please clean the data first.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
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
