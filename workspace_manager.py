#!/usr/bin/env python3
"""
Workspace Manager - Shared Library
Core functions for managing macOS workspace automation.
"""

import subprocess
import time
import sys

# Configuration
EXCLUDED_APPS = {"Terminal", "iTerm2", "iTerm", "Finder", "SystemUIServer"}
COUNTDOWN_SECONDS = 3


def log_info(message):
    """Print an informational message."""
    print(f"  {message}")


def log_success(message):
    """Print a success message."""
    print(f"  ✓ {message}")


def log_error(message):
    """Print an error message."""
    print(f"  ✗ {message}")


def run_applescript(script):
    """
    Execute an AppleScript command and return the output.
    
    Args:
        script: AppleScript code to execute
        
    Returns:
        str: Script output, or None if execution failed
    """
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_error(f"AppleScript error: {e.stderr}")
        return None


def get_applescript_list_running_apps():
    """Generate AppleScript to get list of running GUI applications."""
    return 'tell application "System Events" to get name of every application process whose background only is false'


def get_applescript_check_app_exists(app_name):
    """
    Generate AppleScript to check if an application exists.
    
    Args:
        app_name: Name of the application to check
        
    Returns:
        str: AppleScript code
    """
    return f'''
    try
        tell application "Finder" to get application file id of application "{app_name}"
        return "found"
    on error
        return "not found"
    end try
    '''


def get_applescript_maximize_window(process_name):
    """
    Generate AppleScript to maximize a window to fullscreen.
    
    Args:
        process_name: Process name of the application
        
    Returns:
        str: AppleScript code
    """
    return f'''
    tell application "System Events"
        tell process "{process_name}"
            set frontmost to true
            delay 1
            try
                if exists window 1 then
                    tell window 1
                        -- Try fullscreen first (true maximization)
                        try
                            set value of attribute "AXFullScreen" to true
                        on error
                            -- Fallback: maximize to screen bounds
                            tell application "Finder"
                                set screenBounds to bounds of window of desktop
                                set screenWidth to item 3 of screenBounds
                                set screenHeight to item 4 of screenBounds
                            end tell
                            set position to {{0, 0}}
                            set size to {{screenWidth, screenHeight}}
                        end try
                    end tell
                end if
            on error errMsg
                -- Last resort: try to zoom the window
                try
                    tell window 1
                        set value of attribute "AXZoomButton" to true
                    end tell
                end try
            end try
        end tell
    end tell
    '''


def get_running_gui_apps():
    """
    Get list of all running GUI applications.
    
    Returns:
        list: List of application names
    """
    script = get_applescript_list_running_apps()
    result = run_applescript(script)
    if result:
        apps = [app.strip() for app in result.split(",")]
        return apps
    return []


def close_all_gui_apps(excluded_apps=None):
    """
    Close all GUI applications except the terminal running this script.
    
    Args:
        excluded_apps: Set of app names to exclude (uses default if None)
    """
    if excluded_apps is None:
        excluded_apps = EXCLUDED_APPS
    
    print("Getting list of running GUI applications...")
    apps = get_running_gui_apps()
    
    apps_to_close = [app for app in apps if app not in excluded_apps]
    
    if not apps_to_close:
        print("No GUI applications to close.")
        return
    
    print(f"\nFound {len(apps_to_close)} applications to close:")
    for app in apps_to_close:
        log_info(f"- {app}")
    
    print(f"\nStarting countdown: {COUNTDOWN_SECONDS} seconds to cancel (Ctrl+C)...")
    try:
        for i in range(COUNTDOWN_SECONDS, 0, -1):
            print(f"{i}...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    
    print("\nClosing applications...")
    for app in apps_to_close:
        try:
            script = f'tell application "{app}" to quit'
            run_applescript(script)
            log_success(f"Closed {app}")
            time.sleep(0.2)
        except Exception as e:
            log_error(f"Failed to close {app}: {e}")
    
    time.sleep(1)
    print("\nAll applications closed.")


def maximize_window(app_name, process_name=None):
    """
    Maximize the frontmost window of an application to fullest extent.
    
    Args:
        app_name: Name of the application
        process_name: Process name (defaults to app_name if not provided)
    """
    if process_name is None:
        process_name = app_name
    
    script = get_applescript_maximize_window(process_name)
    run_applescript(script)


def open_and_maximize_apps(apps_to_open):
    """
    Open and maximize specified applications.
    
    Args:
        apps_to_open: List of tuples (app_name, process_name)
    
    Checks which apps are installed, opens them, and maximizes their windows.
    """
    print("\nChecking installed applications...")
    installed_apps = []
    
    for app_name, process_name in apps_to_open:
        check_script = get_applescript_check_app_exists(app_name)
        result = run_applescript(check_script)
        
        if result and "found" in result:
            installed_apps.append((app_name, process_name))
            log_success(f"{app_name} found")
        else:
            log_error(f"{app_name} not found (skipping)")
    
    print("\nOpening and maximizing applications...")
    
    for app_name, process_name in installed_apps:
        try:
            print(f"\n  Opening {app_name}...")
            
            script = f'tell application "{app_name}" to activate'
            run_applescript(script)
            time.sleep(2)
            
            print(f"  Maximizing {app_name}...")
            maximize_window(app_name, process_name)
            
            log_success(f"{app_name} ready")
            time.sleep(0.5)
            
        except Exception as e:
            log_error(f"Failed to open/maximize {app_name}: {e}")
    
    print("\n✓ Workflow complete! All applications opened and maximized.")

