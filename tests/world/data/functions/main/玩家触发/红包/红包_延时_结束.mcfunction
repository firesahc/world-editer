execute @a[score_id_min=1] ~ ~ ~ function main:玩家触发/红包/红包_延时_结束_退回

scoreboard players reset 红包倒计时 公告
scoreboard players set @s 红包金额 0
scoreboard players set @s 红包数量 0

scoreboard objectives remove 抢红包
scoreboard objectives remove 领红包金额

scoreboard players set @s 延时 620