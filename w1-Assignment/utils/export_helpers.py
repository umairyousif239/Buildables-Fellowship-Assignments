import json
import os
from datetime import datetime

def save_results(run_data: dict, file_path="data/results/result.json"):
    """Save analysis results into a JSON file, appending new runs."""

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                results = []
    else:
        results = []

    # Add timestamp
    run_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append new run
    results.append(run_data)

    # Save back
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)
