# mdbook-publisher
# Author: Tenton Lien
# Date: 1/4/2021

import json
import os
import sys

# Global config
config = {}

def generate(name, path):
    with open(path, 'r', encoding='utf-8') as f:
        summary_text = '# Summary\n\n'
        item_array = f.read().split('\n- ')
        print(str(len(item_array) - 1) + ' item(s) found.')
        
        content = None
        for item in item_array:
            if content == None:
                content = item
            else:
                content = content + '\n\n- ' + item

        # Generate single content file
        arr = content.split('\n# ')
        if arr[0].find('# ') == 0:
            arr[0] = arr[0][2:]

        for elem in arr:
            title_pos_start = title_pos_end = 0
            while elem[title_pos_end] != '\n' and title_pos_end < len(elem) - 1:
                title_pos_end = title_pos_end + 1

            title = elem[title_pos_start : title_pos_end]
            with open('projects/' + name + '/src/' + title.replace(' ', '_') + '.md', 'w', encoding='utf-8') as fout:
                fout.write('# ' + title + '\n' + elem[title_pos_end:len(elem)])
                fout.close()
            
            summary_text = summary_text + '- [' + title + '](./' + title.replace(' ', '_') + '.md)\n'
        
        # Generate SUMMARY.md
        with open('projects/' + name + '/src/SUMMARY.md', 'w', encoding='utf-8') as fout:
            fout.write(summary_text)
            fout.close()
                
    print('Generate success')

    os.system('mdbook build projects/' + name)


def upload(name, target, dest):
    target_host_info = {}

    for host in config['hosts']:
        if host['name'] == target:
            target_host_info = host
            break
    
    if target_host_info == {}:
        print('Error: Target host not found')
        exit()


    cmd = 'sshpass -p \'' + target_host_info['password'] + '\' scp -v -r ./projects/' + name + '/book/* ' + target_host_info['username'] + '@' + target_host_info['address'] + ':' + dest
    print(cmd)
    os.system(cmd)


def main():
    # Load config
    global config
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
        if sys.argv[1] == 'gen' or sys.argv[1] == 'update':
            project_name = sys.argv[2]

            # Create if project directory not exists
            if not os.path.exists('./projects'):
                print('Creating project directory...')
                os.mkdir('./projects')

            # Intialize project
            if (not os.path.exists('projects/' + project_name)):
                os.mkdir('projects/' + project_name)
                os.system('mdbook init projects/' + project_name)
    
            # Fetch soruce markdown file path
            src_path = ''
            target_host = ''
            dest_path = ''
            for project in config['projects']:
                if (project['name'] == project_name):
                    src_path = project['src']
                    target_host = project['host']
                    dest_path = project['dest']
                    break
    
            if src_path != '':
                generate(project_name, src_path)
                
                if sys.argv[1] == 'update':
                    upload(project_name, target_host, dest_path)


if __name__ == '__main__':
    main()
