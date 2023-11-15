import argparse
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime
import os

def create_temp_md_file(original_md):
    """ 提取 Markdown 文件的第一行作为标题，第二行作为标签"""
    with open(original_md, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    title = lines[0].strip('#').strip()  # 第一行是标题
    tags = lines[1].strip().split('|')  # 第二行是用 '|' 分割的标签
    """ 创建一个临时的 Markdown 文件，包含除去前几行的内容 """
    temp_md_filename = 'temp_content_markdown.md'
    with open(temp_md_filename, 'w', encoding='utf-8') as temp_md:
        temp_md.writelines(lines[2:])

    return title, tags, temp_md.name

def convert_md_to_html(temp_md_file):
    """ 使用 Pandoc 将 Markdown 转换为 HTML """
    return subprocess.run(['pandoc', temp_md_file, '-t', 'html'],
                          capture_output=True, text=True, encoding='utf-8').stdout

def insert_into_template(title, tags, html_content, template_file, output_file):
    with open(template_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    # Title
    head_div = soup.find('div', {'id': 'head'})
    title_tag = head_div.find('h1', {'id': 'title'})
    title_tag.string = title  # 插入标题
    # time
    current_time = datetime.now().strftime('%Y/%m/%d')
    time_string = soup.new_string(current_time)
    head_div.append("last update: ")
    head_div.append(time_string)

    # Tags
    tags_div = soup.find('div', {'class': 'tags'})
    for tag in tags:
        span = soup.new_tag('span')
        span.string = tag.strip()
        tags_div.append(span)
        if tag != tags[-1]:  # 如果不是最后一个标签，添加分隔符
            separator = soup.new_string(' | ')
            tags_div.append(separator)
    
    content_div = soup.find('div', {'id': 'markdown_content'})
    content_div.clear()
    content_div.append(BeautifulSoup(html_content, 'html.parser'))
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML and embed into a template')
    parser.add_argument('markdown_file', help='The path to the markdown file to convert')
    # parser.add_argument('template_file', help='The path to the HTML template file')
    args = parser.parse_args()
    md_file = args.markdown_file
    template_file = "1900/01/01.html"

    title, tags, temp_md_file = create_temp_md_file(md_file)
    html_content = convert_md_to_html(temp_md_file)
    
    output_file = md_file.rsplit('.', 1)[0] + '.html'  # HTML file with the same name
    insert_into_template(title, tags, html_content, template_file, output_file)
    
    os.remove(temp_md_file)  # 删除临时文件
    
    print(f'HTML generated: {output_file}')
    
    # static generator
    subprocess.run(['python', 'static_generator.py'], check=True)

if __name__ == '__main__':
    main()