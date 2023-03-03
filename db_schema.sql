
-- Create User table
CREATE TABLE User_ (
    user_id SERIAL       NOT NULL,
    first_name    VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    university VARCHAR(255) NOT NULL,
	account_created TIMESTAMP NOT NULL,
	admin_ BOOLEAN NOT NULL,
    authenticated BOOLEAN NOT NULL,
    avatar_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
	UNIQUE (username),
	UNIQUE (email)
);



-- Create Post table
CREATE TABLE  Post (
    post_id SERIAL       NOT NULL,
    user_id    INT          NOT NULL,
    post_title VARCHAR(255) NOT NULL,
    post_text VARCHAR(255) NOT NULL,
    post_datetime TIMESTAMP NOT NULL,
    university VARCHAR(255) NOT NULL,

    number_likes   INT          NOT NULL,
    number_reposts   INT          NOT NULL,
    number_comments   INT          NOT NULL,

    PRIMARY KEY (post_id),
	
    FOREIGN KEY (user_id)
        REFERENCES User_(user_id)
);


-- Create Comment table
CREATE TABLE Comment (

    comment_id SERIAL       NOT NULL,
    user_id    INT          NOT NULL,
    post_id    INT          NOT NULL,
    comment_text VARCHAR(255) NOT NULL,
    comment_datetime TIMESTAMP NOT NULL,
    parent_comment_id INT     NULL,
    PRIMARY KEY (comment_id),

    FOREIGN KEY (user_id)
        REFERENCES User_(user_id),

    FOREIGN KEY (post_id)
        REFERENCES Post(post_id)
);


-- Create Like table
CREATE TABLE LIKE_ (
    
    like_id SERIAL       NOT NULL,
    user_id    INT          NOT NULL,
    post_id    INT          NOT NULL,
    PRIMARY KEY (like_id),

    FOREIGN KEY (user_id)
        REFERENCES User_(user_id),

    FOREIGN KEY (post_id)
        REFERENCES Post(post_id)
);

-- Create Uni table
CREATE TABLE UNI (
    
    university_id SERIAL       NOT NULL,
    acronym    VARCHAR(255) NOT NULL,
    uni_name    VARCHAR(255) NOT NULL
);



-- Create Repost table
CREATE TABLE Repost (
    
    repost_id SERIAL       NOT NULL,
    reposter_user_id    INT          NOT NULL,
    poster_user_id    INT          NOT NULL,
    post_id    INT          NOT NULL,
    PRIMARY KEY (repost_id),

    FOREIGN KEY (reposter_user_id)
        REFERENCES User_(user_id),

    FOREIGN KEY (post_id)
        REFERENCES Post(post_id),

    FOREIGN KEY (poster_user_id)
        REFERENCES User_(user_id)
);



Insert into UNI(acronym, uni_name)
Values('UNCC', 'University of North Carolina at Charlotte');
Insert into UNI(acronym, uni_name)
Values('UNC', 'University of North Carolina at Chapel Hill');
Insert into UNI(acronym, uni_name)
Values('NCSU', 'North Carolina State University');