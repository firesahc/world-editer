scoreboard players add @s 杀僵尸 0
scoreboard players add @s 杀小白 0
scoreboard players add @s 杀蜘蛛 0
scoreboard players add @s id 0
scoreboard players set @s 红石权限 0
scoreboard players set @s 冒险模式 1
scoreboard players set @s 权限 0

give @s iron_sword 1 0 {ench:[{id:17,lvl:2},{id:34,lvl:2}]}
give @s bread 32
give @s leather_helmet 1 0 {display:{Name:"萌新套装",color:65280},ench:[{id:0,lvl:3},{id:34,lvl:3}]}
give @s leather_chestplate 1 0 {display:{Name:"萌新套装",color:65280},ench:[{id:0,lvl:3},{id:34,lvl:3}]}
give @s leather_leggings 1 0 {display:{Name:"萌新套装",color:65280},ench:[{id:0,lvl:3},{id:34,lvl:3}]}
give @s leather_boots 1 0 {display:{Name:"萌新套装",color:65280},ench:[{id:0,lvl:3},{id:34,lvl:3}]}

tp @s -1987 74 -2688 180 0
tellraw @s {"text":"欢迎来到蚂蚁空岛生存 \n完成新手挑战 开始空岛生存~~","color":"aqua","bold":"true"}
scoreboard teams join 萌新 @s

scoreboard players set @s 新人 1
