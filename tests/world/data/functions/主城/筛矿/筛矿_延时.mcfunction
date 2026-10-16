scoreboard players add @s 筛矿延时 1

function 主城:筛矿/筛矿_加成检测

title @s times 0 20 0
title @s[score_筛矿延时=180] subtitle {"text":"矿物熔炼中","color":"gold"}
title @s[score_筛矿延时_min=1,score_筛矿延时=1] title [{"text":"□□□□□□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=20,score_筛矿延时=20] title [{"text":"■□□□□□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=40,score_筛矿延时=40] title [{"text":"■■□□□□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=60,score_筛矿延时=60] title [{"text":"■■■□□□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=80,score_筛矿延时=80] title [{"text":"■■■■□□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=100,score_筛矿延时=100] title [{"text":"■■■■■□□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=120,score_筛矿延时=120] title [{"text":"■■■■■■□□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=140,score_筛矿延时=140] title [{"text":"■■■■■■■□□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=160,score_筛矿延时=160] title [{"text":"■■■■■■■■□□","color":"yellow","bold":"true"}] 
title @s[score_筛矿延时_min=180,score_筛矿延时=180] title [{"text":"■■■■■■■■■□","color":"yellow","bold":"true"}] 
function 主城:筛矿/筛矿_延时_0 if @s[score_筛矿延时_min=200]

scoreboard players set @s[score_筛矿延时_min=200] 筛矿延时 0
