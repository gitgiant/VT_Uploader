# Opens a file given by targetFile, steps through block by block
# and generates a sha256.  Displays the resulting sha256,
# then opens sha256_list to add to list.
import hashlib

def calculate_sha256(targetFile):
    sha256 = hashlib.sha256()

    with open(targetFile, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha256.update(block)

    print("Target File Name: " + f.name)
    print("sha256: " + sha256.hexdigest())

    #search the sha256 list for this file's sha256
    found = False
    with open('sha256_list', "r") as sha256Read:
        for line in sha256Read:
            if sha256.hexdigest() in line:
                #print("sha256 found, this file has already been scanned and uploaded.")
                found = True
                return found

    #If not found, add to sha256_list.txt
    if found == False:
        with open('sha256_list', "a") as sha256write:
            sha256write.write(sha256.hexdigest() + "," + f.name + '\n')
            return found

