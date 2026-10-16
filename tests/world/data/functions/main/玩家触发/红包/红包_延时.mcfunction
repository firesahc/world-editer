execute @a[score_抢红包_min=486,score_抢红包=486,tag=!抢红包] ~ ~ ~ function main:玩家触发/红包/红包_抢红包

scoreboard players remove @s 延时 1

scoreboard players operation 红包延时缓存 延时 = @s 延时
scoreboard players operation 红包延时缓存 延时 /= 20进1 延时
scoreboard players operation 红包倒计时 公告 = 红包延时缓存 延时

function main:玩家触发/红包/红包_延时_结束 if @s[score_延时_min=20,score_延时=20]