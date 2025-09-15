import os
import sys
from collections import defaultdict

# Check for command-line argument
if len(sys.argv) != 2:
	print("Usage: python local-common-occurrences.py <folder_path>")
	sys.exit(1)

folder_path = sys.argv[1]
username_files = defaultdict(set)  # username -> set of filenames

# Verify the path exists
if not os.path.isdir(folder_path):
	print(f"Error: '{folder_path}' is not a valid directory.")
	sys.exit(1)

# Process files
for filename in os.listdir(folder_path):
	file_path = os.path.join(folder_path, filename)
	if os.path.isfile(file_path):
		with open(file_path, 'r') as file:
			for line in file:
				username = line.strip()
				if username:
					username_files[username].add(filename)

results = {
	username: len(files)
	for username, files in username_files.items()
	if len(files) > 1
}

# Write results to file
output_file = 'common-occurrences.txt'
with open(output_file, 'w') as out:
	for username, count in sorted(results.items(), key=lambda x: (-x[1], x[0])):
		out.write(f"https://github.com/{username}, {count}\n")
