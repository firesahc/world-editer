summon minecraft:vindication_illager -3058 12 -960 {CustomName:"地宫●主人",Team:"黑色",Tags:["主人"],CustomNameVisible:1b,Glowing:1b,PersistenceRequired:1b,Health:400,DeathLootTable:"entities/empty",Attributes:[{Name:"generic.attackDamage",Base:12},{Name:"generic.maxHealth",Base:400},{Name:"generic.movementSpeed",Base:0.4},{Name:"generic.knockbackResistance",Base:1},{Name:"generic.followRange",Base:100},{Name:"generic.armor",Base:5},{Name:"generic.armorToughness",Base:20}],ActiveEffects:[{Id:12,Amplifier:0,Duration:12000,ShowParticles:0b}],HandItems:[{id:"minecraft:diamond_axe",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1}]}},{}],ArmorItems:[{id:"minecraft:iron_boots",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_leggings",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_chestplate",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_helmet",Count:1,tag:{ench:[{id:71,lvl:1},{id:1,lvl:10}]}}]}
summon minecraft:illusion_illager -3051 12 -960 {CustomName:"地宫●夫人",Team:"黑色",Tags:["副本"],CustomNameVisible:1b,Glowing:1b,PersistenceRequired:1b,Health:350,DeathLootTable:"entities/empty",Attributes:[{Name:"generic.maxHealth",Base:350},{Name:"generic.movementSpeed",Base:0.75},{Name:"generic.followRange",Base:100},{Name:"generic.armor",Base:5},{Name:"generic.armorToughness",Base:20}],ActiveEffects:[{Id:12,Amplifier:0,Duration:12000,ShowParticles:0b}],HandItems:[{id:"minecraft:bow",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:49,lvl:2},{id:48,lvl:40}]}},{}],ArmorItems:[{id:"minecraft:iron_boots",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_leggings",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_chestplate",Count:1,tag:{ench:[{id:71,lvl:1}]}},{id:"minecraft:iron_helmet",Count:1,tag:{ench:[{id:71,lvl:1}]}}]}
tellraw @a [{"text":"<地宫●主人> 让我来送你们去另一个世界吧！","color":"dark_red"}]
scoreboard players set xz无中生有2 xz恶毒地宫 1
effect @a[x=-3061,y=11,z=-939,dx=23,dy=3,dz=18,m=2] glowing 1 2 true
scoreboard teams join 黑色 @a[x=-3061,y=11,z=-939,dx=23,dy=3,dz=18,m=2]
tp @a[x=-3061,y=11,z=-939,dx=23,dy=3,dz=18] -3044 12 -943
setblock -3117 2 -946 air
setblock -3117 2 -944 minecraft:redstone_block
setblock -3095 2 -946 minecraft:redstone_block
scoreboard players set xz效果状态 xz恶毒地宫 0
kill @e[x=-3136,y=0,z=-979,dx=98,dy=40,dz=58,name=地宫黑蜘蛛]
