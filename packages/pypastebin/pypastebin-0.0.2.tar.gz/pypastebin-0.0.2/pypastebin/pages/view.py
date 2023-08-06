def view_paste(r):
    data = r.database.get(r.path[1:])
    if data != None:
        return data
    return ""
