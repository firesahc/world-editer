scoreboard players add @p[r=1,c=1,x=-1500,y=20,z=-3008] 红石合成 1
blockdata -1500 21 -3010 {Items:[{id:"minecraft:redstone_block",Count:64b,Damage:0s,tag:{display:{Name:"§9高品质红石块",Lore:["§6用4组红石块压缩的高品质红石块","§6是制作蚂蚁晶石的必需品"]},Tags:["高品质红石块"],HideFlags:3,ench:[{id:34,lvl:1}]},Slot:4b}]}
tellraw @a [{"text":"【地宫瓮】","color":"yellow"},{"text":"大家快看！","color":"green"},{"selector":"@p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50]","bold":false},{"text":"合成了","color":"green"},{"text":"[高品质红石块]","color":"blue"}]
scoreboard players remove @p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=50] 副本积分 50