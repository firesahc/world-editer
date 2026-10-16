setblock -3963 1 -947 air
scoreboard players set xz消息 xz贾维斯 0
scoreboard players set xz五行俱下 xz贾维斯 0
scoreboard players set xz五行俱下2 xz贾维斯 0
scoreboard players set xz惊慌失措 xz贾维斯 0
scoreboard players set xz技能过滤 xz贾维斯 0
scoreboard players set xz灵爆 xz贾维斯 0
scoreboard players set xz移形换影 xz贾维斯 0
scoreboard players set xz等量齐观 xz贾维斯 0
scoreboard players set xz复旧如初 xz贾维斯 0
scoreboard players set xz魔唤术 xz贾维斯 0
scoreboard players set xz魔导星辰击 xz贾维斯 0
scoreboard objectives remove xz死亡
scoreboard players tag @a remove 锁链
scoreboard players tag @e[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,type=armor_stand] remove 生
setblock -3993 1 -947 air
fill -3989 1 -947 -3969 1 -947 air
setblock -3987 1 -938 air
setblock -3995 1 -924 air
kill @e[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,tag=副本]
kill @e[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,tag=回]
scoreboard objectives remove xz技能
scoreboard objectives add xz技能 dummy
scoreboard players set xz攻击技能 xz技能 0
scoreboard players set xz防御技能 xz技能 0
scoreboard players set xz治疗技能 xz技能 0
scoreboard players set xz技能冷却 xz技能 0
fill -3967 1 -913 -3967 1 -920 air