scoreboard players add 玩家总数 参数 1

tellraw @s {"text":"恭喜您通过挑战！！ \n点击功能书【回岛】可以创建空岛","color":"aqua","bold":"true"} 
tellraw @a ["",{"text":"考","color":"gold","bold":"true"},{"text":"验","color":"aqua","bold":"true"},{"text":"通","color":"yellow","bold":"true"},{"text":"过","color":"green","bold":"true"},{"text":"！","color":"red","bold":"true"},{"selector":"@s","color":"light_purple","bold":"true"},{"text":"是第[","color":"gold","bold":"true"},{"score":{"name":"玩家总数","objective":"参数"},"color":"green","bold":"true"},{"text":"]位正式玩家","color":"gold","bold":"true"},{"text":" 老玩家多多关照 ~~~","color":"red","bold":"true"}]

give @s carrot_on_a_stick 1 0 {display:{Name:"§b菜单"},Tags:["菜单"],ench:[{id:71s,lvl:0s}],HideFlags:1}

scoreboard players operation @s 年龄 = 火星历 参数
scoreboard players operation @s 最后日期 = 火星历 参数
scoreboard players operation @s 领土 = 玩家总数 参数
scoreboard players operation @s 领地 = 玩家总数 参数
scoreboard players operation @s id = 玩家总数 参数

scoreboard players set @s 副本次数 5
scoreboard players set @s 出售 50
scoreboard players set @s 主线 11
scoreboard players set @s 面板显示 1
scoreboard players set @s 基地等级 1
scoreboard players set @s 基地保护等级 1

scoreboard players add @s 传送延时 0
scoreboard players add @s 每日刷新 0
scoreboard players add @s 今日买入 0
scoreboard players add @s 今日抛售 0
scoreboard players add @s 称号 0
scoreboard players add @s 在线小时 0
scoreboard players add @s ny 0
scoreboard players add @s ky 0
scoreboard players add @s kj 0
scoreboard players add @s 10小时奖励 0
scoreboard players add @s 金钱 0
scoreboard players add @s cp 0

scoreboard teams join 菜鸟 @s

tp @s -2000 73 -2000