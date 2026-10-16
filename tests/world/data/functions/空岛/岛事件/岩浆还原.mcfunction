scoreboard players add @e[type=armor_stand,tag=岩浆还原延时] 延时 1

execute @e[type=armor_stand,tag=岩浆还原延时,score_延时_min=10,score_延时=10] ~ ~ ~ execute @a[score_id_min=1,score_id缓存=0] ~ ~-1 ~ detect ~ ~ ~ minecraft:cobblestone 0 fill ~ ~-1 ~ ~ ~-1 ~ minecraft:lava 0 replace minecraft:obsidian

scoreboard players set @e[type=armor_stand,tag=岩浆还原延时,score_延时_min=10,score_延时=10] 延时 0