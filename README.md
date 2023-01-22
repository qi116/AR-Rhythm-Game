# Boilermake

## What is it?
An osu! like rhythm game that uses Mediapipe to play with your webcam.
## How to play?
Make sure you are in a relatively clear and well lit environment  
Move your index finger to the rectangles on the screen in the order as indicated by the numbers  
Press `spacebar` when the rectangle is filled and turns red
## How to use?
To start, install requirements  
Enter the main directory in terminal  
`pip install -r requirements.txt`  

Run main.py to play with `python main.py`  
Change the song by changing the value of `name` in main.py

## Add more songs
Download an osu! beatmap (should be a .osz file) and extract it (can change the extension to .zip)  
Go to the .osu file and copy the contents under `[HitObjects]` into a txt file and put it in the `songs` folder  
Copy over the `audio.mp3` file as well and rename it to be the same as your txt file  
Change the `name` variable to your new song and play!

