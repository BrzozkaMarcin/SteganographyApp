from cryptography.fernet import Fernet
import os, hashlib, base64
from PIL import Image
from sys import exit


magicBytes = {"encrypted": 0x1410c0de, "unencrypted": 0xfeedc0de}


def encryptData(data: bytes, key: str) -> bytes:
    """
    Function to encrypt data using a symmetric key encryption algorithm (Fernet).

    Parameters:
    data (bytes): The data to be encrypted.
    key (str): The encryption key as a string.

    Returns:
    bytes: The encrypted data.
    """
    key = base64.urlsafe_b64encode(hashlib.md5(key.encode()).hexdigest().encode())

    f = Fernet(key)
    encData = f.encrypt(data)
    return encData


def decryptData(data: bytes, key: str) -> bytes:
    """
    Function to decrypt data using a symmetric key encryption algorithm (Fernet).

    Parameters:
    data (bytes): The data to be decrypted.
    key (str): The encryption key as a string.

    Returns:
    bytes: The decrypted data.

    Raises:
    SystemExit: If the password is invalid or the data cannot be decrypted.
    """
    try:
        key = base64.urlsafe_b64encode(hashlib.md5(key.encode()).hexdigest().encode())

        f = Fernet(key)
        decData = f.decrypt(data)
        return decData
    except Exception:
        print("[!] Invalid password or data.")
        exit()


def changeLast2Bits(oldByte: int, newBits: int) -> int:
    """
    Function to replace the 2 least significant bits (LSBs) of the given oldByte with newBits.

    Parameters:
    oldByte (int): Original byte to be modified.
    newBits (int): New values for the 2 LSBs.

    Returns:
    int: Byte with the two LSBs replaced by the newBits.
    """
    return ((oldByte >> 2) << 2) | newBits


def filesizeToBytes(data: bytes, lenght: int) -> bytes:
    """
    Function to return the size of data in a sequence of 8 bytes.

    Parameters:
    data (bytes): Data to determine its size, represented as a sequence of bytes.
    length (int): Length of the byte sequence to represent the size of the data.

    Returns:
    bytes: Size of the input data represented as a sequence of 8 bytes in big-endian byte order.
    """
    return (len(data)).to_bytes(lenght, byteorder='big')


def serializeData(data: bytes, padding: int = 1) -> list:
    """
    Function to serialize data into 2-bit groups and return a list of them.

    Parameters:
    data (bytes): Input data to be serialized, represented as a sequence of bytes.
    padding (int): Optional parameter specifying the desired padding. 
                   Default value is 1, meaning no padding is added.

    Returns:
    list: List of 2-bit groups representing the serialized data. 
          The length of the list is adjusted to be divisible by the padding value.
    """
    serializedData = list()
    
    for byte in data:
        serializedData.append((byte >> 6) & 0b11)
        serializedData.append((byte >> 4) & 0b11)
        serializedData.append((byte >> 2) & 0b11)
        serializedData.append((byte >> 0) & 0b11)

    while len(serializedData) % padding != 0:
        serializedData.append(0)

    return serializedData


def deserializeData(data: list) -> bytes:
    """
    Function to deserialize a list of 2-bit groups into the original data.

    Parameters:
    data (list): List of 2-bit groups to be deserialized.

    Returns:
    bytes: Original data represented as a sequence of bytes.
    """
    deserializeData = list()
    
    for i in range(0, len(data) - 4 + 1, 4):
        byte = (data[i + 0] << 6) + \
               (data[i + 1] << 4) + \
               (data[i + 2] << 2) + \
               (data[i + 3] << 0)
        deserializeData.append(byte)

    return bytes(deserializeData)


