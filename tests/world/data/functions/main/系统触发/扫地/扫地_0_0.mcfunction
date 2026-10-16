tp @e[rm=1000,type=Zombie] -2007 47 -2025
tp @e[rm=1000,type=Spider] -2007 47 -2025
tp @e[rm=1000,type=Creeper] -2007 47 -2025
tp @e[rm=1000,type=Skeleton] -2007 47 -2025
tp @e[rm=1000,type=slime] -2007 47 -2025

kill @e[type=item]

tellraw @a [{"text":"【系统消息】","color":"gold","bold":true},{"text":" 世界清理完成~","color":"red"}]

scoreboard players reset 世界清理倒计时 公告

scoreboard players set @s 延时 600