##一键恢复计分板 
#调用请使用 /function new3:sidebar2

scoreboard objectives remove 公告
scoreboard objectives add 公告 dummy §e———蚂蚁空岛§a公告栏§e———

scoreboard players set 传送闲置中 公告 1
scoreboard players set §c回主城命令 公告 -1
scoreboard players set §c/trigger_book_set_1 公告 -2