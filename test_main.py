import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from google.genai import errors
from typer.testing import CliRunner

from main import app


class CliTests(unittest.TestCase):
    @patch("main.load_dotenv")
    @patch("main.genai.Client")
    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True)
    def test_message_is_followed_by_welcome_and_operator_notice(
        self, client_class: unittest.mock.MagicMock, load_dotenv: unittest.mock.MagicMock
    ) -> None:
        client = client_class.return_value.__enter__.return_value
        client.interactions.create.return_value.output_text = "Gemini response"
        result = CliRunner().invoke(app, input="Hello\n")

        self.assertEqual(result.exit_code, 0)
        client_class.assert_called_once_with(api_key="test-key")
        client.interactions.create.assert_called_once_with(
            model="gemini-4-hydrogen", input="Hello"
        )
        self.assertLess(
            result.output.index("Please write your message"),
            result.output.index("Welcome!"),
        )
        self.assertLess(
            result.output.index("Welcome!"),
            result.output.index("A human operator will join the conversation soon."),
        )
        self.assertIn("Gemini response", result.output)

    @patch("main.load_dotenv")
    @patch("main.genai.Client")
    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_is_reported(
        self, client_class: unittest.mock.MagicMock, load_dotenv: unittest.mock.MagicMock
    ) -> None:
        result = CliRunner().invoke(app, input="Hello\n")

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("GEMINI_API_KEY is not set", result.output)
        client_class.assert_not_called()

    @patch("main.load_dotenv")
    @patch("main.genai.Client")
    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True)
    def test_empty_response_is_reported(
        self, client_class: unittest.mock.MagicMock, load_dotenv: unittest.mock.MagicMock
    ) -> None:
        client = client_class.return_value.__enter__.return_value
        client.interactions.create.return_value.output_text = None

        result = CliRunner().invoke(app, input="Hello\n")

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Gemini returned no text response", result.output)

    @patch("main.load_dotenv")
    @patch("main.genai.Client")
    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True)
    def test_api_error_is_reported(
        self, client_class: unittest.mock.MagicMock, load_dotenv: unittest.mock.MagicMock
    ) -> None:
        client = client_class.return_value.__enter__.return_value
        client.interactions.create.side_effect = errors.APIError(
            429, {"error": {"message": "Quota exceeded"}}
        )

        result = CliRunner().invoke(app, input="Hello\n")

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Gemini API error", result.output)

    @patch("main.genai.Client")
    def test_environment_file_and_existing_variable(
        self, client_class: unittest.mock.MagicMock
    ) -> None:
        client = client_class.return_value.__enter__.return_value
        client.interactions.create.return_value.output_text = "Gemini response"
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text("GEMINI_API_KEY=file-key\n", encoding="utf-8")
            for environment, expected in (
                ({}, "file-key"),
                ({"GEMINI_API_KEY": "environment-key"}, "environment-key"),
            ):
                with self.subTest(expected=expected):
                    client_class.reset_mock()
                    with patch.dict("os.environ", environment, clear=True):
                        with patch("dotenv.main.find_dotenv", return_value=str(env_file)):
                            result = CliRunner().invoke(app, input="Hello\n")
                    self.assertEqual(result.exit_code, 0)
                    client_class.assert_called_once_with(api_key=expected)

    def test_end_of_input_does_not_welcome_user(self) -> None:
        result = CliRunner().invoke(app, input="")

        self.assertNotEqual(result.exit_code, 0)
        self.assertNotIn("Welcome!", result.output)


if __name__ == "__main__":
    unittest.main()
