import os


def read_and_convert(file_path, num_lines=10):
    # Read the last 'num_lines' values from the text file and convert to float

    with open(file_path, "r") as file:
        # Read all lines from the file
        lines = file.readlines()

        # Get the last 'num_lines' lines
        last_lines = lines[-num_lines:]

    # Convert the last lines to float
    values = [float(line.strip()) for line in last_lines]
    return values


def list_scores(file_path):
    # Function to list all scores from a file

    # Read values from the text file and convert to float
    scores = read_and_convert(file_path)

    return scores


def calculate_mean(file_path):
    # Function to calculate mean

    # Read values from the text files and convert to float
    values = read_and_convert(file_path)

    # Calculate the mean for each set of values
    mean = sum(values) / len(values)

    # Return the means
    return mean


def calculate_median_single(values):
    # Calculate the median for a single set of values

    # Sort the list of numbers
    sorted_values = sorted(values)

    # Calculate the median
    n = len(sorted_values)
    if n % 2 == 0:
        # If the number of elements is even, calculate the average of the middle two
        middle1 = sorted_values[n // 2 - 1]
        middle2 = sorted_values[n // 2]
        median = (middle1 + middle2) / 2
    else:
        # If the number of elements is odd, select the middle element
        median = sorted_values[n // 2]

    return median


def calculate_median(file_path):
    # Read values from the text files and convert to float
    values = read_and_convert(file_path)

    # Calculate the median for each set of values
    median = calculate_median_single(values)

    # Return the medians
    return median


def calculate_mean_wrapper(file_paths):
    # Function to calculate mean for multiple files

    # Calculate the mean for each set of values
    means = [calculate_mean(file_path) for file_path in file_paths]

    # Return the means
    return means


def calculate_median_wrapper(file_paths):
    # Function to calculate median for multiple files

    # Calculate the median for each set of values
    medians = [calculate_median(file_path) for file_path in file_paths]

    # Return the medians
    return medians


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_1 = os.path.join(base_dir, "output1.txt")
    file_path_2 = os.path.join(base_dir, "output2.txt")
    file_path_3 = os.path.join(base_dir, "output3.txt")

    # This kept throwing an error because C:/dev/ is a specific path

    # file_path_1 = "C:/dev/6ix-pac/output1.txt"
    # file_path_2 = "C:/dev/6ix-pac/output2.txt"
    # file_path_3 = "C:/dev/6ix-pac/output3.txt"

    means = calculate_mean_wrapper([file_path_1, file_path_2, file_path_3])
    medians = calculate_median_wrapper([file_path_1, file_path_2, file_path_3])

    # Print medians across each life
    print(f"Median across life 1: {medians[0]}")
    print(f"Median across life 2: {medians[1]}")
    print(f"Median across life 3: {medians[2]}")

    # Print means across each life
    print(f"\nMean across life 1: {means[0]}")
    print(f"Mean across life 2: {means[1]}")
    print(f"Mean across life 3: {means[2]}")

    print("\nSUMMARY OVER 10 ITERATIONS:\n")
    # Print overall median and mean
    overall_median = medians[2]
    overall_mean = means[2]
    print(f"\nOverall median from 10 iterations: {overall_median}")
    print(f"Overall mean from 10 iterations: {overall_mean}")

    # Print scores horizontally for each life
    print("\nLife 1 scores:", list_scores(file_path_1))
    print("Life 2 scores:", list_scores(file_path_2))
    print("Life 3 scores:", list_scores(file_path_3))
