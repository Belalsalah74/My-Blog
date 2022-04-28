import os,re
os.chdir('D:\\ue')
files = os.listdir(r'.')

filenames = [file for file in files if file.endswith('.mp4')]
file_names_base = [file.removesuffix('.mp4') for file in filenames]
# print(filenames[:10])

with open('names.txt') as txt:
    new_names = txt.read().split('\n')
    for i in range(125):
        os.rename(filenames[i],f'{file_names_base[i]}-{new_names[i]}.mp4')