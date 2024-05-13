'''
用于读取相应数据文件中的信息，便于后期核查
'''


import csv

# Define the CSV file name
csv_file = "friendly_characters.csv"

# Define a function to read and print the CSV file contents
def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print("ID:", row['id'])
            print("Name:", row['name'])
            print("Race:", row['race'])
            print("Class:", row['military'])
            print("Gender:", row['gender'])
            print("Personality Traits:", row['personality_traits'])
            print("Character Story:", row['character_story'])
            print("Health:", row['health'])
            print("Magic:", row['magic'])
            print("Physical Attack Power:", row['attack_power'])
            print("Magical Attack Power:", row['magic_power'])
            print("Attack Range:", row['attack_range'])
            print("Physical Defense:", row['physical_def'])
            print("Magical Defense:", row['magic_def'])
            print("Speed:", row['speed'])
            print("Movement:", row['move'])
            print("Jump:", row['jump'])
            print()

# Call the function to read and print the CSV file contents
read_csv(csv_file)