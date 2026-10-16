function main:玩家触发/红包/红包_检测数量_正在使用 if @e[tag=红包延时,type=armor_stand,c=1,score_延时_min=21,score_延时=619]

function main:玩家触发/红包/红包_检测数量_数量过多 if @s[score_红包数量_min=41]

function main:玩家触发/红包/红包_检测数量_数量成功 if @s[score_红包数量_min=1,score_红包数量=40]

scoreboard players set @s 红包数量 0