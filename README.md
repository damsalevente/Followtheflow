# install 

    change to gym-control dir 
    pip install -e .

## run 

    change to gymtest dir
    python main.py


## Description 

the map:

[0 0 0 1 100 1 0 0 0 0]

The goal is to find one tile where the agent gets 100 chocolate
He can speed up to get there faster 

since he either speeds up or down, he cant stay one one tile 

He can get more rewards if he stays in that area 


Observation is a pair of (position, speed), where the position can be 0 -> length of rewardtable, speed can range from -10 to 10

There are two actions he can make  speed or slow by 1 unit
