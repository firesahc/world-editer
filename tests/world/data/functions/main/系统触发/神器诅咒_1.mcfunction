scoreboard players tag @s[tag=!穿天镐使用者] add 工具诅咒 {Inventory:[{id:"minecraft:diamond_pickaxe",tag:{Tags:["穿天镐"]}}]}
scoreboard players tag @s[tag=!破地斧使用者] add 工具诅咒 {Inventory:[{id:"minecraft:diamond_axe",tag:{Tags:["破地斧"]}}]}
effect @s[tag=工具诅咒] minecraft:mining_fatigue 2 255 true
scoreboard players tag @s[tag=工具诅咒] remove 工具诅咒

scoreboard players tag @s add 五毒 {Inventory:[{tag:{Tags:["五毒药水"]}}]}
effect @s[tag=五毒] 19 3 50 true
effect @s[tag=五毒] 17 3 5 true
scoreboard players tag @s[tag=五毒] remove 五毒