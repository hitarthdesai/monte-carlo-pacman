This repository contains code for an updated version of the Pacbot competition.

There are three sub-folders, one for each part of the competition's infrastructure:

- `bot_client`: sample Python code for creating a Pacbot high-level client and algorithm. We also have `elec` code to move the robot in this directory. 
- `server`: a Go (programming language) implementation of the Pacbot server and game engine
- `web_client`: a Svelte-based (JavaScript web frontend) client to serve as a visualizer and game console

Files inside `server` and `web_client` have been provided by the organizers of the Pacbot competition to allow running a game server and visual simulator locally.

Files inside `bot_client` have been added/created by the members of 6ix-pac. This version of the algorithm uses the MCTS approach to solve this Pacman problem, where the goal is to get the highest possible scores with the three given lives.

This algorithm isn't complete yet, however, the work done so far builds a framework for how the whole algo is going to work to allow members tocontribute to it.
