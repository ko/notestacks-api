import sys
notestacks = '/home/yaksok/webapps/notestacks_db/htdocs'
if not notestacks in sys.path:
    sys.path.insert(0, notestacks)

from notestacks import app as application


