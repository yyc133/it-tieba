DROP TABLE mb_message;
DROP TABLE mb_user;


CREATE TABLE mb_user (
    uid int unsigned AUTO_INCREMENT,
    uname varchar(20) NOT NULL UNIQUE,
    upass char(32) NOT NULL,  -- md5加密
    phone char(11) NOT NULL, 
    email varchar(320),
    PRIMARY KEY (uid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;



CREATE TABLE mb_message (
    mid int unsigned AUTO_INCREMENT,
    uid int unsigned,
    content varchar(200) NOT NULL,
    pub_time datetime NOT NULL,
    cid int unsigned,
    from_ip char(15) NOT NULL,
    topic varchar(200) NOT NULL,
    PRIMARY KEY (mid),
    FOREIGN KEY (uid) REFERENCES mb_user (uid),
    FOREIGN KEY (cid) REFERENCES mb_message (mid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;
