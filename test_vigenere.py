import unittest
from unittest import mock

import vigenere as v


class Basic(unittest.TestCase):
    def test_known_vector(self):
        # classic textbook example
        self.assertEqual(v.encrypt_basic("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
        self.assertEqual(v.decrypt_basic("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_non_letters_unchanged_and_case_kept(self):
        ct = v.encrypt_basic("Hello, World! 123", "KEY")
        self.assertEqual(ct[5], ",")
        self.assertEqual(ct[6], " ")
        self.assertEqual(ct[-4:], " 123")
        self.assertTrue(ct[0].isupper() and ct[1].islower())
        self.assertEqual(v.decrypt_basic(ct, "KEY"), "Hello, World! 123")

    def test_lowercase_key_same_as_uppercase(self):
        self.assertEqual(v.encrypt_basic("Attack", "lemon"), v.encrypt_basic("Attack", "LEMON"))

    def test_alphabet_is_an_array_of_26(self):
        self.assertIsInstance(v.ALPHABET, list)
        self.assertEqual(len(v.ALPHABET), 26)

    def test_key_a_changes_nothing(self):
        self.assertEqual(v.encrypt_basic("Hello", "A"), "Hello")


class Advanced(unittest.TestCase):
    def test_roundtrip_all_printable_ascii(self):
        text = "".join(chr(c) for c in range(32, 127))
        for key in ("k", "Secret key!", "~~~", " "):
            self.assertEqual(v.decrypt_advanced(v.encrypt_advanced(text, key), key), text)

    def test_all_chars_encrypted_and_stay_in_range(self):
        ct = v.encrypt_advanced("Hello, World! 123", "key")
        self.assertTrue(all(32 <= ord(c) <= 126 for c in ct))
        self.assertNotEqual(ct, "Hello, World! 123")
        self.assertNotEqual(ct[5], ",")      # punctuation IS encrypted here

    def test_wraparound(self):
        # '~' (126) shifted by key '"' (34 -> shift 2) wraps to code 33 '!'
        self.assertEqual(v.encrypt_advanced("~", '"'), "!")
        self.assertEqual(v.decrypt_advanced("!", '"'), "~")

    def test_outside_range_unchanged(self):
        ct = v.encrypt_advanced("a\nb", "key")
        self.assertEqual(ct[1], "\n")
        self.assertEqual(v.decrypt_advanced(ct, "key"), "a\nb")


class Validation(unittest.TestCase):
    def test_basic_key(self):
        self.assertIsNone(v.validate_basic_key("Lemon"))
        for bad in ("", "abc1", "a b", "é"):
            self.assertIsNotNone(v.validate_basic_key(bad))

    def test_advanced_key(self):
        self.assertIsNone(v.validate_advanced_key("P@ss w0rd!"))
        for bad in ("", "tab\t", "é"):
            self.assertIsNotNone(v.validate_advanced_key(bad))


class Menu(unittest.TestCase):
    def run_menu(self, inputs):
        with mock.patch("builtins.input", side_effect=inputs), mock.patch("builtins.print") as p:
            v.main()
        return [" ".join(map(str, c.args)) for c in p.call_args_list]

    def test_basic_encrypt_with_retries(self):
        out = self.run_menu(["x", "1", "1", "", "ATTACKATDAWN", "", "12", "LEMON", "n"])
        self.assertIn("Result: LXFOPVEFRNHR", out)
        self.assertTrue(any("must not be empty" in line for line in out))
        self.assertTrue(any("letters A-Z only" in line for line in out))

    def test_advanced_decrypt(self):
        ct = v.encrypt_advanced("Hi there!", "key")
        out = self.run_menu(["2", "2", ct, "key", "n"])
        self.assertIn("Result: Hi there!", out)


if __name__ == "__main__":
    unittest.main()
