function main:玩家触发/传送术/传送术_请求检测_发起点击 if @s[score_请求编号=-1,score_book_min=10,score_book=10]

function main:玩家触发/传送术/传送术_请求检测_反复点击 if @s[score_请求编号_min=1,score_book_min=10,score_book=10]

function main:玩家触发/传送术/传送术_请求检测_金币不足 if @s[score_金钱=9,score_book_min=10,score_book=10]

function main:玩家触发/传送术/传送术_请求检测_请求成功 if @s[score_金钱_min=10,score_book_min=10,score_book=10]