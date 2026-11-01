# Vigenère Encryption and Decryption System

A console program that encrypts and decrypts text with the Vigenère cipher, in two modes.

## Run

```
py vigenere.py
```

No extra libraries are needed. Run the tests with `py -m unittest -v`.

## How to use

1. Choose the mode: **1 = Basic**, **2 = Advanced**.
2. Choose the operation: **1 = Encrypt**, **2 = Decrypt**.
3. Enter the text and the key. Empty text or an invalid key is rejected and asked again.
4. The result is printed. Decrypt it with the same key and mode to get the original text.

## How the Vigenère cipher works

Each letter of the text is shifted by an amount given by the matching letter of the key. The key is repeated to cover the whole text.

Example (basic mode), key `LEMON`:

```
Text:  A T T A C K A T D A W N
Key:   L E M O N L E M O N L E
Shift: 11 4 12 14 13 11 4 12 14 13 11 4
Cipher L X F O P V E F R N H R
```

- Encryption: `new_position = (text_position + key_position) mod size`
- Decryption: `new_position = (text_position - key_position) mod size`

## Basic mode

- The alphabet is explicitly stored in an array: `ALPHABET = ['A', 'B', ..., 'Z']` (26 letters).
- Only letters are encrypted. Digits, spaces and punctuation stay unchanged.
- Upper and lower case are preserved. The key is case-insensitive and must contain letters only.
- The key letter moves to the next one only when a letter is encrypted.

## Advanced mode

- Every character with ASCII code **32 to 126** (95 printable characters, from space to `~`) is encrypted, including digits, spaces and punctuation.
- The character set is generated from the codes (`ASCII_MIN`, `ASCII_MAX`), so no array is needed.
- Formula: `new_code = (code - 32 ± key_code_shift) mod 95 + 32`, where the shift is `ord(key_char) - 32`.
- The key may use any character from the same range.
- Characters outside the range (for example a new line) stay unchanged.

## Code structure

| Part | Purpose |
|---|---|
| Constants | `ALPHABET`, `ASCII_MIN`, `ASCII_MAX`, `ASCII_SIZE`, `ENCRYPT`, `DECRYPT` |
| `validate_basic_key`, `validate_advanced_key` | Check the key |
| `vigenere_basic`, `encrypt_basic`, `decrypt_basic` | Basic mode |
| `vigenere_advanced`, `encrypt_advanced`, `decrypt_advanced` | Advanced mode |
| `ask_choice`, `ask_text`, `ask_key`, `main` | User input and menu |
