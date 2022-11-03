""" Backlog:
done by hand - 1. Create folder Garbage in Home_Work_folder
done by script - 2. Create folders: images, documents, audio, video, archives
3. Write recurcive function
   Script Requirements:
- sort all files by CATEGORIES:
                - pictures ('JPEG', 'PNG', 'JPG', 'SVG')
                - video    ('AVI', 'MP4', 'MOV', 'MKV')
                - documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
                - music     ('MP3', 'OGG', 'WAV', 'AMR')
                - archives  ('ZIP', 'GZ', 'TAR')
                 

    Expected results:
                - list of files in each CATEGORIES
                - list of all met EXTENSIONS 
                - list of all unfamiliar extensions 

4. Write functions for each category processing
5. Write normilize function:
6. Rename all files and folders by normalize function
7. Keep all extention immutable.
8. Delete all empty folders
9. Ignore folders: archives, video, audio, documents, images
10. All found archives unpack in the same name folder in archives folder
11. Do not remove files with unfamiliar extensons, but rename them
NEW:
13. Use asyncio module
14. Use aiopath instead pathlib to remove and rename files



"""


import os
from pathlib import Path                     ###Path
import re
import shutil
import sys
from threading import Thread, Semaphore
from time import time
import asyncio
from aiopath import AsyncPath


#SET_UPS######################################################3

### Set up data containers
set_files_images = set()
set_files_documents = set()
set_files_audio = set()
set_files_video = set()
set_files_archives = set()
set_fam_extension = set()
set_unfam_extension = set()

### Set_up for normilize function
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

TREADS = {}
treads_flag = 0



# Create dict trans with help of zip()
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()



#CLASSES############################################

class MyThread(Thread):

    def __init__(self, path, k_space, name):
        super().__init__()
        self.path = path
        self.k_space = k_space
        self.name = name


    def run(self):
        timer = time()
        search_function (self.path, self.k_space) # recursive case
        print (f'Thread #{self.name} is Done. Time: {time()-timer}')



#DEF#################################################

def search_function (path, k_space):   
    """ Function scan intendent folder at all levels of nestiness and find files and 
    folders with defined extensions.

    First parametr (path) - reveal carrent processing folder
    Second parametr (k_space) - regulate empty space for diferenciation levels of nestiness """

    k_space += 1
    space = " " * 3 * k_space
    global treads_flag

    
    if len(os.listdir(path)) == 0: # base case

        return
    else:
        for i in path.iterdir():
            
            on_print = '{:<0} {:<100} {:<10}'.format(space, i.name, 'Folder' if i.is_dir() else 'File')
            
            report.write(on_print + '\n')
            
            if i.is_dir() and i != 'images' and i != 'documents' and i != 'audio' and i != 'video' and i != 'archives' :
                ### All our activities with folders

                print(f'Path: {path}')
                path = Path.joinpath(path, i)                  ###Path
                path_num =len(str(path).split('\\'))
                

                if path_num == path_num_init+1:
                    treads_flag += 1
                    TREADS[treads_flag] = MyThread(path, k_space, treads_flag)
                    TREADS[treads_flag].start()
                    print(f'Tread #{treads_flag} started')
                    print(f'Folder Name: {i}')
                    TREADS[treads_flag].join()


                else:

                    # Recurcive case
                    search_function(path, k_space)  # recursive case


                #search_function (path, k_space) # recursive case
                
                # Delete empty folders or rename it
                if len(os.listdir(i)) == 0:

                    Path.rmdir(i)        ###Path
                
                else:
                    #rename_folder ----> path = i
                    rename_func (i)

            else:
                ### All our activities with files + archives
                #rename_files ----> path = i
                i = rename_func (i)

                                               
                ### Files GRID
                
                # images
                if i.suffix == '.jpeg' or i.suffix == '.png' or i.suffix == '.jpg' or i.suffix == '.svg':
                    
                    #add file in images list
                    set_files_images.add(os.path.basename(i))
                    
                    # add sufix to familiar list
                    set_fam_extension.add(i.suffix)
                    process_pictures (i)

                # video
                elif i.suffix == '.avi' or i.suffix == '.mp4' or i.suffix == '.mov' or i.suffix == '.mkv':
                    
                    #add file in video list
                    set_files_video.add(os.path.basename(i))
                   
                    # add sufix to familiar list
                    set_fam_extension.add(i.suffix)
                    
                    process_video (i)
                
                # documents
                elif i.suffix == '.doc' or i.suffix == '.docx' or i.suffix == '.txt' or i.suffix == '.pdf' or i.suffix == '.xlsx' or i.suffix == '.pptx':
                    
                    #add file in video list
                    set_files_documents.add(os.path.basename(i))
                   
                    # add sufix to familiar list
                    set_fam_extension.add(i.suffix)
                    
                    process_documents (i)
                
                # audio
                elif i.suffix == '.mp3' or i.suffix == '.ogg' or i.suffix == '.wav' or i.suffix == '.amr':
                    
                    #add file in video list
                    set_files_audio.add(os.path.basename(i))
                  
                    # add sufix to familiar list
                    set_fam_extension.add(i.suffix)
                    
                    process_audio (i)
                
                # archives
                elif i.suffix == '.zip' or i.suffix == '.gz' or i.suffix == '.tar':
                    
                    #add file in video list
                    set_files_archives.add(os.path.basename(i))
                  
                    # add sufix to familiar list
                    set_fam_extension.add(i.suffix)
                    
                    process_archives (i)
                else:
                    set_unfam_extension.add(i.suffix)

                continue                              

    k_space -= 1

    
    return k_space, set_files_images, set_files_documents, set_files_audio, set_files_video, set_files_archives

