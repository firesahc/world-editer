scoreboard players set @s 筛矿抽奖 100
function 随机数:随机数_百
scoreboard players operation @s 筛矿抽奖 += 随机数 随机数

give @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] minecraft:coal_ore 48
execute @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼究极暴击！","color":"dark_red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【48个煤矿】","color":"gray","bold":true}]

give @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] minecraft:coal_ore 12
tellraw @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼出","color":"aqua","bold":true},{"text":"【12个煤矿】","color":"gray","bold":true}]

give @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] minecraft:coal_ore 24 
execute @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼大爆击！","color":"red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【24个煤矿】","color":"gray","bold":true}]
