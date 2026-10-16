tellraw @a[score_id_min=1] [{"text":"【传送术】","color":"yellow"},{"selector":"@s"},{"text":" 传送到 ","color":"green"},{"selector":"@a[score_请求编号=-1]"}]

scoreboard players set @s 箱子 0
scoreboard players set @s 酿造台 0
scoreboard players set @s 熔炉 0
scoreboard players set @s 发射器 0
scoreboard players set @s 漏斗 0
scoreboard players set @s 潜影盒 0

scoreboard players remove @s 金钱 10

tp @s @a[score_请求编号=-1]

scoreboard players set @a[score_请求编号=-1] 接受队列 0
scoreboard players enable @a[score_请求编号=-1] 接受队列