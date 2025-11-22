import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('Fixit', 'Bybytoo')
        new_content = new_content.replace('FixIt', 'Bybytoo')
        new_content = new_content.replace('fixit', 'bybytoo')
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.css', '.js', '.json')):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)

if __name__ == "__main__":
    print("Starting rebranding process...")
    process_directory('templates')
    process_directory('static')
    print("Rebranding process completed.")
