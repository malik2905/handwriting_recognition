# Handwriting Recognition with Python and TensorFlow

## Overview

This repository contains a simple handwriting recognition application built using Python and TensorFlow. The application allows users to draw digits on a canvas and predicts the digit using a pre-trained neural network model.

## Files

- **handwriting.py**: Python script containing the implementation of the neural network class for handwriting recognition.

- **runner.py**: Main script for running the handwriting recognition application using Pygame.

- **requirements.txt**: File listing the dependencies required to run the application.

## Dependencies

Make sure you have the following dependencies installed:

- Python 3.x
- TensorFlow
- NumPy
- Pygame

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/handwriting-recognition.git
cd handwriting-recognition
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the `runner.py` script:

```bash
python runner.py
```

4. Use the application to draw digits on the canvas and utilize the various buttons for drawing, erasing, and predicting.

## Features

- **Drawing**: Use the "Draw" button to enable drawing on the canvas.
- **Erasing**: Use the "Rubber" button to enable erasing on the canvas.
- **Erase All**: Use the "Erase" button to clear the entire canvas.
- **Prediction**: Use the "Predict" button to predict the digit based on the drawn input.

## Model

The neural network model for handwriting recognition is stored in the file `handwriting.keras`. The `NeuralNetwork` class in `handwriting.py` loads this pre-trained model for making predictions.

## Contributing

Feel free to contribute to the project by opening issues or creating pull requests. Your feedback and suggestions are highly appreciated.

## License

This project is licensed under the MIT License

## Acknowledgments

- The neural network model used in this project is trained on the MNIST dataset.
- Special thanks to the Pygame community for providing a simple and interactive way to create graphical applications in Python.

Happy coding!
