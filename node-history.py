#!/bin/python3

import requests
from datetime import datetime
import csv
import os
import argparse

# ---------------- CONFIG ----------------
START_DATE = "2023-12"
END_DATE = "2025-04"
PORTS = [
    "14002", "14003", "14004", "14005", "14006",
    "14007", "14008", "14009", "14010", "14011"
]
CUSTOM_HEADERS = [
    "node01", "node02", "node03", "node04", "node05",
    "node06", "node07", "node08", "node09", "node10"
]
NODE_IP = "192.168.0.101"
# ----------------------------------------


def generate_months(start: str, end: str):
    months = []
    current = datetime.strptime(start, "%Y-%m")
    end_date = datetime.strptime(end, "%Y-%m")

    while current <= end_date:
        months.append(current.strftime("%Y-%m"))
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return months


def fetch_payout(ip: str, port: str, year_month: str):
    url = f"http://{ip}:{port}/api/heldamount/paystubs/{year_month}/{year_month}"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        if not data or data == 'null':
            return 0.0
        total_paid = sum(item.get("paid", 0) for item in data)
        return total_paid / 1_000_000
    except (requests.RequestException, ValueError):
        return 0.0


def build_table(months, ports, ip):
    table = []
    sums = [0.0 for _ in ports]

    for month in months:
        row = [f"{month}"]
        row_sum = 0.0
        for i, port in enumerate(ports):
            payout = fetch_payout(ip, port, month)
            row.append(payout)
            sums[i] += payout
            row_sum += payout
        row.append(row_sum)
        table.append(row)

    sum_row = ["SUM"]
    total_sum = 0.0
    for total in sums:
        sum_row.append(total)
        total_sum += total
    sum_row.append(total_sum)

    return table, sum_row


def print_table(table_data, headers, sum_row, locale):
    use_dot = locale == "en"

    def format_number(val):
        number = f"{val:.2f}"
        return f"${number}" if use_dot else f"${number.replace('.', ',')}"

    # Format all rows as strings
    full_headers = ["Pay period"] + headers + ["TOTAL"]
    formatted_rows = []

    for row in table_data:
        formatted_row = [str(row[0])] + [format_number(cell) for cell in row[1:-1]] + [format_number(row[-1])]
        formatted_rows.append(formatted_row)

    formatted_sum = [str(sum_row[0])] + [format_number(cell) for cell in sum_row[1:-1]] + [format_number(sum_row[-1])]

    # Combine everything to compute column widths
    all_rows = [full_headers] + formatted_rows + [formatted_sum]
    col_widths = [max(len(cell) for cell in col) for col in zip(*all_rows)]

    def format_row(row, sep_left='│', sep_mid='│', sep_right='│'):
        return sep_left + sep_mid.join(
            f" {cell:>{w}} " for cell, w in zip(row, col_widths)
        ) + sep_right

    def format_line(left, mid, center, right):
        return left + center.join(mid * (w + 2) for w in col_widths) + right

    # Print table
    print(f"\nPayout across all nodes from {START_DATE} to {END_DATE}:\n")

    top = format_line('╒', '═', '╤', '╕')
    header_sep = format_line('╞', '═', '╪', '╡')
    middle_sep = format_line('├', '─', '┼', '┤')
    bottom = format_line('╘', '═', '╧', '╛')

    print(top)
    print(format_row(full_headers))
    print(header_sep)
    for row in formatted_rows:
        print(format_row(row))
    print(middle_sep)
    print(format_row(formatted_sum))
    print(bottom)


def save_csv(table_data, headers, overwrite, locale):
    use_dot = locale == "en"
    delimiter = "," if use_dot else ";"
    decimals = "." if use_dot else ","

    filename = "node-history.csv"
    if not overwrite:
        i = 1
        while os.path.exists(filename):
            filename = f"node-history{i}.csv"
            i += 1

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(["Pay period"] + headers)
        for row in table_data:
            row_out = [row[0]] + [str(f"{val:.2f}").replace(".", decimals) for val in row[1:-1]]
            writer.writerow(row_out)

    print(f"\nCSV exported to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetches payout data for Storj nodes and outputs a summary table.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-c", "--csv", action="store_true", help="Export the result table as CSV (node-history.csv)")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite 'node-history.csv' if it already exists")
    parser.add_argument("-l", "--locale", choices=["de", "en"], default="de", help="Select number format (de = 1,23 ; en = 1.23)")

    args = parser.parse_args()

    months = generate_months(START_DATE, END_DATE)
    table, sum_row = build_table(months, PORTS, NODE_IP)
    print_table(table, CUSTOM_HEADERS, sum_row, locale=args.locale)

    if args.csv:
        save_csv(table, CUSTOM_HEADERS, args.overwrite, locale=args.locale)


if __name__ == "__main__":
    main()
