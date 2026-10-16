title @s title [{"text":" 中奖号码","color":"gold"},{"text":"(","color":"red","bold":true},{"score":{"name":"cpz","objective":"参数"},"color":"light_purple","bold":true},{"text":")","color":"red","bold":true}]

execute @s[score_cp_min=1] ~ ~ ~ scoreboard players operation @s cp缓存 = @s cp
execute @s[score_cp_min=1] ~ ~ ~ scoreboard players operation @s cp缓存 -= cpz 参数
execute @s[score_cp_min=1] ~ ~ ~ scoreboard players set @s cp 0

scoreboard players add @s[score_cp缓存_min=0,score_cp缓存=0] 金钱 3000