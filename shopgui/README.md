# Shop lua plugin for BDX

Description: use example json template file and a python generator to create all needed files (GUI and lua).

## Software requirements:
1. Python 3.6 or later
2. BDX **0420** (later versions haven't been tested and are known to have some lua bugs at the time of writing)

## How to install and use:
1. Copy included files (py and json) to BDS/BDX root dir (where bedrock_server.exe is located).
2. Review json file: edit menus, add or delete items, change prices etc.
3. Open cmd or powershell console, cd to bdx dir and execute shop generator script with `python shopgen.py`.
4. If there are no errors you can restart your server (or simply do `/lreload`) and use newly generated shop by runnung `/gui shop` command.
