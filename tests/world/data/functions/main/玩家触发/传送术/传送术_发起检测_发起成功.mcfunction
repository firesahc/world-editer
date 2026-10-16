scoreboard players reset 传送闲置中 公告
scoreboard players set 传送倒计时 公告 10

scoreboard objectives add 接受队列 trigger
scoreboard objectives add 请求编号 dummy

scoreboard players enable @s 接受队列
scoreboard players set @s 请求编号 -1

scoreboard players remove @s 金钱 10
scoreboard players set @s book 0

tellraw @a[score_id_min=1] [{"text":"-----------传送术-----------\n","color":"yellow","bold":true,"hoverEvent":{"action":"show_text","value":"①请求者传送后消耗10金币\n②支持多对一传送"}},{"text":" 发起者：","color":"red","bold":true},{"selector":"@s"},{"text":"\n【点击此处请求传送至发起者】","color":"green","clickEvent":{"action":"run_command","value":"/trigger book set 10"}},{"text":"\n----------------------------","color":"yellow","bold":true}]
