scoreboard players set @s[score_传送延时=0] 面板显示 2
scoreboard players set @s[score_传送延时=0] 传送延时 6
scoreboard players set @s[score_传送延时_min=1,score_权限_min=1] 传送延时 0

scoreboard players remove @s[score_传送延时_min=1] 传送延时 1
execute @s[score_传送延时_min=1] ~ ~ ~ title @s[score_传送延时_min=1] actionbar [{"score":{"name":"@s","objective":"传送延时"},"color":"black","bold":true},{"text":" 秒后执行","color":"yellow","bold":true}] 0 200 0

scoreboard players set @s[score_传送延时=0] 面板显示 1
scoreboard players operation @s[score_传送延时=0] cs = @s[score_传送延时=0] book
scoreboard players set @s[score_传送延时=0] book 0