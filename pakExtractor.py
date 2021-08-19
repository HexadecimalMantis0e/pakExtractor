import os
import struct
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pakfile")
    args = parser.parse_args()

    f0 = open(args.pakfile, "rb")
    headerMagic = struct.unpack('I', f0.read(4))[0]

    if headerMagic != 0x1234567A:
        raise ValueError("Not a pak!")

    print("Extracting pak...")
    fileCount = struct.unpack('I', f0.read(4))[0]
    f0.seek(0x18, os.SEEK_SET)

    for i in range(0, fileCount):
        nameAddress = struct.unpack('I', f0.read(4))[0]
        fileAddress = struct.unpack('I', f0.read(4))[0]
        fileSize = struct.unpack('I', f0.read(4))[0]
        getBack = f0.tell()
        f0.seek(nameAddress)

        nameChar = ''
        nameString = ""
        nameChar = struct.unpack('c', f0.read(1))[0].decode()

        while nameChar != '\0':
            nameString += nameChar
            nameChar = struct.unpack('c', f0.read(1))[0].decode()

        print(nameString)
        filePath = os.path.join(args.pakfile[:-4], nameString)

        if os.path.exists(os.path.dirname(filePath)) == False:
            os.makedirs(os.path.dirname(filePath))

        f0.seek(fileAddress, os.SEEK_SET)
        fileBytes = f0.read(fileSize)

        f1 = open(filePath, "wb")
        f1.write(fileBytes)
        f1.close()

        f0.seek(getBack, os.SEEK_SET)
        f0.seek(0x10, os.SEEK_CUR)

    print("Done!")
    f0.close()

if __name__ == "__main__":
    main()
