# ao.sh

"You can't use bash for everything!" -- people who let fear cloud their mind and stifle their potential

## Requirements

- tesseract
- Python
- curl
- bash (recent)

## Installation

`git clone` this repository and copy the script to a convenient location.

I also recommend adding something like the following to your `.bashrc`:
```
alias ao=bash ~/Desktop/ao.sh
```

# File Tracking

A high-level overview of the file tracking scheme follows. "Snapshots" of files and directories are taken periodically, representing file hashes/checksums and metadata as JSON objects. These are stored permanently, and periodically merged into "file nodes" based on some commonsense rules for determining file continuity. The nodes are associated with their snapshots, and new snapshots with matching paths will be merged into their respective nodes (after which the nodes will reflect the most recent metadata). Copies of files are detected by comparing names and checksums and marked accordingly on both nodes. The backup system essentially iterates over these file nodes, mirroring them to the backup location(s) and storing diff information (efficiently) describing a file's state at different points in time and allowing for easy reconstruction if a backup needs to be loaded.
