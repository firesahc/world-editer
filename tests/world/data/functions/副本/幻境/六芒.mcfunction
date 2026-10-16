scoreboard players set xz六芒星阵 xz幻境森林 0
title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] subtitle [{"text":"幻境●宗师释放了得意技","color":"black"}]
title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] title [{"text":"绝●六芒星阵","color":"black"}]
summon minecraft:wither_skeleton -4501 31 -972 {NoAI:1,CustomName:"1",Team:"黄色",Tags:["副本"],PersistenceRequired:1,DeathLootTable:"entities/empty",Rotation:[180.0F,0.0F],Glowing:1,CustomNameVisible:1}
summon minecraft:wither_skeleton -4472 31 -972 {NoAI:1,CustomName:"2",Team:"黄色",PersistenceRequired:1,Tags:["副本"],DeathLootTable:"entities/empty",Rotation:[180.0F,0.0F],Glowing:1,CustomNameVisible:1}
summon minecraft:wither_skeleton -4456.5 31 -997.0 {NoAI:1,CustomName:"3",Team:"黄色",PersistenceRequired:1,Tags:["副本"],Rotation:[90.0F,0.0F],DeathLootTable:"entities/empty",Glowing:1,CustomNameVisible:1}
summon minecraft:wither_skeleton -4472 31 -1023 {NoAI:1,CustomName:"4",Team:"黄色",Tags:["副本"],PersistenceRequired:1,DeathLootTable:"entities/empty",Glowing:1,CustomNameVisible:1}
summon minecraft:wither_skeleton -4501 31 -1023 {NoAI:1,CustomName:"5",Team:"黄色",PersistenceRequired:1,Tags:["副本"],DeathLootTable:"entities/empty",Glowing:1,CustomNameVisible:1}
summon minecraft:wither_skeleton -4515.5 31 -997.0 {NoAI:1,CustomName:"6",Team:"黄色",PersistenceRequired:1,Tags:["副本"],Rotation:[-90.0F,0.0F],DeathLootTable:"entities/empty",Glowing:1,CustomNameVisible:1}
setblock -4492 19 -990 minecraft:air
fill -4493 19 -985 -4493 19 -980 minecraft:redstone_block
scoreboard objectives add xz阵法缓存 dummy
scoreboard players set @e[name=1,type=wither_skeleton,r=1000] xz阵法缓存 1
scoreboard players set @e[name=2,type=wither_skeleton,r=1000] xz阵法缓存 2
scoreboard players set @e[name=3,type=wither_skeleton,r=1000] xz阵法缓存 3
scoreboard players set @e[name=4,type=wither_skeleton,r=1000] xz阵法缓存 4
scoreboard players set @e[name=5,type=wither_skeleton,r=1000] xz阵法缓存 5
scoreboard players set @e[name=6,type=wither_skeleton,r=1000] xz阵法缓存 6
scoreboard players tag @r[type=wither_skeleton,score_xz阵法缓存_min=1] add 顺序1
scoreboard players operation 击杀1 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序1] xz阵法缓存
scoreboard players reset @e[tag=顺序1] xz阵法缓存
scoreboard players tag @r[type=wither_skeleton,score_xz阵法缓存_min=1] add 顺序2
scoreboard players operation 击杀2 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序2] xz阵法缓存
scoreboard players reset @e[tag=顺序2] xz阵法缓存
scoreboard players tag @r[type=wither_skeleton,score_xz阵法缓存_min=1] add 顺序3
scoreboard players operation 击杀3 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序3] xz阵法缓存
scoreboard players reset @e[tag=顺序3] xz阵法缓存
scoreboard players tag @r[type=wither_skeleton,score_xz阵法缓存_min=1] add 顺序4
scoreboard players operation 击杀4 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序4] xz阵法缓存
scoreboard players reset @e[tag=顺序4] xz阵法缓存
scoreboard players operation 击杀5 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序5] xz阵法缓存
scoreboard players reset @e[tag=顺序5] xz阵法缓存
scoreboard players tag @r[type=wither_skeleton,score_xz阵法缓存_min=1] add 顺序6
scoreboard players operation 击杀6 xz阵法缓存 = @e[type=wither_skeleton,tag=顺序6] xz阵法缓存
scoreboard players reset @e[tag=顺序6] xz阵法缓存
setblock -4492 19 -978 redstone_block
scoreboard players add 存活 xz阵法缓存 0
tp @e[type=evocation_illager,r=1000] -4486.0 36.0 -997.0
entitydata @e[type=evocation_illager,r=1000] {NoGravity:1,NoAI:1,Invulnerable:1}
setblock -4492 19 -974 redstone_block
setblock -4492 19 -976 redstone_block
scoreboard players tag @r[x=-4550,y=9,z=-1050,dx=120,dy=50,dz=100,m=!3] add 告知者