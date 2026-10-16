function 随机数:随机数_百
scoreboard players operation @s 剑气 = 随机数 随机数
scoreboard players operation @s 剑气 %= 9星剑剑气 范围

effect @s[score_剑气_min=3,score_剑气=3] minecraft:absorption 10 1 true
tellraw @s[score_剑气_min=3,score_剑气=3] [{"text":"【剑气】","color":"aqua","bold":true},{"text":"护盾","color":"yellow","bold":true}]

scoreboard players set @s 挥剑 0