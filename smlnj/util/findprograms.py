import os

def findprograms (programs, directories=None):
    """
    Searches along the path variable for each program in programs.
    Accepts an optional parameter which is a sequence of
    directories which will also be searched.
    """
    installed = {}
    paths = os.environ["PATH"].split(":")

    if directories is not None:
        paths += directories

    for program in programs:
        installed[program] = None

        for location in map(lambda path : os.path.join (path, program),
                            paths):
            if os.path.exists(location):
                installed[program] = location
                break

    return installed
