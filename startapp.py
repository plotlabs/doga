import platform
import os

platform = platform.system()
if platform in ['Linux', 'Darwin']:
    os.system('sh start.sh')
else:
    os.system('start "" /b start.bat')
