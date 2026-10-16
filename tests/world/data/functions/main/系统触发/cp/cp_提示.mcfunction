scoreboard players operation 福彩抽取倒计时 公告 = @s 延时

execute @s[score_延时_min=60,score_延时=60] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【蚂蚁福彩】","color":"yellow"},{"text":" 开奖倒计时","color":"red"},{"text":"（","color":"gold"},{"text":"60","color":"green","bold":true},{"text":"秒","color":"aqua"},{"text":"）","color":"gold"}]
execute @s[score_延时_min=30,score_延时=30] ~ ~ ~ tellraw @a[score_id_min=1] [{"text":"【蚂蚁福彩】","color":"yellow"},{"text":" 开奖倒计时","color":"red"},{"text":"（","color":"gold"},{"text":"30","color":"green","bold":true},{"text":"秒","color":"aqua"},{"text":"）","color":"gold"}]

execute @s[score_延时_min=1,score_延时=3] ~ ~ ~ title @a[score_id_min=1] subtitle {"text":"幸运大抽奖倒计时","color":"light_purple"}
execute @s[score_延时_min=3,score_延时=3] ~ ~ ~ title @a[score_id_min=1] title {"text":"3","color":"yellow"}
execute @s[score_延时_min=2,score_延时=2] ~ ~ ~ title @a[score_id_min=1] title {"text":"2","color":"yellow"}
execute @s[score_延时_min=1,score_延时=1] ~ ~ ~ title @a[score_id_min=1] title {"text":"1","color":"yellow"}

execute @s[score_延时_min=1,score_延时=1] ~ ~ ~ scoreboard players operation cpz 参数 = @r[name=cl,type=armor_stand,score_CL_min=1] CL

function main:系统触发/cp/cp_奖励 if @s[score_延时_min=0,score_延时=0]