# Chess AI - Deep Learning Based Move Prediction and Evaluation

This project implements a Chess AI using a convolutional neural network (CNN) model to predict the best move and evaluate the board position. It includes an API built with FastAPI for real-time chess move recommendations. The model is trained on historical chess games using a dual-headed neural network: one head predicts the best move (policy head), and the other evaluates the board (value head).

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Policy Head](#policy-head)
  - [Value Head](#value-head)
- [Setup and Installation](#setup-and-installation)
  - [Requirements](#requirements)
  - [Running the Application](#running-the-application)
  - [Training the Model](#training-the-model)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project implements a modern Chess AI that uses deep learning to predict the best move and evaluate board positions. The model is trained on a large dataset of chess games and serves predictions via an API. The architecture is inspired by AlphaZero, featuring a policy network to suggest moves and a value network to evaluate positions.

## Technologies Used
- **FastAPI**: A modern web framework for building APIs in Python.
- **TensorFlow/Keras**: A deep learning framework used to build and train the neural network.
- **Python-Chess**: A Python library for handling chess logic, FEN parsing, and move legality checks.
- **NumPy**: For numerical operations and matrix manipulations.
- **Jupyter Notebooks**: For training and experimenting with the model.
  
## Project Structure


## How It Works

The project consists of two main components:
1. **Model Training** (in `chess_aii_new.ipynb`): 
   - Trains a convolutional neural network on a chess dataset.
   - The model has two heads: one for predicting the best move (policy head) and another for evaluating the board (value head).
   
2. **API Server** (in `app2.py`): 
   - Provides an endpoint to submit a chess position in FEN format and get the best move suggestion along with board evaluation.

### Policy Head
- The policy head predicts the next best move by outputting a probability distribution over all possible legal moves.
- It uses **categorical cross-entropy** as the loss function during training.

### Value Head
- The value head evaluates the current board state, outputting a score between -1 and 1, where -1 indicates a loss, 0 indicates a draw, and 1 indicates a win.
- It uses **mean squared error (MSE)** as the loss function.

## Setup and Installation

### Requirements
- Python 3.8+
- FastAPI
- TensorFlow/Keras
- Python-Chess
- NumPy

You can install the required packages using:
```bash
pip install fastapi uvicorn tensorflow python-chess numpy
```


Running the Application
Clone the repository:
bash
```git clone https://github.com/yourusername/chess-ai.git```

Navigate into the project directory:
bash
```
cd chess-ai
Start the FastAPI server:
```
bash
```uvicorn app2:app --reload```

Training the Model
Open the Jupyter notebook chess_aii_new.ipynb.
Ensure you have the dataset and necessary dependencies installed.
Run through the notebook cells to train the model.
API Endpoints
POST /predict:
Input: FEN string representing the current board position.
Output: Best move and board evaluation.
Example request body:
json

{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}


License
This project is licensed under the MIT License. See the LICENSE file for details.


---
