scoreboard players tag @s[score_金钱_min=10,tag=筛矿失败] remove 筛矿失败 {Inventory:[{id:"minecraft:cobblestone",Damage:0s,Count:64b}]}

tellraw @s[score_金钱=9,tag=筛矿失败] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"金币余额不足。","color":"red"}]
tellraw @s[score_金钱_min=10,tag=筛矿失败] [{"text":"【熔炼机】","color":"yellow","bold":true},{"text":"圆石不足。","color":"red"}]

tp @s[x=-1995,y=60,z=-1966,r=1,tag=筛矿失败] ~2 ~ ~
tp @s[x=-1994,y=60,z=-1972,r=1,tag=筛矿失败] ~2 ~ ~
tp @s[x=-1989,y=60,z=-1975,r=1,tag=筛矿失败] ~-2 ~ ~
tp @s[x=-1986,y=60,z=-1969,r=1,tag=筛矿失败] ~-2 ~ ~
tp @s[x=-1986,y=61,z=-1963,r=1,tag=筛矿失败] ~-2 ~ ~