scoreboard players remove @s 延时 1

scoreboard players operation 传送术延时缓存 延时 = @s 延时
scoreboard players operation 传送术延时缓存 延时 /= 20进1 延时
scoreboard players operation 传送倒计时 公告 = 传送术延时缓存 延时

function main:玩家触发/传送术/传送术_延时_0 if @s[score_延时_min=20,score_延时=20]