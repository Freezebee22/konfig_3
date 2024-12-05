import unittest
from main import parse_config, convert_to_toml, constants

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        # Очищаем глобальные константы перед каждым тестом
        constants.clear()

    def test_simple_constant_definition(self):
        input_text = """
        def name := q(Example);
        def age := 25;
        |name|
        |age|
        """
        expected_output = {
            "name": "Example",
            "age": 25
        }
        parsed_config = parse_config(input_text)
        self.assertEqual(parsed_config, expected_output)

    def test_complex_structure(self):
        input_text = """
        def arr := [1, 2, 3];
        def nested := { key1 => q(Value1), key2 => [4, 5, |arr|] };
        |nested|
        """
        expected_output = {
            "nested": {
                "key1": "Value1",
                "key2": [4, 5, [1, 2, 3]]
            }
        }
        parsed_config = parse_config(input_text)
        self.assertEqual(parsed_config, expected_output)

    def test_convert_to_toml(self):
        input_text = """
        def greeting := q(Hello);
        def numbers := [10, 20, 30];
        |greeting|
        |numbers|
        """
        parsed_config = parse_config(input_text)
        toml_output = convert_to_toml(parsed_config)
        expected_toml = """greeting = "Hello"
numbers = [ 10, 20, 30,]
"""
        self.assertEqual(toml_output.strip(), expected_toml.strip())

    def test_invalid_syntax(self):
        input_text = """
        def invalid := [1, 2, 3;
        """
        with self.assertRaises(ValueError) as context:
            parse_config(input_text)
        self.assertIn("Невалидное значение", str(context.exception))

if __name__ == "__main__":
    unittest.main()
