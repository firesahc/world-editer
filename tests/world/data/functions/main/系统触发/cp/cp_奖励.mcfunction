scoreboard objectives add cp缓存 dummy
execute @a[score_id_min=1] ~ ~ ~ function main:系统触发/cp/cp_奖励_0
tellraw @a[score_id_min=1] [{"text":"【蚂蚁福彩】","color":"yellow"},{"text":" 中奖号码","color":"gold"},{"text":"(","color":"gold","bold":true},{"score":{"name":"cpz","objective":"参数"},"color":"light_purple","bold":true},{"text":")","color":"gold","bold":true},{"text":"【奖金3000金币】","color":"yellow","bold":true},{"text":"\n 中奖名单","color":"red"},{"text":"（","color":"gold","bold":true},{"selector":"@a[score_cp缓存_min=0,score_cp缓存=0]","bold":true,"color":"light_purple"},{"text":"）","color":"gold","bold":true}]
scoreboard objectives remove cp缓存

scoreboard players reset 福彩抽取倒计时 公告

scoreboard players set @s 延时 3600