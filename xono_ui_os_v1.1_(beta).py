import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import customtkinter
from tkinter import Tk, Canvas, NW, BOTH, YES
from PIL import Image, ImageTk
import os
import json
import shutil
import time
import mimetypes

# ========================
root = tk.Tk()
root.title("Xono UI OS v1.1")
root.geometry("800x600")

icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
# =============================================================================


# ==================
# Paths and folders
# ==================
BASE_FOLDER = os.path.expanduser("C:\\Users\\pasnsilu\\XONO_UI_OS_v1.1")
APPSAVES = os.path.join(BASE_FOLDER, "appsaves")
RECYCLE_BIN = os.path.join(BASE_FOLDER, "RecycleBin")
SETUP_FILE = os.path.join(BASE_FOLDER, "system_setup.json")
MANIFEST_PATH = os.path.join(RECYCLE_BIN, "manifest.json")
LOG_PATH = os.path.join(BASE_FOLDER, "activity_log.txt")

os.makedirs(BASE_FOLDER, exist_ok=True)
os.makedirs(APPSAVES, exist_ok=True)
os.makedirs(RECYCLE_BIN, exist_ok=True)

if not os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "w", encoding="utf-8") as mf:
            json.dump([], mf, indent=2)
# ==============================================================================



# =========
# Images
# =========
def load_icon(icon_name):
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", icon_name)
        if os.path.exists(icon_path):
            return ImageTk.PhotoImage(Image.open(icon_path).resize((20, 20)))
    except Exception as e:
        print(f"Could not load icon {icon_name}: {e}")
    return None

file_viewer_icon = load_icon("File Viewer icon.png")
calculator_icon = load_icon("Calculator icon.png")
notepad_icon = load_icon("Notepad icon.png")
settings_icon = load_icon("Settings icon.png")
about_pc_icon = load_icon("About PC icon.png")
command_prompt_icon = load_icon("Command Prompt icon.png")
pc_performances_icon = load_icon("PC Performances icon.png")
browser_icon = load_icon("XONO Brower icon.png")
power_icon = load_icon("power.png")


# ===================
# Shut Down Function
# ===================
def _shutdown():
    try:
        time.sleep(1)
        root.destroy()
    except Exception:
        time.sleep(5)
        root.quit()


# ======
# Apps
# ======

# -------------
# File Viewer
# -------------
def open_file_viewer():
    # Set light theme colors
    BG_COLOR = "#f0f0f0"
    FRAME_BG = "#ffffff"
    BUTTON_BG = "#e0e0e0"
    TEXT_COLOR = "#000000"
    LISTBOX_BG = "#ffffff"
    LISTBOX_FG = "#000000"
    PREVIEW_BG = "#f8f8f8"
    ACCENT_COLOR = "#4a86e8"
    
    # Create a new window for file viewer
    file_viewer_window = tk.Toplevel(root)
    file_viewer_window.title("File Viewer")
    file_viewer_window.geometry("1000x650")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "File Viewer icon.ico")
        if os.path.exists(icon_path):
            file_viewer_window.iconbitmap(icon_path)
    except:
        pass
    
    file_viewer_window.configure(bg=BG_COLOR)

    # Configure ttk style for light theme
    style = ttk.Style(file_viewer_window)
    style.theme_use('clam')  # Use 'clam' theme which works well with custom colors

    # Configure ttk button colors
    style.configure('TButton', 
                    background=BUTTON_BG,
                    foreground=TEXT_COLOR,
                    borderwidth=1,
                    focusthickness=3,
                    focuscolor='none')
    style.map('TButton',
                background=[('active', '#d0d0d0')],
                foreground=[('active', TEXT_COLOR)])

    # Frames
    left_frame = tk.Frame(file_viewer_window, width=320, bg=FRAME_BG, relief="flat", borderwidth=1)
    left_frame.pack(side="left", fill="y", padx=5, pady=5)
    right_frame = tk.Frame(file_viewer_window, bg=BG_COLOR)
    right_frame.pack(side="right", fill="both", expand=True, padx=(0, 5), pady=5)

    # Current path variable (restricted to APPSAVES)
    appsaves_root = os.path.abspath(APPSAVES)
    os.makedirs(appsaves_root, exist_ok=True)
    current_path = tk.StringVar(value=appsaves_root)

    # Clipboard state for cut/copy/paste operations
    clipboard_state = {"type": None, "path": None, "is_cut": False}

    # Controls (no path entry shown to the user)
    btn_frame = tk.Frame(left_frame, bg=FRAME_BG)
    btn_frame.pack(padx=10, pady=(10,10), fill="x")

    def go_up():
        p = os.path.dirname(current_path.get())
        # Prevent navigating above the APPSAVES root
        try:
            p_abs = os.path.abspath(p)
            if os.path.commonpath([appsaves_root, p_abs]) != appsaves_root:
                # already at or above root; reset to appsaves_root
                current_path.set(appsaves_root)
            else:
                current_path.set(p_abs)
        except Exception:
            current_path.set(appsaves_root)
        refresh()
        
    def open_in_explorer():
        p = current_path.get()
        if os.path.exists(p):
            try:
                os.startfile(p)
            except Exception:
                messagebox.showinfo("Open", f"Can't open explorer for: {p}")
                
    ttk.Button(btn_frame, text="Up", command=go_up).pack(side="left", padx=3)
    ttk.Button(btn_frame, text="Open Folder", command=open_in_explorer).pack(side="left", padx=3)
    ttk.Button(btn_frame, text="New Folder", command=lambda: new_folder()).pack(side="left", padx=3)
    ttk.Button(btn_frame, text="Refresh", command=lambda: refresh()).pack(side="left", padx=3)

    # Listbox for entries
    listbox_frame = tk.Frame(left_frame, bg=FRAME_BG)
    listbox_frame.pack(fill="both", expand=True, padx=10, pady=6)
    list_scroll = tk.Scrollbar(listbox_frame, orient="vertical", bg=FRAME_BG, troughcolor=BUTTON_BG)
    listbox = tk.Listbox(listbox_frame, yscrollcommand=list_scroll.set, 
                        selectmode="browse", bg=LISTBOX_BG, fg=LISTBOX_FG,
                        selectbackground=ACCENT_COLOR, selectforeground="white",
                        font=("Arial", 10), relief="flat", borderwidth=1)
    list_scroll.config(command=listbox.yview)
    list_scroll.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    # Bottom action buttons
    action_frame = tk.Frame(left_frame, bg=FRAME_BG)
    action_frame.pack(fill="x", padx=10, pady=(6,10))

    def open_selected():
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        path = os.path.join(current_path.get(), name)
        if os.path.isdir(path):
            current_path.set(path)
            refresh()
        else:
            preview_file(path)
            
    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        path = os.path.join(current_path.get(), name)
        if messagebox.askyesno("Delete", f"Delete '{name}'? This cannot be undone."):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                refresh()
                clear_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")
                
    ttk.Button(action_frame, text="Open", command=open_selected).pack(side="left", padx=4)
    ttk.Button(action_frame, text="Delete", command=delete_selected).pack(side="left", padx=4)
    ttk.Button(action_frame, text="Rename", command=lambda: rename_selected()).pack(side="left", padx=4)
    ttk.Button(action_frame, text="Copy", command=lambda: copy_selected()).pack(side="left", padx=4)
    ttk.Button(action_frame, text="Cut", command=lambda: cut_selected()).pack(side="left", padx=4)
    ttk.Button(action_frame, text="Paste", command=lambda: paste_selected()).pack(side="left", padx=4)

    # Right side: preview area and details
    preview_top = tk.Frame(right_frame, bg=BG_COLOR)
    preview_top.pack(fill="x", padx=12, pady=12)
    preview_title = tk.Label(preview_top, text="Preview", font=("Arial", 14, "bold"), 
                            bg=BG_COLOR, fg=TEXT_COLOR)
    preview_title.pack(side="left")

    preview_area = tk.Frame(right_frame, bg=PREVIEW_BG, relief="flat", borderwidth=1)
    preview_area.pack(fill="both", expand=True, padx=12, pady=(0,12))

    # For image preview
    img_label = tk.Label(preview_area, bg=PREVIEW_BG)
    img_label.pack(fill="both", expand=True)

    # For text preview
    text_preview = tk.Text(preview_area, bg=PREVIEW_BG, fg=TEXT_COLOR, wrap="word",
                            font=("Consolas", 10), relief="flat", borderwidth=0)
    text_preview.config(state="disabled")

    # File info label
    info_label = tk.Label(right_frame, text="", anchor="w", justify="left", 
                            bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 10))
    info_label.pack(fill="x", padx=12, pady=(0,8))

    # Helpers
    def clear_preview():
        img_label.config(image="", text="")
        img_label.image = None
        text_preview.pack_forget()
        img_label.pack(fill="both", expand=True)
        info_label.config(text="")

    def preview_file(path):
        clear_preview()
        if not os.path.exists(path):
            info_label.config(text="File not found.")
            return
        info_lines = []
        info_lines.append(f"Name: {os.path.basename(path)}")
        try:
            info_lines.append(f"Size: {os.path.getsize(path)} bytes")
            info_lines.append(f"Modified: {time.ctime(os.path.getmtime(path))}")
        except Exception:
            pass
        mime, _ = mimetypes.guess_type(path)
        if mime and mime.startswith("image"):
            # Show image
            try:
                img = Image.open(path)
                # Resize to fit preview_area
                w = img_label.winfo_width() or 640
                h = img_label.winfo_height() or 360
                # Preserve aspect ratio
                img.thumbnail((w, h), Image.Resampling.LANCZOS)
                tkimg = ImageTk.PhotoImage(img)
                img_label.config(image=tkimg)
                img_label.image = tkimg
                info_label.config(text="\n".join(info_lines + [f"Type: {mime}"]))
            except Exception as e:
                info_label.config(text=f"Error previewing image: {e}")
        elif mime and (mime.startswith("text") or path.lower().endswith((".py", ".txt", ".md", ".log", ".json"))):
            # Show text
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read(200000)  # limit preview
                text_preview.config(state="normal")
                text_preview.delete("1.0", "end")
                text_preview.insert("1.0", content)
                text_preview.config(state="disabled")
                img_label.pack_forget()
                text_preview.pack(fill="both", expand=True)
                info_label.config(text="\n".join(info_lines + [f"Type: {mime or 'text'}"]))
            except Exception as e:
                info_label.config(text=f"Error previewing text: {e}")
        else:
            info_label.config(text="\n".join(info_lines + [f"Type: {mime or 'Unknown'}"]))
            img_label.config(text="No preview available for this file type.", 
                            fg="#666666", font=("Arial", 12), bg=PREVIEW_BG)

    def refresh():
        path = current_path.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", "Path does not exist.")
            return
        try:
            entries = os.listdir(path)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to list directory: {e}")
            return
        listbox.delete(0, "end")
        # Sort: directories first
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
        dirs.sort(key=str.lower)
        files.sort(key=str.lower)
        for d in dirs:
            # insert directory names (no trailing separators)
            listbox.insert("end", d)
        for f in files:
            listbox.insert("end", f)
        clear_preview()

    def new_folder():
        path = current_path.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", "Current path does not exist.")
            return
        # askstring is in simpledialog, not filedialog
        name = simpledialog.askstring("New folder", "Folder name:")
        if not name:
            return
        newp = os.path.join(path, name)
        try:
            os.makedirs(newp, exist_ok=False)
            refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create folder: {e}")

    def copy_selected():
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        src = os.path.join(current_path.get(), name)
        if not os.path.exists(src):
            messagebox.showerror("Error", "Selected item does not exist.")
            return
        clipboard_state["type"] = "folder" if os.path.isdir(src) else "file"
        clipboard_state["path"] = src
        clipboard_state["is_cut"] = False
        messagebox.showinfo("Copy", f"Copied '{name}' to clipboard.")

    def cut_selected():
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        src = os.path.join(current_path.get(), name)
        if not os.path.exists(src):
            messagebox.showerror("Error", "Selected item does not exist.")
            return
        clipboard_state["type"] = "folder" if os.path.isdir(src) else "file"
        clipboard_state["path"] = src
        clipboard_state["is_cut"] = True
        messagebox.showinfo("Cut", f"Cut '{name}'. Use Paste to move it.")

    def paste_selected():
        if not clipboard_state.get("path") or not os.path.exists(clipboard_state.get("path")):
            messagebox.showerror("Error", "Clipboard is empty or source no longer exists.")
            clipboard_state["path"] = None
            clipboard_state["type"] = None
            clipboard_state["is_cut"] = False
            return
        src = clipboard_state["path"]
        dest_dir = current_path.get()
        name = os.path.basename(src.rstrip(os.sep))
        dest = os.path.join(dest_dir, name)
        if os.path.abspath(src) == os.path.abspath(dest):
            messagebox.showerror("Error", "Source and destination are the same.")
            return
        if os.path.exists(dest):
            messagebox.showerror("Error", f"'{name}' already exists in the destination.")
            return
        try:
            if clipboard_state.get("is_cut"):
                shutil.move(src, dest)
                # clear clipboard after move
                clipboard_state["path"] = None
                clipboard_state["type"] = None
                clipboard_state["is_cut"] = False
            else:
                if os.path.isdir(src):
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
            messagebox.showinfo("Paste", f"Pasted '{name}' successfully.")
            refresh()
            clear_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Paste failed: {e}")

    def rename_selected():
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        src = os.path.join(current_path.get(), name)
        if not os.path.exists(src):
            messagebox.showerror("Error", "Selected item does not exist.")
            refresh()
            return
        new_name = simpledialog.askstring("Rename", f"Enter new name for '{name}':")
        if not new_name:
            return
        # prevent path traversal or creating path components
        if os.path.basename(new_name) != new_name or any(sep in new_name for sep in ("/", "\\")):
            messagebox.showerror("Error", "Invalid name. Do not include path separators.")
            return
        dest = os.path.join(current_path.get(), new_name)
        if os.path.exists(dest):
            messagebox.showerror("Error", "A file or folder with that name already exists.")
            return
        try:
            os.rename(src, dest)
            refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Rename failed: {e}")

    # Double-click and selection bindings
    def on_double_click(evt):
        open_selected()
    listbox.bind("<Double-1>", on_double_click)

    # Initial population
    refresh()

    # Ensure the preview updates its image when the window resizes
    def on_resize(evt):
        sel = listbox.curselection()
        if sel:
            name = listbox.get(sel[0])
            path = os.path.join(current_path.get(), name)
            if os.path.isfile(path):
                # re-preview to fit new size (images only)
                mime, _ = mimetypes.guess_type(path)
                if mime and mime.startswith("image"):
                    preview_file(path)
    preview_area.bind("<Configure>", on_resize)

    # Keyboard shortcuts (work while the file viewer Toplevel is open)
    file_viewer_window.bind('<Control-c>', lambda e: copy_selected())
    file_viewer_window.bind('<Control-C>', lambda e: copy_selected())
    file_viewer_window.bind('<Control-x>', lambda e: cut_selected())
    file_viewer_window.bind('<Control-X>', lambda e: cut_selected())
    file_viewer_window.bind('<Control-v>', lambda e: paste_selected())
    file_viewer_window.bind('<Control-V>', lambda e: paste_selected())
    file_viewer_window.bind('<Delete>', lambda e: delete_selected())
    file_viewer_window.bind('<F2>', lambda e: rename_selected())



