scoreboard players operation @p[r=3,tag=收入者] 金钱 += @s fk
scoreboard players operation @s 金钱 -= @s fk

tellraw @s [{"text":"【蚂蚁支付】","color":"yellow"},{"text":"您通过快捷支付转给","color":"red"},{"selector":"@p[tag=收入者,r=3]","bold":true},{"score":{"name":"@s","objective":"fk"},"color":"yellow","bold":true},{"text":"金币","color":"gold"}]
tellraw @p[tag=收入者,r=3] [{"text":"【蚂蚁支付】","color":"yellow"},{"text":"您收到","color":"green"},{"selector":"@s","bold":true},{"score":{"name":"@s","objective":"fk"},"color":"yellow","bold":true},{"text":"金币","color":"gold"}]
