import os
import json
from bs4 import BeautifulSoup
import posixpath

def find_html_files(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_tags_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        tags_div = soup.find_all('div', class_='tags')
        tags = [tag.get_text() for div in tags_div for tag in div.find_all('span')]
    return tags

def generate_tags_index(root_dir):
    tags_index = {}
    html_files = find_html_files(root_dir)
    for file_path in html_files:
        tags = extract_tags_from_html(file_path)
        relative_path = os.path.relpath(file_path, start=root_dir).replace(os.sep, '/')
        for tag in tags:
            if tag in tags_index:
                tags_index[tag].append(relative_path)
            else:
                tags_index[tag] = [relative_path]
    # sort
    tags_index = {k:sorted(v) for k,v in sorted(tags_index.items())}
    return tags_index

def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        

def generate_time_index(root_dir):
    time_index = []
    html_files = find_html_files(root_dir)
    for file_path in html_files:
        relative_path = os.path.relpath(file_path, start=root_dir).replace(os.sep, '/')
        time_index.append(relative_path)
    time_index.sort(reverse=True)
    return time_index

root_directory = '.'
tags_index = generate_tags_index(root_directory)
save_to_json(tags_index, 'tag_index.json')
time_index = generate_time_index(root_directory)
save_to_json(time_index, 'time_index.json')