tellraw @a[score_id_min=1] [{"text":"【传送术】","color":"yellow"},{"text":"传送已结束","color":"green"}]

scoreboard players reset 传送倒计时 公告
scoreboard players set 传送闲置中 公告 0

scoreboard objectives remove 接受队列
scoreboard objectives remove 请求编号

scoreboard players set @s 延时 220
