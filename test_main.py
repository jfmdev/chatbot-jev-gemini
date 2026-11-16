import unittest

from typer.testing import CliRunner

from main import app


class CliTests(unittest.TestCase):
    def test_message_is_followed_by_welcome_and_operator_notice(self) -> None:
        result = CliRunner().invoke(app, input="Hello\n")

        self.assertEqual(result.exit_code, 0)
        self.assertLess(
            result.output.index("Please write your message"),
            result.output.index("Welcome!"),
        )
        self.assertLess(
            result.output.index("Welcome!"),
            result.output.index("A human operator will join the conversation soon."),
        )

    def test_end_of_input_does_not_welcome_user(self) -> None:
        result = CliRunner().invoke(app, input="")

        self.assertNotEqual(result.exit_code, 0)
        self.assertNotIn("Welcome!", result.output)


if __name__ == "__main__":
    unittest.main()