# ------------
# Calculator
# ------------
def calculator():
    """Create a calculator application"""
    
    # Create calculator window
    calc_window = tk.Toplevel()
    calc_window.title("Calculator")
    
    # Get screen dimensions
    screen_width = calc_window.winfo_screenwidth()
    screen_height = calc_window.winfo_screenheight()
    
    # Set to full screen
    calc_window.geometry(f"{screen_width}x{screen_height}")
    
    # Optional: Remove window decorations for true full screen
    # calc_window.attributes('-fullscreen', True)
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "Calculator icon.ico")
        if os.path.exists(icon_path):
            file_viewer_window.iconbitmap(icon_path)
    except:
        pass
    
    # Calculator display
    display_var = tk.StringVar(value="0")
    
    # Calculator state
    current_value = "0"
    first_value = None
    operator = None
    waiting_for_second = False
    
    def update_display(value):
        """Update the calculator display"""
        display_var.set(value)
    
    def button_click(number):
        """Handle number button clicks"""
        nonlocal current_value, waiting_for_second
        
        if waiting_for_second:
            current_value = str(number)
            waiting_for_second = False
        else:
            if current_value == "0":
                current_value = str(number)
            else:
                current_value += str(number)
        
        update_display(current_value)
    
    def clear():
        """Clear the calculator"""
        nonlocal current_value, first_value, operator, waiting_for_second
        current_value = "0"
        first_value = None
        operator = None
        waiting_for_second = False
        update_display(current_value)
    
    def decimal():
        """Add decimal point"""
        nonlocal current_value, waiting_for_second
        
        if waiting_for_second:
            current_value = "0."
            waiting_for_second = False
        elif "." not in current_value:
            current_value += "."
        
        update_display(current_value)
    
    def backspace():
        """Remove last character"""
        nonlocal current_value
        
        if len(current_value) > 1:
            current_value = current_value[:-1]
        else:
            current_value = "0"
        
        update_display(current_value)
    
    def operation(op):
        """Handle operation buttons"""
        nonlocal first_value, operator, current_value, waiting_for_second
        
        if operator is not None and not waiting_for_second:
            equals()
        
        first_value = float(current_value)
        operator = op
        waiting_for_second = True
    
    def equals():
        """Perform calculation"""
        nonlocal current_value, first_value, operator, waiting_for_second
        
        if operator is None or first_value is None:
            return
        
        second_value = float(current_value)
        
        try:
            if operator == "+":
                result = first_value + second_value
            elif operator == "-":
                result = first_value - second_value
            elif operator == "×":
                result = first_value * second_value
            elif operator == "÷":
                if second_value == 0:
                    result = "Error"
                else:
                    result = first_value / second_value
            elif operator == "%":
                result = first_value % second_value
            else:
                result = current_value
            
            # Format result
            if result == "Error":
                current_value = result
            else:
                # Check if result is integer
                if result.is_integer():
                    current_value = str(int(result))
                else:
                    # Limit decimal places
                    current_value = f"{result:.10f}".rstrip('0').rstrip('.')
                    if len(current_value) > 15:
                        current_value = f"{result:.10e}"
            
            update_display(current_value)
            
        except Exception:
            current_value = "Error"
            update_display(current_value)
        
        first_value = None
        operator = None
        waiting_for_second = False
    
    def square_root():
        """Calculate square root"""
        nonlocal current_value
        
        try:
            value = float(current_value)
            if value < 0:
                current_value = "Error"
            else:
                result = math.sqrt(value)
                if result.is_integer():
                    current_value = str(int(result))
                else:
                    current_value = f"{result:.10f}".rstrip('0').rstrip('.')
                    if len(current_value) > 15:
                        current_value = f"{result:.10e}"
            
            update_display(current_value)
        except Exception:
            current_value = "Error"
            update_display(current_value)
    
    def percentage():
        """Convert to percentage"""
        nonlocal current_value
        
        try:
            value = float(current_value)
            result = value / 100
            if result.is_integer():
                current_value = str(int(result))
            else:
                current_value = f"{result:.10f}".rstrip('0').rstrip('.')
            
            update_display(current_value)
        except Exception:
            current_value = "Error"
            update_display(current_value)
    
    def plus_minus():
        """Toggle positive/negative"""
        nonlocal current_value
        
        if current_value != "0" and current_value != "Error":
            if current_value.startswith("-"):
                current_value = current_value[1:]
            else:
                current_value = "-" + current_value
            
            update_display(current_value)
    
    # Create display - make it responsive for full screen
    display_frame = tk.Frame(calc_window, bg="#2c2c2c")
    display_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=20)
    
    display_label = tk.Label(display_frame, textvariable=display_var, 
                            font=("Arial", 48), anchor="e", bg="#2c2c2c", 
                            fg="white", padx=40, pady=40)
    display_label.pack(fill=tk.BOTH, expand=True)
    
    # Create button frame
    button_frame = tk.Frame(calc_window)
    button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Define button layout
    buttons = [
        ("C", "CE", "⌫", "÷"),
        ("7", "8", "9", "×"),
        ("4", "5", "6", "-"),
        ("1", "2", "3", "+"),
        ("±", "0", ".", "=")
    ]
    
    # Special buttons at the top
    special_buttons = [
        ("√", square_root, "#4CAF50"),
        ("%", percentage, "#4CAF50")
    ]
    
    # Create special buttons frame
    special_frame = tk.Frame(button_frame)
    special_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 5))
    
    for i, (text, command, color) in enumerate(special_buttons):
        btn = tk.Button(special_frame, text=text, font=("Arial", 24, "bold"),
                       bg=color, fg="white", activebackground="#45a049",
                       activeforeground="white", relief="flat",
                       command=command)
        btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
    
    # Configure special frame grid
    special_frame.grid_columnconfigure(0, weight=1)
    special_frame.grid_columnconfigure(1, weight=1)
    
    # Create calculator buttons
    button_commands = {
        "C": clear,
        "CE": clear,
        "⌫": backspace,
        "÷": lambda: operation("÷"),
        "×": lambda: operation("×"),
        "-": lambda: operation("-"),
        "+": lambda: operation("+"),
        "=": equals,
        ".": decimal,
        "±": plus_minus
    }
    
    # Create buttons with larger font for full screen
    button_font = ("Arial", 24, "bold")
    
    for i, row in enumerate(buttons, start=1):
        for j, text in enumerate(row):
            # Determine button color
            if text in ["C", "CE"]:
                bg_color = "#f44336"  # Red
            elif text in ["÷", "×", "-", "+", "="]:
                bg_color = "#FF9800"  # Orange
            elif text == "⌫":
                bg_color = "#9E9E9E"  # Gray
            else:
                bg_color = "#424242"  # Dark gray
            
            # Create button
            if text.isdigit() or text == ".":
                cmd = lambda t=text: button_click(t)
            elif text in button_commands:
                cmd = button_commands[text]
            else:
                cmd = lambda t=text: button_click(t)
            
            btn = tk.Button(button_frame, text=text, font=button_font,
                           bg=bg_color, fg="white", activebackground="#616161",
                           activeforeground="white", relief="flat",
                           command=cmd)
            
            btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
    
    # Configure grid weights for responsiveness
    for i in range(6):  # 5 rows + special row
        button_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        button_frame.grid_columnconfigure(j, weight=1)
    
    # Add ESC key to exit full screen or close calculator
    def close_calculator(event=None):
        calc_window.destroy()
    
    calc_window.bind('<Escape>', close_calculator)
    
    # Optional: Add maximize/minimize button
    def toggle_fullscreen(event=None):
        current_state = calc_window.attributes('-fullscreen')
        calc_window.attributes('-fullscreen', not current_state)
    
    calc_window.bind('<F11>', toggle_fullscreen)
    
    # Make calculator window modal
    calc_window.transient(root)
    calc_window.grab_set()
    
    # Optional: Start in true full screen mode (uncomment if you want it)
    # calc_window.attributes('-fullscreen', True)