def hideDataToImage(inputImagePath: str, fileToHidePath: str, outputImagePath: str, password: str) -> None:
    """
    Function to hide data within an image using LSB steganography.

    Parameters:
    inputImagePath (str): Path to the input image file.
    fileToHidePath (str): Path to the file to be hidden within the image.
    outputImagePath (str): Path to save the output image with hidden data.
    password (str): Password used for encryption.

    Returns:
    None
    """
    openedFile = open(fileToHidePath, "rb")
    fileToHideName = os.path.basename(fileToHidePath)
    encodeName = fileToHideName.encode()
    data = openedFile.read()
    print("[*] {} file size: {} bytes.".format(fileToHidePath, len(data)))
    
    image = Image.open(inputImagePath).convert('RGB')
    pixels = image.load()
    
    if password:
        data = encryptData(data, password)
        encodeName = encryptData(encodeName, password)
        print("[*] Encrypted data size: {} bytes".format(len(data)))
        data = (magicBytes["encrypted"]).to_bytes(4, byteorder='big') + \
                filesizeToBytes(encodeName, 3) + filesizeToBytes(data, 8) + encodeName + data
    else:
        data = (magicBytes["unencrypted"]).to_bytes(4, byteorder='big') + \
                filesizeToBytes(encodeName, 3) + filesizeToBytes(data, 8) + encodeName + data

    max_hidden_size = (image.size[0] * image.size[1] * 3 * 2) // 8
    if len(data) > max_hidden_size:
        print("[*] Maximum hidden file size for this image: {} bytes.".format(max_hidden_size))
        print("[~] To hide this file, choose an image with a higher resolution.")
        exit()

    print("[*] Hiding file in image.")
    data = serializeData(data, padding=3)
    data.reverse()
    
    imageX, imageY = 0, 0
    while data:
        pixel_val = pixels[imageX, imageY]
        pixel_val = (changeLast2Bits(pixel_val[0], data.pop()),
                     changeLast2Bits(pixel_val[1], data.pop()),
                     changeLast2Bits(pixel_val[2], data.pop()))
        pixels[imageX, imageY] = pixel_val

        if imageX == image.size[0] - 1:
            imageX = 0
            imageY += 1
        else:
            imageX += 1
    
    print(f"[+] Saving image to {outputImagePath}.")
    image.save(outputImagePath)


def extractDataFromImage(inputImagePath: str, password: str) -> None:
    """
    Function to extract hidden data from an image using LSB steganography.

    Parameters:
    inputImagePath (str): Path to the input image file.
    password (str): Password used for decryption if the hidden data is encrypted.

    Returns:
    None
    """
    image = Image.open(inputImagePath).convert('RGB')
    pixels = image.load()
    data = list()
    
    for imageY in range(image.size[1]):
        for imageX in range(image.size[0]):
            if len(data) >= (16 + 32 + 12):
                break
            pixel = pixels[imageX, imageY]
            data.append(pixel[0] & 0b11)
            data.append(pixel[1] & 0b11)
            data.append(pixel[2] & 0b11)

    encrypted = False
    
    if deserializeData(data)[:4] == bytes.fromhex(hex(magicBytes["unencrypted"])[2:]):
        print("[+] Hidden file found in image.")
        pass
    elif deserializeData(data)[:4] == bytes.fromhex(hex(magicBytes["encrypted"])[2:]):
        print("[*] Hidden file is encrypted.")
        encrypted = True
    else:
        print("[!] Image don't have any hidden file.")
        exit()

    print("[*] Extracting hidden file from image.")
    hiddenPathSize = int.from_bytes(deserializeData(data)[4:7], byteorder='big') * 4
    hiddenDataSize = int.from_bytes(deserializeData(data)[7:15], byteorder='big') * 4
    data = list()
    
    for imageY in range(image.size[1]):
        for imageX in range(image.size[0]):
            if len(data) >= hiddenPathSize + hiddenDataSize + 60:
                break
            pixel = pixels[imageX, imageY]
            data.append(pixel[0] & 0b11)
            data.append(pixel[1] & 0b11)
            data.append(pixel[2] & 0b11)

    encodeName = deserializeData(data[60 : (60 + hiddenPathSize)])
    data = deserializeData(data[(60 + hiddenPathSize) :])
    if encrypted:
        encodeName = decryptData(encodeName, password)
        data = decryptData(data, password)
    outputFilePath = os.path.join(os.getcwd(), encodeName.decode())

    print("[+] Saving hidden file to {}.".format(outputFilePath))
    print("[*] Size of hidden file recovered: {} bytes.".format(len(data)))

    f = open(outputFilePath, 'wb')
    f.write(data)
    f.close()
