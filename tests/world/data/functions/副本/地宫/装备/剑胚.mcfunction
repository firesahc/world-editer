blockdata -1500 21 -3010 {Items:[{id:"minecraft:diamond_sword",Count:1b,Damage:0s,tag:{display:{Name:"§6基础剑胚",Lore:["§e当前属性：","§7抢夺3","§7耐久3","§7经验修补","§7火焰附加2","§7横扫之刃3","§e宝剑用途：§a可被升级淬炼","§e可升级别：§a可升级至5-16级","§e可升属性：§a锋利、亡灵、节肢","§e剑胚用法：§a将此宝剑放在主城","§a铁匠铺锻造炉的烧制格中","§a锻造炉的燃料格放淬炼石","§4警告：请勿用附魔书自行附魔"]},Tags:["FL0"],HideFlags:1,ench:[{id:21,lvl:3},{id:34,lvl:3},{id:20,lvl:2},{id:22,lvl:3},{id:70,lvl:1}]},Slot:4b}]}
tellraw @a [{"text":"【地宫瓮】","color":"yellow"},{"text":"大家快看！","color":"green"},{"selector":"@p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=5]","bold":false},{"text":"合成了","color":"green"},{"text":"基础剑胚","color":"red"}]
scoreboard players remove @p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=5] 副本积分 5
scoreboard players add @p[r=1,c=1,x=-1500,y=20,z=-3008,score_副本积分_min=5] 剑胚购买 1

