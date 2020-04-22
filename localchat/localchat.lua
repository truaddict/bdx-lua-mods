json = require "json"


DISTANCE = 100		-- local chat radius in blocks
ADMINTAG = "admin"  -- use in-game command /tag <player> add <ADMINTAG>
OP_PREFIX = "[§cA§r]"


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


Listen("onChat",function(name,text)

    if(text:sub(1,1) == "!")
    then
    	--global chat--
		runCmd("tellraw @a " .. rawtext("§6Ⓖ§r " .. opPrefix(name) .. ": " .. text:sub(2)))
    else
		--local chat--
		runCmd(string.format("execute %s ~ ~ ~ tellraw @a[r=%i] %s", name, DISTANCE, rawtext("§3Ⓛ§r " .. opPrefix(name) .. ": " .. text)))
		--send to admins--
		runCmd(string.format("execute %s ~ ~ ~ tellraw @a[rm=%i,tag=%s] %s", name, DISTANCE + 1, ADMINTAG, rawtext("§7Ⓛ <" .. opPrefix(name) .. "> " .. text)))
	end
	
	return -1
end)