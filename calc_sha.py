# Opens a file given by targetFile, steps through block by block
# and generates a sha256.  Displays the resulting sha256,
# then opens sha256_list to add to list.
import hashlib

def calculate_sha256(targetFile):
    sha256 = hashlib.sha256()

    # Build sha256 hex digest block by block
    try:
        with open(targetFile, 'rb') as f:
            for block in iter(lambda: f.read(65536), b''):
                sha256.update(block)
    except Exception as e:
        print(e)


    #search the sha256 list for this file's sha256
    found = False
    with open('sha256_list', "r") as sha256Read:
        for line in sha256Read:
            if sha256.hexdigest() in line:
                # TODO If file hash the same but name is different, display name of previous upload?
                print("SHA found under previous upload with path: " + line.strip(sha256.hexdigest()).strip(','))
                found = True
                return found

    #If not found, add to sha256_list.txt
    if found == False:
        with open('sha256_list', "a") as sha256write:
            sha256write.write(sha256.hexdigest() + "," + f.name + '\n')
            return found

