blockdata -1500 21 -3010 {Items:[{id:"minecraft:diamond",Count:32b,Damage:0s,tag:{display:{Name:"§c§l蚂蚁晶石",Lore:["§6坚硬无比的宝石，由多种","§6材料合制而成。可用于合","§6成高级进阶装备"]},Tags:["蚂蚁晶石"],Unbreakable:1,HideFlags:1,ench:[{id:34,lvl:10}]},Slot:4b}]}
scoreboard players add @p[r=1,c=1,x=-1500,y=20,z=-3008] 晶石合成 1
tellraw @a [{"text":"【地宫瓮】","color":"yellow"},{"text":"大家快看！","color":"green"},{"selector":"@p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50]","bold":false},{"text":"合成了","color":"green"},{"text":"[蚂蚁晶石]","color":"red"}]
scoreboard players remove @p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50] 副本积分 50
