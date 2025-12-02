import os
import json
import ctypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser

SETTINGS_FILE = "launcher_settings.json"
EXPECTED_BOOT_DIR = os.path.join("config", "boot")  # relative to Py script location

# ------------------------
# Tab group definitions
# ------------------------
TAB_GROUPS = {
    "General": ["ashita.launcher", "ashita.boot", "ashita.misc"],
    "Input & Controls": ["ashita.input", "ffxi.registry"],
    "Language & Logging": ["ashita.language", "ashita.logging"],
    "Plugins": ["ashita.polplugins", "ashita.polplugins.args", "ashita.resources", "ashita.taskpool"],
    "Window & Graphics": ["ashita.window.startpos", "ffxi.direct3d8", "ashita.fonts"]
}

class AshitaConfigLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ashita Config & Launcher")
        self.geometry("950x650")

        # ------------------------
        # State
        # ------------------------
        self.config_file_path = None
        self._config_saved = True
        self.config = configparser.RawConfigParser(strict=False)
        self.config.optionxform = str  # preserve case

        # ------------------------
        # Ashita executable
        # ------------------------
        self.ashita_cli = os.path.join(os.getcwd(), "ashita-cli.exe")
        if not os.path.exists(self.ashita_cli):
            messagebox.showerror("Error", f"ashita-cli.exe not found in {os.getcwd()}")
            self.destroy()
            return

        # ------------------------
        # Status bar (loaded INI)
        # ------------------------
        self.status_var = tk.StringVar(value="No config loaded")
        self.status_label = tk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="top", fill="x", padx=6, pady=(6,0))

        # ------------------------
        # Top frame buttons
        # ------------------------
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=6, pady=6)

        tk.Button(top_frame, text="Load Config", command=self.load_config).pack(side="left", padx=4)
        tk.Button(top_frame, text="Save Config", command=self.save_config).pack(side="left", padx=4)
        tk.Button(top_frame, text="Save As", command=self.save_as_config).pack(side="left", padx=4)
        tk.Button(top_frame, text="Launch Ashita", command=self.launch_ashita).pack(side="right", padx=4)

        # ------------------------
        # Unsaved warning label
        # ------------------------
        self.warning_var = tk.StringVar(value="")
        self.warning_label = tk.Label(self, textvariable=self.warning_var, fg="red", font=("Arial", 10, "bold"))
        self.warning_label.pack(side="top", fill="x", padx=6, pady=(0,6))

        # ------------------------
        # Notebook tabs
        # ------------------------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=6, pady=6)

        self.tab_frames = {}
        self.vars = {}  # (section, key) -> StringVar / BooleanVar

        for tab_name in TAB_GROUPS.keys():
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tab_frames[tab_name] = frame

        # Load last used INI
        self.load_last_ini()

    # ------------------------
    # Config saved state
    # ------------------------
    def set_config_saved(self, saved: bool):
        self._config_saved = saved
        self.warning_var.set("" if saved else "⚠ Unsaved changes! Save before launching.")

    def is_config_saved(self):
        return self._config_saved

    def mark_unsaved(self, *args):
        self.set_config_saved(False)

    # ------------------------
    # Load/save last INI
    # ------------------------
    def load_last_ini(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    last_ini = data.get("last_ini", "")
                    if last_ini and os.path.exists(last_ini):
                        self.load_config(last_ini)
            except Exception:
                pass

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump({"last_ini": self.config_file_path or ""}, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")

    # ------------------------
    # Config loading/saving
    # ------------------------
    def load_config(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(
                title="Select Ashita Boot Config",
                initialdir=os.path.join(os.getcwd(), EXPECTED_BOOT_DIR),
                filetypes=[("INI files", "*.ini")]
            )
        if not file_path:
            return

        try:
            self.config.read(file_path, encoding="utf-8")
        except configparser.Error as e:
            messagebox.showerror("Error", f"Failed to read config:\n{e}")
            return

        self.config_file_path = file_path
        self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
        self.populate_tabs()
        self.set_config_saved(True)
        self.save_settings()

    def populate_tabs(self):
        self.vars.clear()
        for frame in self.tab_frames.values():
            for w in frame.winfo_children():
                w.destroy()

        for tab_name, sections in TAB_GROUPS.items():
            frame = self.tab_frames[tab_name]
            row = 0
            for section in sections:
                if section not in self.config:
                    continue
                tk.Label(frame, text=f"[{section}]", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(6,0))
                row += 1
                for key, value in self.config[section].items():
                    if section == "ashita.boot" and key == "command":
                        # parse command
                        parts = value.split()
                        server_ip = parts[1] if len(parts) > 1 else ""
                        username = password = ""
                        hide_val = False
                        if "--user" in parts:
                            try: username = parts[parts.index("--user")+1]
                            except: username=""
                        if "--pass" in parts:
                            try: password = parts[parts.index("--pass")+1]
                            except: password=""
                        if "--hide" in parts: hide_val=True

                        # Server IP
                        tk.Label(frame, text="Server IP").grid(row=row, column=0, sticky="w", padx=10)
                        sv = tk.StringVar(value=server_ip)
                        e = tk.Entry(frame, textvariable=sv)
                        e.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                        sv.trace_add("write", self.mark_unsaved)
                        self.vars[("ashita.boot","server")] = sv
                        row+=1

                        # Username
                        tk.Label(frame, text="Username (optional)").grid(row=row, column=0, sticky="w", padx=10)
                        uv = tk.StringVar(value=username)
                        ue = tk.Entry(frame, textvariable=uv)
                        ue.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                        uv.trace_add("write", self.mark_unsaved)
                        self.vars[("ashita.boot","username")] = uv
                        row+=1

                        # Password
                        tk.Label(frame, text="Password (optional)").grid(row=row, column=0, sticky="w", padx=10)
                        pv = tk.StringVar(value=password)
                        pe = tk.Entry(frame, textvariable=pv, show="*")
                        pe.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                        pv.trace_add("write", self.mark_unsaved)
                        self.vars[("ashita.boot","password")] = pv
                        row+=1

                        # Hide console
                        hv = tk.BooleanVar(value=hide_val)
                        chk = tk.Checkbutton(frame, text="Hide Console", variable=hv)
                        chk.grid(row=row, column=0, sticky="w", padx=10)
                        hv.trace_add("write", self.mark_unsaved)
                        self.vars[("ashita.boot","hide")] = hv
                        row+=1
                    else:
                        tk.Label(frame, text=key).grid(row=row, column=0, sticky="w", padx=10)
                        v = tk.StringVar(value=value)
                        e = tk.Entry(frame, textvariable=v)
                        e.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                        v.trace_add("write", self.mark_unsaved)
                        self.vars[(section,key)] = v
                        row+=1
            frame.columnconfigure(1, weight=1)

    def update_config_from_vars(self):
        for (section,key), var in list(self.vars.items()):
            if section not in self.config:
                self.config[section] = {}

            if section=="ashita.boot" and key=="server":
                server_ip = self.vars.get(("ashita.boot","server"),tk.StringVar()).get().strip()
                username = self.vars.get(("ashita.boot","username"),tk.StringVar()).get().strip()
                password = self.vars.get(("ashita.boot","password"),tk.StringVar()).get().strip()
                hide_console = self.vars.get(("ashita.boot","hide"),tk.BooleanVar()).get()

                # validation
                if (username and not password) or (password and not username):
                    messagebox.showerror("Validation Error","Both Username and Password must be supplied for auto-login, or leave both empty.")
                    return False

                cmd = f"--server {server_ip}"
                if username and password:
                    cmd += f" --user {username} --pass {password}"
                if hide_console:
                    cmd += " --hide"
                self.config["ashita.boot"]["command"] = cmd
            elif key not in ["username","password","hide"]:
                self.config[section][key] = var.get()
        return True

    def save_config(self):
        if not self.config_file_path:
            messagebox.showerror("Error","No config loaded!")
            return False
        if not self.update_config_from_vars():
            return False
        try:
            with open(self.config_file_path,"w",encoding="utf-8") as f:
                self.config.write(f)
            messagebox.showinfo("Saved",f"Config saved to {os.path.basename(self.config_file_path)}")
            self.set_config_saved(True)
            self.save_settings()
            return True
        except Exception as e:
            messagebox.showerror("Error",f"Failed to save config:\n{e}")
            return False

    def save_as_config(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Config As",
            defaultextension=".ini",
            initialdir=os.path.join(os.getcwd(), EXPECTED_BOOT_DIR),
            filetypes=[("INI files","*.ini")]
        )
        if not file_path:
            return False
        self.config_file_path = file_path
        return self.save_config()

    # ------------------------
    # Launch Ashita
    # ------------------------
    def launch_ashita(self):
        if not self.config_file_path:
            messagebox.showerror("Error","No config loaded!")
            return

        if not self.is_config_saved():
            answer = messagebox.askyesno("Unsaved Config","Config has unsaved changes. Save before launching?")
            if not answer:
                return
            if not self.save_config():
                return

        ini_name = os.path.basename(self.config_file_path)
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", self.ashita_cli, ini_name, None, 1)
            self.save_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Ashita:\n{e}")

if __name__ == "__main__":
    app = AshitaConfigLauncher()
    app.mainloop()
