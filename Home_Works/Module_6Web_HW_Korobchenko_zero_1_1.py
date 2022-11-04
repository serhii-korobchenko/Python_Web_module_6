import os
import re
import sys
import asyncio
from aiopath import AsyncPath
from time import time
import aioshutil
import platform

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

async def search_function (path: AsyncPath):
    """ Function scan intendent folder at all levels of nestiness and find files and 
    folders with defined extensions.

    First parametr (path) - reveal carrent processing folder
    Second parametr (k_space) - regulate emty space for diferenciation levels of nestiness """


    async for i in path.iterdir():

        if await i.is_dir() and i != 'images' and i != 'documents' and i != 'audio' and i != 'video' and i != 'archives' :
            ### All our activities with folders

            path = AsyncPath.joinpath(path, i)
            await search_function(path)# recursive case

            # Delete empty folders or rename it
            if len(os.listdir(i)) == 0:
                await AsyncPath.rmdir(i)


        else:

            ### Files GRID

            # images
            if i.suffix == '.jpeg' or i.suffix == '.png' or i.suffix == '.jpg' or i.suffix == '.svg':

                await process_pictures (i)

            # video
            elif i.suffix == '.avi' or i.suffix == '.mp4' or i.suffix == '.mov' or i.suffix == '.mkv':

                await process_video (i)

            # documents
            elif i.suffix == '.doc' or i.suffix == '.docx' or i.suffix == '.txt' or i.suffix == '.pdf' or i.suffix == '.xlsx' or i.suffix == '.pptx':

                await process_documents (i)

            # audio
            elif i.suffix == '.mp3' or i.suffix == '.ogg' or i.suffix == '.wav' or i.suffix == '.amr':

                await process_audio (i)

            # archives
            elif i.suffix == '.zip' or i.suffix == '.gz' or i.suffix == '.tar':

                await process_archives (i)

            continue
    return

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

    path = new_name_path
    return await path

async def process_pictures (path):
    """ Function process pictures category"""
    
    path_base = AsyncPath.joinpath(p, 'images')

    isExist = await path_base.is_dir() # Check whether the specified path exists or not

    if not isExist:
        await path_base.mkdir(exist_ok=True, parents=True)  # Create a new directory because it does not exist

    file_name = os.path.basename(path)
    
    dest_pass = AsyncPath.joinpath(path_base, file_name)

    await aioshutil.move(path, dest_pass)
        
async def process_video (path):
    """ Function process video category"""
        
    # Make dir if it does not exist yet
    path_base = await AsyncPath.joinpath(p, 'video')

    isExist = await path_base.is_dir()  # Check whether the specified path exists or not

    if not await isExist:
        await path_base.mkdir(exist_ok=True, parents=True)  # Create a new directory because it does not exist

    file_name = os.path.basename(path)

    dest_pass = await AsyncPath.joinpath(path_base, file_name)

    await aioshutil.move(path, dest_pass)

async def process_documents (path):
    """ Function process documents category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'documents')

    isExist = await path_base.is_dir()  # Check whether the specified path exists or not

    if not isExist:
        await path_base.mkdir(exist_ok=True, parents=True)  # Create a new directory because it does not exist

    file_name = os.path.basename(path)

    dest_pass = AsyncPath.joinpath(path_base, file_name)

    await aioshutil.move(path, dest_pass)

async def process_audio (path):
    """ Function process music category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'audio')

    isExist = await path_base.is_dir()  # Check whether the specified path exists or not

    if not isExist:
        await path_base.mkdir(exist_ok=True, parents=True)  # Create a new directory because it does not exist

    file_name = os.path.basename(path)

    dest_pass = AsyncPath.joinpath(path_base, file_name)

    await aioshutil.move(path, dest_pass)

async def process_archives (path):
    """ Function process archives category"""
    
    # Make dir if it does not exist yet
    path_base = AsyncPath.joinpath(p, 'archives')

    isExist = await path_base.is_dir()  # Check whether the specified path exists or not

    if not isExist:
        await path_base.mkdir(exist_ok=True, parents=True)  # Create a new directory because it does not exist

    file_name = os.path.basename(path)

    dest_pass = AsyncPath.joinpath(path_base, file_name)
    
    await aioshutil.move(path, dest_pass)
    await aioshutil.unpack_archive(dest_pass, path_base)
    os.remove(dest_pass)

#MAIN_BODY########################################
async def main():
    global p
    timer = time()
    print('LOG:')
    if sys.argv[1]:
        p = AsyncPath(sys.argv[1])
        print(f'Target folder is: {p}.')
        await search_function(p)

    print(f'Total time: {time() - timer}')

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


# python Module_6_HW_Korobchenko.py D:\TEST\Garbage
    

    

