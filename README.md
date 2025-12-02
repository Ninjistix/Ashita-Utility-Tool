# Ashita Config & Launcher

A Python-based GUI tool for managing Ashita configurations and launching Ashita with custom settings. Inspired by AshitaV4, this launcher simplifies editing configuration options, managing plugins, and launching Ashita with saved settings.

---

## Features

- Load, edit, and save Ashita configuration files (`.ini`)
- Organize settings into logical tab groups (e.g., General, Input & Controls, Plugins)
- Save last used configuration automatically
- Launch Ashita directly from the GUI with current settings
- Edit server IP, login credentials, console hiding, and other options
- Visual indicator for unsaved changes
- Customizable window layout and tab organization

---

## Screenshots

*(Screenshot of the GUI window)*
<img width="951" height="680" alt="image" src="https://github.com/user-attachments/assets/00536ce0-b4c9-464a-96c1-b0ae610c8005" />


---

## Requirements

- Python 3.x (tested on Python 3.8+)
- `tkinter` (usually bundled with Python)
- `configparser` (standard library)
- `ctypes` (standard library)

## Setup Instructions

1. **Place `AshitaConfigLauncher.pyw` in the same folder as your `ashita-cli.exe`.**

2. **Ensure `ashita-cli.exe` is in the same directory as the launcher script.**

3. **Run the launcher:**

   - Double-click `AshitaConfigLauncher.pyw` or run it from the command line:

     ```bash
     pythonw AshitaConfigLauncher.pyw
     ```

4. **Configure your settings, load your `.ini` config, and launch Ashita.**

---

## Usage

- Click **Load Config** to select an existing Ashita `.ini` config file.
- Edit settings across the tabs (e.g., server IP, login, plugins).
- Save your changes with **Save Config** or **Save As**.
- Launch Ashita with the current config by clicking **Launch Ashita**.
- The launcher will remember your last used configuration for convenience.

---

## Customization & Extending

- Modify `TAB_GROUPS` dictionary to reorganize tabs.
- Add or remove settings sections in your `.ini` files.
- Extend the GUI with new controls or features as needed.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Would you like me to generate a sample folder structure or help create an icon or other assets?
