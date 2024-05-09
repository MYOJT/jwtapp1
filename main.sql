-- ループの回数を指定
SET @i = 1;
SET @max = 10000; -- 挿入するレコードの数

-- ループ処理を実行してデータを目的のテーブルに直接挿入
WHILE @i <= @max DO
    INSERT INTO target_table (content, create_date)
    VALUES (CONCAT('Content ', @i), CURRENT_TIMESTAMP(6));
    SET @i = @i + 1;
END WHILE;

