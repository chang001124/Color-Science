1. 使用numpy計算平均值和標準差
2. 使用open cv 讀取特徵值


程式流程:
        讀取bctresult內的sou 和tar圖片，分別取出他們的RGB，再將各個RGB用 dt/ds [S(x.y)-ms]+mt 的式子做轉換，判斷是否有overflow與underflow的情況並解決，最後merge起來存成新的圖片