def namestr(obj, namespace):
    """ Function return name of veriable in string"""
    
    return [name for name in namespace if namespace[name] is obj]

def set_prep_for_write (set_x):
    """ Function write list of categories in report file"""

    with open('report.txt', 'a') as report:
        
        report.write(f'{namestr(set_x, globals())}: \n') 
        for item in set_x:
           report.write(str(item) + '\n') 
        report.write('\n\n')
    return namestr(set_x, globals())

def normalize (name):
    """ Function normalize names files and folders"""
    
    p = name.translate(TRANS)
    result = re.sub(r'[^a-zA-Z0-9.]', '_', p)
    return result

def rename_func (path):

    path_file_item = Path (path)               ###Path
    path_folder_item = path_file_item.parent.absolute()
    old_name = os.path.basename(path_file_item)               
    new_name = normalize (old_name)
    new_name_path = Path.joinpath(path_folder_item, new_name)  ###Path

    if new_name != old_name:
        os.rename(path_file_item, new_name_path, src_dir_fd=None, dst_dir_fd=None) ###-----> RENAME
    
    path = new_name_path
    return path

def process_pictures (path):
    """ Function process pictures category"""
    
    #print ('In Path >>>>', path)
    # Make dir if it does not exist yet
    path_base = Path.joinpath(p, 'images')   ###Path

    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Images directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = Path.joinpath(path_base, file_name)       ###Path
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)    ###------> MOVE
        
def process_video (path):
    """ Function process video category"""
        
    # Make dir if it does not exist yet
    path_base = Path.joinpath(p, 'video')                    ###Path
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Video directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = Path.joinpath(path_base, file_name)      ###Path
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)            ###------> MOVE

def process_documents (path):
    """ Function process documents category"""
    
    # Make dir if it does not exist yet
    path_base = Path.joinpath(p, 'documents')                      ###Path
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Documents directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = Path.joinpath(path_base, file_name)                ###Path
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)                 ###------> MOVE

def process_audio (path):
    """ Function process music category"""
    
    # Make dir if it does not exist yet
    path_base = Path.joinpath(p, 'audio')            ###Path
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Audio directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = Path.joinpath(path_base, file_name)            ###Path
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)              ###------> MOVE

def process_archives (path):
    """ Function process archives category"""
    
    # Make dir if it does not exist yet
    path_base = Path.joinpath(p, 'archives')             ###Path
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Archives directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = Path.joinpath(path_base, file_name)           ###Path
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)                          ###------> MOVE
    shutil.unpack_archive(dest_pass, path_base)
    os.remove(dest_pass)

#MAIN_BODY########################################
print('LOG:')
#print(f'Target folder is: {p}.')

with open('report.txt', 'w') as report:
    total_timer = time()
    if __name__ == '__main__':
        if sys.argv[1]:
            p = Path(sys.argv[1])                     ###Path
            path_num_init = (len(str(p).split('\\')))

            print(f'Target folder is: {p}.')
    
            report.write('File structure processing:' + '\n\n')
            search_function (p, 0)

            report.write('\n\n\n')

print (f'You could read report file (report.txt) in your current directory')
print(f"Total time is: {time()-total_timer}")

# python Module_4Web_HW_Korobchenko_04.py D:\TEST\Garbage
    

    

