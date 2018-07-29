# Scoring for Tin Can Rally

_Tin Can Rally_ is scored dynamically during the game, so each linesman must
record all the relevant actions of the robot they are scoring.

This must be done using the following notation:

- `C` - the robot passed a track boundary in the anticlockwise direction
- `B` - the robot passed a track boundary in the clockwise direction

- `U` - the robot picked up a token
- `D` - the robot dropped a token

The scoring script in this repo can be used to convert a score sheet which conforms to the above notation into a scores for each of the competing teams.
