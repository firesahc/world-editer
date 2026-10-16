scoreboard players operation @s id缓存 = @s 领土
scoreboard players operation @s id缓存 -= @e[score_保护编号_min=1,type=armor_stand,name=保护,c=1,r=80] 保护编号
scoreboard players operation @s id缓存 *= @s id缓存

scoreboard players set @s[score_id缓存_min=1] 冒险模式 1
effect @s[score_id缓存_min=1] 18 10 250 true
function 空岛:岛保护/容器保护 if @s[score_id缓存_min=1]

scoreboard players set @s[score_id缓存=0] 冒险模式 0