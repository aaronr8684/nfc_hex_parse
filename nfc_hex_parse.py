import re
import os
import argparse

def parse_nfc_rows(rows):
    combined_hex_data = []
    combined_UID = []

    for row in rows:
        match = re.match(r"\[\s*([0-9A-Fa-f:]+)\s*\]\s*(.+)\s*:\s*(.+)\s*", row)
        if match:
            hex_data = match.group(1).split(":")
            category = match.group(3)
            if category == "DATA":
                combined_hex_data.extend(hex_data)
            else:
                if "UID0" in category:
                    combined_UID.extend(hex_data[0:3])
                    bcc0 = hex_data[3]
                elif "UID3" in category:
                    combined_UID.extend(hex_data)
                elif "BCC1" in category:
                    bcc1 = hex_data[0]
                else:
                    pass # discard extra hex_data for now

    if not combined_hex_data:
        return None

    # Combine UID into single hex string
    uid = ':'.join(combined_UID)

    # Extract data header (first 7 bytes)
    ndef_header = combined_hex_data[:7]

    # Extract ASCII string from remaining bytes
    ascii_bytes = combined_hex_data[7:]
    ascii_string = ''.join(chr(int(byte, 16)) for byte in ascii_bytes if 32 <= int(byte, 16) <= 126)

    data = {
        "UID": uid,
        # "BCC0": bcc0,
        # "BCC1": bcc1,
        "NDEF Header": ndef_header,
        "Payload": ascii_string
    }

    return data

def process_nfc(input, output_file):
    if os.path.isfile(input):
        with open(input, 'r', encoding='utf-8') as infile:
            lines = [line.strip() for line in infile.readlines()]
    else:
        lines = input.strip().split("\n")

    data = parse_nfc_rows(lines)

    if not data:
        return None

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(f"{data}\n")
    else:
        print(data)

    return data

def main():
    parser = argparse.ArgumentParser(description="Convert NFC hex data to metadata and ASCII string.")
    parser.add_argument("-i", "--input", help="Input file containing NFC hex data rows")
    parser.add_argument("-s", "--string", help="NFC hex data as a string with optional '\\n'")
    parser.add_argument("-o", "--output", help="Output file to store parsed metadata")

    args = parser.parse_args()
    print(args.input or args.string)
    if args.input or args.string:
        process_nfc((args.input or args.string), (args.output or ""))
    else:
        print("Please provide either an input file (-i) to process.")

    print("Processing complete.")

if __name__ == "__main__":
    main()
