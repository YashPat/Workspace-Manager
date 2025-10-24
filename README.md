# Workspace Manager

A Python script that automates your development workspace setup on macOS by closing all GUI applications and opening a curated set of development tools.

## Features

- **Smart App Detection**: Only closes GUI applications, preserves terminal and system apps
- **Configurable App List**: Easy to customize which development tools to open
- **Window Maximization**: Automatically maximizes windows to fullscreen for optimal workspace
- **Safety Features**: 3-second countdown with cancellation option
- **Error Handling**: Graceful handling of missing applications and failed operations

## Usage

```bash
cd Workspace-Manager
./xcode_flow.py
```

## Configuration

Edit the `APPS_TO_OPEN` list in `xcode_flow.py` to customize which applications are launched:

```python
APPS_TO_OPEN = [
    ("Google Chrome", "Google Chrome"),
    ("GitHub Desktop", "GitHub Desktop"),
    ("Cursor", "Cursor"),
    ("Xcode-26.0.1", "Xcode-26.0.1")
]
```

## Requirements

- macOS (uses AppleScript)
- Python 3.6+
- Applications must be installed in `/Applications/`

## Safety

⚠️ **Warning**: This script force quits all GUI applications without saving prompts. Only run when you don't have unsaved work.

## License

GPL-3.0
