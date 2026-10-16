scoreboard players set 随机数 随机数 0

scoreboard players operation 个位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 十位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 十位 随机数基 *= 十 随机数基
scoreboard players operation 百位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 百位 随机数基 *= 百 随机数基
scoreboard players operation 千位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 千位 随机数基 *= 千 随机数基
scoreboard players operation 万位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 万位 随机数基 *= 万 随机数基
scoreboard players operation 十万位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 十万位 随机数基 *= 十万 随机数基
scoreboard players operation 百万位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 百万位 随机数基 *= 百万 随机数基
scoreboard players operation 千万位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 千万位 随机数基 *= 千万 随机数基
scoreboard players operation 亿位 随机数基 = @r[type=armor_stand,name=cl] CL
scoreboard players operation 亿位 随机数基 *= 亿 随机数基
scoreboard players operation 十亿位 随机数基 = @r[type=armor_stand,name=cl,score_随机数基=1] CL
scoreboard players operation 十亿位 随机数基 *= 十亿 随机数基

scoreboard players operation 随机数 随机数 += 个位 随机数基
scoreboard players operation 随机数 随机数 += 十位 随机数基
scoreboard players operation 随机数 随机数 += 百位 随机数基
scoreboard players operation 随机数 随机数 += 千位 随机数基
scoreboard players operation 随机数 随机数 += 万位 随机数基
scoreboard players operation 随机数 随机数 += 十万位 随机数基
scoreboard players operation 随机数 随机数 += 百万位 随机数基
scoreboard players operation 随机数 随机数 += 千万位 随机数基
scoreboard players operation 随机数 随机数 += 亿位 随机数基
scoreboard players operation 随机数 随机数 += 十亿位 随机数基

scoreboard players add 随机数 随机数 1