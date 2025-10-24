# Workspace Manager

Automates your development workspace setup on macOS by closing all GUI applications and opening a curated set of development tools.

## Features

- Smart app detection and window maximization
- Multiple workflow scripts for different setups
- 3-second countdown with cancellation option
- Graceful error handling

## Setup

Add these aliases to your `~/.zshrc` file to enable global commands:

```bash
echo 'alias workspace-xcode="cd /Users/ypatil/Code/Personal/Workspace-Manager && ./xcode_flow.py"' >> ~/.zshrc
echo 'alias workspace-chrome="cd /Users/ypatil/Code/Personal/Workspace-Manager && ./chrome_flow.py"' >> ~/.zshrc
source ~/.zshrc
```

## Available Workflows

**Xcode Development** - Opens Chrome, GitHub Desktop, Cursor, and Xcode
```bash
workspace-xcode
```

**Chrome Only** - Opens only Chrome
```bash
workspace-chrome
```

*Run these commands from any directory in your terminal!*

## Creating Custom Workflows

Create a new workflow script:

```python
#!/usr/bin/env python3
from workspace_manager import close_all_gui_apps, open_and_maximize_apps

APPS_TO_OPEN = [
    ("App Name", "Process Name")
]

close_all_gui_apps()
open_and_maximize_apps(APPS_TO_OPEN)
```

## Requirements

- macOS (uses AppleScript)
- Python 3.6+

## Safety

⚠️ Force quits all GUI apps without saving. Only run when you don't have unsaved work.

## License

GPL-3.0
