# coding=UTF-8
# The MIT License (MIT)
# Copyright (c) 2016-2017 HIS e. G.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
from backend.db import PostsaiDB

try:
    import config
    import warnings
except ImportError:
    pass


class Extension:

    def install_extension_setup(self, config):
        """install.py - hook invoked after reading the configuration file"""

        if not "repository_status_permission" in config:
            print("ERROR: Configuration for committstop is missing.")
            self.install_print_config_stub()
            sys.exit(1)



    def install_print_config_stub(self):
        """adds stubs for retrieving the current user name and for permission checking to the config file"""

        print("# configuration for " + __name__)
        print("")
        print("""
def repository_status_permission():
    \"\"\"checks the permission to submit a new commit stop configuration\"\"\"

    # return os.environ.get("AUTHENTICATE_POSTSAI_COMMITSTOP_MANAGER", "False") == "True"
    # return os.environ.get("REMOTE_USER", "-") in ("admin1", "admin2")
    return True
""")


    def install_post_database_structure_update(self):
        """install.py - hook invoked after the main database structure has been created or updated. 
        Extension can add additional tables here"""

        """ Hier die Erstellung der Datenbank """

        create_config_table_sql = """\
CREATE TABLE IF NOT EXISTS repository_status (
    id             INT AUTO_INCREMENT NOT NULL, -- Datenbank id
    configtext     TEXT,                        -- Inhalt der Konfiguration
    username       VARCHAR(254),                -- Benutzername
    changecomment  VARCHAR(254),                -- Änderungskommentar
    changetime     DATETIME,                    -- Änderungszeitpunkt
    PRIMARY KEY (id)
);\
"""
        db = PostsaiDB(vars(config))
        db.connect()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            db.query(create_config_table_sql, None, cursor_type=None)
        db.disconnect()


