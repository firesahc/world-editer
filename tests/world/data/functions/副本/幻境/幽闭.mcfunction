title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] subtitle [{"text":"幻境●宗师释放了得意技","color":"black"}]
title @a[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70] title [{"text":"绝●幻境幽闭","color":"black"}]
scoreboard players set xz幻境幽闭 xz幻境森林 0
tp @r[x=-4525,y=0,z=-1032,dx=80,dy=50,dz=70,m=2] -4459 10 -975
summon stray -4451 10 -966 {CustomName:"幻境●梦魇",CustomNameVisible:1,Team:"黑色",Tags:["副本"],PersistenceRequired:1b,Health:300,Silent:1b,Attributes:[{Name:"generic.attackDamage",Base:102},{Name:"generic.maxHealth",Base:300},{Name:"generic.movementSpeed",Base:0.4},{Name:"generic.knockbackResistance",Base:1},{Name:"generic.followRange",Base:100},{Name:"generic.armor",Base:5},{Name:"generic.armorToughness",Base:20}],ActiveEffects:[{Id:12,Amplifier:0,Duration:12000,ShowParticles:0b}],HandItems:[{id:"minecraft:diamond_axe",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:19,lvl:2}]}},{}],Glowing:1,DeathLootTable:"entities/empty",Tags:["副本"],ArmorItems:[{id:"minecraft:iron_boots",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_leggings",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_chestplate",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_helmet",Count:1,tag:{ench:[{id:71,lvl:1},{id:1,lvl:10}]}}]}
execute @a[x=-4459,y=10,z=-975,r=5] ~ ~ ~ playsound minecraft:block.portal.travel player @p ~ ~ ~ 0.6 2
setblock -4492 19 -994 minecraft:air
setblock -4500 19 -994 minecraft:redstone_block
effect @a[x=-4459,y=10,z=-975,r=2] glowing 10000 0 true