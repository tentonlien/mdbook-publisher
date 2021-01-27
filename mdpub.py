# mdbook-publisher
# Author: Tenton Lien
# Date: 1/4/2021

import json
import os
import sys

def parse(name, path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        arr = content.split('\n# ')
        for elem in arr:
            title_pos_start = title_pos_end = 0
            while elem[title_pos_end] != '\n' and title_pos_end < len(elem) - 1:
                title_pos_end = title_pos_end + 1

            title = elem[title_pos_start:title_pos_end]
            with open('projects/' + name + '/src/' + title + '.md', 'w', encoding='utf-8') as fout:
                fout.write(elem[title_pos_end:len(elem)])
                fout.close()


def main():
    # Check and retrieve args
    if len(sys.argv) < 2:
        print('Argument required')
        exit()
    
    project_name = sys.argv[1]

    # Create if project directory not exists
    if not os.path.exists('./projects'):
        print('Creating project directory...')
        os.mkdir('./projects')

    # Intialize project
    if (not os.path.exists('projects/' + project_name)):
        os.mkdir('projects/' + prject_name)
        os.system('mdbook init projects/' + project_name)
    
    # Load config
    src_path = ''
    with open('mdpub.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        for project in config['projects']:
            if (project['name'] == project_name):
                src_path = project['src']
    
    if src_path != '':
        parse(project_name, src_path)


if __name__ == '__main__':
    main()
