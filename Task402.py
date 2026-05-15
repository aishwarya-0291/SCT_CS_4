import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime

class ModernTextWorkspace:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Text Workspace & Input Monitor")
        self.root.geometry("850x600")
        self.root.minimum_size = (600, 400)
        
        # Configure overall window theme color
        self.root.config(bg="#1e1e24")

        # ---------- TTK STYLING ----------
        self.style = ttk.Style()
        self.theme_use = self.style.theme_use("clam")
        
        self.style.configure("Vertical.TScrollbar", gripcount=0, background="#2a2a35", troughcolor="#1e1e24", bordercolor="#1e1e24", arrowcolor="white")

        # ---------- TOP NAVIGATION HEADER ----------
        self.header = tk.Frame(root, bg="#252530", height=65)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False)

        self.title_icon = tk.Label(
            self.header, 
            text=" 📝  Workspace Monitor", 
            bg="#252530", 
            fg="#ffffff", 
            font=("Segoe UI", 14, "bold")
        )
        self.title_icon.pack(side=tk.LEFT, padx=20)

        # ---------- CONTROL ACTION PANEL (TOOL BAR) ----------
        self.toolbar = tk.Frame(root, bg="#1a1a20", height=50)
        self.toolbar.pack(fill=tk.X)
        self.toolbar.pack_propagate(False)

        def create_tool_btn(parent, text, color, command):
            return tk.Button(
                parent, text=text, command=command, bg=color, fg="white",
                activebackground=color, activeforeground="white",
                font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
                padx=15, cursor="hand2", bd=0
            )

        self.save_btn = create_tool_btn(self.toolbar, "💾  Save Workspace", "#2e7d32", self.save_to_file)
        self.save_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.word_btn = create_tool_btn(self.toolbar, "📊  Statistics", "#1565c0", self.show_word_count)
        self.word_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.clear_btn = create_tool_btn(self.toolbar, "🗑️  Clear Editor", "#c62828", self.clear_text)
        self.clear_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # ---------- MAIN WORKSPACE SPLIT FRAME ----------
        self.workspace = tk.Frame(root, bg="#1e1e24")
        self.workspace.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)

        self.editor_container = tk.Frame(self.workspace, bg="#282833", bd=1, relief=tk.SOLID, highlightbackground="#3d3d4d")
        self.editor_container.pack(expand=True, fill=tk.BOTH)

        self.text_area = tk.Text(
            self.editor_container,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#282833",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            selectbackground="#404050",
            relief=tk.FLAT,
            padx=12,
            pady=12,
            undo=True
        )

        self.scrollbar = ttk.Scrollbar(self.editor_container, orient=tk.VERTICAL, style="Vertical.TScrollbar", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # ---------- LIVE INFOBAR (METRICS & EVENTS) ----------
        self.infobar = tk.Frame(root, bg="#252530", height=32)
        self.infobar.pack(fill=tk.X, side=tk.BOTTOM)
        self.infobar.pack_propagate(False)

        self.metric_label = tk.Label(self.infobar, text="Lines: 1  |  Words: 0  |  Chars: 0", bg="#252530", fg="#a0a0b0", font=("Segoe UI", 9))
        self.metric_label.pack(side=tk.LEFT, padx=15, pady=6)

        self.input_hook_label = tk.Label(self.infobar, text="Last Character: None", bg="#252530", fg="#81c784", font=("Segoe UI", 9, "bold"))
        self.input_hook_label.pack(side=tk.RIGHT, padx=15, pady=6)

        # ---------- KEY BINDINGS ----------
        self.text_area.bind("<KeyRelease>", self.process_keyboard_stream)
        self.text_area.focus_set()

    def process_keyboard_stream(self, event=None):
        """
        Processes text changes and captures the exact visible character typed.
        """
        content = self.text_area.get("1.0", tk.END)
        
        # Calculate file metrics
        char_count = max(0, len(content) - 1)
        word_count = len(content.split())
        line_count = int(self.text_area.index(tk.END).split('.')[0]) - 1

        if event:
            time_stamp = datetime.now().strftime("%H:%M:%S")
            
            # Check if it's a normal printable character (alphabet, number, symbol)
            if event.char and event.char.isprintable():
                display_key = f"'{event.char}'"
            else:
                # Fallback to system key name for structural items (e.g., Backspace, Shift)
                display_key = f"[{event.keysym}]"
                if event.keysym == "space": display_key = "' ' (Space)"
                elif event.keysym == "Return": display_key = "[Enter ↵]"
            
            self.input_hook_label.config(text=f"Last Character: {display_key} at {time_stamp}")
        
        self.metric_label.config(text=f"Lines: {line_count}  |  Words: {word_count}  |  Chars: {char_count}")

    def save_to_file(self):
        content = self.text_area.get("1.0", tk.END).strip()

        if not content:
            messagebox.showwarning("Empty Document", "There is no text input recorded to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Plain Text File", "*.txt"), ("All Document Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("Export Complete", "Data securely committed and logged to output file.")
            except Exception as error:
                messagebox.showerror("File Error", f"Encountered unexpected operational failure during save:\n{error}")

    def clear_text(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the current workspace buffer?"):
            self.text_area.delete("1.0", tk.END)
            self.input_hook_label.config(text="Last Character: None")
            self.process_keyboard_stream()

    def show_word_count(self):
        content = self.text_area.get("1.0", tk.END).strip()
        words = len(content.split())
        chars = len(content)
        sentences = content.count('.') + content.count('!') + content.count('?')
        
        if chars == 0: sentences = 0

        stats_summary = f"📊 Metrics Analytics Engine\n" \
                        f"-----------------------------\n" \
                        f"• Total Character Registry: {chars}\n" \
                        f"• Total Extracted Words: {words}\n" \
                        f"• Sentences Checked: {sentences}"
                        
        messagebox.showinfo("Workspace Diagnostics Dashboard", stats_summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTextWorkspace(root)
    root.mainloop()