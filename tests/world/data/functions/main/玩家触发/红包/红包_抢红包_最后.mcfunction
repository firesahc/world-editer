scoreboard players operation @s 领红包金额 = @e[type=armor_stand,c=1,tag=红包延时] 红包金额

tellraw @a[score_id_min=1] [{"text":"【红包】","color":"yellow"},{"text":"玩家","color":"red"},{"selector":"@s"},{"text":"抢到红包","color":"red"},{"score":{"name":"@s","objective":"领红包金额"}},{"text":"金","color":"red"}]
scoreboard players operation @s 金钱 += @s 领红包金额

scoreboard players operation @e[type=armor_stand,c=1,tag=红包延时] 红包金额 -= @s 领红包金额
scoreboard players set @e[type=armor_stand,c=1,tag=红包延时] 延时 21

scoreboard players tag @s add 抢红包