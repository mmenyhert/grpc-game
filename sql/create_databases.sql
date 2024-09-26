DROP DATABASE IF EXISTS `game`;

create database if not exists `game`;

USE `game`;

DROP TABLE IF EXISTS `Session`;


CREATE TABLE IF NOT EXISTS `Session` (
  `session_id` varchar(70) NOT NULL,   
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `metadata` varchar(1000),
  PRIMARY KEY  (`session_id`)
);

DROP TABLE IF EXISTS `Session_data`;


CREATE TABLE IF NOT EXISTS `Session_data` (
  `id` int NOT NULL auto_increment,
  `session_id` varchar(70) NOT NULL,
  `step` int NOT NULL,
  `data` TEXT NOT NULL, -- MAX 64KB
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (`session_id`) REFERENCES Session(`session_id`),
   PRIMARY KEY  (`id`)
);

SELECT EXISTS(SELECT 1 FROM (select session.session_id, session.date, session.metadata, counted.count, counted.latest  from `session`
inner join 
(select session_id, count(*) as count, max(`date`) as latest  from session_data group by session_id) 
as counted
on session.session_id = counted.session_id) as res ) WHERE session_id=`b0e9f2f2-125b-42ee-b7b0-32eb3cd54fb6`;


