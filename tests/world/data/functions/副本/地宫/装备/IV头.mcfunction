blockdata -1500 21 -3010 {Items:[{id:"minecraft:diamond_helmet",Count:1b,Damage:0s,tag:{Unbreakable:1,Tags:["1"],ench:[{id:0,lvl:4}]},Slot:4b}]}
tellraw @a [{"text":"【地宫瓮】","color":"yellow"},{"text":"大家快看！","color":"green"},{"selector":"@p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50]","bold":false},{"text":"合成了","color":"green"},{"text":"特制头盔","color":"red"}]
scoreboard players remove @p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50] 副本积分 50
scoreboard players add @p[r=1,c=1,x=-1500,y=20,z=-3008] 特制头合成 1