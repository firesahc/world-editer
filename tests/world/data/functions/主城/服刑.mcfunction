tp @a[x=-1944,y=67,z=-2018,rm=5,score_牢狱_min=1] -1944 67 -2018
execute @a[score_牢狱_min=1] ~ ~ ~ title @a[r=1,c=1] title [{"score":{"name":"@a[score_牢狱_min=1,c=1]","objective":"牢狱"},"color":"gold"},{"text":"秒后释放 再违规立刻BAN","color":"red"}]
scoreboard players remove @a[score_牢狱_min=1] 牢狱 1