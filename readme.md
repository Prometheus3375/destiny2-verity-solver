A tool to solve the 4th encounter, Verity, in Destiny 2 raid "Salvation's Edge".

# Features

- Can solve both solo rooms and dissection.
- Can make a solution which meets triumph requirements.

# Installation

1. Clone this project.
2. Install [Python 3.12.4](https://www.python.org/downloads/release/python-3124/)
   or higher version of Python 3.12.
3. Copy `config-template.toml` as `config.toml`.

# Usage

1. Open PowerShell in the root of the project you cloned.
2. There is always a way to make the same 2 people go to solo rooms.
   Follow [this guide](https://www.reddit.com/r/raidsecrets/comments/1duz6qp/manipulating_who_goes_top_and_bottom_in_the/)
   on how to accomplish that.
3. Wrote nicknames of two solo room players as aliases
   for `player1` and `player2` in the config file `config.toml`.
4. The 3rd solo player will be always random, so use "The third" as the alias for `player3`.
5. If you are doing the triumph, set `is_doing_triumph` to `true`.
6. Start the encounter.
7. Player 1 must tell symbols in solo rooms from left to right. Fill `inner_shapes`.
8. Player 1 must tell their shape and other shape on the wall. Complete `player1`.
9. Player 2 and player 3 must do the same. Complete `player2` and `player3` respectively.
10. Meanwhile, someone in the main room must tell shapes held by the statues from the left to right.
    Fill `held_shapes`.
11. In opened PowerShell window type `python -m solve both` and press Enter.
12. Follow the steps printed in the console window.
13. If you are doing the challenge, on the second phase set `key_set` to `double`.

Run `python -m solve --help` to see more options.

- For example, instead of `both` you can use `solo-rooms` to get steps only for solo rooms.
- Option `-i` pauses output after every step. Press Enter to proceed to the next step.
