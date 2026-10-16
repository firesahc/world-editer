tellraw @s [{"text":"每","color":"gold","bold":true},{"text":"日","color":"aqua","bold":true},{"text":"登","color":"yellow","bold":true},{"text":"录","color":"green","bold":true},{"text":"奖","color":"red","bold":true},{"text":"励","color":"blue","bold":true},{"text":"！！！","color":"gold","bold":true},{"text":" 积分+20 ","color":"green","bold":true},{"text":" 金币+30","color":"aqua","bold":true},{"text":"已经重置出售次数","color":"green"}]

scoreboard players add @s jf 20
scoreboard players add @s 金钱 30

scoreboard players set @s 今日买入 0
scoreboard players set @s 今日抛售 0

scoreboard players set @s 活动任务次数 0
scoreboard players set @s 副本次数 5

scoreboard players set @s[score_主线_min=11,score_主线=31] 出售 100
scoreboard players set @s[score_主线_min=32,score_主线=33] 出售 175
scoreboard players set @s[score_主线_min=34,score_主线=35] 出售 275

scoreboard players set @s 每日刷新 1