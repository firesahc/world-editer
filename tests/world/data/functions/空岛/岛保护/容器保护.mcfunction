scoreboard players add @s[score_潜影盒_min=1] 箱子 1
scoreboard players set @s[score_潜影盒_min=1] 潜影盒 0
scoreboard players add @s[score_漏斗_min=1] 箱子 1
scoreboard players set @s[score_漏斗_min=1] 漏斗 0
scoreboard players add @s[score_发射器_min=1] 箱子 1
scoreboard players set @s[score_发射器_min=1] 发射器 0
scoreboard players add @s[score_熔炉_min=1] 箱子 1
scoreboard players set @s[score_熔炉_min=1] 熔炉 0
scoreboard players add @s[score_酿造台_min=1] 箱子 1
scoreboard players set @s[score_酿造台_min=1] 酿造台 0

tp @s[score_箱子_min=1] ~ ~15 ~
title @s[score_箱子_min=1] title {"text":"你没有权限！！","color":"red","bold":true}
scoreboard players set @s 箱子 0
