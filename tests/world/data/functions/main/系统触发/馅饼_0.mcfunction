scoreboard players set @r[score_id_min=1] 馅饼 1
scoreboard players add @a[score_馅饼_min=1,score_馅饼=1,c=1] 金钱 666
tellraw @a ["",{"text":"【天降馅饼】","color":"yellow","bold":true},{"text":"砸中了","color":"red","bold":true},{"selector":"@a[score_馅饼_min=1,score_馅饼=1,c=1]","color":"yellow","bold":true},{"text":" 获得 ","color":"yellow"},{"text":"(","color":"red","bold":true},{"text":">>>","color":"green","bold":true},{"text":"&","color":"white","bold":true},{"text":"666金币","color":"gold","bold":true},{"text":")","color":"red","bold":true}]
scoreboard players set @a[score_馅饼_min=1,score_馅饼=1] 馅饼 0

scoreboard players set @s 延时 0