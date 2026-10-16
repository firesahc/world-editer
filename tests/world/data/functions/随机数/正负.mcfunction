scoreboard players operation @e[type=armor_stand,tag=正负] 随机数 = @r[type=armor_stand,name=cl] CL
execute @e[type=armor_stand,tag=正负,score_随机数_min=0,score_随机数=4] ~ ~ ~ scoreboard players set @s 随机数 -1
execute @e[type=armor_stand,tag=正负,score_随机数_min=5,score_随机数=9] ~ ~ ~ scoreboard players set @s 随机数 1