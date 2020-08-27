import os
import struct
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("pakfile")
args = parser.parse_args()

f0 = open(args.pakfile,"rb")

headerMagic = struct.unpack('i', f0.read(4))[0]

if headerMagic != 0x1234567A:
    raise ValueError("Not a pak!")

print "Extracting pak..."

fileCount = struct.unpack('i', f0.read(4))[0]

f0.seek(0x18, os.SEEK_SET)

for i in range(0x00, fileCount):
    nameAddress = struct.unpack('i', f0.read(4))[0]
    fileAddress = struct.unpack('i', f0.read(4))[0]
    fileSize = struct.unpack('i', f0.read(4))[0]

    getBack = f0.tell()

    f0.seek(nameAddress)

    nameChar = ''
    nameString = ""

    while nameChar != '\0':
        nameChar = struct.unpack('c', f0.read(1))[0]
        nameString += nameChar
    nameString = nameString[:-1]

    if '/' in nameString:
        print nameString
        dirMarker = nameString.find('/')
        dirString = nameString[:+dirMarker]
        nameString = nameString[+dirMarker+1:]
        filePath = os.path.join(args.pakfile[:-4], dirString)
        if os.path.exists(filePath) == False:
            os.makedirs(filePath)
    else:
        print nameString
        filePath = args.pakfile[:-4]
        if os.path.exists(filePath) == False:
            os.mkdir(filePath)


    f0.seek(fileAddress, os.SEEK_SET)
    fileBytes = f0.read(fileSize)

    newFilePath = os.path.join(filePath, nameString)
    f1 = open(newFilePath, "wb")
    f1.write(fileBytes)
    f1.close()

    f0.seek(getBack, os.SEEK_SET)
    f0.seek(0x10, os.SEEK_CUR)

print "Done!"
f0.close()
