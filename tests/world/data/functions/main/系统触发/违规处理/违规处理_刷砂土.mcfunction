clear @s minecraft:dirt 1
scoreboard players tag @e[type=item,r=10] add 砂土 {Item:{id:"minecraft:dirt",Damage:1s}}
kill @e[type=item,r=10,tag=砂土]

scoreboard players tag @s add 刷砂土
execute @a[tag=!刷砂土,r=4] ~ ~ ~ function main:系统触发/违规处理/违规处理_参与砂土
scoreboard players tag @s remove 刷砂土

tellraw @a [{"text":"【警告】","color":"dark_red","bold":true},{"selector":"@s"},{"text":"因尝试刷砂土被关牢狱，牢狱+1000，金币-1000,严重警告一次！！！","color":"yellow"}]
scoreboard players add @s 牢狱 1000
scoreboard players remove @s[score_金钱_min=1000] 金钱 1000
scoreboard players set @s[score_金钱=999] 金钱 0
tp @s -1944 67 -2018
scoreboard players set @s 合成砂土 0
