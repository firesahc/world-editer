function 随机数:随机数_百
scoreboard players operation @s 剑气 = 随机数 随机数
scoreboard players operation @s 剑气 %= 天剑剑气 范围

effect @s[score_剑气_min=3,score_剑气=3] minecraft:instant_health 1 6 true
tellraw @s[score_剑气_min=3,score_剑气=3] [{"text":"【剑气】","color":"aqua","bold":true},{"text":"再生","color":"green","bold":true}]

effect @s[score_剑气_min=4,score_剑气=4] minecraft:absorption 10 2 true
tellraw @s[score_剑气_min=4,score_剑气=4] [{"text":"【剑气】","color":"aqua","bold":true},{"text":"护盾","color":"yellow","bold":true}]

scoreboard players set @s 挥剑 0