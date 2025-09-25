CREATE TABLE GUESTBOOK (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    message TEXT
);

SELECT * FROM GUESTBOOK;
INSERT INTO GUESTBOOK (username, message) VALUES ('theo', 'hello world');