# ------------
# Notepad
# ------------
def notepad():
    """Create a Notepad application"""
    
    # Create notepad window
    notepad_window = tk.Toplevel(root)
    notepad_window.title("Notepad - Untitled")
    notepad_window.geometry("900x600")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "Notepad icon.ico")
        if os.path.exists(icon_path):
            notepad_window.iconbitmap(icon_path)
    except:
        pass
    
    # Variables
    current_file = None
    text_changed = False
    
    # Main text area with scrollbar
    text_frame = tk.Frame(notepad_window)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Text widget with scrollbar
    text_scrollbar = tk.Scrollbar(text_frame)
    text_scrollbar.pack(side="right", fill="y")
    
    text_area = tk.Text(text_frame, 
                        wrap="word", 
                        font=("Consolas", 11),
                        yscrollcommand=text_scrollbar.set,
                        bg="white",
                        fg="black",
                        insertbackground="black")
    text_area.pack(fill="both", expand=True)
    text_scrollbar.config(command=text_area.yview)
    
    # Button frame at bottom
    button_frame = tk.Frame(notepad_window)
    button_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    def save_file():
        """Save the current text to a file"""
        nonlocal current_file, text_changed
        
        # If no current file, show save dialog
        if not current_file:
            save_dialog()
        else:
            # Save to existing file
            try:
                content = text_area.get("1.0", "end-1c")
                with open(current_file, "w", encoding="utf-8") as f:
                    f.write(content)
                text_changed = False
                notepad_window.title(f"Notepad - {os.path.basename(current_file)}")
                messagebox.showinfo("Saved", f"File saved successfully!\n{current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def save_dialog():
        """Show save file dialog"""
        nonlocal current_file, text_changed
        
        # Create a custom file dialog that only allows saving to APPSAVES
        save_window = tk.Toplevel(notepad_window)
        save_window.title("Save File")
        save_window.geometry("500x400")
        save_window.transient(notepad_window)
        save_window.grab_set()
        
        # Center the save window
        save_window.update_idletasks()
        x = notepad_window.winfo_x() + (notepad_window.winfo_width() // 2) - (500 // 2)
        y = notepad_window.winfo_y() + (notepad_window.winfo_height() // 2) - (400 // 2)
        save_window.geometry(f"+{x}+{y}")
        
        # Frame for listbox
        list_frame = tk.Frame(save_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label
        label = tk.Label(list_frame, text="Save in APPSAVES folder:", font=("Arial", 12, "bold"))
        label.pack(pady=(0, 10))
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15, font=("Arial", 10))
        file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=file_listbox.yview)
        
        # Load existing .txt files
        try:
            files = [f for f in os.listdir(APPSAVES) if f.lower().endswith('.txt')]
            files.sort()
            for file in files:
                file_listbox.insert("end", file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list files: {e}")
        
        # Frame for filename input and buttons
        input_frame = tk.Frame(save_window)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Filename label and entry
        tk.Label(input_frame, text="Filename:").pack(side="left", padx=(0, 10))
        filename_var = tk.StringVar()
        filename_entry = tk.Entry(input_frame, textvariable=filename_var, width=30)
        filename_entry.pack(side="left", padx=(0, 20))
        filename_entry.focus()
        
        # Function to fill filename from listbox selection
        def fill_filename(event):
            selection = file_listbox.curselection()
            if selection:
                filename = file_listbox.get(selection[0])
                filename_var.set(filename)
        
        file_listbox.bind("<<ListboxSelect>>", fill_filename)
        
        # Button frame
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(side="right")
        
        def perform_save():
            filename = filename_var.get().strip()
            if not filename:
                messagebox.showwarning("Warning", "Please enter a filename")
                return
            
            # Ensure .txt extension
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            
            filepath = os.path.join(APPSAVES, filename)
            
            # Check if file exists
            if os.path.exists(filepath):
                if not messagebox.askyesno("Confirm", f"File '{filename}' already exists. Overwrite?"):
                    return
            
            try:
                content = text_area.get("1.0", "end-1c")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                
                nonlocal current_file, text_changed
                current_file = filepath
                text_changed = False
                notepad_window.title(f"Notepad - {filename}")
                save_window.destroy()
                messagebox.showinfo("Saved", f"File saved successfully!\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        
        def cancel_save():
            save_window.destroy()
        
        tk.Button(btn_frame, text="Save", command=perform_save, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=cancel_save, width=10).pack(side="left", padx=5)
    
    def open_file():
        """Open a file selection dialog and load the selected file"""
        nonlocal current_file, text_changed
        
        # Create a custom file dialog that only shows APPSAVES folder
        open_window = tk.Toplevel(notepad_window)
        open_window.title("Open File")
        open_window.geometry("500x400")
        open_window.transient(notepad_window)
        open_window.grab_set()
        
        # Center the open window
        open_window.update_idletasks()
        x = notepad_window.winfo_x() + (notepad_window.winfo_width() // 2) - (500 // 2)
        y = notepad_window.winfo_y() + (notepad_window.winfo_height() // 2) - (400 // 2)
        open_window.geometry(f"+{x}+{y}")
        
        # Frame for listbox
        list_frame = tk.Frame(open_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label
        label = tk.Label(list_frame, text="Select a file from APPSAVES folder:", font=("Arial", 12, "bold"))
        label.pack(pady=(0, 10))
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15, font=("Arial", 10))
        file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=file_listbox.yview)
        
        # Load existing .txt files
        try:
            files = [f for f in os.listdir(APPSAVES) if f.lower().endswith('.txt')]
            files.sort()
            for file in files:
                file_listbox.insert("end", file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list files: {e}")
        
        # Button frame
        btn_frame = tk.Frame(open_window)
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def perform_open():
            selection = file_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a file")
                return
            
            filename = file_listbox.get(selection[0])
            filepath = os.path.join(APPSAVES, filename)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Clear text area and insert new content
                text_area.delete("1.0", "end")
                text_area.insert("1.0", content)
                
                nonlocal current_file, text_changed
                current_file = filepath
                text_changed = False
                notepad_window.title(f"Notepad - {filename}")
                open_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        
        def cancel_open():
            open_window.destroy()
        
        tk.Button(btn_frame, text="Open", command=perform_open, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=cancel_open, width=10).pack(side="left", padx=5)
        
        # Double-click to open
        def on_double_click(event):
            perform_open()
        
        file_listbox.bind("<Double-Button-1>", on_double_click)
    
    def new_file():
        """Create a new empty file"""
        nonlocal current_file, text_changed
        
        if text_changed:
            if not messagebox.askyesno("Notepad", "Save changes to current file?"):
                return
            save_file()
        
        text_area.delete("1.0", "end")
        current_file = None
        text_changed = False
        notepad_window.title("Notepad - Untitled")
    
    # Track text changes
    def on_text_change(event=None):
        nonlocal text_changed
        if not text_changed:
            text_changed = True
            # Add asterisk to window title if unsaved
            if not notepad_window.title().startswith("*"):
                notepad_window.title("*" + notepad_window.title())
    
    text_area.bind("<Key>", on_text_change)
    
    # Create buttons
    tk.Button(button_frame, text="New", command=new_file, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Open", command=open_file, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Save", command=save_file, width=10).pack(side="left", padx=5)
    
    # Add some spacing
    tk.Label(button_frame, text="", width=10).pack(side="left")
    
    # Copy, Cut, Paste buttons
    tk.Button(button_frame, text="Copy", 
              command=lambda: notepad_window.focus_get().event_generate("<<Copy>>"), 
              width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cut", 
              command=lambda: notepad_window.focus_get().event_generate("<<Cut>>"), 
              width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Paste", 
              command=lambda: notepad_window.focus_get().event_generate("<<Paste>>"), 
              width=10).pack(side="left", padx=5)
    
    # Add keyboard shortcuts
    notepad_window.bind('<Control-n>', lambda e: new_file())
    notepad_window.bind('<Control-o>', lambda e: open_file())
    notepad_window.bind('<Control-s>', lambda e: save_file())
    notepad_window.bind('<Control-N>', lambda e: new_file())
    notepad_window.bind('<Control-O>', lambda e: open_file())
    notepad_window.bind('<Control-S>', lambda e: save_file())
    
    # Warn before closing if unsaved changes
    def on_closing():
        if text_changed:
            if messagebox.askyesno("Notepad", "You have unsaved changes. Save before closing?"):
                save_file()
        notepad_window.destroy()
    
    notepad_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Make text area get focus
    text_area.focus_set()


# -------------
# Settings App
# -------------
def settings():
    """Create Settings application"""
    
    # Create settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x400")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "Settings icon.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            settings_window.iconphoto(True, photo)
    except Exception as e:
        print(f"Could not load settings icon: {e}")
    
    # Main frame
    main_frame = tk.Frame(settings_window, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    title_label = tk.Label(main_frame, text="Settings", font=("Arial", 24, "bold"), 
                          bg="#f0f0f0", fg="#333333")
    title_label.pack(pady=(0, 30))
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#f0f0f0")
    button_frame.pack(fill="both", expand=True)
    
    # Change Username and Password button
    def open_change_credentials():
        """Open window to change username and password"""
        
        change_window = tk.Toplevel(settings_window)
        change_window.title("Change Username & Password")
        change_window.geometry("450x450")
        change_window.transient(settings_window)
        change_window.grab_set()
        
        # Center the window
        change_window.update_idletasks()
        x = settings_window.winfo_x() + (settings_window.winfo_width() // 2) - (450 // 2)
        y = settings_window.winfo_y() + (settings_window.winfo_height() // 2) - (450 // 2)
        change_window.geometry(f"+{x}+{y}")
        
        # Main frame
        change_frame = tk.Frame(change_window, bg="#f0f0f0")
        change_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(change_frame, text="Change Credentials", font=("Arial", 18, "bold"),
                bg="#f0f0f0", fg="#333333").pack(pady=(0, 20))
        
        # Current username
        current_username = ""
        if os.path.exists(SETUP_FILE):
            with open(SETUP_FILE, "r", encoding="utf-8") as sf:
                setup_data = json.load(sf)
                current_username = setup_data.get("username", "")
        
        tk.Label(change_frame, text=f"Current Username: {current_username}", 
                font=("Arial", 10), bg="#f0f0f0", fg="#666666").pack(pady=(0, 20))
        
        # New Username
        tk.Label(change_frame, text="New Username:", font=("Arial", 11, "bold"),
                bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", pady=(10, 5))
        
        new_username_var = tk.StringVar()
        new_username_entry = tk.Entry(change_frame, textvariable=new_username_var, 
                                     font=("Arial", 11), width=30)
        new_username_entry.pack(pady=(0, 15))
        new_username_entry.focus()
        
        # New Password Frame
        tk.Label(change_frame, text="New Password:", font=("Arial", 11, "bold"),
                bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", pady=(10, 5))
        
        new_password_frame = tk.Frame(change_frame, bg="#f0f0f0")
        new_password_frame.pack(fill="x", pady=(0, 15))
        
        new_password_var = tk.StringVar()
        new_password_entry = tk.Entry(new_password_frame, textvariable=new_password_var, 
                                     show="*", font=("Arial", 11), width=30)
        new_password_entry.pack(side="left")
        
        # Show/Hide Password Button for New Password
        show_new_pass_var = tk.BooleanVar(value=False)
        
        def toggle_new_password():
            if show_new_pass_var.get():
                new_password_entry.config(show="")
                show_new_pass_btn.config(text="🙈 Hide")
            else:
                new_password_entry.config(show="*")
                show_new_pass_btn.config(text="👁️ Show")
        
        show_new_pass_btn = tk.Button(new_password_frame, text="👁️ Show", 
                                     font=("Arial", 9), bg="#e3f2fd", fg="#1976d2",
                                     relief="flat", cursor="hand2",
                                     command=lambda: [show_new_pass_var.set(not show_new_pass_var.get()), 
                                                     toggle_new_password()])
        show_new_pass_btn.pack(side="left", padx=5)
        
        # Confirm Password Frame
        tk.Label(change_frame, text="Confirm Password:", font=("Arial", 11, "bold"),
                bg="#f0f0f0", fg="#333333", anchor="w").pack(fill="x", pady=(10, 5))
        
        confirm_password_frame = tk.Frame(change_frame, bg="#f0f0f0")
        confirm_password_frame.pack(fill="x", pady=(0, 25))
        
        confirm_password_var = tk.StringVar()
        confirm_password_entry = tk.Entry(confirm_password_frame, textvariable=confirm_password_var, 
                                         show="*", font=("Arial", 11), width=30)
        confirm_password_entry.pack(side="left")
        
        # Show/Hide Password Button for Confirm Password
        show_confirm_pass_var = tk.BooleanVar(value=False)
        
        def toggle_confirm_password():
            if show_confirm_pass_var.get():
                confirm_password_entry.config(show="")
                show_confirm_pass_btn.config(text="🙈 Hide")
            else:
                confirm_password_entry.config(show="*")
                show_confirm_pass_btn.config(text="👁️ Show")
        
        show_confirm_pass_btn = tk.Button(confirm_password_frame, text="👁️ Show", 
                                         font=("Arial", 9), bg="#e3f2fd", fg="#1976d2",
                                         relief="flat", cursor="hand2",
                                         command=lambda: [show_confirm_pass_var.set(not show_confirm_pass_var.get()), 
                                                         toggle_confirm_password()])
        show_confirm_pass_btn.pack(side="left", padx=5)
        
        # Message label
        message_label = tk.Label(change_frame, text="", font=("Arial", 10), 
                                bg="#f0f0f0", fg="red")
        message_label.pack(pady=(0, 10))
        
        # Button frame
        btn_frame = tk.Frame(change_frame, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)
        
        def save_changes():
            """Save the new username and password"""
            new_username = new_username_var.get().strip()
            new_password = new_password_var.get()
            confirm_password = confirm_password_var.get()
            
            # Validation
            if not new_username:
                message_label.config(text="Username cannot be empty!", fg="red")
                return
            
            if not new_password:
                message_label.config(text="Password cannot be empty!", fg="red")
                return
            
            if new_password != confirm_password:
                message_label.config(text="Passwords do not match!", fg="red")
                return
            
            try:
                # Read existing settings
                with open(SETUP_FILE, "r", encoding="utf-8") as sf:
                    setup_data = json.load(sf)
                
                # Update username and password
                setup_data["username"] = new_username
                setup_data["password"] = new_password
                
                # Save back to file
                with open(SETUP_FILE, "w", encoding="utf-8") as sf:
                    json.dump(setup_data, sf, indent=2)
                
                message_label.config(text="✓ Credentials updated successfully!", fg="green")
                
                # Clear entries after success
                new_username_var.set("")
                new_password_var.set("")
                confirm_password_var.set("")
                
                # Close window after 2 seconds
                change_window.after(2000, change_window.destroy)
                
            except Exception as e:
                message_label.config(text=f"Error: {str(e)}", fg="red")
        
        def cancel_changes():
            """Close the change window"""
            change_window.destroy()
        
        # Buttons
        tk.Button(btn_frame, text="Save Changes", command=save_changes,
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=cancel_changes,
                 bg="#f44336", fg="white", font=("Arial", 11),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        # Bind Enter key to save
        change_window.bind('<Return>', lambda e: save_changes())
    
    # View Current Settings button
    def open_view_settings():
        """Open window to view current settings"""
        
        view_window = tk.Toplevel(settings_window)
        view_window.title("Current Settings")
        view_window.geometry("550x500")  # Slightly wider for the show button
        view_window.transient(settings_window)
        view_window.grab_set()
        
        # Center the window
        view_window.update_idletasks()
        x = settings_window.winfo_x() + (settings_window.winfo_width() // 2) - (550 // 2)
        y = settings_window.winfo_y() + (settings_window.winfo_height() // 2) - (500 // 2)
        view_window.geometry(f"+{x}+{y}")
        
        # Main frame with scrollbar
        main_view_frame = tk.Frame(view_window, bg="#f0f0f0")
        main_view_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_view_frame, text="Current System Settings", 
                font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=(0, 20))
        
        # Create a canvas for scrollable content
        canvas = tk.Canvas(main_view_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_view_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Load current settings
        settings_data = {}
        current_password = ""
        if os.path.exists(SETUP_FILE):
            with open(SETUP_FILE, "r", encoding="utf-8") as sf:
                settings_data = json.load(sf)
                current_password = settings_data.get("password", "")
        
        # Display settings in a nice format
        settings_card = tk.Frame(scrollable_frame, bg="white", relief="solid", 
                                borderwidth=1, padx=20, pady=20)
        settings_card.pack(fill="x", pady=10)
        
        # Settings title
        tk.Label(settings_card, text="📋 User Configuration", 
                font=("Arial", 14, "bold"), bg="white", fg="#333333").pack(anchor="w", pady=(0, 15))
        
        # Define settings to display
        display_settings = [
            ("👤 Username", settings_data.get("username", "Not set")),
            ("🌍 Country", settings_data.get("country", "Not set")),
            ("💻 Device Name", settings_data.get("device_name", "Not set")),
            ("🔊 Sound Effects", "Enabled" if settings_data.get("sound_effects", False) else "Disabled")
        ]
        
        # Display regular settings
        for i, (label, value) in enumerate(display_settings):
            # Create a frame for each setting
            setting_frame = tk.Frame(settings_card, bg="white")
            setting_frame.pack(fill="x", pady=8)
            
            # Label
            tk.Label(setting_frame, text=label, font=("Arial", 11, "bold"), 
                    bg="white", fg="#555555", width=20, anchor="w").pack(side="left", padx=(0, 10))
            
            # Value
            tk.Label(setting_frame, text=str(value), font=("Consolas", 10), 
                    bg="#f8f8f8", fg="#333333", relief="solid", 
                    borderwidth=1, padx=10, pady=5, anchor="w", width=30).pack(side="left", fill="x", expand=True)
        
        # Password setting with show/hide button
        password_frame = tk.Frame(settings_card, bg="white")
        password_frame.pack(fill="x", pady=8)
        
        # Password label
        tk.Label(password_frame, text="🔒 Password", font=("Arial", 11, "bold"), 
                bg="white", fg="#555555", width=20, anchor="w").pack(side="left", padx=(0, 10))
        
        # Password value frame
        password_value_frame = tk.Frame(password_frame, bg="white")
        password_value_frame.pack(side="left", fill="x", expand=True)
        
        # Password display (hidden by default)
        password_display_var = tk.StringVar(value="••••••••")
        password_display_label = tk.Label(password_value_frame, textvariable=password_display_var, 
                                         font=("Consolas", 10), bg="#f8f8f8", fg="#333333", 
                                         relief="solid", borderwidth=1, padx=10, pady=5, 
                                         anchor="w", width=30)
        password_display_label.pack(side="left", fill="x", expand=True)
        
        # Show/Hide Password Button
        show_password_var = tk.BooleanVar(value=False)
        
        def toggle_password_display():
            if show_password_var.get():
                # Show actual password
                password_display_var.set(current_password if current_password else "Not set")
                show_password_btn.config(text="🙈 Hide")
            else:
                # Show dots
                password_display_var.set("••••••••" if current_password else "Not set")
                show_password_btn.config(text="👁️ Show")
        
        show_password_btn = tk.Button(password_value_frame, text="👁️ Show", 
                                     font=("Arial", 9), bg="#e3f2fd", fg="#1976d2",
                                     relief="flat", cursor="hand2",
                                     command=lambda: [show_password_var.set(not show_password_var.get()), 
                                                     toggle_password_display()])
        show_password_btn.pack(side="left", padx=5)
        
        # System info card
        sysinfo_card = tk.Frame(scrollable_frame, bg="white", relief="solid", 
                               borderwidth=1, padx=20, pady=20)
        sysinfo_card.pack(fill="x", pady=10)
        
        tk.Label(sysinfo_card, text="🖥️ System Information", 
                font=("Arial", 14, "bold"), bg="white", fg="#333333").pack(anchor="w", pady=(0, 15))
        
        # Add custom system info
        import platform
        import datetime
        
        system_info = [
            ("OS", "XONO OS UI Edition"),
            ("OS Version", "1.1"),
            ("Python Version", platform.python_version()),
            ("Current Time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("Build", "Alpha Release"),
            ("Developer", "XONO Development Team")
        ]
        
        for label, value in system_info:
            info_frame = tk.Frame(sysinfo_card, bg="white")
            info_frame.pack(fill="x", pady=5)
            
            tk.Label(info_frame, text=label, font=("Arial", 10, "bold"), 
                    bg="white", fg="#666666", width=15, anchor="w").pack(side="left")
            
            tk.Label(info_frame, text=value, font=("Consolas", 9), 
                    bg="#f0f0f0", fg="#333333", relief="solid", 
                    borderwidth=1, padx=8, pady=3, anchor="w").pack(side="left", fill="x", expand=True)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        tk.Button(scrollable_frame, text="Close", command=view_window.destroy,
                 bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                 padx=30, pady=10, cursor="hand2").pack(pady=20)
        
        # Configure canvas scrolling with mouse wheel
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    
    # Create the two main buttons
    button_style = {
        "font": ("Arial", 14, "bold"),
        "width": 30,
        "height": 2,
        "cursor": "hand2",
        "pady": 15
    }
    
    # Button 1: Change Username and Password
    change_btn = tk.Button(button_frame, text="🔐 Change Username & Password", 
                          command=open_change_credentials,
                          bg="#2196F3", fg="white", activebackground="#1976d2",
                          activeforeground="white", **button_style)
    change_btn.pack(pady=20)
    
    # Button 2: View Current Settings
    view_btn = tk.Button(button_frame, text="👁️ View Current Settings", 
                        command=open_view_settings,
                        bg="#4CAF50", fg="white", activebackground="#45a049",
                        activeforeground="white", **button_style)
    view_btn.pack(pady=20)



# ------------------
# About PC App
# ------------------
def about_pc():
    """Create About Your PC application"""
    
    # Try to import required modules
    try:
        import platform
        import uuid
        import shutil
        import os
        import psutil
        import wmi
        has_psutil = True
        has_wmi = True
    except ImportError:
        # Create fallback values
        has_psutil = False
        has_wmi = False
    
    # Create about window
    about_window = tk.Toplevel(root)
    about_window.title("About Your PC")
    about_window.geometry("700x700")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "About PC icon.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            about_window.iconphoto(True, photo)
    except Exception as e:
        print(f"Could not load about icon: {e}")
    
    # Main frame with scrollbar
    main_frame = tk.Frame(about_window, bg="#1a1a1a")
    main_frame.pack(fill="both", expand=True)
    
    # Create canvas for scrollable content
    canvas = tk.Canvas(main_frame, bg="#1a1a1a", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Title section
    title_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
    title_frame.pack(fill="x", pady=(20, 10), padx=30)
    
    # XONO Logo/Title
    tk.Label(title_frame, text="--- XONO ---", 
            font=("Consolas", 24, "bold"), bg="#1a1a1a", fg="#4CAF50").pack()
    
    tk.Label(title_frame, text="XONO OS UI Edition v1.1", 
            font=("Arial", 18), bg="#1a1a1a", fg="white").pack(pady=(5, 10))
    
    # Device ID section
    device_frame = tk.Frame(scrollable_frame, bg="#2c2c2c", relief="solid", 
                           borderwidth=1, padx=20, pady=15)
    device_frame.pack(fill="x", padx=30, pady=10)
    
    try:
        # Get device ID
        mac = uuid.getnode()
        device_id = f"{mac:012x}".upper()
    except:
        device_id = str(uuid.uuid4()) if 'uuid' in globals() else "Unknown Device"
    
    tk.Label(device_frame, text="Device ID:", 
            font=("Arial", 12, "bold"), bg="#2c2c2c", fg="white", anchor="w").pack(anchor="w")
    
    # Device ID with copy button
    device_id_frame = tk.Frame(device_frame, bg="#2c2c2c")
    device_id_frame.pack(fill="x", pady=(5, 0))
    
    device_label = tk.Label(device_id_frame, text=device_id, font=("Consolas", 11), 
                           bg="#3c3c3c", fg="#4CAF50", padx=10, pady=5, anchor="w")
    device_label.pack(side="left", fill="x", expand=True)
    
    def copy_device_id():
        about_window.clipboard_clear()
        about_window.clipboard_append(device_id)
        device_label.config(fg="#FF9800")
        about_window.after(1000, lambda: device_label.config(fg="#4CAF50"))
    
    tk.Button(device_id_frame, text="📋 Copy", font=("Arial", 9), 
             bg="#2196F3", fg="white", relief="flat", cursor="hand2",
             command=copy_device_id).pack(side="left", padx=5)
    
    # Hardware Information Section
    hardware_frame = tk.Frame(scrollable_frame, bg="#2c2c2c", relief="solid", 
                            borderwidth=1, padx=20, pady=15)
    hardware_frame.pack(fill="x", padx=30, pady=10)
    
    tk.Label(hardware_frame, text="Hardware Information", 
            font=("Arial", 16, "bold"), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(0, 15))
    
    # Get hardware info
    def get_hardware_info():
        info = {}
        
        # CPU Info
        try:
            cpu_name = platform.processor() or "Unknown CPU"
            if not cpu_name:
                cpu_name = " ".join(platform.uname())
        except:
            cpu_name = "Unknown CPU"
        
        try:
            cpu_cores = os.cpu_count() or "Unknown"
        except:
            cpu_cores = "Unknown"
        
        info["CPU"] = f"{cpu_name} ({cpu_cores} cores)"
        
        # RAM Info
        if has_psutil:
            try:
                mem = psutil.virtual_memory()
                total_ram_gb = round(mem.total / (1024 ** 3), 2)
                info["RAM"] = f"{total_ram_gb} GB"
            except:
                info["RAM"] = "Unknown"
        else:
            # Try Linux /proc/meminfo
            try:
                if os.path.exists("/proc/meminfo"):
                    with open("/proc/meminfo", "r") as mf:
                        for line in mf:
                            if line.startswith("MemTotal:"):
                                parts = line.split()
                                kb = int(parts[1])
                                total_ram_gb = round(kb / 1024 / 1024, 2)
                                info["RAM"] = f"{total_ram_gb} GB"
                                break
                        else:
                            info["RAM"] = "Unknown"
                else:
                    info["RAM"] = "Unknown"
            except:
                info["RAM"] = "Unknown"
        
        # Storage Info
        try:
            usage = shutil.disk_usage(BASE_FOLDER if os.path.exists(BASE_FOLDER) else os.getcwd())
            total_storage_gb = round(usage.total / (1024 ** 3), 2)
            free_storage_gb = round(usage.free / (1024 ** 3), 2)
            info["Storage"] = f"{total_storage_gb} GB (free {free_storage_gb} GB)"
        except:
            info["Storage"] = "Unknown"
        
        # GPU Info
        if has_wmi:
            try:
                c = wmi.WMI()
                gpus = []
                for gpu in c.Win32_VideoController():
                    name = getattr(gpu, "Name", None)
                    if name:
                        gpus.append(name.strip())
                info["GPU"] = ", ".join(gpus) if gpus else "Unknown"
            except:
                info["GPU"] = "Unknown"
        else:
            # Try Linux lspci
            try:
                if shutil.which("lspci"):
                    out = os.popen("lspci -nn | grep -i 'vga\\|3d\\|2d'").read().strip()
                    if out:
                        lines = out.splitlines()
                        gpu_str = "; ".join([l.split(": ", 1)[1] if ": " in l else l for l in lines])
                        info["GPU"] = gpu_str
                    else:
                        info["GPU"] = "Unknown"
                else:
                    info["GPU"] = "Unknown"
            except:
                info["GPU"] = "Unknown"
        
        return info
    
    # Display hardware info
    hardware_info = get_hardware_info()
    
    for label, value in hardware_info.items():
        info_row = tk.Frame(hardware_frame, bg="#2c2c2c")
        info_row.pack(fill="x", pady=8)
        
        tk.Label(info_row, text=f"{label}:", 
                font=("Arial", 12, "bold"), bg="#2c2c2c", fg="#CCCCCC", 
                width=20, anchor="w").pack(side="left")
        
        tk.Label(info_row, text=value, font=("Consolas", 11), 
                bg="#3c3c3c", fg="white", padx=10, pady=5,
                anchor="w").pack(side="left", fill="x", expand=True)
    
    # XONO Specifications Section
    xono_frame = tk.Frame(scrollable_frame, bg="#2c2c2c", relief="solid", 
                         borderwidth=1, padx=20, pady=15)
    xono_frame.pack(fill="x", padx=30, pady=10)
    
    tk.Label(xono_frame, text="XONO Specifications", 
            font=("Arial", 16, "bold"), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(0, 15))
    
    xono_specs = [
        ("OS:", "XONO OS UI Edition"),
        ("Version:", "1.1 (Beta)"),
        ("OS Build:", "26100.45946"),
        ("Developer:", "XONO Development Team")
    ]
    
    for label, value in xono_specs:
        spec_row = tk.Frame(xono_frame, bg="#2c2c2c")
        spec_row.pack(fill="x", pady=8)
        
        tk.Label(spec_row, text=label, 
                font=("Arial", 12, "bold"), bg="#2c2c2c", fg="#CCCCCC", 
                width=15, anchor="w").pack(side="left")
        
        tk.Label(spec_row, text=value, font=("Consolas", 11), 
                bg="#3c3c3c", fg="#4CAF50", padx=10, pady=5,
                anchor="w").pack(side="left", fill="x", expand=True)
    
    # System Status Section
    status_frame = tk.Frame(scrollable_frame, bg="#2c2c2c", relief="solid", 
                           borderwidth=1, padx=20, pady=15)
    status_frame.pack(fill="x", padx=30, pady=10)
    
    tk.Label(status_frame, text="System Status", 
            font=("Arial", 16, "bold"), bg="#2c2c2c", fg="white").pack(anchor="w", pady=(0, 15))
    
    def get_system_status():
        status = {}
        
        # CPU Usage
        if has_psutil:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                status["CPU Usage"] = f"{cpu_percent}%"
                status["CPU Status"] = "🟢 Normal" if cpu_percent < 80 else "🟡 High" if cpu_percent < 95 else "🔴 Critical"
            except:
                status["CPU Usage"] = "N/A"
                status["CPU Status"] = "⚪ Unknown"
        else:
            status["CPU Usage"] = "N/A"
            status["CPU Status"] = "⚪ Unknown"
        
        # Memory Usage
        if has_psutil:
            try:
                mem = psutil.virtual_memory()
                mem_percent = mem.percent
                status["Memory Usage"] = f"{mem_percent}%"
                status["Memory Status"] = "🟢 Normal" if mem_percent < 80 else "🟡 High" if mem_percent < 95 else "🔴 Critical"
            except:
                status["Memory Usage"] = "N/A"
                status["Memory Status"] = "⚪ Unknown"
        else:
            status["Memory Usage"] = "N/A"
            status["Memory Status"] = "⚪ Unknown"
        
        # Disk Usage
        try:
            usage = shutil.disk_usage(BASE_FOLDER if os.path.exists(BASE_FOLDER) else os.getcwd())
            disk_percent = (usage.used / usage.total) * 100
            status["Disk Usage"] = f"{disk_percent:.1f}%"
            status["Disk Status"] = "🟢 Normal" if disk_percent < 80 else "🟡 High" if disk_percent < 95 else "🔴 Critical"
        except:
            status["Disk Usage"] = "N/A"
            status["Disk Status"] = "⚪ Unknown"
        
        # System Uptime
        if has_psutil:
            try:
                uptime_seconds = psutil.boot_time()
                current_time = time.time()
                uptime_seconds = current_time - uptime_seconds
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                status["System Uptime"] = f"{days}d {hours}h"
            except:
                status["System Uptime"] = "Unknown"
        else:
            status["System Uptime"] = "Unknown"
        
        return status
    
    # Display system status
    system_status = get_system_status()
    
    status_items = [
        ("CPU Usage", "CPU Status"),
        ("Memory Usage", "Memory Status"),
        ("Disk Usage", "Disk Status"),
        ("System Uptime", "")
    ]
    
    for metric, status in status_items:
        status_row = tk.Frame(status_frame, bg="#2c2c2c")
        status_row.pack(fill="x", pady=8)
        
        metric_value = system_status.get(metric, "N/A")
        status_value = system_status.get(status, "")
        
        tk.Label(status_row, text=metric.replace("Usage", ""), 
                font=("Arial", 12, "bold"), bg="#2c2c2c", fg="#CCCCCC", 
                width=15, anchor="w").pack(side="left")
        
        tk.Label(status_row, text=metric_value, font=("Consolas", 11), 
                bg="#3c3c3c", fg="white", padx=10, pady=5,
                anchor="w", width=15).pack(side="left")
        
        if status_value:
            tk.Label(status_row, text=status_value, font=("Arial", 11), 
                    bg="#2c2c2c", fg=("#4CAF50" if "Normal" in status_value else 
                                    "#FF9800" if "High" in status_value else 
                                    "#f44336" if "Critical" in status_value else "#CCCCCC"),
                    padx=10, pady=5).pack(side="left", padx=10)
    
    # Refresh button
    def refresh_info():
        # You can add refresh functionality here
        messagebox.showinfo("Refresh", "Information refreshed!")
    
    refresh_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
    refresh_frame.pack(fill="x", pady=20, padx=30)
    
    tk.Button(refresh_frame, text="🔄 Refresh Information", 
             command=refresh_info, font=("Arial", 12, "bold"),
             bg="#2196F3", fg="white", padx=20, pady=10,
             cursor="hand2").pack()
    
    # Close button
    close_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
    close_frame.pack(fill="x", pady=(0, 30), padx=30)
    
    tk.Button(close_frame, text="Close", 
             command=about_window.destroy, font=("Arial", 12),
             bg="#f44336", fg="white", padx=30, pady=10,
             cursor="hand2").pack()
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Configure mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)



# -------------------
# Command Prompt App
# -------------------
def command_prompt():
    """Create Command Prompt application"""
    
    # Create command prompt window
    cmd_window = tk.Toplevel(root)
    cmd_window.title("XONO Command Prompt")
    cmd_window.geometry("800x600")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "Command Prompt icon.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            cmd_window.iconphoto(True, photo)
    except Exception as e:
        print(f"Could not load command prompt icon: {e}")
    
    # Configure dark theme colors
    BG_COLOR = "#0C0C0C"
    TEXT_COLOR = "#CCCCCC"
    PROMPT_COLOR = "#01A81A"  # Green like real cmd
    ERROR_COLOR = "#C50F1F"   # Red for errors
    COMMAND_COLOR = "#9A9A9A" # Light gray for commands
    
    cmd_window.configure(bg=BG_COLOR)
    
    # Main frame
    main_frame = tk.Frame(cmd_window, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Command history text widget
    history_frame = tk.Frame(main_frame, bg=BG_COLOR)
    history_frame.pack(fill="both", expand=True)
    
    history_scrollbar = tk.Scrollbar(history_frame)
    history_scrollbar.pack(side="right", fill="y")
    
    history_text = tk.Text(history_frame, wrap="word", font=("Consolas", 11),
                          bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                          yscrollcommand=history_scrollbar.set, state="disabled",
                          relief="flat", borderwidth=0)
    history_text.pack(side="left", fill="both", expand=True)
    history_scrollbar.config(command=history_text.yview)
    
    # Input frame
    input_frame = tk.Frame(main_frame, bg=BG_COLOR)
    input_frame.pack(fill="x", pady=(10, 0))
    
    # Prompt label
    prompt_label = tk.Label(input_frame, text="XONO:\\>", font=("Consolas", 11, "bold"),
                           bg=BG_COLOR, fg=PROMPT_COLOR)
    prompt_label.pack(side="left")
    
    # Command entry
    command_var = tk.StringVar()
    command_entry = tk.Entry(input_frame, textvariable=command_var, font=("Consolas", 11),
                            bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                            relief="flat", borderwidth=0, highlightthickness=1,
                            highlightbackground="#333333", highlightcolor="#555555")
    command_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
    command_entry.focus()
    
    # Command history list
    command_history = []
    history_index = -1
    
    # Available commands dictionary
    commands = {
        "/file viewer": open_file_viewer,
        "/notepad": notepad,
        "/settings": settings,
        "/about pc": about_pc,
        "/pc performances": lambda: None,  # Placeholder for now
        "/browser": lambda: None,  # Placeholder for now
        "/help": None,  # Will be handled separately
        "/clear": None,  # Will be handled separately
        "/exit": None  # Will be handled separately
    }
    
    # Help text
    help_text = """
Available Commands:
  /file viewer      - Open File Viewer application
  /notepad          - Open Notepad application
  /settings         - Open Settings application
  /about pc         - Open About Your PC application
  /pc performances  - Open PC Performances application
  /browser          - Open XONO Browser application
  /help             - Show this help message
  /clear            - Clear command history
  /exit             - Close Command Prompt

Type any command above and press Enter to execute.
"""
    
    def execute_command(event=None):
        """Execute the entered command"""
        nonlocal history_index
        command = command_var.get().strip()
        
        if not command:
            return
        
        # Add command to history
        command_history.append(command)
        history_index = -1
        
        # Display command in history
        history_text.config(state="normal")
        history_text.insert("end", f"XONO:\\> {command}\n", "prompt")
        
        # Execute command
        execute_specific_command(command)
        
        # Clear input
        command_var.set("")
        
        # Scroll to bottom
        history_text.see("end")
        history_text.config(state="disabled")
    
    def execute_specific_command(cmd):
        """Execute a specific command"""
        cmd_lower = cmd.lower()
        
        if cmd_lower == "/help":
            display_help()
        elif cmd_lower == "/clear":
            clear_history()
        elif cmd_lower == "/exit":
            cmd_window.destroy()
        elif cmd_lower in commands:
            # Execute the command function
            func = commands[cmd_lower]
            if func:
                history_text.insert("end", f"Opening {cmd_lower[1:]}...\n", "output")
                cmd_window.after(100, func)  # Open app after a short delay
            else:
                history_text.insert("end", f"Command '{cmd}' is not yet implemented.\n", "error")
        else:
            history_text.insert("end", f"'{cmd}' is not recognized as an internal or external command.\n", "error")
            history_text.insert("end", f"Type '/help' for a list of available commands.\n", "output")
    
    def display_help():
        """Display help message"""
        history_text.insert("end", help_text, "help")
    
    def clear_history():
        """Clear command history display"""
        history_text.config(state="normal")
        history_text.delete("1.0", "end")
        history_text.config(state="disabled")
    
    def navigate_history(event):
        """Navigate through command history"""
        nonlocal history_index
        
        if not command_history:
            return
        
        if event.keysym == "Up":
            if history_index < len(command_history) - 1:
                history_index += 1
            elif history_index == -1:
                history_index = 0
        elif event.keysym == "Down":
            if history_index > 0:
                history_index -= 1
            elif history_index == 0:
                history_index = -1
                command_var.set("")
                return
            elif history_index == -1:
                return
        
        if history_index >= 0 and history_index < len(command_history):
            command_var.set(command_history[-(history_index + 1)])
            command_entry.icursor(tk.END)
    
    def auto_complete(event=None):
        """Auto-complete command"""
        current = command_var.get().strip()
        if not current:
            return
        
        # Find matching commands
        matches = [cmd for cmd in commands.keys() if cmd.startswith(current)]
        
        if len(matches) == 1:
            command_var.set(matches[0])
            command_entry.icursor(tk.END)
        elif len(matches) > 1:
            # Show possible completions
            history_text.config(state="normal")
            history_text.insert("end", f"\nPossible completions:\n", "output")
            for match in matches:
                history_text.insert("end", f"  {match}\n", "help")
            history_text.insert("end", "\n")
            history_text.see("end")
            history_text.config(state="disabled")
    
    # Configure text tags for different colors
    history_text.tag_config("prompt", foreground=PROMPT_COLOR, font=("Consolas", 11, "bold"))
    history_text.tag_config("output", foreground=TEXT_COLOR)
    history_text.tag_config("error", foreground=ERROR_COLOR)
    history_text.tag_config("help", foreground=COMMAND_COLOR)
    history_text.tag_config("command", foreground="#569CD6")  # Blue for commands
    
    # Welcome message
    history_text.config(state="normal")
    history_text.insert("end", "XONO Command Prompt v1.1\n", "prompt")
    history_text.insert("end", "Copyright (c) 2024 XONO Development Team. All rights reserved.\n\n", "output")
    history_text.insert("end", "Type '/help' for a list of available commands.\n\n", "help")
    history_text.config(state="disabled")
    
    # Bind keys
    command_entry.bind("<Return>", execute_command)
    command_entry.bind("<Up>", navigate_history)
    command_entry.bind("<Down>", navigate_history)
    command_entry.bind("<Tab>", auto_complete)
    
    # Bind Ctrl+C to clear (like real cmd)
    cmd_window.bind('<Control-c>', lambda e: command_var.set(""))
    cmd_window.bind('<Control-C>', lambda e: command_var.set(""))
    
    # Bind Alt+F4 to exit
    cmd_window.bind('<Alt-F4>', lambda e: cmd_window.destroy())
    
    # Add right-click menu
    def show_context_menu(event):
        context_menu = tk.Menu(cmd_window, tearoff=0, bg="#2d2d2d", fg=TEXT_COLOR,
                              activebackground="#3d3d3d", activeforeground="white")
        context_menu.add_command(label="Copy", command=lambda: cmd_window.clipboard_append(history_text.selection_get()) if history_text.tag_ranges("sel") else None)
        context_menu.add_command(label="Paste", command=lambda: command_entry.event_generate('<<Paste>>'))
        context_menu.add_separator()
        context_menu.add_command(label="Clear All", command=clear_history)
        context_menu.add_command(label="Select All", command=lambda: history_text.tag_add("sel", "1.0", "end"))
        context_menu.tk_popup(event.x_root, event.y_root)
    
    history_text.bind("<Button-3>", show_context_menu)
    
    # Make window modal
    cmd_window.transient(root)
    cmd_window.grab_set()



# -----------------------
# PC Performances App
# -----------------------
def pc_performances():
    """Create PC Performances application"""
    
    # Try to import required modules
    try:
        import psutil
        import platform
        import subprocess
        from datetime import datetime
        has_psutil = True
    except ImportError:
        has_psutil = False
    
    # Create performances window
    perf_window = tk.Toplevel(root)
    perf_window.title("PC Performances")
    perf_window.geometry("700x800")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "PC Performances icon.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            perf_window.iconphoto(True, photo)
    except Exception as e:
        print(f"Could not load performances icon: {e}")
    
    # Configure dark theme colors
    BG_COLOR = "#1a1a1a"
    CARD_BG = "#2c2c2c"
    TEXT_COLOR = "white"
    GREEN_COLOR = "#4CAF50"
    YELLOW_COLOR = "#FF9800"
    RED_COLOR = "#f44336"
    BLUE_COLOR = "#2196F3"
    
    perf_window.configure(bg=BG_COLOR)
    
    # Main frame with scrollbar
    main_frame = tk.Frame(perf_window, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True)
    
    # Create canvas for scrollable content
    canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Center container
    center_container = tk.Frame(scrollable_frame, bg=BG_COLOR)
    center_container.pack(expand=True)
    
    inner_frame = tk.Frame(center_container, bg=BG_COLOR, width=600)
    inner_frame.pack(expand=True)
    
    # Title section
    title_frame = tk.Frame(inner_frame, bg=BG_COLOR)
    title_frame.pack(fill="x", pady=(20, 10))
    
    tk.Label(title_frame, text="===== PC Performances =====", 
            font=("Consolas", 20, "bold"), bg=BG_COLOR, fg="#4CAF50").pack()
    
    tk.Label(title_frame, text="Real-time System Performance Monitor", 
            font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 20))
    
    # Function to get WiFi name
    def get_wifi_name():
        """Get connected WiFi network name"""
        try:
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("utf-8")
            for line in result.split('\n'):
                if "SSID" in line:
                    ssid = line.split(":")[1].strip()
                    return ssid
            return "No Wi-Fi connected"
        except subprocess.CalledProcessError:
            return "Error: Could not retrieve Wi-Fi name."
        except IndexError:
            return "Error: Could not parse netsh output."
        except Exception:
            return "Wi-Fi information unavailable"
    
    # Function to get system info
    def get_system_info():
        """Get all system performance information"""
        info = {}
        
        # CPU Usage
        if has_psutil:
            try:
                cpu_usage = psutil.cpu_percent(interval=0.5)
                info["cpu_usage"] = cpu_usage
                info["cpu_status"] = "🟢 Normal" if cpu_usage < 70 else "🟡 High" if cpu_usage < 90 else "🔴 Critical"
            except:
                info["cpu_usage"] = "Unknown"
                info["cpu_status"] = "⚪ Unknown"
        else:
            info["cpu_usage"] = "N/A"
            info["cpu_status"] = "⚪ Unknown"
        
        # CPU Name
        try:
            cpu_name = platform.processor() or "Unknown CPU"
            info["cpu_name"] = cpu_name
        except:
            info["cpu_name"] = "Unknown CPU"
        
        # CPU Cores
        try:
            cpu_cores = os.cpu_count() or "Unknown"
            info["cpu_cores"] = cpu_cores
        except:
            info["cpu_cores"] = "Unknown"
        
        # RAM Usage
        if has_psutil:
            try:
                mem_info = psutil.virtual_memory()
                info["ram_usage"] = mem_info.percent
                info["ram_used_gb"] = round(mem_info.used / (1024**3), 2)
                info["ram_total_gb"] = round(mem_info.total / (1024**3), 2)
                info["ram_status"] = "🟢 Normal" if mem_info.percent < 70 else "🟡 High" if mem_info.percent < 90 else "🔴 Critical"
            except:
                info["ram_usage"] = "Unknown"
                info["ram_status"] = "⚪ Unknown"
        else:
            info["ram_usage"] = "N/A"
            info["ram_status"] = "⚪ Unknown"
        
        # Battery Info
        if has_psutil:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info["battery_percent"] = battery.percent
                    info["battery_plugged"] = battery.power_plugged
                    info["battery_status"] = "🔌 Charging" if battery.power_plugged else "🔋 Discharging"
                else:
                    info["battery_percent"] = "No battery"
                    info["battery_status"] = "⚪ No battery"
            except:
                info["battery_percent"] = "Unknown"
                info["battery_status"] = "⚪ Unknown"
        else:
            info["battery_percent"] = "N/A"
            info["battery_status"] = "⚪ Unknown"
        
        # Date & Time
        try:
            now = datetime.now()
            info["date"] = now.strftime("%Y-%m-%d")
            info["time"] = now.strftime("%H:%M:%S")
            info["day"] = now.strftime("%A")
        except:
            info["date"] = "Unknown"
            info["time"] = "Unknown"
            info["day"] = "Unknown"
        
        # Internet Connection
        info["wifi_name"] = get_wifi_name()
        
        # Disk Usage
        try:
            usage = shutil.disk_usage(BASE_FOLDER if os.path.exists(BASE_FOLDER) else os.getcwd())
            info["disk_usage"] = (usage.used / usage.total) * 100
            info["disk_free_gb"] = round(usage.free / (1024**3), 2)
            info["disk_total_gb"] = round(usage.total / (1024**3), 2)
            info["disk_status"] = "🟢 Normal" if info["disk_usage"] < 70 else "🟡 High" if info["disk_usage"] < 90 else "🔴 Critical"
        except:
            info["disk_usage"] = "Unknown"
            info["disk_status"] = "⚪ Unknown"
        
        # System Uptime
        if has_psutil:
            try:
                uptime_seconds = psutil.boot_time()
                current_time = time.time()
                uptime_seconds = current_time - uptime_seconds
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                info["uptime"] = f"{days}d {hours}h {minutes}m"
            except:
                info["uptime"] = "Unknown"
        else:
            info["uptime"] = "Unknown"
        
        return info
    
    # CPU Performance Card
    cpu_frame = tk.Frame(inner_frame, bg=CARD_BG, relief="solid", 
                        borderwidth=1, padx=20, pady=15)
    cpu_frame.pack(fill="x", pady=10)
    
    tk.Label(cpu_frame, text="💻 CPU Performance", 
            font=("Arial", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="center", pady=(0, 15))
    
    # CPU info will be updated dynamically
    cpu_info_frame = tk.Frame(cpu_frame, bg=CARD_BG)
    cpu_info_frame.pack(fill="x")
    
    cpu_name_label = tk.Label(cpu_info_frame, text="", font=("Arial", 11), 
                             bg=CARD_BG, fg="#CCCCCC")
    cpu_name_label.pack(pady=(0, 10))
    
    cpu_usage_frame = tk.Frame(cpu_frame, bg=CARD_BG)
    cpu_usage_frame.pack(fill="x", pady=10)
    
    cpu_usage_label = tk.Label(cpu_usage_frame, text="", font=("Arial", 14, "bold"), 
                              bg=CARD_BG, fg=TEXT_COLOR)
    cpu_usage_label.pack(side="left")
    
    cpu_status_label = tk.Label(cpu_usage_frame, text="", font=("Arial", 14), 
                               bg=CARD_BG, fg=GREEN_COLOR)
    cpu_status_label.pack(side="left", padx=10)
    
    # CPU Usage Progress Bar
    cpu_progress_frame = tk.Frame(cpu_frame, bg=CARD_BG)
    cpu_progress_frame.pack(fill="x", pady=10)
    
    cpu_progress_canvas = tk.Canvas(cpu_progress_frame, height=20, bg=CARD_BG, 
                                   highlightthickness=0)
    cpu_progress_canvas.pack(fill="x")
    
    # RAM Performance Card
    ram_frame = tk.Frame(inner_frame, bg=CARD_BG, relief="solid", 
                        borderwidth=1, padx=20, pady=15)
    ram_frame.pack(fill="x", pady=10)
    
    tk.Label(ram_frame, text="🧠 Memory (RAM) Performance", 
            font=("Arial", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="center", pady=(0, 15))
    
    ram_usage_frame = tk.Frame(ram_frame, bg=CARD_BG)
    ram_usage_frame.pack(fill="x", pady=10)
    
    ram_usage_label = tk.Label(ram_usage_frame, text="", font=("Arial", 14, "bold"), 
                              bg=CARD_BG, fg=TEXT_COLOR)
    ram_usage_label.pack(side="left")
    
    ram_status_label = tk.Label(ram_usage_frame, text="", font=("Arial", 14), 
                               bg=CARD_BG, fg=GREEN_COLOR)
    ram_status_label.pack(side="left", padx=10)
    
    ram_details_label = tk.Label(ram_frame, text="", font=("Arial", 11), 
                                bg=CARD_BG, fg="#CCCCCC")
    ram_details_label.pack(pady=(0, 10))
    
    # RAM Usage Progress Bar
    ram_progress_frame = tk.Frame(ram_frame, bg=CARD_BG)
    ram_progress_frame.pack(fill="x", pady=10)
    
    ram_progress_canvas = tk.Canvas(ram_progress_frame, height=20, bg=CARD_BG, 
                                   highlightthickness=0)
    ram_progress_canvas.pack(fill="x")
    
    # Battery & Power Card
    battery_frame = tk.Frame(inner_frame, bg=CARD_BG, relief="solid", 
                           borderwidth=1, padx=20, pady=15)
    battery_frame.pack(fill="x", pady=10)
    
    tk.Label(battery_frame, text="🔋 Battery & Power", 
            font=("Arial", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="center", pady=(0, 15))
    
    battery_info_frame = tk.Frame(battery_frame, bg=CARD_BG)
    battery_info_frame.pack(fill="x", pady=10)
    
    battery_percent_label = tk.Label(battery_info_frame, text="", font=("Arial", 14, "bold"), 
                                    bg=CARD_BG, fg=TEXT_COLOR)
    battery_percent_label.pack(side="left")
    
    battery_status_label = tk.Label(battery_info_frame, text="", font=("Arial", 14), 
                                   bg=CARD_BG, fg=GREEN_COLOR)
    battery_status_label.pack(side="left", padx=10)
    
    # Battery Progress Bar
    battery_progress_frame = tk.Frame(battery_frame, bg=CARD_BG)
    battery_progress_frame.pack(fill="x", pady=10)
    
    battery_progress_canvas = tk.Canvas(battery_progress_frame, height=20, bg=CARD_BG, 
                                       highlightthickness=0)
    battery_progress_canvas.pack(fill="x")
    
    # System Info Card
    system_frame = tk.Frame(inner_frame, bg=CARD_BG, relief="solid", 
                           borderwidth=1, padx=20, pady=15)
    system_frame.pack(fill="x", pady=10)
    
    tk.Label(system_frame, text="🖥️ System Information", 
            font=("Arial", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="center", pady=(0, 15))
    
    # Create system info labels
    system_info_labels = {}
    system_items = [
        ("📅 Date", "date"),
        ("🕒 Time", "time"),
        ("📡 Internet", "wifi_name"),
        ("⏱️ Uptime", "uptime"),
        ("💾 Disk Usage", "disk_status")
    ]
    
    for icon_label, data_key in system_items:
        info_row = tk.Frame(system_frame, bg=CARD_BG)
        info_row.pack(fill="x", pady=8)
        
        tk.Label(info_row, text=icon_label, font=("Arial", 12, "bold"), 
                bg=CARD_BG, fg="#CCCCCC", width=15, anchor="w").pack(side="left", padx=(0, 10))
        
        value_label = tk.Label(info_row, text="", font=("Consolas", 11), 
                              bg="#3c3c3c", fg="white", padx=10, pady=5,
                              anchor="w")
        value_label.pack(side="left", fill="x", expand=True)
        
        system_info_labels[data_key] = value_label
    
    # Disk Usage Info
    disk_info_label = tk.Label(system_frame, text="", font=("Arial", 11), 
                              bg=CARD_BG, fg="#CCCCCC")
    disk_info_label.pack(pady=(10, 0))
    
    # Function to update progress bar
    def draw_progress_bar(canvas, percentage, width=400, height=20):
        """Draw a colored progress bar"""
        canvas.delete("all")
        
        # Determine color based on percentage
        if percentage <= 50:
            color = GREEN_COLOR
        elif percentage <= 80:
            color = YELLOW_COLOR
        else:
            color = RED_COLOR
        
        # Draw background
        canvas.create_rectangle(0, 0, width, height, fill="#3c3c3c", outline="")
        
        # Draw progress
        progress_width = (percentage / 100) * width
        canvas.create_rectangle(0, 0, progress_width, height, fill=color, outline="")
        
        # Draw percentage text
        canvas.create_text(width/2, height/2, text=f"{percentage:.1f}%", 
                          fill="white", font=("Arial", 10, "bold"))
    
    # Function to update all performance data
    def update_performance_data():
        """Update all performance metrics"""
        info = get_system_info()
        
        # Update CPU info
        cpu_name_label.config(text=f"CPU: {info.get('cpu_name', 'Unknown')} ({info.get('cpu_cores', '?')} cores)")
        
        if isinstance(info.get('cpu_usage'), (int, float)):
            cpu_usage = info['cpu_usage']
            cpu_usage_label.config(text=f"CPU Usage: {cpu_usage:.1f}%")
            cpu_status_label.config(text=info.get('cpu_status', ''))
            draw_progress_bar(cpu_progress_canvas, cpu_usage)
        else:
            cpu_usage_label.config(text=f"CPU Usage: {info.get('cpu_usage', 'Unknown')}")
            cpu_status_label.config(text="")
        
        # Update RAM info
        if isinstance(info.get('ram_usage'), (int, float)):
            ram_usage = info['ram_usage']
            ram_usage_label.config(text=f"RAM Usage: {ram_usage:.1f}%")
            ram_status_label.config(text=info.get('ram_status', ''))
            ram_details_label.config(text=f"Using {info.get('ram_used_gb', '?')} GB of {info.get('ram_total_gb', '?')} GB")
            draw_progress_bar(ram_progress_canvas, ram_usage)
        else:
            ram_usage_label.config(text=f"RAM Usage: {info.get('ram_usage', 'Unknown')}")
            ram_status_label.config(text="")
            ram_details_label.config(text="")
        
        # Update Battery info
        battery_percent = info.get('battery_percent', 'Unknown')
        if isinstance(battery_percent, (int, float)):
            battery_percent_label.config(text=f"Battery: {battery_percent:.0f}%")
            battery_status_label.config(text=info.get('battery_status', ''))
            draw_progress_bar(battery_progress_canvas, battery_percent)
        else:
            battery_percent_label.config(text=f"Battery: {battery_percent}")
            battery_status_label.config(text=info.get('battery_status', ''))
        
        # Update System info
        for key, label in system_info_labels.items():
            value = info.get(key, 'Unknown')
            if key == 'disk_status':
                # For disk status, show both status and usage percentage
                disk_usage = info.get('disk_usage', '?')
                if isinstance(disk_usage, (int, float)):
                    value = f"{info.get('disk_status', '')} ({disk_usage:.1f}%)"
                else:
                    value = f"{info.get('disk_status', 'Unknown')}"
            label.config(text=str(value))
        
        # Update disk info details
        disk_usage = info.get('disk_usage', '?')
        if isinstance(disk_usage, (int, float)):
            disk_info_label.config(text=f"Free: {info.get('disk_free_gb', '?')} GB of {info.get('disk_total_gb', '?')} GB")
        else:
            disk_info_label.config(text="")
        
        # Schedule next update
        perf_window.after(2000, update_performance_data)  # Update every 2 seconds
    
    # Start updating data
    update_performance_data()
    
    # Control buttons frame
    buttons_frame = tk.Frame(inner_frame, bg=BG_COLOR)
    buttons_frame.pack(fill="x", pady=20)
    
    def refresh_now():
        """Force refresh all data"""
        update_performance_data()
    
    def close_app():
        """Close the performances window"""
        perf_window.destroy()
    
    # Buttons
    tk.Button(buttons_frame, text="🔄 Refresh Now", 
             command=refresh_now, font=("Arial", 12, "bold"),
             bg=BLUE_COLOR, fg="white", padx=20, pady=10,
             cursor="hand2").pack(side="left", padx=10)
    
    tk.Button(buttons_frame, text="📊 Performance Log", 
             command=lambda: messagebox.showinfo("Info", "Performance logging feature coming soon!"),
             font=("Arial", 12), bg="#9C27B0", fg="white", 
             padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)
    
    tk.Button(buttons_frame, text="❌ Close", 
             command=close_app, font=("Arial", 12),
             bg=RED_COLOR, fg="white", padx=30, pady=10,
             cursor="hand2").pack(side="right", padx=10)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Configure mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)



# -------------------
# XONO Browser App
# -------------------
def xono_browser():
    """Create XONO Browser application"""
    
    # Try to import required modules
    try:
        import requests
        import socket
        has_requests = True
        has_socket = True
    except ImportError:
        has_requests = False
        has_socket = False
    
    # Create browser window
    browser_window = tk.Toplevel(root)
    browser_window.title("XONO Browser")
    browser_window.geometry("900x700")
    
    # Try to set icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "XONO Brower icon.ico")
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            browser_window.iconphoto(True, photo)
    except Exception as e:
        print(f"Could not load browser icon: {e}")
    
    # Configure colors
    BG_COLOR = "#1a1a1a"
    CARD_BG = "#2c2c2c"
    TEXT_COLOR = "white"
    ACCENT_COLOR = "#4CAF50"
    ERROR_COLOR = "#f44336"
    INFO_COLOR = "#2196F3"
    INPUT_BG = "#3c3c3c"
    
    browser_window.configure(bg=BG_COLOR)
    
    # Main frame
    main_frame = tk.Frame(browser_window, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title section
    title_frame = tk.Frame(main_frame, bg=BG_COLOR)
    title_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(title_frame, text="=+=+= XONO Browser =+=+=", 
            font=("Consolas", 24, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR).pack()
    
    tk.Label(title_frame, text="Your Personal Web Browser", 
            font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(5, 10))
    
    # Options card
    options_frame = tk.Frame(main_frame, bg=CARD_BG, relief="solid", 
                           borderwidth=1, padx=30, pady=20)
    options_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(options_frame, text="Browser Options", 
            font=("Arial", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="center", pady=(0, 15))
    
    # Create option buttons
    option_style = {
        "font": ("Arial", 12, "bold"),
        "width": 25,
        "height": 2,
        "cursor": "hand2",
        "pady": 10
    }
    
    # Option 1: Search anything
    def open_search_panel():
        """Open search panel"""
        # Hide options
        options_frame.pack_forget()
        back_button.pack(pady=(0, 20))
        search_frame.pack(fill="both", expand=True)
        search_entry.focus()
    
    search_btn = tk.Button(options_frame, text="🔍 Search Anything", 
                          command=open_search_panel, bg=INFO_COLOR, fg="white",
                          activebackground="#1976d2", activeforeground="white",
                          **option_style)
    search_btn.pack(pady=10)
    
    # Option 2: Check internet connection
    def check_internet():
        """Check internet connection"""
        # Function to check internet
        def has_internet(host="8.8.8.8", port=53, timeout=2):
            if not has_socket:
                return False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(timeout)
                s.connect((host, port))
                s.close()
                return True
            except Exception:
                return False
        
        up = has_internet()
        if up:
            messagebox.showinfo("Internet Check", "✅ Internet: Available", parent=browser_window)
        else:
            messagebox.showwarning("Internet Check", "❌ Internet: Not available", parent=browser_window)
    
    internet_btn = tk.Button(options_frame, text="🌐 Check Internet Connection", 
                            command=check_internet, bg="#9C27B0", fg="white",
                            activebackground="#7b1fa2", activeforeground="white",
                            **option_style)
    internet_btn.pack(pady=10)
    
    # Option 3: Return to Desktop
    def return_to_desktop():
        browser_window.destroy()
    
    return_btn = tk.Button(options_frame, text="🏠 Return to Desktop", 
                          command=return_to_desktop, bg="#f44336", fg="white",
                          activebackground="#d32f2f", activeforeground="white",
                          **option_style)
    return_btn.pack(pady=10)
    
    # Back button (initially hidden)
    back_button = tk.Button(main_frame, text="← Back to Options", 
                           command=lambda: [search_frame.pack_forget(), 
                                          back_button.pack_forget(),
                                          options_frame.pack(fill="x", pady=(0, 20))],
                           font=("Arial", 11), bg="#555555", fg="white",
                           padx=15, pady=5, cursor="hand2")
    
    # Search Panel (initially hidden)
    search_frame = tk.Frame(main_frame, bg=BG_COLOR)
    
    # Search input area
    search_input_frame = tk.Frame(search_frame, bg=BG_COLOR)
    search_input_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(search_input_frame, text="Enter search topic:", 
            font=("Arial", 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 10))
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_input_frame, textvariable=search_var, 
                           font=("Arial", 12), bg=INPUT_BG, fg=TEXT_COLOR,
                           insertbackground=TEXT_COLOR, width=50)
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    def perform_search():
        """Perform the search"""
        query = search_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search topic!", parent=browser_window)
            return
        
        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = tk.Label(results_frame, text="🔍 Searching... Please wait...", 
                                font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
        loading_label.pack(pady=20)
        browser_window.update()
        
        # Check internet connection
        def has_internet(host="8.8.8.8", port=53, timeout=2):
            if not has_socket:
                return False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(timeout)
                s.connect((host, port))
                s.close()
                return True
            except Exception:
                return False
        
        # Try to get Wikipedia summary
        result_text = ""
        wiki_found = False
        
        if has_internet() and has_requests:
            try:
                safe_query = query.strip().replace(" ", "_")
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe_query}"
                headers = {"User-Agent": "XONO-Browser/1.0"}
                r = requests.get(url, timeout=6, headers=headers)
                
                if r.status_code == 200:
                    data = r.json()
                    extract = data.get("extract")
                    if extract:
                        # Get first 3 sentences
                        sentences = extract.split(". ")
                        short = ". ".join(sentences[:3]).strip()
                        if not short.endswith("."):
                            short += "."
                        result_text = short
                        wiki_found = True
                    else:
                        result_text = "⚠️ No detailed information found for that exact title."
                else:
                    result_text = "⚠️ Could not find information.."
            except Exception as e:
                result_text = f"⚠️ Error fetching information: {str(e)}"
        else:
            result_text = "❌ No internet connection or requests module not available."
        
        # Clear loading and show results
        loading_label.destroy()
        
        # Results card
        results_card = tk.Frame(results_frame, bg=CARD_BG, relief="solid", 
                               borderwidth=1, padx=20, pady=20)
        results_card.pack(fill="both", expand=True)
        
        if wiki_found:
            # Show Wikipedia results
            tk.Label(results_card, text="📚 Summary", 
                    font=("Arial", 16, "bold"), bg=CARD_BG, fg=ACCENT_COLOR).pack(anchor="w", pady=(0, 15))
            
            # Result text with scrollbar
            text_frame = tk.Frame(results_card, bg=CARD_BG)
            text_frame.pack(fill="both", expand=True)
            
            text_scrollbar = tk.Scrollbar(text_frame)
            text_scrollbar.pack(side="right", fill="y")
            
            result_text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 11),
                                        bg="#3c3c3c", fg=TEXT_COLOR, height=10,
                                        yscrollcommand=text_scrollbar.set)
            result_text_widget.insert("1.0", result_text)
            result_text_widget.config(state="disabled")
            result_text_widget.pack(side="left", fill="both", expand=True)
            text_scrollbar.config(command=result_text_widget.yview)
            
            # Source info
            tk.Label(results_card, text="Source: XONO Browser", 
                    font=("Arial", 10), bg=CARD_BG, fg="#888888").pack(anchor="w", pady=(10, 0))
            
        else:
            # Show alternative search option
            tk.Label(results_card, text="🔍 Search Results", 
                    font=("Arial", 16, "bold"), bg=CARD_BG, fg=INFO_COLOR).pack(anchor="w", pady=(0, 15))
            
            tk.Label(results_card, text=result_text, 
                    font=("Arial", 12), bg=CARD_BG, fg=TEXT_COLOR, wraplength=600,
                    justify="left").pack(fill="x", pady=(0, 20))
            
            # Google search link
            google_query = query.replace(" ", "+")
            google_url = f"https://www.google.com/search?q={google_query}"
            
            link_frame = tk.Frame(results_card, bg=CARD_BG)
            link_frame.pack(fill="x", pady=10)
            
            tk.Label(link_frame, text="Try this Google search:", 
                    font=("Arial", 12, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 5))
            
            # URL display with copy button
            url_frame = tk.Frame(link_frame, bg=CARD_BG)
            url_frame.pack(fill="x", pady=5)
            
            url_label = tk.Label(url_frame, text=google_url, font=("Consolas", 10), 
                                bg="#3c3c3c", fg="#4CAF50", padx=10, pady=5,
                                anchor="w", relief="solid", borderwidth=1)
            url_label.pack(side="left", fill="x", expand=True)
            
            def copy_url():
                browser_window.clipboard_clear()
                browser_window.clipboard_append(google_url)
                url_label.config(fg="#FF9800")
                browser_window.after(1000, lambda: url_label.config(fg="#4CAF50"))
            
            tk.Button(url_frame, text="📋 Copy", font=("Arial", 9), 
                     bg=INFO_COLOR, fg="white", relief="flat", cursor="hand2",
                     command=copy_url).pack(side="left", padx=5)
            
            # Open in browser button
            def open_in_browser():
                try:
                    import webbrowser
                    webbrowser.open(google_url)
                except:
                    messagebox.showinfo("Open Browser", f"Please open this URL manually:\n{google_url}", parent=browser_window)
            
            tk.Button(link_frame, text="🌐 Open in Browser", 
                     command=open_in_browser, font=("Arial", 11, "bold"),
                     bg=ACCENT_COLOR, fg="white", padx=20, pady=8,
                     cursor="hand2").pack(pady=(10, 0))
        
        # New search button
        def new_search():
            search_var.set("")
            results_card.destroy()
            search_entry.focus()
        
        tk.Button(results_card, text="🔍 New Search", 
                 command=new_search, font=("Arial", 11),
                 bg="#9C27B0", fg="white", padx=15, pady=5,
                 cursor="hand2").pack(pady=(20, 0))
    
    search_btn = tk.Button(search_input_frame, text="Search", 
                          command=perform_search, font=("Arial", 12, "bold"),
                          bg=ACCENT_COLOR, fg="white", padx=20, pady=5,
                          cursor="hand2")
    search_btn.pack(side="left")
    
    # Bind Enter key to search
    search_entry.bind("<Return>", lambda e: perform_search())
    
    # Results area
    results_frame = tk.Frame(search_frame, bg=BG_COLOR)
    results_frame.pack(fill="both", expand=True)
    
    # Initial message in results area
    tk.Label(results_frame, text="🔍 Enter a search term above and click Search", 
            font=("Arial", 12), bg=BG_COLOR, fg="#888888", pady=50).pack()
    
    # Status bar at bottom
    status_frame = tk.Frame(main_frame, bg="#2c2c2c", height=30)
    status_frame.pack(side="bottom", fill="x", pady=(10, 0))
    status_frame.pack_propagate(False)
    
    def update_status():
        """Update status bar with connection info"""
        def has_internet():
            if not has_socket:
                return False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1)
                s.connect(("8.8.8.8", 53))
                s.close()
                return True
            except:
                return False
        
        status = "✅ Online" if has_internet() else "❌ Offline"
        status_label.config(text=f"Status: {status} | XONO Browser v1.1")
        browser_window.after(5000, update_status)  # Update every 5 seconds
    
    status_label = tk.Label(status_frame, text="", font=("Arial", 9), 
                           bg="#2c2c2c", fg="#CCCCCC")
    status_label.pack(side="left", padx=10)
    
    # Start status updates
    update_status()


    

# ===============
# Start Menu
# ===============
def open_start_menu():
    """Open Windows 8-style Start Menu with tile layout"""
    
    # Create start menu window
    start_window = tk.Toplevel(root)
    start_window.title("Start Menu")
    start_window.attributes('-fullscreen', True)  # Full screen start menu
    
    # Remove window decorations for true full screen
    start_window.overrideredirect(True)
    
    # Set background color
    start_window.configure(bg="#1a1a1a")
    
    # Main container frame
    main_container = tk.Frame(start_window, bg="#1a1a1a")
    main_container.pack(fill="both", expand=True, padx=50, pady=50)
    
    # Try to load background image
    try:
        bg_path = os.path.join(os.path.dirname(__file__), "assets", "start_menu_bg.png")
        if os.path.exists(bg_path):
            bg_image = Image.open(bg_path)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(start_window, image=bg_photo)
            bg_label.image = bg_photo  # Keep reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            main_container.lift()  # Bring tiles above background
    except:
        pass
    
    # Header with time and date
    header_frame = tk.Frame(main_container, bg="#1a1a1a")
    header_frame.pack(fill="x", pady=(0, 30))
    
    # Time label
    time_label = tk.Label(header_frame, font=("Arial", 48, "bold"), 
                         fg="white", bg="#1a1a1a")
    time_label.pack(side="left", padx=20)
    
    # Date label
    date_label = tk.Label(header_frame, font=("Arial", 24), 
                         fg="#4CAF50", bg="#1a1a1a")
    date_label.pack(side="left", padx=20)
    
    # Update time function
    def update_time():
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%A, %B %d, %Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        start_window.after(1000, update_time)  # Update every second
    
    update_time()
    
    # User info frame
    user_frame = tk.Frame(main_container, bg="#2c2c2c", relief="flat", borderwidth=2)
    user_frame.pack(side="left", fill="y", padx=(0, 30))
    
    # Load user info
    username = "User"
    if os.path.exists(SETUP_FILE):
        with open(SETUP_FILE, "r", encoding="utf-8") as sf:
            setup_data = json.load(sf)
            username = setup_data.get("username", "User")
    
    # User profile section
    profile_frame = tk.Frame(user_frame, bg="#2c2c2c")
    profile_frame.pack(pady=30, padx=20)
    
    # User icon (placeholder)
    user_icon_label = tk.Label(profile_frame, text="👤", font=("Arial", 48), 
                              bg="#2c2c2c", fg="white")
    user_icon_label.pack()
    
    # Username
    username_label = tk.Label(profile_frame, text=username, font=("Arial", 18, "bold"), 
                            bg="#2c2c2c", fg="white")
    username_label.pack(pady=10)
    
    # User email/status
    status_label = tk.Label(profile_frame, text="Online", font=("Arial", 12), 
                           bg="#2c2c2c", fg="#4CAF50")
    status_label.pack()
    
    # User actions
    actions_frame = tk.Frame(user_frame, bg="#2c2c2c")
    actions_frame.pack(pady=30, padx=20, fill="x")
    
    user_actions = [
        ("Account Settings", "#"),
        ("Change Password", "#")
    ]
    
    for action_text, _ in user_actions:
        btn = tk.Button(actions_frame, text=action_text, font=("Arial", 12),
                       bg="#3c3c3c", fg="white", activebackground="#4c4c4c",
                       activeforeground="white", relief="flat", padx=20, pady=10,
                       width=20, cursor="hand2")
        btn.pack(pady=5)
    
    # Tiles container
    tiles_container = tk.Frame(main_container, bg="#1a1a1a")
    tiles_container.pack(side="left", fill="both", expand=True)
    
    # Tiles grid
    tiles_frame = tk.Frame(tiles_container, bg="#1a1a1a")
    tiles_frame.pack(expand=True)
    
    # Define tiles (name, command, color)
    tiles = [
        ("File Viewer", open_file_viewer, "#2196F3"),
        ("Calculator", calculator, "#4CAF50"),
        ("Notepad", notepad, "#FF9800"),
        ("Settings", settings, "#9C27B0"),
        ("About PC", about_pc, "#009688"),
        ("Command Prompt", command_prompt, "#795548"),
        ("PC Performance", pc_performances, "#F44336"),
        ("XONO Browser", xono_browser, "#3F51B5"),
    ]
    
    # Load tile icons
    tile_icons = {}
    for tile_name, _, _ in tiles:
        icon_name = tile_name.replace(" ", "_").lower() + "_icon.png"
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", icon_name)
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                img = img.resize((40, 40), Image.Resampling.LANCZOS)
                tile_icons[tile_name] = ImageTk.PhotoImage(img)
            except:
                tile_icons[tile_name] = None
        else:
            tile_icons[tile_name] = None
    
    # Create tiles in 4x3 grid
    for i, (tile_name, tile_command, tile_color) in enumerate(tiles):
        row = i // 4
        col = i % 4
        
        tile_frame = tk.Frame(tiles_frame, bg=tile_color, relief="flat", 
                            borderwidth=0, highlightthickness=2,
                            highlightbackground="#ffffff", highlightcolor="#ffffff")
        tile_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Make tiles expandable
        tiles_frame.grid_rowconfigure(row, weight=1, minsize=150)
        tiles_frame.grid_columnconfigure(col, weight=1, minsize=200)
        
        # Tile content
        content_frame = tk.Frame(tile_frame, bg=tile_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tile icon
        if tile_name in tile_icons and tile_icons[tile_name]:
            icon_label = tk.Label(content_frame, image=tile_icons[tile_name], 
                                bg=tile_color)
            icon_label.image = tile_icons[tile_name]  # Keep reference
            icon_label.pack()
        else:
            # Fallback icon
            icon_label = tk.Label(content_frame, text="📱", font=("Arial", 24), 
                                bg=tile_color, fg="white")
            icon_label.pack()
        
        # Tile name
        name_label = tk.Label(content_frame, text=tile_name, font=("Arial", 14, "bold"), 
                            bg=tile_color, fg="white", wraplength=150)
        name_label.pack(pady=10)
        
        # Bind click event to entire tile
        tile_frame.bind("<Button-1>", lambda e, cmd=tile_command: (cmd(), start_window.destroy()))
        content_frame.bind("<Button-1>", lambda e, cmd=tile_command: (cmd(), start_window.destroy()))
        icon_label.bind("<Button-1>", lambda e, cmd=tile_command: (cmd(), start_window.destroy()))
        name_label.bind("<Button-1>", lambda e, cmd=tile_command: (cmd(), start_window.destroy()))
        
        # Hover effects
        def on_enter(e, frame=tile_frame, color=tile_color):
            # Darken color on hover
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            darker_color = f'#{r:02x}{g:02x}{b:02x}'
            frame.config(bg=darker_color)
            for widget in frame.winfo_children():
                widget.config(bg=darker_color)
                for child in widget.winfo_children():
                    child.config(bg=darker_color)
            frame.config(cursor="hand2")
        
        def on_leave(e, frame=tile_frame, color=tile_color):
            frame.config(bg=color)
            for widget in frame.winfo_children():
                widget.config(bg=color)
                for child in widget.winfo_children():
                    child.config(bg=color)
        
        tile_frame.bind("<Enter>", on_enter)
        tile_frame.bind("<Leave>", on_leave)
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
    
    # Close button (bottom right)
    close_frame = tk.Frame(main_container, bg="#1a1a1a")
    close_frame.pack(side="bottom", fill="x", pady=(30, 0))
    
    def close_start_menu():
        start_window.destroy()
    
    close_btn = tk.Button(close_frame, text="Close Start Menu", font=("Arial", 14),
                         bg="#f44336", fg="white", activebackground="#d32f2f",
                         activeforeground="white", relief="flat", padx=30, pady=15,
                         cursor="hand2", command=close_start_menu)
    close_btn.pack(side="right", padx=20)
    
    # Add ESC key to close
    start_window.bind('<Escape>', lambda e: close_start_menu())
    
    # Add Windows key to close
    start_window.bind('<Super_L>', lambda e: close_start_menu())
    
    # Center the tiles
    tiles_container.update_idletasks()


# ====================
# Main display
# ====================
def display_main_os():
    # Clear root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Create main frame
    main_frame = tk.Frame(root, bg="#1a1a1a")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="Welcome to Xono UI OS v1.1!", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
    title_label.pack(pady=20)
    
    # Buttons frame
    buttons_frame = tk.Frame(main_frame, bg="#1a1a1a")
    buttons_frame.pack(pady=20)
    
    file_viewer_button = customtkinter.CTkButton(master=buttons_frame, image=file_viewer_icon, text="File Viewer", width=190, height=40, command=open_file_viewer)
    file_viewer_button.pack(pady=10, padx=20)

    calculator_button = customtkinter.CTkButton(master=buttons_frame, image=calculator_icon, text="Calculator", width=190, height=40, command=calculator)
    calculator_button.pack(pady=10, padx=20)

    notepad_button = customtkinter.CTkButton(master=buttons_frame, image=notepad_icon, text="Notepad", width=190, height=40, command=notepad)
    notepad_button.pack(pady=10, padx=20)

    settings_button = customtkinter.CTkButton(master=buttons_frame, image=settings_icon, text="Settings", width=190, height=40, command=settings)
    settings_button.pack(pady=10, padx=20)

    about_pc_button = customtkinter.CTkButton(master=buttons_frame, image=about_pc_icon, text="About your PC", width=190, height=40, command=about_pc)
    about_pc_button.pack(pady=10, padx=20)

    command_prompt_button = customtkinter.CTkButton(master=buttons_frame, image=command_prompt_icon, text="Command Prompt", width=190, height=40, command=command_prompt)
    command_prompt_button.pack(pady=10, padx=20)

    pc_performances_button = customtkinter.CTkButton(master=buttons_frame, image=pc_performances_icon, text="PC Performances", width=190, height=40, command=pc_performances)
    pc_performances_button.pack(pady=10, padx=20)

    browser_button = customtkinter.CTkButton(master=buttons_frame, image=browser_icon, text="XONO Browser", width=190, height=40, command=xono_browser)
    browser_button.pack(pady=10, padx=20)

    # Small power button (bottom-left) — icon-only, closes the app
    def _shutdown():
        try:
            time.sleep(5)
            root.destroy()
        except Exception:
            time.sleep(5)
            root.quit()

    if power_icon:
        power_btn = customtkinter.CTkButton(master=main_frame, image=power_icon, text="", width=40, height=40, command=_shutdown)
        power_btn.image = power_icon
    else:
        # fallback: small button with unicode power symbol
        power_btn = customtkinter.CTkButton(master=main_frame, text="⏻", width=40, height=40, command=_shutdown)
    power_btn.place(relx=0.01, rely=0.98, anchor='sw')

    # Start button (bottom-left) - opens Start Menu
    def load_start_icon():
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "start_icon.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((30, 30), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Could not load start icon: {e}")
            return None

    start_icon = load_start_icon()

    if start_icon:
        start_btn = customtkinter.CTkButton(master=main_frame, image=start_icon, text="", 
                                           width=40, height=40, command=open_start_menu,
                                           fg_color="#1a1a1a", hover_color="#2c2c2c")
        start_btn.image = start_icon
    else:
        # Fallback: button with Windows logo or simple start symbol
        start_btn = customtkinter.CTkButton(master=main_frame, text="◰", font=("Arial", 16),
                                           width=40, height=40, command=open_start_menu,
                                           fg_color="#4CAF50", text_color="white",
                                           hover_color="#45a049")

    # Position Start button (left of power button)
    start_btn.place(relx=0.01, rely=0.98, anchor='sw')

    # Move Power button to the right of Start button
    if power_icon:
        power_btn = customtkinter.CTkButton(master=main_frame, image=power_icon, text="", 
                                           width=40, height=40, command=_shutdown,
                                           fg_color="#1a1a1a", hover_color="#2c2c2c")
        power_btn.image = power_icon
    else:
        power_btn = customtkinter.CTkButton(master=main_frame, text="⏻", font=("Arial", 16),
                                           width=40, height=40, command=_shutdown,
                                           fg_color="#f44336", text_color="white",
                                           hover_color="#d32f2f")

    # Position Power button next to Start button
    power_btn.place(relx=0.06, rely=0.98, anchor='sw')

    


# ==============================
# LOGIN PAGE
# ==============================
def login_page():
    """Display login page with wallpaper background"""
    # Clear root window
    for widget in root.winfo_children():
        widget.destroy()
    
    if os.path.exists(SETUP_FILE):
        with open(SETUP_FILE, "r", encoding="utf-8") as sf:
            setup_data = json.load(sf)
            saved_password = setup_data.get("password", "")
            username = setup_data.get("username", "User")
        
        # Create main login frame
        login_frame = tk.Frame(root, bg="#1a1a1a")
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Try to load background wallpaper
        wallpaper_path = os.path.join(os.path.dirname(__file__), "assets", "login_page_wallpaper.png")
        
        # Store image reference globally to prevent garbage collection
        global bg_photo, original_wallpaper
        
        if os.path.exists(wallpaper_path):
            try:
                original_wallpaper = Image.open(wallpaper_path)
                
                bg_label = tk.Label(login_frame, bg="#1a1a1a")
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                def update_wallpaper(event=None):
                    global bg_photo
                    # Get current window size
                    width = login_frame.winfo_width()
                    height = login_frame.winfo_height()
                    
                    if width > 1 and height > 1:
                        # Resize image to match window size
                        resized_image = original_wallpaper.resize((width, height), Image.Resampling.LANCZOS)
                        bg_photo = ImageTk.PhotoImage(resized_image)
                        bg_label.config(image=bg_photo)
                
                # Bind resize event to update wallpaper
                login_frame.bind("<Configure>", update_wallpaper)
                # Initial update
                root.update_idletasks()
                update_wallpaper()
                
            except Exception as e:
                print(f"Could not load wallpaper: {e}")
                login_frame.config(bg="#1a1a1a")
        else:
            login_frame.config(bg="#1a1a1a")

        # Create centered input frame (transparent-like)
        input_frame = tk.Frame(login_frame, bg="#2c2c2c", highlightthickness=2, highlightbackground="#4CAF50")
        input_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)
        
        # Title
        title_label = tk.Label(input_frame, text="XONO UI OS v1.1", font=("Arial", 18, "bold"), bg="#2c2c2c", fg="white")
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(input_frame, text=f"Welcome back, {username}!", font=("Arial", 12), bg="#2c2c2c", fg="#4CAF50")
        subtitle_label.pack(pady=5)
        
        # Password label
        password_label = tk.Label(input_frame, text="Enter your password:", font=("Arial", 11), bg="#2c2c2c", fg="white")
        password_label.pack(pady=10)
        
        # Password entry
        password_entry = tk.Entry(input_frame, show="*", width=35, font=("Arial", 12), bg="#1a1a1a", fg="white", insertbackground="white")
        password_entry.pack(pady=10, padx=20)
        password_entry.focus()
        
        # Message label
        message_label = tk.Label(input_frame, text="", font=("Arial", 10), bg="#2c2c2c", fg="red")
        message_label.pack(pady=5)
        
        def check_password(event=None):
            entered_password = password_entry.get()
            if entered_password == saved_password:
                message_label.config(text="Access granted! Loading...", fg="#4CAF50")
                root.update()
                time.sleep(1)
                display_main_os()
            else:
                message_label.config(text="Incorrect password! Try again.", fg="red")
                password_entry.delete(0, tk.END)
                password_entry.focus()
        
        # Login button
        login_button = tk.Button(input_frame, text="Login", command=check_password, bg="#4CAF50", fg="white", padx=30, pady=10, font=("Arial", 11), cursor="hand2")
        login_button.pack(pady=15)
        
        # Bind Enter key to login
        password_entry.bind("<Return>", check_password)


# ====================
# First time wizard
# ====================
if not os.path.exists(SETUP_FILE):
    # Create a frame for setup wizard using grid geometry manager
    setup_frame = tk.Frame(root)
    setup_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    title_label = tk.Label(setup_frame, text="Welcome to Xono UI OS v1.1!\nLet's set up your system.", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
    label_country = tk.Label(setup_frame, text="Enter your country:")
    label_country.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    label_username = tk.Label(setup_frame, text="Create your username:")
    label_username.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    label_password = tk.Label(setup_frame, text="Create your password:")
    label_password.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    label_password_confirm = tk.Label(setup_frame, text="Confirm your password:")
    label_password_confirm.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    label_device_name = tk.Label(setup_frame, text="Name your device:")
    label_device_name.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    label_sound_effects = tk.Label(setup_frame, text="Enable sound effects?")
    label_sound_effects.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    # Create Entry widgets
    country_entry = tk.Entry(setup_frame, width=30)
    country_entry.grid(row=1, column=1, padx=5, pady=5)
    username_entry = tk.Entry(setup_frame, width=30)
    username_entry.grid(row=2, column=1, padx=5, pady=5)
    password_entry = tk.Entry(setup_frame, show="*", width=30)
    password_entry.grid(row=3, column=1, padx=5, pady=5)
    password_confirm_entry = tk.Entry(setup_frame, show="*", width=30)
    password_confirm_entry.grid(row=4, column=1, padx=5, pady=5)
    device_name_entry = tk.Entry(setup_frame, width=30)
    device_name_entry.grid(row=5, column=1, padx=5, pady=5)
    
    sound_effects_var = tk.IntVar(value=1)
    sound_effects_entry = tk.Radiobutton(setup_frame, text="Yes", variable=sound_effects_var, value=1)
    sound_effects_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
    sound_effects_no = tk.Radiobutton(setup_frame, text="No", variable=sound_effects_var, value=0)
    sound_effects_no.grid(row=6, column=1, padx=5, pady=5)
    
    # Submit button function
    def save_setup():
        country = country_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()
        device_name = device_name_entry.get().strip()
        
        # Validation
        if not country or not username or not password or not device_name:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if password != password_confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Save setup configuration
        setup_data = {
            "country": country,
            "username": username,
            "password": password,
            "device_name": device_name,
            "sound_effects": bool(sound_effects_var.get())
        }

        # Hide setup frame and show loading screen
        setup_frame.destroy()
        
        # Create loading frame
        loading_frame = tk.Frame(root, bg="#2c2c2c")
        loading_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_loading = tk.Label(loading_frame, text="Setting up your system...", font=("Arial", 18, "bold"), bg="#2c2c2c", fg="white")
        title_loading.pack(pady=40)
        
        # Status label
        status_label = tk.Label(loading_frame, text="", font=("Arial", 14), bg="#2c2c2c", fg="#4CAF50")
        status_label.pack(pady=20)
        
        # Progress label
        progress_label = tk.Label(loading_frame, text="", font=("Arial", 11), bg="#2c2c2c", fg="#cccccc")
        progress_label.pack(pady=10)
        
        root.update()
        
        install_steps = [
            "Initializing XONO Core Engine...",
            "Setting up user environment...",
            "Configuring hardware drivers...",
            "Optimizing CPU threads...",
            "Installing base applications...",
            "Applying security layers...",
            "Preparing XONO Writer and Post modules...",
            "Setting device name and region...",
            "Activating background services...",
            "Running first-time system check...",
            "Installing update manager...",
            "Creating internal cache folders...",
            "Finalizing settings...",
            "Configuring XONO Recycle Bin...",
            "Installing terminal environment...",
            "Optimizing memory handling...",
            "Applying power configurations...",
            "Installing system utilities...",
            "Indexing applications...",
            "Finishing setup..."
        ]

        # Display each loading step
        for index, step in enumerate(install_steps, 1):
            status_label.config(text=step)
            progress_label.config(text=f"[{'=' * (index - 1)}{'>' if index < len(install_steps) else '='}{' ' * (len(install_steps) - index)}] {index}/{len(install_steps)}")
            root.update()
            time.sleep(0.8)
        
        # Save setup configuration
        try:
            with open(SETUP_FILE, "w", encoding="utf-8") as sf:
                json.dump(setup_data, sf, indent=2)
            
            status_label.config(text="System setup complete!")
            progress_label.config(text="Launching system...")
            root.update()
            time.sleep(1)
            
            loading_frame.destroy()
            display_main_os()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save setup: {str(e)}")

    
    # Submit button
    submit_button = tk.Button(setup_frame, text="Complete Setup", command=save_setup, bg="#4CAF50", fg="white", padx=20, pady=10)
    submit_button.grid(row=7, column=0, columnspan=2, pady=20)

else:
    login_page()

# Start the application
root.mainloop()
