function main:玩家触发/红包/红包_抢红包_最后 if @e[type=armor_stand,c=1,tag=红包延时,score_红包数量=1]

execute @e[type=armor_stand,c=1,tag=红包延时,score_红包数量_min=2] ~ ~ ~ function main:玩家触发/红包/红包_抢红包_随机
function main:玩家触发/红包/红包_抢红包_领取 if @e[type=armor_stand,c=1,tag=红包延时,score_红包数量_min=2]
