**FILE INTEGRITY CHECKER**
A lightweight Python-based tool to monitor file integrity using cryptographic hashes.
Detects unauthorized file modifications, additions, and deletions by comparing SHA-256 checksums over time.

**Features**
Creates a secure baseline of SHA-256 hashes for all files in a directory.
Periodically verifies integrity by comparing current file hashes to the stored baseline.
Tracks and logs:
  New files
  Modified files
  Deleted files
Stores both old and new hashes in a JSON file for accurate change tracking.

