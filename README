# Storj Node Payout History Viewer

This Python script fetches and summarizes payout data across multiple [Storj](https://www.storj.io/) storage nodes via their local dashboards. It displays a detailed monthly earnings table in the terminal and optionally exports the data to a CSV file.

## Features

- Monthly payout overview from a configurable date range
- Terminal summary table with per-node totals and a final SUM row
- Locale-aware number formatting (English or German)
- Optional CSV export
- Handles missing or unreachable nodes gracefully

## Usage

```bash
./node-history.py [-c] [-o] [-l {de,en}]
```

## Options

- `-c`, `--csv`
Export the table as node-history.csv.

- `-o`, `--overwrite`
Overwrite node-history.csv if it already exists.

- `-l {de,en}`, `--locale {de,en}`
Choose number formatting (de for German style, en for English style). Default is de.

## Example

```
user@host:~$ ./node-history.py -c -l en
Payout across all nodes from 2023-12 to 2025-04:

╒════════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╕
│ Pay period │ node01 │ node02 │ node03 │ node04 │ node05 │ node06 │ node07 │ node08 │ node09 │ node10 │ TOTAL  │
╞════════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
│   2024-01: │  $0.11 │  $0.10 │  $0.09 │  $0.10 │  $0.09 │  $0.00 │  $0.00 │  $0.00 │  $0.00 │  $0.00 │  $0.48 │
│   2024-02: │  $0.16 │  $0.16 │  $0.15 │  $0.21 │  $0.14 │  $0.00 │  $0.00 │  $0.00 │  $0.00 │  $0.00 │  $0.81 │
│     ...    │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │   ...  │
╞════════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
│       SUM: │ $89.18 │ $76.77 │ $66.39 │ $109.20│ $60.10 │ $22.89 │ $21.39 │ $22.42 │ $20.00 │ $20.93 │ $509.28│
╘════════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╛
```

## Configuration

Adjust the following constants in the script as needed:

```
START_DATE = "2023-12"
END_DATE = "2025-04"
PORTS = ["14002", ..., "14011"]
CUSTOM_HEADERS = ["node01", ..., "node10"]
NODE_IP = "192.168.0.101"
```

## Requirements

- Python 3.7+
- `requests` module (`pip install requests`)