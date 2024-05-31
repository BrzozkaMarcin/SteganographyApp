# Steganography App

Steganography App is a desktop application that enables users to hide files in images and extract hidden files from images using steganography. The application is available in two versions: with a graphical user interface (GUI) and a command-line interface (CLI).

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [How to Use](#how-to-use)
5. [Author](#author)
6. [License](#license)

## Introduction

Steganography is the technique of hiding information in a way that is invisible to third parties. Steganography App utilizes this technique, allowing users to hide files in images. This process enables the storage of confidential data within seemingly innocent image files, which can be useful in various scenarios, from maintaining privacy to concealing information from unauthorized individuals.

## Installation

Steganography App requires Python and the PyQt5 library. To install the necessary dependencies, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/BrzozkaMarcin/SteganographyApp
```

2. Navigate to the project directory:
```bash
cd SteganographyApp
```

3. Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

## Usage
### GUI Application

To run the application with a graphical user interface, follow these steps:

1. Navigate to the project directory:
```bash
cd SteganographyApp
```

2. Run the `StegoGui.py` file:
```bash
python StegoGui.py
```

### Command-Line Application
Steganography App also has a command-line version that allows for operations without a graphical interface. To run the command-line application, follow these steps:

1. Navigate to the project directory:
```bash
cd SteganographyApp
```

2. Run the `StegoScript.py` file with the appropriate arguments. For more information on usage, execute:
```bash
python StegoScript.py --help
```

## How to Use
Upon launching the application with a graphical user interface, users can utilize various features such as hiding files in images, extracting hidden files from images, and accessing help and information about the application. The interface is intuitive and easy to use.

The command-line version allows for the same operations but without the need for a graphical interface. Users can provide appropriate command-line arguments to perform specific tasks.

## Author
Steganography App was created, maintained, and developed by Marcin Brzózka.

## License
This project is licensed under the MIT. For more information, see the LICENSE file.
