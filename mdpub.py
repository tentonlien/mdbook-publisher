# mdbook-publisher
# Author: Tenton Lien
# Date: 1/4/2021

import json
import os
import sys

def generate(name, path):
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
                
    print('Generate success')


def main():
    # Load config
    config = {}
    with open('mdpub.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Check and retrieve args
    if len(sys.argv) == 2:
        if sys.argv[1] == 'help':
            print('mdpub (mdbook-publisher)')
            print('Copyright 2021 Tenton Lien. All Rights Reserved.')
            print()
            print('config add host        -- Add host info to config')
            print('       add project     -- Add project to config')
            print('       rm host         -- Remove host info from config')
            print('       rm project      -- Remove project info from config')
            print('gen                    -- Generate mdbook project from source markdown file')
            print('list                   -- List existing projects')
            print('update                 -- Generate from source and upload to target host')
        elif sys.argv[1] == 'list':
            for project in config['projects']:
                print(project['name'], project['src'])
        else:
            print('Missing argument')

    elif len(sys.argv) == 3:
        if sys.argv[1] == 'gen':
            project_name = sys.argv[2]

            # Create if project directory not exists
            if not os.path.exists('./projects'):
                print('Creating project directory...')
                os.mkdir('./projects')

            # Intialize project
            if (not os.path.exists('projects/' + project_name)):
                os.mkdir('projects/' + prject_name)
                os.system('mdbook init projects/' + project_name)
    
            # Fetch soruce markdown file path
            src_path = ''
            for project in config['projects']:
                if (project['name'] == project_name):
                    src_path = project['src']
                    break
    
            if src_path != '':
                generate(project_name, src_path)


if __name__ == '__main__':
    main()
