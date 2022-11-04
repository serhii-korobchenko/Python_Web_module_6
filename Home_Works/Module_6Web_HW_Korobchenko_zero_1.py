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
11. Do not remove files with unfamiliar extensons, but rename them """

from dataclasses import replace
import os
from pathlib import Path
import re
import shutil
import sys
import asyncio
from aiopath import AsyncPath
from time import time

#SET_UPS######################################################3



### Set_up for normilize function
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

# Create dict trans with help of zip()
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

#DEF#################################################

async def search_function (path, k_space):
    """ Function scan intendent folder at all levels of nestiness and find files and 
    folders with defined extensions.

    First parametr (path) - reveal carrent processing folder
    Second parametr (k_space) - regulate emty space for diferenciation levels of nestiness """

    k_space += 1
    space = " " * 3 * k_space
    
    if len(os.listdir(path)) == 0: # base case
        # Delete empty folders
        #Path.rmdir(path)
        return 
    else:
        async for i in path.iterdir():
            
            on_print = '{:<0} {:<100} {:<10}'.format(space, i.name, 'Folder' if i.is_dir() else 'File')
            

            
            if i.is_dir() and i != 'images' and i != 'documents' and i != 'audio' and i != 'video' and i != 'archives' :
                ### All our activities with folders

                path = AsyncPath.joinpath(path, i)
                await search_function (path, k_space) # recursive case
                
                # Delete empty folders or rename it
                if len(os.listdir(i)) == 0: 
                    await AsyncPath.rmdir(i)
                
                else:
                    #rename_folder ----> path = i
                    await rename_func (i)

            else:
                ### All our activities with files + archives
                #rename_files ----> path = i
                i = await rename_func (i)
                                               
                ### Files GRID
                
                # images
                if i.suffix == '.jpeg' or i.suffix == '.png' or i.suffix == '.jpg' or i.suffix == '.svg':
                    
                    #add file in images list
                    #set_files_images.add(os.path.basename(i))
                    
                    # add sufix to familiar list
                    #set_fam_extension.add(i.suffix)
                    await process_pictures (i)

                # video
                elif i.suffix == '.avi' or i.suffix == '.mp4' or i.suffix == '.mov' or i.suffix == '.mkv':
                    
                    #add file in video list
                    #set_files_video.add(os.path.basename(i))
                   
                    # add sufix to familiar list
                    #set_fam_extension.add(i.suffix)
                    
                    process_video (i)
                
                # documents
                elif i.suffix == '.doc' or i.suffix == '.docx' or i.suffix == '.txt' or i.suffix == '.pdf' or i.suffix == '.xlsx' or i.suffix == '.pptx':
                    
                    #add file in video list
                    #set_files_documents.add(os.path.basename(i))
                   
                    # add sufix to familiar list
                    #set_fam_extension.add(i.suffix)
                    
                    process_documents (i)
                
                # audio
                elif i.suffix == '.mp3' or i.suffix == '.ogg' or i.suffix == '.wav' or i.suffix == '.amr':
                    
                    #add file in video list
                    #set_files_audio.add(os.path.basename(i))
                  
                    # add sufix to familiar list
                    #set_fam_extension.add(i.suffix)
                    
                    process_audio (i)
                
                # archives
                elif i.suffix == '.zip' or i.suffix == '.gz' or i.suffix == '.tar':
                    
                    #add file in video list
                    #set_files_archives.add(os.path.basename(i))
                  
                    # add sufix to familiar list
                    #set_fam_extension.add(i.suffix)
                    
                    process_archives (i)
                #else:
                    #set_unfam_extension.add(i.suffix)

                continue                              

    k_space -= 1
    
    return await k_space

def namestr(obj, namespace):
    """ Function return name of veriable in string"""
    
    return [name for name in namespace if namespace[name] is obj]


def normalize (name):
    """ Function normalize names files and folders"""
    
    p = name.translate(TRANS)
    result = re.sub(r'[^a-zA-Z0-9\.]', '_', p)
    return result

async def rename_func (path):

    path_file_item = AsyncPath(path)

    path_folder_item = path_file_item.parent.absolute()
    old_name = os.path.basename(path_file_item)               
    new_name = normalize (old_name)
    new_name_path = AsyncPath.joinpath(path_folder_item, new_name)



    if new_name != old_name:
        await path_file_item.rename(new_name_path)
        #os.rename(path_file_item, new_name_path, src_dir_fd=None, dst_dir_fd=None)
    

    path = new_name_path

    return await path

async def process_pictures (path):
    """ Function process pictures category"""
    
    #print ('In Path >>>>', path)
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'images')

    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Images directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)
        
def process_video (path):
    """ Function process video category"""
        
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'video')
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Video directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)

def process_documents (path):
    """ Function process documents category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'documents')
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Documents directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)

def process_audio (path):
    """ Function process music category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'audio')
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Audio directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)

def process_archives (path):
    """ Function process archives category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'archives')
    
    isExist = os.path.exists(path_base) # Check whether the specified path exists or not

    if not isExist:
        os.makedirs(path_base)  # Create a new directory because it does not exist 
        #print("Archives directory has been created!")

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)
    #print ('Dest path>>>>', dest_pass)
    
    shutil.move(path, dest_pass)
    shutil.unpack_archive(dest_pass, path_base)
    os.remove(dest_pass)

#MAIN_BODY########################################
async def main():
    global p
    timer = time()
    print('LOG:')
    if sys.argv[1]:
        p = AsyncPath(sys.argv[1])
        print(f'Target folder is: {p}.')
        await search_function(p, 0)

    print(f'You could read report file (report.txt) in your current directory')
    print(f'Total time: {time() - timer}')




if __name__ == '__main__':
    asyncio.run (main())


# python Module_6_HW_Korobchenko.py D:\TEST\Garbage
    

    

