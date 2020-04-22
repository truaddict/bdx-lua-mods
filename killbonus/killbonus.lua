-- BedrockX lua mod for killbonus
-- https://github.com/truaddict/bdx-lua-mods

local DEBUG = false --debug mode will print killed mob id to player (op only)

local BONUS_TBL = {
	[2849] = 3,
	[1116974] = 2,
	[2854] = 1,
	[2861] = 5,
	[2853] = 1,
	[2858] = 1,
	[2870] = 10,
	[2873] = 3,
	[2930] = 3,
	[2920] = 5,
	[2875] = 10,
	[2857] = 2,
	[68388] = 1,
	[2866] = 100,
	[2869] = 800,
	[68404] = 500,
	[1116976] = 4,
	[265015] = 13,
	[2921] = 5
}

Listen("onPlayerKillMob", function(name,mob_id)

	-- print killed mob id to player (op only) if debug mode is turned on
	if(isOP(name) and DEBUG) then
		sendText(name, string.format("§7You killed mob with id = %i", mob_id))
	end
	-- use bonus table to get the reward sum
	if(BONUS_TBL[mob_id] ~= nil) then
		addMoney(name, BONUS_TBL[mob_id])
		sendText(name, string.format("§6§lНаграда за убийство моба: %i §r!", BONUS_TBL[mob_id]), 3)
	end

end)