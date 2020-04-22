# Local chat plugin

## Requirements:

json.lua lib (https://github.com/rxi/json.lua)



## Installation

1. Put json.lua in bdx/lualib directory.
2. Put localchat.lua in bdx/lua directory.
3. Check localchat.lua source code: edit DISTANCE and OP_TAG vars if needed.
4. Execute ```/lreload``` command (as op) or restart the server.
5. Don't forget to add tag (=OP_TAG) to operators for them to be able to get distant local chat messages (doesn't work between different dimensions atm).
