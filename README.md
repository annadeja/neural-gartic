# Neural Gartic
Neural Gartic is an application that allows you to play a game similar to [GarticPhone](https://garticphone.com/pl)!

<p align="center">
  <img src="https://user-images.githubusercontent.com/32665400/153521957-2cf4f837-f486-4e99-94d7-9a76f9c7f9d4.png" />
</p>

Rules are simple - you draw and neural network guesses!  
# Rules continued
Game's rules:
- draw a picture that corresponds to the text on screen - you can do it in your web browser or in desktop application (you can use our app - DesktopDrawing)
- upload the image if you used the desktop appliaction to draw the picture
- repeat previous steps till the end of the game
- in the summary you can see what neural net guessed for particular drawings!
# Requirements
General:
- Python (3.8 or later)

NeuralGartic:  
- Tensorflow (2.8.0 was used)
- Numpy (1.22.2 was used)
- Flask (2.0.3 was used)

NeuralNet
- Tensorflow (2.8.0 was used)

DrawingDesktop:
- PyQt5 (5.15.6 was used)

# Recommended packages
While training a neural network on a CPU is possible, it is is <i>highly</i> recommended to make use of CUDA to drastically speed up the process. In this project CUDA v11.5 and cuDNN v8.2.4 were used.

# Installation
After downloading or cloning this repo, install all required packages (see <b>Requirements</b>). In folder <i>NeuralGartic</i> you will find the main part of this application. In <i>NeuralNet</i> can be found the code and data that was used for training and validation. <i>DesktopDrawing</i> contains application that can be used to create the drawings (but it's not required for the game).

# Authors
[Mateusz Chłopek](https://github.com/OftenDeadKanji)  
[Anna Deja](https://github.com/annadeja)  
[Dawid Duży](https://github.com/davidfigaromacintosh)  
