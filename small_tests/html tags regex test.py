import re

line = '<ia>S</ia>-malate'

def process_html(text):
    html_tags = re.findall('</?[A-Za-z]+>', text)

    print(html_tags)

    for tag in html_tags:
        text = text.replace(tag, '')

    return text

print(process_html(line))