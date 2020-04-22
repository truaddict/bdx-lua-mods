-- BedrockX lua mod for localchat
-- https://github.com/truaddict/bdx-lua-mods

local json = require "json"

DISTANCE = 100		-- local chat radius in blocks
local OP_TAG = "admin"  -- use in-game command /tag <player> add <OP_TAG>
local OP_PREFIX = "[§cA§r]"


function rawtext(content)
	return json.encode({rawtext = {{text = content}} })
end

function opPrefix(playername)
	if(isOP(playername)) then
		return OP_PREFIX .. playername
	else
		return playername
	end
end


Listen("onChat", function(name,text)

    if(text:sub(1,1) == "!")
    then
    	--global chat
		runCmd("tellraw @a " .. rawtext("§6Ⓖ§r " .. opPrefix(name) .. ": " .. text:sub(2)))
    else
		--local chat
		runCmd(string.format("execute %s ~ ~ ~ tellraw @a[r=%i] %s", name, DISTANCE, rawtext("§3Ⓛ§r " .. opPrefix(name) .. ": " .. text)))
		--send to ops (doesn't work if op is in different dimension)
		runCmd(string.format("execute %s ~ ~ ~ tellraw @a[rm=%i,tag=%s] %s", name, DISTANCE + 1, OP_TAG, rawtext("§7Ⓛ <" .. opPrefix(name) .. "> " .. text)))
	end
	
	return -1
end)
