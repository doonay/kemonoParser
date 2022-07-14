with open('kemono_authors', 'r', encoding='utf-8') as file:
    kemono_authors = file.read().split('\n')
''''
for kemono_author in kemono_authors:
    print(kemono_author)
'''
with open('vam_authors', 'r', encoding='utf-8') as file:
    vam_authors = file.read().split('\n')
'''
for vam_author in vam_authors:
    print(vam_author)
'''

for kemono_author in kemono_authors:
    for vam_author in vam_authors:
        if kemono_author == vam_author:
            print(kemono_author)
