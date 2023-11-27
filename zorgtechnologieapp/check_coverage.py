import sys
import subprocess

def calculate_line_coverage(lcov_info_file):
    try:
        # Run lcov to calculate line coverage
        result = subprocess.run(['lcov', '--rc', 'lcov_exclude=external/*', '--summary', lcov_info_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Parse the output to extract line coverage percentage
        lines_summary = result.stdout.splitlines()
        for line in lines_summary:
            if 'lines' in line:
                line_coverage = float(line.split()[1][:-1])  # Extract the percentage value
                return line_coverage
    except subprocess.CalledProcessError as e:
        print(f"Error running lcov: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python check_coverage.py <lcov_info_file> <minimum_line_coverage>")
        sys.exit(1)

    lcov_info_file = sys.argv[1]
    minimum_line_coverage = float(sys.argv[2])

    line_coverage = calculate_line_coverage(lcov_info_file)

    print(f"Line coverage: {line_coverage}%")

    if line_coverage < minimum_line_coverage:
        print(f"Line coverage is below {minimum_line_coverage}%")
        sys.exit(1)
    else:
        print(f"Line coverage is above or equal to {minimum_line_coverage}%")

if __name__ == "__main__":
    main()
