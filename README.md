# nfc_hex_parse.py
Parse NFC raw hex dumps into usable values. This has only been tested with MiFare EV1 cards

## Parameters
### -i / --input
Input file
### -s / --string
Input string with each line separated by `\n`
### -o / --output
Output file, if this option is omitted, the script will output to the console


## Example usage
### Input file
Text file containing the raw hex data from a utility like NFC Tools

Example (dummy data):
```text
[ 01:02:03:04 ] Addr. 00 : UID0 - UID2 / BCC0
[ 05:06:07:08 ] Addr. 01 : UID3 - UDI6
[ 09:00:00:00 ] Addr. 02 : BCC1 / INT. / LOCK0 - LOCK1
[ 00:00:00:00 ] Addr. 03 : OTP0 - OTP3
[ 03:2D:D1:01 ] Addr. 04 : DATA
[ 29:55:04:79 ] Addr. 05 : DATA
...
```
### Command
```python
python .\nfc_hex_parse.py -i nfc_hex_data.txt
```

### Output
```shell
{'UID': '01:02:03:05:06:07:08', 'NDEF Header': ['03', '2D', 'D1', '01', '29', '55', '04'], 'Payload': 'ascii_string'}
```
