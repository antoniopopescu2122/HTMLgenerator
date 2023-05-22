import json
import datetime


class ModificationsTracker:
    def __init__(self, modifications_file):
        self.modifications_file = modifications_file
        self.modifications = []

    def track_modification(self, component, branch, revision):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification = {
            'timestamp': timestamp,
            'component': component,
            'branch': branch,
            'revision': revision
        }
        self.modifications.append(modification)

    def save_modifications(self):
        with open(self.modifications_file, 'w') as f:
            json.dump(self.modifications, f)


# Example usage:
modifications_file = 'modifications.json'
tracker = ModificationsTracker(modifications_file)

# Track modifications
component = input("Component Name: ")
branch = input("Branch: ")
revision = input("Revision: ")
tracker.track_modification(component, branch, revision)

# Save modifications
tracker.save_modifications()
