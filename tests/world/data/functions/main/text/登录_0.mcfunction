tellraw @s [{"text":"欢","color":"gold","bold":true},{"text":"迎","color":"aqua","bold":true},{"text":"回","color":"yellow","bold":true},{"text":"来","color":"green","bold":true},{"text":"！！！","color":"gold","bold":true},{"text":" 空岛日历","color":"gold","bold":true},{"score":{"name":"火星历","objective":"参数"},"color":"green","bold":true},{"text":"年 ~~","color":"gold","bold":true}]
title @s title [{"text":"欢","color":"red","bold":"true"},{"text":"迎","color":"aqua","bold":"true"},{"text":"回","color":"yellow","bold":"true"},{"text":"来","color":"green","bold":"true"},{"text":"！！！","color":"gold","bold":"true"}] 10 600 10

function main:text/登录_0_删抢红包 if @e[type=armor_stand,tag=红包延时,score_延时_min=620,score_延时=620]

scoreboard players set @s 登录 0