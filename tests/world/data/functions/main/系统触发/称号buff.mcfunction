effect @a[score_王者_min=1] strength 3 3 true
effect @a[score_王者_min=1] resistance 3 2 true
effect @a[x=-4490,y=40,z=-1030,rm=100,score_王者_min=1] night_vision 3 1 true
effect @a[score_王者_min=1] haste 3 1 true
effect @a[score_王者_min=1] speed 3 1 true

effect @a[score_战神_min=1] speed 3 1 true
effect @a[score_战神_min=1] strength 3 2 true

effect @a[team=修罗] minecraft:strength 3 1 true
effect @a[team=修罗] speed 3 0 true

effect @a[team=猎手] minecraft:strength 3 0 true

scoreboard players add @e[type=armor_stand,c=1,tag=称号buff延时] 延时 1

execute @e[type=armor_stand,c=1,tag=称号buff延时,score_延时_min=90,score_延时=90] ~ ~ ~ function main:系统触发/称号buff_0