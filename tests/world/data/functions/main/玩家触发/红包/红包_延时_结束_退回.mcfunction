tellraw @s [{"text":"----------红包发送完毕----------","color":"red"}]
scoreboard players tag @s[tag=抢红包] remove 抢红包

scoreboard players operation @s id缓存 = @s id
scoreboard players operation @s id缓存 -= 发红包id 参数

scoreboard players operation @s[score_id缓存_min=0,score_id缓存=0] 金钱 += @e[type=armor_stand,c=1,tag=红包延时] 红包金额
scoreboard players operation @s[score_id缓存_min=0,score_id缓存=0] 发红包总值 -= @e[type=armor_stand,c=1,tag=红包延时] 红包金额
tellraw @s[score_id缓存_min=0,score_id缓存=0] [{"text":"【红包】","color":"yellow"},{"text":"红包发送完毕，退回","color":"dark_red"},{"score":{"name":"@e[type=armor_stand,c=1,tag=红包延时]","objective":"红包金额"}},{"text":"金","color":"dark_red"}]
