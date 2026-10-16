scoreboard players test xz迷雾 xz幻境森林 1 1
scoreboard players tag @r[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,m=2] add 传送1
scoreboard players tag @r[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,tag=!传送1,m=2] add 传送2
execute @a[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,m=2,tag=传送1] ~ ~ ~ summon armor_stand ~ ~ ~ {CustomName:"cs1",Marker:1,NoGravity:1,Invisible:1}
execute @a[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,m=2,tag=传送2] ~ ~ ~ summon armor_stand ~ ~ ~ {CustomName:"cs2",Marker:1,NoGravity:1,Invisible:1}
tp @a[tag=传送1] @e[type=armor_stand,name=cs2]
tp @a[tag=传送2] @e[type=armor_stand,name=cs1]
kill @e[type=armor_stand,name=cs1]
kill @e[type=armor_stand,name=cs2]
scoreboard players tag @a[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,tag=传送1,m=2] remove 传送1
scoreboard players tag @a[x=-4550,y=20,z=-1050,dx=120,dy=50,dz=100,m=2,tag=传送2] remove 传送2
setblock -4492 19 -996 minecraft:air
title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] subtitle [{"text":"幻境●宗师释放了技能","color":"dark_red"}]
title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] title [{"text":"迷雾","color":"dark_red"}]
execute @e[name=幻境●宗师,type=evocation_illager,x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] ~ ~ ~ execute @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70,m=!3] ~ ~ ~ particle cloud ~ ~1 ~ 0.01 0.01 0.01 0.5 1000
execute @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] ~ ~ ~ playsound minecraft:entity.generic.splash player @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] ~ ~ ~ 1000 0.8 1
scoreboard players set xz迷雾 xz幻境森林 0

