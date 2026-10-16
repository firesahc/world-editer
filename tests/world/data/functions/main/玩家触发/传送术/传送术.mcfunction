execute @a[score_book_min=9,score_book=9] ~ ~ ~ function main:玩家触发/传送术/传送术_发起检测

execute @a[score_请求编号=-1] ~ ~ ~ scoreboard players remove @e[type=armor_stand,c=1,tag=传送术延时,score_延时_min=220,score_延时=220] 延时 1

execute @e[type=armor_stand,c=1,tag=传送术延时,score_延时_min=21,score_延时=219] ~ ~ ~ function main:玩家触发/传送术/传送术_延时

execute @a[score_book_min=10,score_book=10] ~ ~ ~ function main:玩家触发/传送术/传送术_请求检测

execute @a[score_请求编号=-1,score_接受队列_min=1] ~ ~ ~ function main:玩家触发/传送术/传送术_同意请求