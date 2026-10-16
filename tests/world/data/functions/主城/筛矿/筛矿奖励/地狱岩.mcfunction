scoreboard players set @s 筛矿抽奖 100
function 随机数:随机数_百
scoreboard players operation @s 筛矿抽奖 += 随机数 随机数

give @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] minecraft:netherrack 64 
execute @s[score_筛矿抽奖_min=101,score_筛矿抽奖=106] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼究极暴击！","color":"dark_red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【64个地狱岩】","color":"gray","bold":true}]

give @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] minecraft:netherrack 16 
tellraw @s[score_筛矿抽奖_min=107,score_筛矿抽奖=191] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼出","color":"aqua","bold":true},{"text":"【16个地狱岩】","color":"gray","bold":true}]

give @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] minecraft:netherrack 32 
execute @s[score_筛矿抽奖_min=192,score_筛矿抽奖=200] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"熔炼大爆击！","color":"red","bold":true},{"selector":"@s"},{"text":" 熔炼出","color":"aqua","bold":true},{"text":"【32个地狱岩】","color":"gray","bold":true}]
