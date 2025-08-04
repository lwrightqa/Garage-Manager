import pytest
from garage.garage import Car, Garage, prompt_for_new_car, list_cars, delete_car

# --- Fixtures ---
@pytest.fixture
def sample_car():
    """Fixture creates a single, standard Car object for testing."""
    return Car(color="Red", year=2022, make="Ford", model="Mustang")

@pytest.fixture
def populated_garage():
    """Fixture creates a garage with a couple of cars in it for testing."""
    g = Garage()
    g.add_car(Car("Blue", 2020, "Tesla", "Model 3"))
    g.add_car(Car("Black", 2023, "Rivian", "R1T"))
    return g


# --- Test Classes for Models and Logic ---

class TestCar:
    """Groups tests related to the Car data model."""

    def test_car_creation(self, sample_car):
        """Tests that the Car object is initialized with the correct attributes."""
        assert sample_car.color == "Red"
        assert sample_car.year == 2022
        assert sample_car.make == "Ford"
        assert sample_car.model == "Mustang"

    def test_car_str(self, sample_car):
        """Tests the __str__ method to ensure it's human-readable."""
        assert str(sample_car) == "Red 2022 Ford Mustang"


class TestGarage:
    """Groups tests related to the Garage class logic and persistence."""

    def test_garage_add_car(self, sample_car):
        """Tests adding a single car to an empty garage."""
        g = Garage()
        g.add_car(sample_car)
        assert len(g.cars) == 1
        assert g.cars[0].make == "Ford"

    def test_garage_remove_car(self, populated_garage):
        """Tests removing a car by its index from the populated garage object."""
        # Act: Remove the car at index 0 (the Tesla).
        deleted_car = populated_garage.remove_car(0)

        # Assert: Check that the garage now contains only one car.
        assert len(populated_garage.cars) == 1
        # Assert that the `remove_car` method returned the correct car.
        assert deleted_car.make == "Tesla"
        # Assert that the remaining car in the garage is the Rivian.
        assert populated_garage.cars[0].make == "Rivian"

    def test_remove_car_invalid_index(self, populated_garage):
        """Tests removing a car with an out-of-bounds index raises an IndexError."""
        with pytest.raises(IndexError):
            populated_garage.remove_car(99)  # 99 is an invalid index.

    def test_save_and_load_cycle(self, populated_garage, tmp_path):
        """
        Tests that saving and then loading a garage preserves the data.
        The `tmp_path` fixture provides a safe, temporary directory for file
        operations, which is automatically cleaned up after the test.
        """
        # Arrange
        file_path = tmp_path / "test_garage.csv"

        # Act: Save the garage, then create a new one and load from the file.
        populated_garage.save(file_path)
        new_garage = Garage()
        new_garage.load(file_path)

        # Assert: The loaded garage should be identical to the original.
        assert len(new_garage.cars) == len(populated_garage.cars)
        assert new_garage.cars == populated_garage.cars

    def test_load_non_existent_file(self, tmp_path, capsys):
        """Tests that loading a non-existent file is handled gracefully."""
        g = Garage()
        non_existent_path = tmp_path / "no_file_here.csv"
        g.load(non_existent_path)

        assert len(g.cars) == 0
        captured = capsys.readouterr()
        assert "Garage file not found" in captured.out

    def test_load_malformed_file(self, tmp_path, capsys):
        """
        Tests that loading a corrupted CSV is handled gracefully.
        The garage should end up empty and a message should be printed.
        """
        # Arrange: Create a file with a row that has missing columns.
        file_path = tmp_path / "malformed_garage.csv"
        file_path.write_text("color,year,make,model\nRed,2022,Ford")

        # Act
        g = Garage()
        g.load(file_path)

        # Assert
        assert len(g.cars) == 0
        captured = capsys.readouterr()
        assert "Error reading from" in captured.out
        assert "Starting with an empty garage" in captured.out


# --- Tests for User Interface Functions ---

def test_prompt_for_new_car(monkeypatch):
    """Tests the user input flow for creating a new car by mocking `input()`."""
    inputs = iter(["Green", "1998", "Honda", "Civic"])

    # Tell monkeypatch to replace the built-in `input` function with a function that returns the next item from our list.
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Act: Call the function that uses `input()`.
    new_car = prompt_for_new_car()

    # Assert: Check that the car was created with our simulated answers.
    assert new_car.year == 1998
    assert new_car.make == "Honda"

def test_list_cars_with_cars(populated_garage, capsys):
    """Tests that `list_cars` prints the correct output when garage has cars."""
    list_cars(populated_garage)

    captured = capsys.readouterr()
    assert "1. Blue 2020 Tesla Model 3" in captured.out
    assert "2. Black 2023 Rivian R1T" in captured.out
    assert "The garage is empty" not in captured.out

def test_list_cars_empty(capsys):
    """Tests that `list_cars` prints the correct message for an empty garage."""
    empty_garage = Garage()
    list_cars(empty_garage)

    captured = capsys.readouterr()
    assert "The garage is empty." in captured.out
    assert "1." not in captured.out  # Make sure no numbered list appears

def test_delete_car_ui_success(populated_garage, monkeypatch, capsys):
    """Tests the user flow for successfully deleting a car."""
    # Arrange
    # 1. Mock the input() to return '1' (for the first car).
    monkeypatch.setattr('builtins.input', lambda _: '1')
    # 2. Mock the save method to prevent file I/O during this unit test.
    monkeypatch.setattr(populated_garage, 'save', lambda _: None)

    # Act
    delete_car(populated_garage)

    # Assert
    assert len(populated_garage.cars) == 1
    assert populated_garage.cars[0].make == "Rivian"
    captured = capsys.readouterr()
    assert "Car 'Blue 2020 Tesla Model 3' deleted successfully." in captured.out

def test_delete_car_ui_invalid_input_non_numeric(populated_garage, monkeypatch, capsys):
    """Tests the user flow for entering non-numeric input for deletion."""
    # Arrange: Mock input() to return 'abc', which should be handled.
    monkeypatch.setattr('builtins.input', lambda _: 'abc')
    original_car_count = len(populated_garage.cars)

    # Act
    delete_car(populated_garage)

    # Assert
    assert len(populated_garage.cars) == original_car_count # No car should be deleted
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a number." in captured.out

def test_delete_car_ui_invalid_input_out_of_bounds(populated_garage, monkeypatch, capsys):
    """Tests the user flow for entering an out-of-bounds number for deletion."""
    monkeypatch.setattr('builtins.input', lambda _: '99')
    delete_car(populated_garage)
    captured = capsys.readouterr()
    assert "Invalid car number." in captured.out