execute @a[score_红包金额=-1] ~ ~ ~ function main:玩家触发/红包/红包_检测金额_负数金额
execute @a[score_红包金额_min=1] ~ ~ ~ function main:玩家触发/红包/红包_检测金额

execute @a[score_红包数量=-1] ~ ~ ~ function main:玩家触发/红包/红包_检测数量_负数数量
execute @a[score_红包数量_min=1] ~ ~ ~ function main:玩家触发/红包/红包_检测数量

scoreboard players remove @e[type=armor_stand,c=1,tag=红包延时,score_延时_min=620,score_延时=620,score_红包金额_min=100] 延时 1

execute @e[type=armor_stand,c=1,tag=红包延时,score_延时_min=21,score_延时=619] ~ ~ ~ function main:玩家触发/红包/红包_延时