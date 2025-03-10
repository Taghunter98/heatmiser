import unittest
from unittest.mock import patch
from app.commands import commands
import os

class TestCommands(unittest.TestCase):
    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def testCommand(self):
        com = commands.Command("wss://192.168.4.174:4243", "0e0df290-8821-4de8-b14a-45cd3b83c33f")
        com.runRecipe("6am Start Time.")

if __name__ == "__main__":
    unittest.main()