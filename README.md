# clueMaster_AI

# Overview

The board game Clue Master Detective(hereafter referred as "Clue") is a murder mystery board game for 3-10 players(The British version is called "Cluedo"). The goal of the game is to determine WHO murdered the game's victim, WHERE the crime took place, and WHICH weapon was used. More history and stories about the board game can be find at [https://en.wikipedia.org/wiki/Cluedo](https://en.wikipedia.org/wiki/Cluedo), and there's even a movie based on this board game [https://en.wikipedia.org/wiki/Clue_(film)](https://en.wikipedia.org/wiki/Clue_(film)). 

This web app is designed for game players, and serve as a robot to help you make the best actions with Artificial Intelligence Computations.


## Game Details

The app is taking the latest American Version of Clue, with the following cards and map.

### Suspects(10 total)

- Miss Scarlet, Mr. Green, Mrs White, Mrs Peacock, Colonel Mustard, Professor Plum, Miss Peach, Sgt. Gray, Monsieur Brunette, Mme. Rose

### Weapons(8 total)

- Candlestick, Knife, Lead Pipe, Revolver, Rope, Wrench, Horseshoe, Poison

### Rooms(12 total)

- Carriage House, Conservatory, Kitchen, Trophy Room, Dining Room, Drawing Room, Gazebo, Courtyard, Fountain, Library, Billiard Room, Studio

![image](https://user-images.githubusercontent.com/71299664/139190175-7efec4d3-2a3a-4a51-9904-9a6f5ec7fe42.png)

## General Design

The app has two modes, advisor mode and simulator mode. 

- Advisor mode is designed for a game player who's playing the board game with other players, which free you from taking notes with pens and papers(this is what most players would usually do without the app), the AI will meanwhile display the analytics graphics and recommendations for your next move, and guide you towards winning.
- Simulator mode, as you can imagine, is a mode for robots playing against robots. The purpose is mainly for testing the performance of AI algorithms, and validating their performance by running large amount of experiments.

 
 
Here's how the frontend looks like(in dark mode),

![image](https://user-images.githubusercontent.com/71299664/139190438-20a70864-e243-49b7-a359-f004a44255d9.png)


On the back end  backend structure

- src
    - frontend
    - main
    - test
    - utils
- log

