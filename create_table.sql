DROP TABLE IF EXISTS covid;

CREATE TABLE covid (
	news_source VARCHAR(50) NOT NULL,
	news_title TEXT NOT NULL UNIQUE,
	news_content TEXT NOT NULL,
	publish_time TIMESTAMP,
	image_source TEXT
);

