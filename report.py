import os
import zipfile
import json

def extract_values(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            return [element["string_list_data"][0]["value"] for element in data]
        elif isinstance(data, dict):
            return [item["string_list_data"][0]["value"] for item in data["relationships_following"]]
        else:
            print("Unknown JSON structure")
            return []

def unzip_latest_zip():
    # Get the list of files in the working directory
    files = os.listdir()

    # Filter out only the zip files
    zip_files = [file for file in files if file.endswith('.zip')]

    if not zip_files:
        print("No zip files found in the working directory.")
        return

    # Find the latest zip file based on modification time
    latest_zip_file = max(zip_files, key=lambda x: os.path.getmtime(x))

    # Extract directory name from the zip file name
    extract_dir = os.path.splitext(latest_zip_file)[0]

    # Create the directory if it does not exist
    os.makedirs(extract_dir, exist_ok=True)

    # Unzip the latest zip file
    with zipfile.ZipFile(latest_zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Successfully extracted {latest_zip_file} to {extract_dir}")

    # Check if the required directories and files exist
    connections_dir = os.path.join(extract_dir, 'connections')
    followers_and_following_dir = os.path.join(connections_dir, 'followers_and_following')
    following_file = os.path.join(followers_and_following_dir, 'following.json')
    followers_file = os.path.join(followers_and_following_dir, 'followers_1.json')

    if os.path.exists(following_file):
        print("Values in following.json:")
        following_values = extract_values(following_file)
        #for value in following_values:
        #    print(value)
    else:
        print(f"The file '{following_file}' does not exist.")

    if os.path.exists(followers_file):
        print("Values in followers_1.json:")
        followers_values = extract_values(followers_file)
        #for value in followers_values:
        #    print(value)
    else:
        print(f"The file '{followers_file}' does not exist.")

    if os.path.exists(following_file) and os.path.exists(followers_file):
        unique_values = set(following_values) - set(followers_values)
        print("Values in following.json but not in followers_1.json:")
        for value in unique_values:
            print(value)

# Example usage:
unzip_latest_zip()
