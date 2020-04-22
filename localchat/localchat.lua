json = require "json"

Listen("onChat",function(name,text)

    if(text:sub(1,1) == "!")
    then
    	--global chat--
    	chatStr1 = "§6Ⓖ§r " .. name .. ": " .. text:sub(2)
    	chatStr2 = json.encode({rawtext = {{text = chatStr1}} })
		runCmd("tellraw @a " .. chatStr2)
    else
		--local chat--
		chatStr1 = "§3Ⓛ§r " .. name .. ": " .. text
    	chatStr2 = json.encode({rawtext = {{text = chatStr1}} })
		runCmd("execute " .. name .. " ~ ~ ~ tellraw @a[r=100] " .. chatStr2)
		--send to admins--
		spyStr1 = "§7Ⓛ <" .. name .. "> " .. text
		spyStr2 = json.encode({rawtext = {{text = spyStr1}} })
		runCmd("execute " .. name .. " ~ ~ ~ tellraw @a[rm=101,tag=admin] " .. spyStr2)
	end
	
	return -1
end)