CREATE TABLE mb_reply (
    rid int unsigned AUTO_INCREMENT,
    uid int unsigned,
    mid int unsigned,
    reply varchar(300) NOT NULL,
    r_pub_time datetime NOT NULL,
    PRIMARY KEY (rid),
    FOREIGN KEY (uid) REFERENCES mb_user (uid),
    FOREIGN KEY (mid) REFERENCES mb_message (mid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;