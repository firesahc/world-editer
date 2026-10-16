scoreboard players add 火星历 参数 1

scoreboard objectives remove 每日刷新
scoreboard objectives add 每日刷新 dummy

scoreboard objectives remove 每日任务
scoreboard objectives add 每日任务 dummy
scoreboard objectives remove 任务1
scoreboard objectives add 任务1 dummy
scoreboard objectives remove 任务2
scoreboard objectives add 任务2 dummy
scoreboard objectives remove 任务3
scoreboard objectives add 任务3 dummy
scoreboard objectives remove 任务4
scoreboard objectives add 任务4 dummy
scoreboard objectives remove 任务5
scoreboard objectives add 任务5 dummy

scoreboard objectives remove 今日买入
scoreboard objectives add 今日买入 dummy
scoreboard objectives remove 今日抛售
scoreboard objectives add 今日抛售 dummy

scoreboard objectives remove 活动任务次数
scoreboard objectives add 活动任务次数 dummy
scoreboard objectives remove 副本次数
scoreboard objectives add 副本次数 dummy

function 随机数:股市
scoreboard players operation 科技 gp增幅 = 股市 随机数
scoreboard players operation @e[type=armor_stand,tag=股价] kj += 科技 gp增幅
function 随机数:股市
scoreboard players operation 农业 gp增幅 = 股市 随机数
scoreboard players operation @e[type=armor_stand,tag=股价] ny += 农业 gp增幅
function 随机数:股市
scoreboard players operation 矿业 gp增幅 = 股市 随机数
scoreboard players operation @e[type=armor_stand,tag=股价] ky += 矿业 gp增幅