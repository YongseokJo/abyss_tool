import yt

def getEnzoPath(path, dir_name, snap_num):
    print("getEnzoPath")
    if dir_name is not None:
        if dir_name == "RD":
            path = \
                "{}/{}{:04}/RD{:04}".format(path, dir_name, snap_num, snap_num)
        else:
            path = \
                "{}/{}{:04}/DD{:04}".format(path, dir_name, snap_num, snap_num)
    else:
        print("Please provide the dir_name")
        return
    return path