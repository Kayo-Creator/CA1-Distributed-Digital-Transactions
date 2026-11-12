#!/usr/bin/env bash
set -eu

# Locate the project relative to this script, regardless of the terminal folder.
project_root="$(cd -- "$(dirname -- "$0")/.." && pwd)"
python_exe="$project_root/.venv/Scripts/python.exe"
app_file="$project_root/app/main.py"

# Stop with a useful message if required project files are missing.
if [[ ! -f "$python_exe" ]]; then
    echo "Project Python environment not found: $python_exe" >&2
    echo "Create .venv and install requirements.txt before starting." >&2
    exit 1
fi

if [[ ! -f "$app_file" ]]; then
    echo "Application file not found: $app_file" >&2
    exit 1
fi

echo "Starting the hotel booking DApp..."

# Run the application with the project's Python and preserve its exit status.
exec "$python_exe" "$app_file"