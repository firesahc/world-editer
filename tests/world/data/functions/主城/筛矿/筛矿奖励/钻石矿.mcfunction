scoreboard players set @s 筛矿抽奖 100
function 随机数:随机数_百
scoreboard players operation @s 筛矿抽奖 += 随机数 随机数

give @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] minecraft:diamond_ore 16
execute @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼究极暴击！","color":"dark_red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【16个钻石矿】","color":"aqua","bold":true}]

give @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] minecraft:diamond_ore 4
tellraw @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼出","color":"aqua","bold":true},{"text":"【4个钻石矿】","color":"aqua","bold":true}]

give @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] minecraft:diamond_ore 8
execute @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼大爆击！","color":"red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【8个钻石矿】","color":"aqua","bold":true}]
