import json  # Imports the JSON module for reading and writing flashcards to a file
import random  # Imports the random module for selecting random flashcards in the test mode

class Flashcard:
    def __init__(self, filename="flashcards.json"):
        """
        Initializes the Flashcard class.
        - `filename`: The name of the file where flashcards are stored.
        - Loads flashcards from the file when the program starts.
        """
        self.filename = filename
        self.flashcards = self.load_flashcards()  # Loads flashcards from the file

    def load_flashcards(self):
        """
        A function that loads the flashcards from a JSON file.
        Returns a list of flashcards or an empty list if the file doesn't exist or is invalid.
        """
        try:
            with open(self.filename, "r") as file:
                return json.load(file)  # Loads flashcards as a list of dictionaries
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or contains invalid data, returns an empty list
            return []

    def save_flashcards(self):
        """
        A function that saves the current flashcards to a JSON file.
        Ensures that all changes are persistent across sessions.
        """
        with open(self.filename, "w") as file:
            json.dump(self.flashcards, file, indent=4)  # Saves flashcards in a human-readable format

    def add_flashcard(self):
        """
        A function to add a new flashcard.
        Prompts the user for a question and an answer, then saves it to the list and file.
        """
        question = input("Enter the question for your new Flashcard: ")
        if question.lower() == "menu":
            return  # Returns to the menu if the user types 'menu'
        answer = input("Enter the answer for your new Flashcard: ")
        if answer.lower() == "menu":
            return  # Returns to the menu if the user types 'menu'

        # Adds the new flashcard to the list
        self.flashcards.append({'question': question, 'answer': answer})
        self.save_flashcards()  # Saves the updated flashcards to the file
        print("Flashcard added successfully!")

    def view_flashcards(self):
        """
        Function to display all flashcards with their questions and answers.
        """
        if not self.flashcards:
            print("No flashcards available.")  # Informs the user if the list is empty
        else:
            for i, flashcard in enumerate(self.flashcards, start=1):
                # Prints each flashcard with a number
                print(f"{i}. Question: {flashcard['question']} - Answer: {flashcard['answer']}")

    def delete_flashcard(self):
        """
        Function to delete a specific flashcard by typing its number.
        Prompts the user to select a flashcard to delete and removes it from the list.
        """
        self.view_flashcards()  # Shows all flashcards first
        try:
            flashcard_num = input("Enter the number of the flashcard to delete (or type 'menu' to go back): ")
            if flashcard_num.lower() == "menu":
                return  # Returns to the menu if the user types 'menu'
            flashcard_num = int(flashcard_num)  # Converts the input to an integer

            if 1 <= flashcard_num <= len(self.flashcards):
                # Removes the selected flashcard from the list
                removed = self.flashcards.pop(flashcard_num - 1)
                self.save_flashcards()  # Saves the updated list to the file
                print(f"Flashcard '{removed['question']}' deleted successfully!")
            else:
                print("Invalid flashcard number.")  # Informs the user of an invalid flashcard selection
        except ValueError:
            print("Invalid input. Please enter a number.")  # Handles non-integer inputs

    def study_flashcards(self):
        """
        Function to study flashcards.
        The user reviews a specified number of flashcards by seeing the question and revealing the answer.
        """
        if not self.flashcards:
            print("No flashcards available to study.")
            return

        try:
            # Asks the user how many flashcards they want to study
            num = int(input(f"How many flashcards would you like to study? (Max: {len(self.flashcards)}): "))
            if num > len(self.flashcards):
                print("You requested more flashcards than available. Using all available flashcards.")
                num = len(self.flashcards)
        except ValueError:
            print("Invalid input. Returning to menu.")
            return

        for i, flashcard in enumerate(self.flashcards[:num]):
            print(f"\nQuestion {i + 1}: {flashcard['question']}")
            command = input("Press Enter to see the answer or type 'menu' to go back: ").strip().lower()
            if command == "menu":
                return  # Returns to the menu if the user types 'menu'
            print(f"Answer: {flashcard['answer']}")

    def test_flashcards(self):
        """
        Function to test the user on random flashcards.
        The user answers a random selection of flashcards and receives a score.
        """
        if not self.flashcards:
            print("No flashcards available for testing.")
            return

        try:
            # Asks the user how many flashcards they want to be tested on
            num = int(input(f"How many flashcards would you like to be on the test? (Max: {len(self.flashcards)}): "))
            if num > len(self.flashcards):
                print("You requested more flashcards than available. Using all available flashcards.")
                num = len(self.flashcards)
        except ValueError:
            print("Invalid input. Returning to menu.")
            return

        score = 0  # Initializes the score
        total = num
        test_flashcards = random.sample(self.flashcards, num)  # Randomly selects flashcards

        for i, flashcard in enumerate(test_flashcards, start=1):
            print(f"\nQuestion {i}: {flashcard['question']}")
            user_answer = input("Your answer (or type 'skip' to move on, 'menu' to go back): ").strip()
            if user_answer.lower() == "menu":
                return  # Returns to the menu if the user types 'menu'
            elif user_answer.lower() == "skip":
                print(f"Skipped. The correct answer was: {flashcard['answer']}")
            elif user_answer.lower() == flashcard['answer'].lower():
                print("Correct!")
                score += 1  # Increments the score for a correct answer
            else:
                print(f"Wrong! The correct answer is: {flashcard['answer']}")
        print(f"\nTest complete! Your score: {score}/{total}")

def show_menu():
    """
    Displays the main menu options to the user.
    """
    print("\nWelcome to the Flashcard Management System")
    print("1. Add a new flashcard")
    print("2. View all flashcards")
    print("3. Delete a flashcard")
    print("4. Study flashcards")
    print("5. Take a test")
    print("6. Exit")

def flashcard_app():
    """
    Main application loop.
    Handles user input and navigation between menu options.
    """
    app = Flashcard()  # Creates an instance of the Flashcard class
    while True:
        show_menu()  # Displays the menu
        try:
            choice = int(input("Enter your choice: "))  # Gets user's choice
            if choice == 1:
                app.add_flashcard()
            elif choice == 2:
                app.view_flashcards()
            elif choice == 3:
                app.delete_flashcard()
            elif choice == 4:
                app.study_flashcards()
            elif choice == 5:
                app.test_flashcards()
            elif choice == 6:
                print("Exiting the Flashcard Management System. Goodbye!")
                break  # Exits the loop to end the program
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")  # Handles non-integer inputs

# Runs the app
flashcard_app()
