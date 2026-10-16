function main:玩家触发/红包/红包_检测金额_正在使用 if @e[tag=红包延时,type=armor_stand,c=1,score_延时_min=21,score_延时=619]

function main:玩家触发/红包/红包_检测金额_未设数量 unless @e[type=armor_stand,c=1,tag=红包延时,score_红包数量_min=1,score_红包数量=40]

function main:玩家触发/红包/红包_检测金额_金额过低 if @s[score_红包金额_min=1,score_红包金额=99]

scoreboard players operation @s[score_红包金额_min=100] 金钱判断缓存 = @s[score_红包金额_min=100] 红包金额
scoreboard players operation @s[score_红包金额_min=100] 金钱判断缓存 -= @s[score_红包金额_min=100] 金钱

function main:玩家触发/红包/红包_检测金额_金钱不足 if @s[score_红包金额_min=100,score_金钱判断缓存_min=1]

function main:玩家触发/红包/红包_检测金额_金额成功 if @s[score_红包金额_min=100,score_金钱判断缓存=0]

scoreboard players set @s 红包金额 0
scoreboard players set @s 金钱判断缓存 1