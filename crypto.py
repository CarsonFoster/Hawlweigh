## crypto.py ##
# simple hashing function

def folding(msg, foldNum, length):
    folds = []
    i = 0
    while i < len(msg):
        folds.append(msg[i:i+int(len(msg) / foldNum)])
        i += int(len(msg) / foldNum)
    if len(folds) > 4:
        folds = folds[:4]
    for fold in range(len(folds)):
        folds[fold] = ''.join([str(ord(a)) for a in folds[fold]])
    joined = ''.join(folds)
    joined = hex(int(joined))[2:].upper()
    while len(joined) < length * 2:
        joined = ''.join([joined, joined])
    if len(joined) > length:
        joined = joined[length:length * 2]
    return joined
