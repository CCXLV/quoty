
CREATE TABLE posts (
    id INT NOT NULL AUTO_INCREMENT,
    author TEXT,
    content TEXT,
    upload_date TIMESTAMP,
    category TEXT,
    PRIMARY KEY (id)
);
