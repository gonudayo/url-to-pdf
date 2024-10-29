import pdfkit
import re
import time
import random
import os

def extract_urls_and_titles_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    urls_and_titles = []
    title = None

    for line in lines:
        line = line.strip()
        if line and line[0] == "[" and "]" in line:
            title = line.split(" ", 1)[1]
        elif line.startswith("http"):
            if title:
                urls_and_titles.append((title, line))
                title = None

    return urls_and_titles

def sanitize_filename(title):
    return re.sub(r'[\/:*?"<>|]', '', title).strip()

def generate_unique_filename(title, extension=".pdf"):
    base_filename = title
    counter = 1
    unique_filename = f"{base_filename}{extension}"
    while os.path.exists(unique_filename):
        unique_filename = f"{base_filename}_{counter}{extension}"
        counter += 1
    return unique_filename

def save_webpage_as_pdf(url, title, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            options = {
                'disable-javascript': '',
                'encoding': "UTF-8",
                'no-stop-slow-scripts': None
            }

            # 파일명 중복 방지
            unique_filename = generate_unique_filename(title)

            pdfkit.from_url(url, unique_filename, options=options)
            print(f"{unique_filename} 저장 완료!")
            break
        except OSError as e:
            print(f"Error 발생: {e}. 재시도 중... ({retries + 1}/{max_retries})")
            retries += 1
            time.sleep(random.uniform(2, 4))

urls_and_titles = extract_urls_and_titles_from_file("output.txt")

for title, url in urls_and_titles:
    safe_title = sanitize_filename(title)
    save_webpage_as_pdf(url, safe_title)
    time.sleep(random.uniform(2, 4))  # 요청 간격 조정
