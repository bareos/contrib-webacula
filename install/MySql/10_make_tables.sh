#!/bin/bash
#
# Script to create webacula tables
#

db_user=${db_user:-`/usr/sbin/webacula-config get_db_user`}
db_password=${db_password:-`/usr/sbin/webacula-config get_db_password`}

CMD="${CMD:-`/usr/sbin/webacula-config get_sql_cmd`}"

eval $CMD <<END-OF-DATA

-- set password
UPDATE mysql.user SET Password=PASSWORD('$db_password') WHERE User='$db_user';
flush privileges;

CREATE TABLE IF NOT EXISTS webacula_logbook (
	logId		INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	logDateCreate	DATETIME NOT NULL,
	logDateLast	DATETIME,
	logTxt		TEXT NOT NULL,
	logTypeId	INTEGER UNSIGNED NOT NULL,
	logIsDel	INTEGER,

	PRIMARY KEY(logId),
	INDEX (logDateCreate)
) ENGINE=MyISAM;

CREATE INDEX wbidx1 ON webacula_logbook(logDateCreate);
CREATE FULLTEXT INDEX idxTxt ON webacula_logbook(logTxt);


DROP TABLE IF EXISTS webacula_logtype;
CREATE TABLE webacula_logtype (
	typeId	INTEGER UNSIGNED NOT NULL,
	typeDesc TINYBLOB NOT NULL,

	PRIMARY KEY(typeId)
);

INSERT INTO webacula_logtype (typeId,typeDesc) VALUES
	(10, 'Info'),
	(20, 'OK'),
	(30, 'Warning'),
	(255, 'Error')
;


/* Job descriptions */
CREATE TABLE IF NOT EXISTS webacula_jobdesc (
    desc_id  INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    name_job    CHAR(64) UNIQUE NOT NULL,
    retention_period CHAR(32),
    short_desc      VARCHAR(128) NOT NULL,
    description     TEXT NOT NULL,
    PRIMARY KEY(desc_id),
    INDEX (name_job),
    INDEX (short_desc)
);


/* list if tables to restore files */
CREATE TABLE IF NOT EXISTS webacula_tmp_tablelist (
    tmpId    INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    tmpName  CHAR(64) UNIQUE NOT NULL,
    tmpJobIdHash CHAR(64) NOT NULL,
    tmpCreate   TIMESTAMP NOT NULL,
    tmpIsCloneOk INTEGER DEFAULT 0,
    PRIMARY KEY(tmpId)
);


DROP TABLE IF EXISTS webacula_version;
CREATE TABLE webacula_version (
   versionId INTEGER UNSIGNED NOT NULL
);

INSERT INTO webacula_version (versionId) VALUES (5);

END-OF-DATA

res=$?
if test $res = 0; then
   echo "Creation of webacula MySQL tables succeeded."
else
   echo "Creation of webacula MySQL tables failed."
fi
exit $res
