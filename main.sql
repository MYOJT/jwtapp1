-- DDL準備
-- Redshiftのクエリエディタで実行可能なDDLスクリプト
CREATE TABLE example_table (
    id INT,
    content VARCHAR(100),
    create_date VARCHAR(30)
);

-- Auroraのクエリエディタで実行可能なDDLスクリプト
CREATE TABLE temp_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(100),
    create_date TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6)
);

-- テストデータ準備(Auroraのクエリエディタで実行する）
-- ループの回数を指定
SET @i = 1;
SET @max = 10000; -- 挿入するレコードの数

-- ループ処理を実行してデータを目的のテーブルに直接挿入
WHILE @i <= @max DO
    INSERT INTO target_table (content, create_date)
    VALUES (CONCAT('Content ', @i), CURRENT_TIMESTAMP(6));
    SET @i = @i + 1;
END WHILE;
