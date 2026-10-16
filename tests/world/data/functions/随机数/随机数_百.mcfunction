scoreboard players set 随机数 随机数 0

scoreboard players operation 个位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 十位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 十位 随机数基 *= 十 随机数基

scoreboard players operation 随机数 随机数 += 个位 随机数基
scoreboard players operation 随机数 随机数 += 十位 随机数基

scoreboard players add 随机数 随机数 1