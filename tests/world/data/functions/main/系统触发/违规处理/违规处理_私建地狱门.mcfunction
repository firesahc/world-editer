fill ~ ~-1 ~ ~5 ~5 ~5 air 0 replace portal
tellraw @a [{"text":"【警告】","color":"dark_red","bold":true},{"selector":"@s"},{"text":"因在岛屿违规[激活/进入]地狱门被关牢狱！！！","color":"dark_red"}]
scoreboard players add @s 牢狱 500