tellraw @a[score_死亡_min=1,score_id_min=1] {"text":"输入 trigger book set 1 可回城~","color":"red"}
tellraw @a[score_死亡_min=1,score_在线小时_min=10] ["",{"text":"[","color":"gold","bold":true},{"text":"！","color":"dark_red","bold":true},{"text":"]","color":"gold","bold":true},{"text":" 死亡等级-1 ","color":"dark_red","bold":true},{"text":"存活","color":"red","bold":true},{"score":{"name":"@a[score_死亡_min=1,score_在线小时_min=10]","objective":"存活小时"},"color":"yellow","bold":true},{"text":"小时","color":"red","bold":true}]
xp -1l @a[score_死亡_min=1,score_在线小时_min=10]
scoreboard players set @a[score_死亡_min=1] 单次死亡杀怪 0
scoreboard players set @a[score_死亡_min=1] 存活小时 0
scoreboard players set @a[score_死亡_min=1] 死亡 0

scoreboard players enable @a[score_id_min=1] book

execute @a[score_id_min=1,score_在线时间_min=72000] ~ ~ ~ function main:系统触发/在线奖励
scoreboard players add @a[score_在线时间_min=72000] 在线小时 1
scoreboard players set @a[score_在线时间_min=72000] 在线时间 0
scoreboard players add @a[score_存活时间_min=72000] 存活小时 1
scoreboard players set @a[score_存活时间_min=72000] 存活时间 0