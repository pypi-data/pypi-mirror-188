#!/usr/bin/env python
################################################################
import transaction
from traitlets.config import get_config
from IPython import embed
import ZODB
import ZODB.FileStorage
################################################################


class Command:

    def __init__(self, cmd):
        self.cmd = cmd

    def __repr__(self):
        return self.cmd()


def make_command(func):
    return Command(func)


@make_command
def commit():
    transaction.commit()
    return ""


################################################################


if __name__ == '__main__':

    storage = ZODB.FileStorage.FileStorage(
        '.bd/bd.zeo', blob_dir='.bd/blob_data')
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root

    c = get_config()
    c.InteractiveShellEmbed.colors = "Linux"

    embed(config=c, banner1="""
Your database is accessible as the object 'db'.
Your root is accessible in the object 'root'.

For any changes you do you should hit 'commit' to make them permanent
""")
