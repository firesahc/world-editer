scoreboard players set @a[rx=-50,rxm=-90,score_id缓存=0] 飞行控制 1 {OnGround:0b,Inventory:[{tag:{Tags:["飞行魔棒"]},Slot:-106b}]}
scoreboard players set @a[rx=49,rxm=-49,score_id缓存=0] 飞行控制 2 {OnGround:0b,Inventory:[{tag:{Tags:["飞行魔棒"]},Slot:-106b}]}
scoreboard players set @a[rx=90,rxm=50,score_id缓存=0] 飞行控制 3 {OnGround:0b,Inventory:[{tag:{Tags:["飞行魔棒"]},Slot:-106b}]}
scoreboard players set @a[score_id缓存=0] 飞行控制 4 {OnGround:0b,SelectedItem:{tag:{Tags:["飞行魔棒"]}}}

execute @a[score_飞行控制_min=1,score_飞行控制=4] ~ ~ ~ function 玩家:行动/使用物品/岛屿飞行_0