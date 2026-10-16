scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空套头部"]}}]}
scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空套铠甲"]}}]}
scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空套腿部"]}}]}
scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空套脚部"]}}]}
scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空剑"]}}]}
scoreboard players add @s[score_主线_min=33] 神器 1 {Inventory:[{tag:{Tags:["天空弓"]}}]}
scoreboard players add @s 神器 1 {Inventory:[{tag:{Tags:["御神盾"]}}]}

scoreboard players tag @s add 神盾诅咒 {Inventory:[{tag:{Tags:["御神盾"]}}]}

effect @s[tag=神盾诅咒,score_神器_min=1,score_神器=6] minecraft:mining_fatigue 2 255 true

effect @s[score_主线_min=33,score_神器_min=3] minecraft:strength 2 1 true
effect @s[score_主线_min=33,score_神器_min=5] minecraft:resistance 2 1 true

scoreboard players set @s[score_神器_min=1] 神器 0
scoreboard players tag @s[tag=神盾诅咒] remove 神盾诅咒
