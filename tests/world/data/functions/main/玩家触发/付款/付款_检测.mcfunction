scoreboard players tag @s add 转出者

scoreboard players operation @s 金钱判断缓存 = @s fk
scoreboard players operation @s 金钱判断缓存 -= @s 金钱

tellraw @s[score_金钱判断缓存_min=1] [{"text":"【蚂蚁支付】","color":"yellow"},{"selector":"@s"},{"text":"转出请求失败！金币不足！","color":"dark_red"}]

execute @s[score_金钱判断缓存=0] ~ ~ ~ function main:玩家触发/付款/付款_无人 unless @a[r=3,tag=!转出者]
tellraw @s[score_金钱判断缓存=0,tag=周围无人] [{"text":"【蚂蚁支付】","color":"yellow"},{"selector":"@s"},{"text":"转出请求失败！3格内没有玩家！","color":"dark_red"}]

execute @s[score_金钱判断缓存=0,tag=!周围无人] ~ ~ ~ scoreboard players tag @p[tag=!转出者,r=3] add 收入者
function main:玩家触发/付款/付款_支付 if @s[score_金钱判断缓存=0,tag=!周围无人]

scoreboard players set @s fk 0
scoreboard players set @s 金钱判断缓存 1

scoreboard players tag @s[tag=转出者] remove 转出者
scoreboard players tag @s[tag=周围无人] remove 周围无人
scoreboard players tag @a[r=3,tag=收入者] remove 收入者