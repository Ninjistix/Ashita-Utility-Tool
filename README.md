# Ashita Config & Launcher

A Python-based GUI tool for managing Ashita configurations and launching Ashita with custom settings. Inspired by AshitaV4, this launcher simplifies editing configuration options, managing plugins, and launching Ashita with saved settings.

---

## Features

* Load, edit, and save Ashita configuration files (`.ini`)
* Organize settings into logical tab groups (e.g., General, Input & Controls, Plugins)
* Save last used configuration automatically
* Launch Ashita directly from the GUI with current settings
* Edit server IP, login credentials, console hiding, and other options
* Visual indicator for unsaved changes
* Customizable window layout and tab organization

---

## Screenshots

*(Screenshot of the GUI window)* <img width="951" height="680" alt="image" src="https://github.com/user-attachments/assets/00536ce0-b4c9-464a-96c1-b0ae610c8005" />

---

## Requirements

If using the **Python script** version:

* Python 3.x (tested on Python 3.8+)
* `tkinter` (bundled with most Python installs)
* `configparser` (standard library)
* `ctypes` (standard library)

If using the **EXE version**:

* No dependencies — just run the file.

---

## Setup Instructions

You may use **either** the Python script (`AshitaConfigLauncher.pyw`) **or** the standalone executable (`AshitaConfigLauncher.exe`). Both work the same way.

### 1. Place the launcher in your Ashita folder

Put **`AshitaConfigLauncher.pyw`** **or** **`AshitaConfigLauncher.exe`** in the **same directory** as:

* `ashita-cli.exe`
* Any Ashita `.ini` configuration files you want to manage (optional)

> **Important:** The launcher *must* be in the same folder as `ashita-cli.exe`.
> If they are separated, Ashita will not launch.

---

### 2. Run the launcher

#### **Using the EXE (recommended):**

Double-click:

```
AshitaConfigLauncher.exe
```

No Python installation is required.

#### **Using the Python script:**

```bash
pythonw AshitaConfigLauncher.pyw
```

---

## Usage

* Click **Load Config** to select an Ashita `.ini` file.
* Edit settings across the various configuration tabs.
* Save your edits using **Save Config** or **Save As**.
* Click **Launch Ashita** to run `ashita-cli.exe` using the current settings.
* The launcher remembers the last configuration you used for convenience.

---

## Customization & Extending

* Modify the `TAB_GROUPS` dictionary in the source code to reorganize tab structure.
* Add new configuration sections or extend existing ones in your `.ini` files.
* Enhance the GUI with extra features or plugin management tools.

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
