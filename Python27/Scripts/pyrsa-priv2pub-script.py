#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'rsa==3.1.2','console_scripts','pyrsa-priv2pub'
__requires__ = 'rsa==3.1.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('rsa==3.1.2', 'console_scripts', 'pyrsa-priv2pub')()
    )
