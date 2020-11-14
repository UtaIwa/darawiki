from bottle import run, get, post, template, request, redirect
from markdown import markdown
import os
import urllib.parse
import glob

@get('/')
def index():
    files = glob.glob('./docs/**/*.md', recursive=True)
    page_items = []
    for file in files:
        link_text = file[7:].replace('\\','/')
        page_items.append(f'<li><a href="{file[:-3]}">{link_text}</a></li>')
    page_list = ''.join(page for page in page_items)
    return template('./index.html', page_list = page_list)

if __name__ == '__main__':
    run(host='localhost', port=8080, reloader=True)