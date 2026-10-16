scoreboard players set xz副本状态 xz贾维斯 1
scoreboard players set xz副本成功 xz贾维斯 0
scoreboard players set xz副本失败 xz贾维斯 0
summon minecraft:vindication_illager -3980 13 -915 {CustomName:"贾维斯",Team:"金色",Tags:["副本"],CustomNameVisible:1b,PersistenceRequired:1b,Health:40,DeathLootTable:"entities/empty",Attributes:[{Name:"generic.attackDamage",Base:18},{Name:"generic.maxHealth",Base:40},{Name:"generic.movementSpeed",Base:0.45},{Name:"generic.knockbackResistance",Base:1},{Name:"generic.followRange",Base:100},{Name:"generic.armor",Base:20},{Name:"generic.armorToughness",Base:20}],ActiveEffects:[{Id:11,Amplifier:3,Duration:120000,ShowParticles:0b},{Id:12,Amplifier:1,Duration:120000,ShowParticles:0b}],HandItems:[{id:"minecraft:diamond_axe",Count:1b,Damage:0s,tag:{ench:[{id:19,lvl:2},{id:71,lvl:1}]}},{}],ArmorItems:[{id:"minecraft:diamond_boots",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:3,lvl:20},{id:4,lvl:20}]}},{id:"minecraft:diamond_leggings",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:2,lvl:20}]}},{id:"minecraft:diamond_chestplate",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:1,lvl:20}]}},{id:"minecraft:diamond_helmet",Count:1b,Damage:0s,tag:{ench:[{id:71,lvl:1},{id:0,lvl:20}]}}]}
tellraw @a {"text":"<贾维斯> 欢迎你们，新来的搓澡师傅,过来帮我搓搓后背。","color":"gold"}
setblock -3993 1 -947 minecraft:redstone_torch
setblock -3989 1 -947 minecraft:redstone_block
setblock -3987 1 -947 minecraft:redstone_torch
setblock -3995 1 -924 minecraft:redstone_block
scoreboard players set xz消息3 xz贾维斯 0
scoreboard players set xz消息2 xz贾维斯 0
give @p[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,score_xz技能_min=1,score_xz技能=1] minecraft:splash_potion 1 0 {display:{Name:"§c§l烈火燎原",Lore:["§a右键使用或扔出即可释放技能"]},HideFlags:32,Tags:["攻击技能"],Potion:water}
give @p[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,score_xz技能_min=2,score_xz技能=2] minecraft:splash_potion 1 0 {display:{Name:"§2§l固若金汤",Lore:["§a右键使用或扔出即可释放技能"]},HideFlags:32,Tags:["防御技能"],Potion:water}
give @p[x=-4001,y=0,z=-951,dx=42,dy=50,dz=42,score_xz技能_min=3,score_xz技能=3] minecraft:splash_potion 1 0 {display:{Name:"§d§l回天术",Lore:["§a右键使用或扔出即可释放技能"]},HideFlags:32,Tags:["治疗技能"],Potion:water}
fill -3967 1 -915 -3967 1 -919 minecraft:redstone_block
scoreboard objectives add xz死亡 deathCount



