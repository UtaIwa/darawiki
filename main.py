from bottle import run, get, post, template, request, redirect
from markdown import markdown
import os
import urllib.parse
import glob

def parse_index_list(link_item, nests):
    result = ''
    splited = link_item.split('/')
    depth = 0
    for item in splited[:-1]:
        if depth < len(nests) and item != nests[depth]:
            nests = nests[:depth-1]
            result += f'</ul><ul><li>{item}</li><ul>'
            nests.append(item)
    result += f'<li><a href="/docs/{link_item[:-3]}">{splited[-1][:-3]}</a></li>'
    return result, nests

@get('/')
def index():
    files = glob.glob('./docs/**/*.md', recursive=True)
    page_items = []
    nests = ['']
    for file in files:
        link_text = file[7:].replace('\\','/')
        html, nests = parse_index_list(link_text, nests)
        print(nests)
        page_items.append(html)
        # page_items.append(f'<li><a href="{file[:-3]}">{parse_index_list(link_text)}</a></li>')
    page_list = ''.join(page for page in page_items) + '</ul>'
    return template('./index.html', page_list = page_list)

@get('/docs/<word:path>')
def view(word):
    edit_mode = 'edit' in request.params
    if edit_mode:
        template_file = './templates/edit.html'
    else:
        template_file = './templates/view.html'

    filename = f'./docs/{urllib.parse.unquote(word, "utf8")}.md'
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            content = f.read()
            content = content.replace('\r\n','\n')
            return template(template_file, title = word, content = content if edit_mode else markdown(content, extensions=['nl2br']))
    else:
        return template('./templates/edit.html', title = word, content = '')

if __name__ == '__main__':
    run(host='localhost', port=8080, reloader=True)