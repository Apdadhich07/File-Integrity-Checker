import hashlib
import os
import json

# ------------------------------
# Function: Calculate SHA-256 Hash of a File
# ------------------------------
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # 64KB chunks
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()

# ------------------------------
# Function: Create Baseline Hashes
# ------------------------------
def create_baseline(directory, baseline_file):
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            absolute_path = os.path.abspath(file_path)
            file_hash = calculate_sha256(absolute_path)
            baseline[absolute_path] = {
                "old_hash": file_hash,
                "new_hash": file_hash
            }

    with open(baseline_file, 'w') as f:
        json.dump(baseline, f, indent=4)

    print(f"\n✅ Baseline hashes saved in '{baseline_file}'")

# ------------------------------
# Function: Verify Integrity
# ------------------------------
def verify_integrity(directory, baseline_file="hash.json"):
    if not os.path.exists(baseline_file):
        print("❌ Baseline file not found.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"❌ Directory '{directory}' does not exist.")
        return

    new_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            absolute_path = os.path.abspath(file_path)
            new_hashes[absolute_path] = calculate_sha256(absolute_path)

    print("\n🔍 Integrity Check Results:\n")
    updated_baseline = {}
    changes_detected = False

    # Check for deleted or modified files
    for file_path, hashes in baseline.items():
        old_hash = hashes["new_hash"]
        if file_path not in new_hashes:
            print(f"[DELETED]   {file_path}")
            changes_detected = True
        elif new_hashes[file_path] != old_hash:
            print(f"[MODIFIED]  {file_path}")
            changes_detected = True
            updated_baseline[file_path] = {
                "old_hash": old_hash,
                "new_hash": new_hashes[file_path]
            }
        else:
            updated_baseline[file_path] = {
                "old_hash": old_hash,
                "new_hash": old_hash
            }

    # Check for new files
    for file_path, new_hash in new_hashes.items():
        if file_path not in baseline:
            print(f"[NEW FILE]  {file_path}")
            changes_detected = True
            updated_baseline[file_path] = {
                "old_hash": new_hash,
                "new_hash": new_hash
            }

    if not changes_detected:
        print("✅ No changes detected.")

    # Save updated baseline with both old and new hashes
    with open(baseline_file, 'w') as f:
        json.dump(updated_baseline, f, indent=4)

    print("\n✅ Integrity check complete. Baseline updated.\n")

# ------------------------------
# Main Driver
# ------------------------------
if __name__ == "__main__":
    print("📁 File Integrity Checker")
    directory_to_monitor = input("Enter the directory path: ").strip()
    baseline_file = "hash.json"

    print("\nChoose an option:")
    print("1. Create baseline")
    print("2. Verify integrity")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        create_baseline(directory_to_monitor, baseline_file)
    elif choice == "2":
        verify_integrity(directory_to_monitor, baseline_file)
    else:
        print("❌ Invalid input.")
