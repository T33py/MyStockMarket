## Backend project
I'm implementing most of the logic and variables as a library so I can better sepperate all the names and functions of the market from the actual logistics of running the thing.
I want this to be the part of the game that I don't have to worry about fiddeling with, it should just implement functions and variables that can be used to populate the stockmarket from other applications.
This will guarantee that I can eventually make a server/client setup that share this library as computational and deffinition basis, allowing me to not duplicate any of this code.