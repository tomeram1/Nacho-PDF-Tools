import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def get_asset_path(filename):
    # This function finds the image even when it is packed inside the exe
    if "__compiled__" in globals():
        return os.path.join(os.path.dirname(__file__), filename)
    return filename

class PDFMasterApp:
    def __init__(self, root, file_paths):
        self.root = root
        self.root.title("Nacho PDF Help")
        self.root.geometry("680x550")
        # --- Adding the icon to the window ---
        try:
            # This command extracts the icon directly from the currently running exe
            self.root.iconbitmap(sys.executable)
        except Exception:
            pass
        # -------------------------
        
        # ==========================================
        # Screen division: Image on top left, content on the right
        # ==========================================
        main_container = tk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # --- Left area: Logo (anchored to top - anchor="n") ---
        logo_frame = tk.Frame(main_container)
        logo_frame.pack(side=tk.LEFT, anchor="n", padx=(0, 15)) 
        
        # --- Adding the main logo to the window ---
        try:
            logo_path = get_asset_path("NachoLogo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            tk.Label(logo_frame, image=self.logo_img).pack(pady=(15, 0))
        except Exception as e:
            print(f"Logo not found: {e}")
        # ---------------------------------
        
        # --- Right area: File list and buttons ---
        content_frame = tk.Frame(main_container)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        # Creating a dictionary to track the full path of each file
        self.file_map = {os.path.basename(path): path for path in file_paths if path.lower().endswith('.pdf')}
        tk.Label(content_frame, text="Selected Files:", font=("Arial", 12, "bold")).pack(pady=(0, 5), anchor="e")
        
        # File list
        self.listbox = tk.Listbox(content_frame, selectmode=tk.SINGLE, font=("Arial", 11), justify=tk.RIGHT)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for name in self.file_map.keys():
            self.listbox.insert(tk.END, name)
            
        # Management buttons area (Up/Down/Remove/Add)
        manage_frame = tk.Frame(content_frame)
        manage_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(manage_frame, text="⬆ Move Up", command=self.move_up, width=8).pack(side=tk.RIGHT, padx=4)
        tk.Button(manage_frame, text="⬇ Move Down", command=self.move_down, width=8).pack(side=tk.RIGHT, padx=4)
        tk.Button(manage_frame, text="❌ Remove", command=self.remove_file, width=8).pack(side=tk.RIGHT, padx=4)
        tk.Button(manage_frame, text="➕ Add", command=self.add_files, width=8).pack(side=tk.RIGHT, padx=4)
        
        # Action buttons area (Merge / Split)
        action_frame = tk.Frame(content_frame)
        action_frame.pack(fill=tk.X, pady=15)
        
        tk.Button(action_frame, text="✅ Merge All Files", command=self.merge_files, height=2, bg="#90EE90", font=("Arial", 11, "bold")).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
        tk.Button(action_frame, text="✂️ Extract Pages from Selected", command=self.open_split_window, height=2, bg="#ADD8E6", font=("Arial", 11, "bold")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Copyright signature at the bottom of the window
        tk.Label(root, text="Developed by Tomer Amran © 2026", font=("Arial", 9), fg="gray").pack(side=tk.BOTTOM, pady=10)
        
    def move_up(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == 0: return
        idx = selected[0]
        val = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx - 1, val)
        self.listbox.selection_set(idx - 1)

    def move_down(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == self.listbox.size() - 1: return
        idx = selected[0]
        val = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx + 1, val)
        self.listbox.selection_set(idx + 1)

    def remove_file(self):
        selected = self.listbox.curselection()
        if not selected: return
        idx = selected[0]
        self.listbox.delete(idx)
        if self.listbox.size() > 0:
            self.listbox.selection_set(min(idx, self.listbox.size() - 1))

    # --- Merge Function ---
    def merge_files(self):
        ordered_names = self.listbox.get(0, tk.END)
        if len(ordered_names) < 2:
            messagebox.showwarning("Error", "At least 2 files are required in the list to perform a merge.")
            return
            
        ordered_paths = [self.file_map[name] for name in ordered_names]
        initial_dir = os.path.dirname(ordered_paths[0])
        
        output_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile="Merged_File",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Merged File"
        )
        
        if not output_path: return
            
        try:
            merger = PdfMerger()
            for path in ordered_paths:
                merger.append(path)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Success", f"Files merged successfully!\nSaved in:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during merge:\n{e}")

    # --- Split Function ---
    def open_split_window(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please click and select one file from the list to split.")
            return
            
        file_name = self.listbox.get(selected[0])
        file_path = self.file_map[file_name]
        
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read the file:\n{e}")
            return

        # Creating a new popup window (Toplevel) for extraction
        split_win = tk.Toplevel(self.root)
        split_win.title("Extract Pages")
        split_win.geometry("400x250")
        split_win.grab_set() # Locks the focus to this window
        
        tk.Label(split_win, text=f"File: {file_name}", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        tk.Label(split_win, text=f"Total pages in this file: {total_pages}", font=("Arial", 10)).pack()
        
        tk.Label(split_win, text="Enter pages (e.g., 1-3, 5, 8-10):", font=("Arial", 11)).pack(pady=(15, 5))
        pages_entry = tk.Entry(split_win, font=("Arial", 12), justify=tk.CENTER, width=25)
        pages_entry.pack()
        
        def perform_split():
            pages_str = pages_entry.get()
            if not pages_str: return
            
            try:
                pages_to_extract = set()
                parts = pages_str.replace(" ", "").split(",")
                for part in parts:
                    if not part: continue
                    if "-" in part:
                        start, end = part.split("-")
                        for p in range(int(start), int(end) + 1):
                            pages_to_extract.add(p - 1)
                    else:
                        pages_to_extract.add(int(part) - 1)
                        
                valid_pages = sorted([p for p in pages_to_extract if 0 <= p < total_pages])
            except ValueError:
                messagebox.showerror("Error", "Invalid format. Use numbers and commas.", parent=split_win)
                return
                
            if not valid_pages:
                messagebox.showwarning("Error", "No valid pages found.", parent=split_win)
                return
                
            output_path = filedialog.asksaveasfilename(
                initialdir=os.path.dirname(file_path),
                initialfile=f"Split_{file_name}",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                title="Save split file as...",
                parent=split_win
            )
            
            if not output_path: return
                
            try:
                writer = PdfWriter()
                for p_num in valid_pages:
                    writer.add_page(reader.pages[p_num])
                with open(output_path, "wb") as out_pdf:
                    writer.write(out_pdf)
                messagebox.showinfo("Success", "Pages extracted successfully!", parent=split_win)
                split_win.destroy() # Closes the split window upon completion
            except Exception as e:
                messagebox.showerror("Error", f"Error during split:\n{e}", parent=split_win)
                
        tk.Button(split_win, text="✂️ Extract and Save", command=perform_split, bg="#ADD8E6", font=("Arial", 10, "bold")).pack(pady=15)
        
    def add_files(self):
        # 1. Opening Windows dialog to select multiple files (PDF files only)
        new_files = filedialog.askopenfilenames(
            title="Select PDF files to add",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        # 2. Iterating over each file selected by the user
        for path in new_files:
            name = os.path.basename(path)
            
            # 3. Smart condition: Add only if it is a PDF and the name isn't already in our dictionary
            if name not in self.file_map and path.lower().endswith('.pdf'):
                self.file_map[name] = path           # Add to background memory
                self.listbox.insert(tk.END, name)    # Add visually to the listbox in the window
                
if __name__ == "__main__":
    files = sys.argv[1:]
    root = tk.Tk()
    app = PDFMasterApp(root, files)
    root.mainloop()