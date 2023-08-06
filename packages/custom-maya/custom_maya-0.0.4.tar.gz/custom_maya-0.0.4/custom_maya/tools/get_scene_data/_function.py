import os
import sys

import maya.standalone
import custom_maya


def get_data(file_path):
    maya.standalone.initialize(name='python')
    import maya.cmds as cmds
    cs = custom_maya.CustomScene(file_path)
    cmds.file(file_path, open=True, options='v=0', iv=True, f=True)
    short_name, _ = os.path.splitext(os.path.basename(file_path))
    #
    with open(f'D:\\Maya\\{short_name}.txt', 'w') as f:
        f.write(str(cs.get_custom_properties())+str(cmds.ls(type='transform')))

        print('写入文件')
    maya.standalone.uninitialize()
    os._exit()


if __name__ == '__main__':
    get_data(sys.argv[1])
