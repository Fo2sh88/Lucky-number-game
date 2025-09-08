import random
from datetime import datetime

class Player:
    def __init__(self):
        self.player_name = ""
        self.player_birthdate = ""
        self.player_age = 0
    
    def validate_name(self, name):
        """Validate player name - only letters and one whitespace between first and last name"""
        if not name or not isinstance(name, str):
            return False
        
        # Check if name contains only letters and spaces
        if not all(c.isalpha() or c.isspace() for c in name):
            return False
        
        # Check for exactly one space (between first and last name)
        spaces = name.count(' ')
        if spaces != 1:
            return False
        
        # Check that name doesn't start or end with space
        if name.startswith(' ') or name.endswith(' '):
            return False
        
        return True
    
    def validate_birthdate(self, birthdate):
        """Validate birthdate in yyyymmdd format"""
        if not birthdate or len(birthdate) != 8:
            return False
        
        if not birthdate.isdigit():
            return False
        
        try:
            year = int(birthdate[:4])
            month = int(birthdate[4:6])
            day = int(birthdate[6:8])
            
            # Basic validation
            if year < 1900 or year > 2022:
                return False
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 31:
                return False
            
            # Try to create a date to validate
            datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    def calculate_age(self, birthdate):
        """Calculate age from birthdate (assuming current year is 2022)"""
        if not self.validate_birthdate(birthdate):
            return 0
        
        birth_year = int(birthdate[:4])
        birth_month = int(birthdate[4:6])
        birth_day = int(birthdate[6:8])
        
        # Using December 1, 2022 as reference date instead of December 31
        current_year = 2022
        current_month = 12
        current_day = 1
        
        age = current_year - birth_year
        
        # Adjust if birthday hasn't occurred this year
        if (birth_month > current_month) or (birth_month == current_month and birth_day > current_day):
            age -= 1
        
        return age
    
    def set_player_info(self, name, birthdate):
        """Set player information after validation"""
        if self.validate_name(name) and self.validate_birthdate(birthdate):
            self.player_name = name
            self.player_birthdate = birthdate
            self.player_age = self.calculate_age(birthdate)
            return True
        return False

class LuckyNumberGame:
    def __init__(self):
        self.player = Player()
        self.lucky_list = []
        self.lucky_number = 0
        self.shorter_lucky_list = []
        self.tries_count = 0
    
    def generate_lucky_list(self):
        """Generate a list of 9 random integers between 0-100"""
        self.lucky_list = [random.randint(0, 100) for _ in range(9)]
    
    def generate_lucky_number(self):
        """Generate lucky number and add to lucky list"""
        self.lucky_number = random.randint(0, 100)
        self.lucky_list.append(self.lucky_number)
    
    def create_shorter_list(self):
        """Create shorter list with numbers within 10 of lucky number"""
        min_range = max(0, self.lucky_number - 10)
        max_range = min(100, self.lucky_number + 10)
        
        self.shorter_lucky_list = [num for num in self.lucky_list 
                                 if min_range <= num <= max_range]
    
    def remove_wrong_guess(self, wrong_number):
        """Remove wrong guess from shorter lucky list"""
        if wrong_number in self.shorter_lucky_list:
            self.shorter_lucky_list.remove(wrong_number)
    
    def is_game_over(self):
        """Check if game should end (lucky number found or list too short)"""
        return len(self.shorter_lucky_list) <= 2
    
    def play_game(self):
        """Main game loop"""
        print("Welcome to the Lucky Number Game!")
        
        # Get player information
        while True:
            name = input("Enter your full name (first and last name only): ")
            birthdate = input("Enter your birthdate (yyyymmdd): ")
            
            if self.player.set_player_info(name, birthdate):
                if self.player.player_age >= 18:
                    print(f"Welcome {self.player.player_name}, age {self.player.player_age}!")
                    break
                else:
                    print("You must be at least 18 years old to play. Please try again.")
            else:
                print("Invalid input. Please try again.")
        
        # Game loop
        while True:
            # Generate new game
            self.generate_lucky_list()
            self.generate_lucky_number()
            self.tries_count = 0
            
            print(f"\nLucky list: {self.lucky_list}")
            
            # First guess
            while True:
                self.tries_count += 1
                try:
                    player_input = int(input("Pick the lucky number from the list: "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                
                if player_input == self.lucky_number:
                    print(f"Congratulations, game is over! You got the lucky number from try#{self.tries_count}")
                    break
                else:
                    # Create shorter list
                    self.create_shorter_list()
                    
                    # Game continues with shorter list
                    while True:
                        if self.is_game_over():
                            print("Game over! The list is too short.")
                            break
                        
                        print(f"This is try#{self.tries_count} and new list is: {self.shorter_lucky_list}, choose the lucky number?")
                        
                        try:
                            player_input = int(input())
                        except ValueError:
                            print("Please enter a valid number.")
                            continue
                        
                        self.tries_count += 1
                        
                        if player_input == self.lucky_number:
                            print(f"Congratulations, game is over! You got the lucky number from try#{self.tries_count}")
                            break
                        else:
                            self.remove_wrong_guess(player_input)
                    
                    break
            
            # Ask to play again
            play_again = input("Do you like to play again? (Input y: Yes, and n: No): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    game = LuckyNumberGame()
    game.play_game()