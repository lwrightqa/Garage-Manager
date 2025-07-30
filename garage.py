import csv
import os

# --- Constants ---
GARAGE_FILE = "garage.csv"

# --- Class Definitions ---
class Car:
    """Represents a single car with its attributes."""

    def __init__(self, color: str, year: int, make: str, model: str):
        self.color = color
        # Store the year as an integer for potential future operations (e.g., sorting).
        self.year = year
        self.make = make
        self.model = model

    def __str__(self):
        """Provides a user-friendly string representation of the Car object."""
        return f"{self.color} {self.year} {self.make} {self.model}"

class Garage:
    """Manages a collection of Car objects and handles persistence via a CSV file."""

    def __init__(self):
        """Initializes an empty list to hold car objects."""
        self.cars = []

    def load(self, file_path: str):
        """Loads car data from a CSV file into the garage."""
        if not os.path.exists(file_path):
            print("Garage file not found. Starting with an empty garage.")
            return

        try:
            # Open the file in read mode ('r').
            with open(file_path, mode='r', newline='') as f:
                reader = csv.reader(f)
                try:
                    # Skip the header row to avoid creating a car from it.
                    next(reader)
                except StopIteration:
                    # This occurs if the file is empty (e.g., only has a header), which is fine.
                    return

                for row in reader:
                    if row:  # Ensure the row is not empty.
                        # Create a new Car object from the row data.
                        new_car = Car(color=row[0], year=int(row[1]), make=row[2], model=row[3])
                        self.cars.append(new_car)
            print("Garage loaded successfully.")
        except (IOError, IndexError, ValueError) as e:
            # Catch potential errors from a corrupted file and start fresh.
            print(f"Error reading from {file_path}: {e}. Starting with an empty garage.")
            self.cars = []

    def add_car(self, car: Car):
        """Adds a Car object to the list."""
        self.cars.append(car)

    def remove_car(self, car_index: int) -> Car:
        """Removes a car by its 0-based index and returns it."""
        return self.cars.pop(car_index)

    def save(self, file_path: str):
        """Saves the current list of cars to a CSV file."""
        try:
            # Open the file in 'write' mode.
            with open(file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                # Write the header first for clarity and portability.
                writer.writerow(["color", "year", "make", "model"])
                # Write the data for each car object in the list.
                for car_obj in self.cars:
                    writer.writerow([car_obj.color, car_obj.year, car_obj.make, car_obj.model])
            print("Garage saved successfully.")
        except IOError as e:
            print(f"Error saving garage to {file_path}: {e}")

# --- User Interface Functions ---
# Clear screen in terminal view
def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def prompt_for_new_car() -> Car:
    """Handles the user interface for creating a new car."""
    print("\n--- Add a New Car ---")
    color = input("Enter color: ")

    # Input validation for the year to ensure it's a number.
    while True:
        year_input = input("Enter year: ")
        try:
            year = int(year_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the year.")

    make = input("Enter make: ")
    model = input("Enter model: ")

    return Car(color, year, make, model)

def list_cars(garage: Garage):
    """Displays the list of cars currently in the garage."""
    print("Cars in Garage: ")
    if not garage.cars:
        print("The garage is empty.")
    else:
        for i, car_obj in enumerate(garage.cars):
            print(f"{i + 1}. {car_obj}")

def delete_car(garage: Garage):
    """Handles the user interface flow for deleting a car."""
    print("\n--- Delete a Car ---")
    if not garage.cars:
        print("The garage is empty. Nothing to delete.")
        return

    list_cars(garage)  # Show the user the cars to choose from
    try:
        car_num_to_delete = int(input("Enter the number of the car to delete: "))

        if 1 <= car_num_to_delete <= len(garage.cars):
            # Use the remove_car method, adjusting for 0-based index
            deleted_car = garage.remove_car(car_num_to_delete - 1)
            print(f"\nCar '{deleted_car}' deleted successfully.")
            garage.save(GARAGE_FILE)
        else:
            print("Invalid car number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# --- Main Application Logic ---
def main():
    """Main function to run the garage management application."""
    my_garage = Garage()
    my_garage.load(GARAGE_FILE)

    while True:
        clear_screen()

        print("\n--------- GARAGE MAIN MENU ---------")
        print("1. Add Car")
        print("2. List Cars")
        print("3. Delete Car")
        print("4. Exit")
        print("------------------------------------")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_car = prompt_for_new_car()
            my_garage.add_car(new_car)
            my_garage.save(GARAGE_FILE)
            print(f"\nCar '{new_car}' added to the garage.")

        elif choice == "2":
            list_cars(my_garage)

        elif choice == "3":
            delete_car(my_garage)

        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Script Entry Point ---
if __name__ == "__main__":
    main()