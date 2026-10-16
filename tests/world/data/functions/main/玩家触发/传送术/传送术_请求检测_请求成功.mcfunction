scoreboard players add 请求者总编号 请求编号 1
scoreboard players operation @s 请求编号 = 请求者总编号 请求编号

execute @s[score_请求编号=1,score_请求编号_min=1] ~ ~ ~ tellraw @a[score_请求编号=-1,c=1] [{"text":"\n"},{"selector":"@s","color":"yellow","bold":true},{"text":" 请求到你身边 ","color":"red"},{"text":"【点击接受】\n","color":"green","bold":true,"underlined":true,"hoverEvent":{"action":"show_text","value":"①注意财产保护\n②陌生人请求忽略即可"},"clickEvent":{"action":"run_command","value":"/trigger 接受队列 set 1"}}]

execute @s[score_请求编号=2,score_请求编号_min=2] ~ ~ ~ tellraw @a[score_请求编号=-1,c=1] [{"text":"\n"},{"selector":"@s","color":"yellow","bold":true},{"text":" 请求到你身边 ","color":"red"},{"text":"【点击接受】\n","color":"green","bold":true,"underlined":true,"hoverEvent":{"action":"show_text","value":"①注意财产保护\n②陌生人请求忽略即可"},"clickEvent":{"action":"run_command","value":"/trigger 接受队列 set 2"}}]

execute @s[score_请求编号=3,score_请求编号_min=3] ~ ~ ~ tellraw @a[score_请求编号=-1,c=1] [{"text":"\n"},{"selector":"@s","color":"yellow","bold":true},{"text":" 请求到你身边 ","color":"red"},{"text":"【点击接受】\n","color":"green","bold":true,"underlined":true,"hoverEvent":{"action":"show_text","value":"①注意财产保护\n②陌生人请求忽略即可"},"clickEvent":{"action":"run_command","value":"/trigger 接受队列 set 3"}}]

tellraw @s[score_请求编号_min=4] [{"text":"【传送术】","color":"yellow"},{"text":"请求已达上限！！","color":"red"}]

scoreboard players set @s book 0