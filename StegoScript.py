from getopt import getopt, GetoptError
from sys import exit, argv, getsizeof
from StegoAlgorithm import *
import warnings


warnings.filterwarnings("ignore", category=UserWarning, 
                        message="Palette images with Transparency expressed in bytes should be converted to RGBA images")


def usage():
    """
    Display usage instructions for the script.
    
    Parameters:
        None

    Returns:
        None
    """
    print("Usage: python stego.py -i <input_image> [-h <hidden_file>] [-o <output_image>] [-p <password>] [-e] [--help]")
    print("Options:")
    print("  -i <input_image>    Path to the input image file.")
    print("  -h <hidden_file>    Path to the file to hide.")
    print("  -o <output_image>   Path to the output image file.")
    print("  -p <password>       Password used for encryption/decryption.")
    print("  -e                  Extraction mode. Extract hidden file from the image.")
    print("  --help              Display usage instructions for the script.")
    exit()


def main():
    """
    Function to handle command-line arguments and perform hiding or extraction of files in images.

    Parameters:
        None

    Returns:
        None
    """
    inputImagePath = str()
    hiddenFilePath = str()
    outputImagePath = str()
    password = str()
    extractionMode = False
    try:
        options, _ = getopt(argv[1:], "i:h:o:p:e", ["help"])
    except GetoptError as err:
        print(str(err))
        usage()
    
    for opt, arg in options:
        if opt == "-i":
            inputImagePath = arg
        elif opt == "-h":
            hiddenFilePath = arg
        elif opt == "-o":
            outputImagePath = arg
        elif opt == "-p":
            password = arg
        elif opt == "-e":
            extractionMode = True
        elif opt == "--help":
            usage()
            
    if extractionMode:
        if not inputImagePath:
            usage()
        else: 
            extractDataFromImage(inputImagePath, password)
    else:
        if not (inputImagePath and hiddenFilePath):
            usage()
        else:
            if not outputImagePath:
                outputImagePath = "".join(inputImagePath.split(".")[:-1]) + "_steg.png"
            if not outputImagePath.endswith(".png"):
                print("[!] Output image should be a PNG.")
                exit()
            hideDataToImage(inputImagePath, hiddenFilePath, outputImagePath, password)

if __name__ == '__main__':
    main()
