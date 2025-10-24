#!/usr/bin/env python3
"""
Chrome-Only Workflow
Closes all GUI apps and opens only Chrome.
"""

from workspace_manager import close_all_gui_apps, open_and_maximize_apps

# Configure apps for this workflow
APPS_TO_OPEN = [
    ("Google Chrome", "Google Chrome")
]


def main():
    """Execute Chrome-only workflow."""
    print("=" * 60)
    print("Chrome-Only Workflow")
    print("=" * 60)
    print()
    
    close_all_gui_apps()
    open_and_maximize_apps(APPS_TO_OPEN)
    
    print("\nDone!")


if __name__ == "__main__":
    main()

