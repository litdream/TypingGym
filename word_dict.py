def get_all_levels():
    rtn = list()
    with open("word-list.dat") as fh:
        tmp = None
        for l in fh:
            if l.startswith("Level"):
                if tmp:
                    rtn.append(tmp)
                tmp = list()
            else:
                tmp.append(l.strip())
    return rtn

