import asyncio
import os
import time

from custom_maya import is_ascii


def get_file_path_list(root_dir):
    res = []
    # root_dir = r'D:\Maya\test_scenes'
    # root_dir = r'D:\test_scenes'
    suffix_list = ['.mb']

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            short_file_name, suffix = os.path.splitext(os.path.basename(file))
            full_path = os.path.join(root, file)
            if suffix in suffix_list and is_ascii(full_path):
                res.append(full_path)
    return res


async def async_get_data(file_path):
    mayapy_path = os.path.normpath(r'C:\Program Files\Autodesk\Maya2023\bin\python.exe')
    script_path = os.path.normpath(r'./_function.py')
    lo = asyncio.get_event_loop()
    f = lo.run_in_executor(
        None,
        os.system,
        '"%s" %s %s' % (mayapy_path, script_path, file_path)
    )
    await f


def main():
    root_dir = r'd:\maya'
    t1 = time.time()
    tasks = [async_get_data(i) for i in get_file_path_list(root_dir)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f'程序运行了{time.time() - t1}')


if __name__ == '__main__':
    main()
