scoreboard players operation @s 离线日期 = @s 最后日期
scoreboard players operation @s 离线日期 *= -1 参数
scoreboard players remove @s 离线日期 1

tellraw @s [{"text":"您已离线：","color":"gold","bold":true},{"score":{"name":"@s","objective":"离线日期"},"color":"green","bold":true},{"text":"年 相关奖励已发放","color":"gold","bold":true}]

scoreboard players set @s[score_离线日期_min=5] 离线日期 4