import unittest
from game import Player, LuckyNumberGame

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
    
    def test_validate_name_valid(self):
        """Test valid name validation"""
        self.assertTrue(self.player.validate_name("John Doe"))
        self.assertTrue(self.player.validate_name("Alice Smith"))
    
    def test_validate_name_invalid(self):
        """Test invalid name validation"""
        self.assertFalse(self.player.validate_name("John"))  # No last name
        self.assertFalse(self.player.validate_name("John  Doe"))  # Multiple spaces
        self.assertFalse(self.player.validate_name("John123"))  # Contains numbers
        self.assertFalse(self.player.validate_name(" John Doe"))  # Starts with space
        self.assertFalse(self.player.validate_name("John Doe "))  # Ends with space
        self.assertFalse(self.player.validate_name(""))  # Empty string
        self.assertFalse(self.player.validate_name("John Doe Smith"))  # Too many names
    
    def test_validate_birthdate_valid(self):
        """Test valid birthdate validation"""
        self.assertTrue(self.player.validate_birthdate("19900101"))
        self.assertTrue(self.player.validate_birthdate("20001215"))
        self.assertTrue(self.player.validate_birthdate("19851030"))
    
    def test_validate_birthdate_invalid(self):
        """Test invalid birthdate validation"""
        self.assertFalse(self.player.validate_birthdate("1990101"))  # Too short
        self.assertFalse(self.player.validate_birthdate("199001011"))  # Too long
        self.assertFalse(self.player.validate_birthdate("19901301"))  # Invalid month
        self.assertFalse(self.player.validate_birthdate("19900132"))  # Invalid day
        self.assertFalse(self.player.validate_birthdate("abcd0101"))  # Contains letters
        self.assertFalse(self.player.validate_birthdate(""))  # Empty string
    
    def test_calculate_age(self):
        """Test age calculation"""
        # Test with valid birthdates (assuming current year is 2022)
        self.assertEqual(self.player.calculate_age("19900101"), 32)
        self.assertEqual(self.player.calculate_age("20000101"), 22)
        self.assertEqual(self.player.calculate_age("20041231"), 17)  # Not 18 yet
    
    def test_set_player_info_valid(self):
        """Test setting valid player information"""
        result = self.player.set_player_info("John Doe", "19900101")
        self.assertTrue(result)
        self.assertEqual(self.player.player_name, "John Doe")
        self.assertEqual(self.player.player_birthdate, "19900101")
        self.assertEqual(self.player.player_age, 32)
    
    def test_set_player_info_invalid(self):
        """Test setting invalid player information"""
        result = self.player.set_player_info("John", "19900101")
        self.assertFalse(result)
        
        result = self.player.set_player_info("John Doe", "1990101")
        self.assertFalse(result)

class TestLuckyNumberGame(unittest.TestCase):
    def setUp(self):
        self.game = LuckyNumberGame()
    
    def test_generate_lucky_list(self):
        """Test lucky list generation"""
        self.game.generate_lucky_list()
        self.assertEqual(len(self.game.lucky_list), 9)
        for num in self.game.lucky_list:
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 100)
    
    def test_generate_lucky_number(self):
        """Test lucky number generation and addition to list"""
        self.game.generate_lucky_list()
        initial_length = len(self.game.lucky_list)
        self.game.generate_lucky_number()
        
        self.assertEqual(len(self.game.lucky_list), initial_length + 1)
        self.assertGreaterEqual(self.game.lucky_number, 0)
        self.assertLessEqual(self.game.lucky_number, 100)
        self.assertIn(self.game.lucky_number, self.game.lucky_list)
    
    def test_create_shorter_list(self):
        """Test shorter list creation"""
        self.game.lucky_list = [5, 1, 20, 99, 70, 12, 22, 2, 89, 15]
        self.game.lucky_number = 12
        self.game.create_shorter_list()
        
        expected = [5, 20, 12, 22, 2, 15]  # Numbers between 2 and 22
        self.assertEqual(sorted(self.game.shorter_lucky_list), sorted(expected))
    
    def test_remove_wrong_guess(self):
        """Test removing wrong guess from shorter list"""
        self.game.shorter_lucky_list = [5, 20, 12, 22, 2, 15]
        self.game.remove_wrong_guess(20)
        self.assertNotIn(20, self.game.shorter_lucky_list)
        self.assertEqual(len(self.game.shorter_lucky_list), 5)
    
    def test_is_game_over(self):
        """Test game over condition"""
        self.game.shorter_lucky_list = [1, 2, 3]
        self.assertFalse(self.game.is_game_over())
        
        self.game.shorter_lucky_list = [1, 2]
        self.assertTrue(self.game.is_game_over())
        
        self.game.shorter_lucky_list = [1]
        self.assertTrue(self.game.is_game_over())

if __name__ == '__main__':
    unittest.main()