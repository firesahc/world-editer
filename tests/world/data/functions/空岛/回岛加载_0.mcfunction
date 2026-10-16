effect @s 25 8 255
title @s title {"text":"正在创建空岛","color":"green"}

setblock ~-3 28 ~-3 minecraft:structure_block 1 0 {mode:LOAD,name:"scjd",ignoreEntities: 0}
setblock ~-3 28 ~-2 minecraft:redstone_block
summon armor_stand ~ 30 ~ {CustomName:"保护",Invisible:1b,Silent:1b,Invulnerable:1b,Marker:1b,NoGravity:1b}

scoreboard players set @e[r=10,type=armor_stand,name=保护] 保护等级 1
scoreboard players operation @e[r=10,type=armor_stand,name=保护] 保护编号 = @s 领地

spawnpoint @s ~ ~ ~
scoreboard players set @s 新人奖励 2
scoreboard players set @s jiazai -1
