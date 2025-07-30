import pytest
from garage import Car, Garage, prompt_for_new_car, list_cars

# PyTest fixtures
@pytest.fixture
def sample_car():
    # Fixture creates a single, standard Car object for testing
    return Car(color="Red", year=2022, make="Ford", model="Mustang")

@pytest.fixture
def populated_garage():
    # Fixture creates a garage with a couple of cars in it for testing
    g = Garage()
    g.add_car(Car("Blue", 2020, "Tesla", "Model 3"))
    g.add_car(Car("Black", 2023, "Rivian", "R1T"))
    return g

# --- Model Tests ---
def test_car_creation(sample_car):
    # Tests that the Car object is initialized with the correct attributes.
    assert sample_car.color == "Red"
    assert sample_car.year == 2022
    assert sample_car.make == "Ford"
    assert sample_car.model == "Mustang"

def test_car_str_representation(sample_car):
    # Tests the __str__ method to ensure it's human-readable.
    assert str(sample_car) == "Red 2022 Ford Mustang"

# --- Logic/Service Tests ---
def test_garage_add_car(sample_car):
    # Tests adding a single car to an empty garage.
    g = Garage()

    g.add_car(sample_car)

    assert len(g.cars) == 1
    assert g.cars[0].make == "Ford"

def test_garage_remove_car(populated_garage):
    # Tests removing a car by its index from the populated garage object.

    # Act: Remove the car at index 0 (the Tesla).
    deleted_car = populated_garage.remove_car(0)

    # Assert: Check that the garage now contains only one car.
    assert len(populated_garage.cars) == 1
    # Assert that the `remove_car` method returned the correct car.
    assert deleted_car.make == "Tesla"
    # Assert that the remaining car in the garage is the Rivian.
    assert populated_garage.cars[0].make == "Rivian"

def test_remove_car_invalid_index(populated_garage):
    # Tests removing a car with an out-of-bounds index raises an IndexError, as expected.
    with pytest.raises(IndexError):
        populated_garage.remove_car(99) # 99 is an invalid index.

# --- File I/O Tests ---

def test_save_and_load_cycle(populated_garage, tmp_path):
    """
    Tests that saving and then loading a garage preserves the data.
    The `tmp_path` fixture provides a safe, temporary directory for file
    operations, which is automatically cleaned up after the test.
    """
    # Arrange:
    # 1. The `populated_garage` fixture provides our data.
    # 2. `tmp_path` gives us a temporary directory. We create a file path inside it.
    file_path = tmp_path / "test_garage.csv"

    # Act (Part 1): Save the garage data to the temporary file.
    populated_garage.save(file_path)

    # Act (Part 2): Create a NEW, empty garage and load the data from the file.
    new_garage = Garage()
    new_garage.load(file_path)

    # Assert: Check that the new garage has the same data as the original.
    # We compare the number of cars and the attributes of each car.
    assert len(new_garage.cars) == 2
    assert new_garage.cars[0].__dict__ == populated_garage.cars[0].__dict__
    assert new_garage.cars[1].make == "Rivian"


def test_load_non_existent_file(tmp_path, capsys):
    # Tests that the program handles trying to load a file that doesn't exist.
    # The `capsys` fixture lets us capture and inspect text printed to the console.
    g = Garage()
    non_existent_path = tmp_path / "no_file_here.csv"

    g.load(non_existent_path)

    # 1. The garage should remain empty.
    assert len(g.cars) == 0
    # 2. A friendly message should be printed to the user.
    captured = capsys.readouterr() # Reads what was printed
    assert "Garage file not found" in captured.out

# --- User Interface Tests ---

def test_prompt_for_new_car(monkeypatch):
    # Simulates user typing, replacing the input() function
    # Create a list of answers we want to "type" in. The `iter()` makes it so we can get to the next answer each time.
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
    # Use the garage with 2 cars and the `capsys` fixture and call the function that prints to the screen.
    list_cars(populated_garage)

    # Assert: Check the captured output.
    captured = capsys.readouterr()
    assert "1. Blue 2020 Tesla Model 3" in captured.out
    assert "2. Black 2023 Rivian R1T" in captured.out
    assert "The garage is empty" not in captured.out