execute @r[type=cow] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"cow",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=cow] ~ ~ ~ execute @e[r=100,type=cow] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=cow] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=cow] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=cow]"},"color":"yellow","bold":true},{"text":"只牛被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=cow] ~ ~ ~ kill @e[r=100,type=cow]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=cow] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=cow]

execute @r[type=sheep] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"sheep",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=sheep] ~ ~ ~ execute @e[r=100,type=sheep] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=sheep] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=sheep] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=sheep]"},"color":"yellow","bold":true},{"text":"只羊被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=sheep] ~ ~ ~ kill @e[r=100,type=sheep]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=sheep] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=sheep]

execute @r[type=wolf] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"wolf",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=wolf] ~ ~ ~ execute @e[r=100,type=wolf] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=wolf] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=wolf] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=wolf]"},"color":"yellow","bold":true},{"text":"只狼被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=wolf] ~ ~ ~ kill @e[r=100,type=wolf]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=wolf] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=wolf]

execute @r[type=horse] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"horse",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=horse] ~ ~ ~ execute @e[r=100,type=horse] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=horse] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=horse] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=horse]"},"color":"yellow","bold":true},{"text":"只马被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=horse] ~ ~ ~ kill @e[r=100,type=horse]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=horse] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=horse]

execute @r[type=llama] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"llama",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=llama] ~ ~ ~ execute @e[r=100,type=llama] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=llama] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=llama] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=llama]"},"color":"yellow","bold":true},{"text":"只羊驼被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=llama] ~ ~ ~ kill @e[r=100,type=llama]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=llama] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=llama]

execute @r[type=donkey] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"donkey",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=donkey] ~ ~ ~ execute @e[r=100,type=donkey] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=donkey] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=donkey] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=donkey]"},"color":"yellow","bold":true},{"text":"只驴被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=donkey] ~ ~ ~ kill @e[r=100,type=donkey]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=donkey] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=donkey]

execute @r[type=mule] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"mule",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=mule] ~ ~ ~ execute @e[r=100,type=mule] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=mule] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=mule] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=mule]"},"color":"yellow","bold":true},{"text":"只骡被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=mule] ~ ~ ~ kill @e[r=100,type=mule]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=mule] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=mule]

execute @r[type=chicken] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"chicken",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=chicken] ~ ~ ~ execute @e[r=100,type=chicken] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=chicken] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=chicken] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=chicken]"},"color":"yellow","bold":true},{"text":"只鸡被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=chicken] ~ ~ ~ kill @e[r=100,type=chicken]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=chicken] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=chicken]

execute @r[type=pig] ~ ~ ~ summon minecraft:armor_stand ~ ~ ~ {CustomName:"pig",Invisible:1,Invulnerable:1,Marker:1,NoGravity:1,PersistenceRequired:1}
execute @e[type=armor_stand,name=pig] ~ ~ ~ execute @e[r=100,type=pig] ~ ~ ~ scoreboard players add @e[type=armor_stand,name=pig] xz瘟疫 1
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=pig] ~ ~ ~ tellraw @a [{"text":"【瘟疫警告】","color":"red"},{"selector":"@p"},{"text":"附近有"},{"score":{"objective":"xz瘟疫","name":"@e[score_xz瘟疫_min=17,type=armor_stand,name=pig]"},"color":"yellow","bold":true},{"text":"只猪被瘟疫夺去了生命"}]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=pig] ~ ~ ~ kill @e[r=100,type=pig]
execute @e[score_xz瘟疫_min=17,type=armor_stand,name=pig] ~ ~ ~ kill @e[r=20,type=item]
kill @e[type=armor_stand,name=pig]


scoreboard players set @s 延时 0