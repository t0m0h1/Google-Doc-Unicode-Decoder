import requests
import re

def extract_and_print_grid(google_doc_url):
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', google_doc_url)
    if not match:
        raise ValueError("Invalid Google Doc URL.")
    doc_id = match.group(1)

    export_url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
    
    response = requests.get(export_url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the document: status {response.status_code}")
    text = response.text

    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        m = re.match(r'^(.),\s*(\d+),\s*(\d+)$', line)
        if m:
            char, x, y = m.groups()
            points.append((int(x), int(y), char))

    if not points:
        print("No valid data found in the document.")
        return


    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)


    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in points:
        grid[y][x] = char

    # Print grid 
    for row in grid:
        print(''.join(row))