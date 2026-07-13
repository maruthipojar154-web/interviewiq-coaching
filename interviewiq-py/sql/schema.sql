-- ============================================================
-- InterviewIQ Database Schema (MySQL)
-- Run this once to create the database and all tables.
-- ============================================================

CREATE DATABASE IF NOT EXISTS interviewiq
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE interviewiq;

-- ---------------------------------------------------------------
-- Users table — stores login credentials & verification state
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(150) NOT NULL,
  email           VARCHAR(190) NOT NULL UNIQUE,
  password_hash   VARCHAR(255) NOT NULL,
  is_verified     TINYINT(1) NOT NULL DEFAULT 0,
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------
-- OTP codes — used for both email verification & password reset
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS otp_codes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  email       VARCHAR(190) NOT NULL,
  code_hash   VARCHAR(255) NOT NULL,
  purpose     ENUM('register','reset') NOT NULL,
  expires_at  DATETIME NOT NULL,
  used        TINYINT(1) NOT NULL DEFAULT 0,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email_purpose (email, purpose)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------
-- Profiles — one-to-one with users
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profiles (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT NOT NULL UNIQUE,
  role          VARCHAR(150) DEFAULT '',
  phone         VARCHAR(30)  DEFAULT '',
  location      VARCHAR(150) DEFAULT '',
  linkedin      VARCHAR(255) DEFAULT '',
  github        VARCHAR(255) DEFAULT '',
  summary       TEXT,
  photo_path    VARCHAR(255) DEFAULT NULL,
  resume_text   MEDIUMTEXT,
  resume_path   VARCHAR(255) DEFAULT NULL,
  skills        JSON,
  updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------
-- Projects — many-to-one with users
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  name         VARCHAR(255) DEFAULT '',
  stack        VARCHAR(255) DEFAULT '',
  description  TEXT,
  highlights   TEXT,
  photo_path   VARCHAR(255) DEFAULT NULL,
  sort_order   INT DEFAULT 0,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------
-- Interview sessions — analytics history
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  avg_score    INT NOT NULL,
  total_qs     INT NOT NULL,
  categories   JSON,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;


mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| cake_house         |
| cake_mane          |
| cake_mng           |
| cakemng            |
| information_schema |
| interviewiq        |
| maruthi_cafe       |
| maruthi_cake_house |
| maruthicakehouse   |
| mysql              |
| performance_schema |
| sakila             |
| sys                |
| world              |
+--------------------+
14 rows in set (0.06 sec)

mysql> use interviewiq;
Database changed
mysql> CREATE TABLE IF NOT EXISTS users (
    ->   id            INT AUTO_INCREMENT PRIMARY KEY,
    ->   name          VARCHAR(150) NOT NULL,
    ->   email         VARCHAR(190) NOT NULL UNIQUE,
    ->   password_hash VARCHAR(255) NOT NULL,
    ->   is_verified   TINYINT(1) NOT NULL DEFAULT 0,
    ->   created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   updated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected, 1 warning (0.07 sec)

mysql> CREATE TABLE IF NOT EXISTS otp_codes (
    ->   id         INT AUTO_INCREMENT PRIMARY KEY,
    ->   email      VARCHAR(190) NOT NULL,
    ->   code_hash  VARCHAR(255) NOT NULL,
    ->   purpose    ENUM('register','reset') NOT NULL,
    ->   expires_at DATETIME NOT NULL,
    ->   used       TINYINT(1) NOT NULL DEFAULT 0,
    ->   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   INDEX idx_email_purpose (email, purpose)
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> CREATE TABLE IF NOT EXISTS profiles (
    ->   id          INT AUTO_INCREMENT PRIMARY KEY,
    ->   user_id     INT NOT NULL UNIQUE,
    ->   role        VARCHAR(150) DEFAULT '',
    ->   phone       VARCHAR(30)  DEFAULT '',
    ->   location    VARCHAR(150) DEFAULT '',
    ->   linkedin    VARCHAR(255) DEFAULT '',
    ->   github      VARCHAR(255) DEFAULT '',
    ->   summary     TEXT,
    ->   photo_path  VARCHAR(255) DEFAULT NULL,
    ->   resume_text MEDIUMTEXT,
    ->   resume_path VARCHAR(255) DEFAULT NULL,
    ->   skills      JSON,
    ->   updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ->   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.05 sec)

mysql> CREATE TABLE IF NOT EXISTS projects (
    ->   id          INT AUTO_INCREMENT PRIMARY KEY,
    ->   user_id     INT NOT NULL,
    ->   name        VARCHAR(255) DEFAULT '',
    ->   stack       VARCHAR(255) DEFAULT '',
    ->   description TEXT,
    ->   highlights  TEXT,
    ->   photo_path  VARCHAR(255) DEFAULT NULL,
    ->   sort_order  INT DEFAULT 0,
    ->   created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.05 sec)

mysql> CREATE TABLE IF NOT EXISTS sessions (
    ->   id         INT AUTO_INCREMENT PRIMARY KEY,
    ->   user_id    INT NOT NULL,
    ->   avg_score  INT NOT NULL,
    ->   total_qs   INT NOT NULL,
    ->   categories JSON,
    ->   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.04 sec)

mysql> show tables;
+-----------------------+
| Tables_in_interviewiq |
+-----------------------+
| otp_codes             |
| profiles              |
| projects              |
| sessions              |
| users                 |
+-----------------------+
5 rows in set (0.00 sec)

mysql> describe otp_codes;
+------------+--------------------------+------+-----+-------------------+-------------------+
| Field      | Type                     | Null | Key | Default           | Extra             |
+------------+--------------------------+------+-----+-------------------+-------------------+
| id         | int                      | NO   | PRI | NULL              | auto_increment    |
| email      | varchar(190)             | NO   | MUL | NULL              |                   |
| code_hash  | varchar(255)             | NO   |     | NULL              |                   |
| purpose    | enum('register','reset') | NO   |     | NULL              |                   |
| expires_at | datetime                 | NO   |     | NULL              |                   |
| used       | tinyint(1)               | NO   |     | 0                 |                   |
| created_at | datetime                 | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+--------------------------+------+-----+-------------------+-------------------+
7 rows in set (0.06 sec)

mysql> describe profiles;
+-------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field       | Type         | Null | Key | Default           | Extra                                         |
+-------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id          | int          | NO   | PRI | NULL              | auto_increment                                |
| user_id     | int          | NO   | UNI | NULL              |                                               |
| role        | varchar(150) | YES  |     |                   |                                               |
| phone       | varchar(30)  | YES  |     |                   |                                               |
| location    | varchar(150) | YES  |     |                   |                                               |
| linkedin    | varchar(255) | YES  |     |                   |                                               |
| github      | varchar(255) | YES  |     |                   |                                               |
| summary     | text         | YES  |     | NULL              |                                               |
| photo_path  | varchar(255) | YES  |     | NULL              |                                               |
| resume_text | mediumtext   | YES  |     | NULL              |                                               |
| resume_path | varchar(255) | YES  |     | NULL              |                                               |
| skills      | json         | YES  |     | NULL              |                                               |
| updated_at  | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+-------------+--------------+------+-----+-------------------+-----------------------------------------------+
13 rows in set (0.00 sec)

mysql> describe projects;
+-------------+--------------+------+-----+-------------------+-------------------+
| Field       | Type         | Null | Key | Default           | Extra             |
+-------------+--------------+------+-----+-------------------+-------------------+
| id          | int          | NO   | PRI | NULL              | auto_increment    |
| user_id     | int          | NO   | MUL | NULL              |                   |
| name        | varchar(255) | YES  |     |                   |                   |
| stack       | varchar(255) | YES  |     |                   |                   |
| description | text         | YES  |     | NULL              |                   |
| highlights  | text         | YES  |     | NULL              |                   |
| photo_path  | varchar(255) | YES  |     | NULL              |                   |
| sort_order  | int          | YES  |     | 0                 |                   |
| created_at  | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+-------------+--------------+------+-----+-------------------+-------------------+
9 rows in set (0.00 sec)

mysql> describe sessions;
+------------+----------+------+-----+-------------------+-------------------+
| Field      | Type     | Null | Key | Default           | Extra             |
+------------+----------+------+-----+-------------------+-------------------+
| id         | int      | NO   | PRI | NULL              | auto_increment    |
| user_id    | int      | NO   | MUL | NULL              |                   |
| avg_score  | int      | NO   |     | NULL              |                   |
| total_qs   | int      | NO   |     | NULL              |                   |
| categories | json     | YES  |     | NULL              |                   |
| created_at | datetime | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+----------+------+-----+-------------------+-------------------+
6 rows in set (0.00 sec)

mysql> describe users;
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field         | Type         | Null | Key | Default           | Extra                                         |
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id            | int          | NO   | PRI | NULL              | auto_increment                                |
| name          | varchar(150) | NO   |     | NULL              |                                               |
| email         | varchar(190) | NO   | UNI | NULL              |                                               |
| password_hash | varchar(255) | NO   |     | NULL              |                                               |
| is_verified   | tinyint(1)   | NO   |     | 0                 |                                               |
| created_at    | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at    | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+---------------+--------------+------+-----+-------------------+-----------------------------------------------+
7 rows in set (0.00 sec)


















-- ---------------------------------------------------------------
-- Chat history — stores every conversation message per user
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS chat_messages (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  user_id    INT NOT NULL,
  session_id VARCHAR(36) NOT NULL,
  role       ENUM('user','assistant') NOT NULL,
  content    TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_session (user_id, session_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------
-- Chat sessions — groups messages into named conversations
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS chat_sessions (
  id         VARCHAR(36) PRIMARY KEY,
  user_id    INT NOT NULL,
  title      VARCHAR(255) DEFAULT 'New Chat',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user (user_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;
 use interviewiq;
Database changed
mysql> CREATE TABLE IF NOT EXISTS chat_sessions (
    ->   id         VARCHAR(36) PRIMARY KEY,
    ->   user_id    INT NOT NULL,
    ->   title      VARCHAR(255) DEFAULT 'New Chat',
    ->   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ->   INDEX idx_user (user_id),
    ->   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.12 sec)

mysql> CREATE TABLE IF NOT EXISTS chat_messages (
    ->   id         INT AUTO_INCREMENT PRIMARY KEY,
    ->   user_id    INT NOT NULL,
    ->   session_id VARCHAR(36) NOT NULL,
    ->   role       ENUM('user','assistant') NOT NULL,
    ->   content    TEXT NOT NULL,
    ->   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ->   INDEX idx_user_session (user_id, session_id),
    ->   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -> ) ENGINE=InnoDB;
Query OK, 0 rows affected (0.07 sec)

mysql> show tables;
+-----------------------+
| Tables_in_interviewiq |
+-----------------------+
| chat_messages         |
| chat_sessions         |
| otp_codes             |
| profiles              |
| projects              |
| sessions              |
| users                 |
+-----------------------+
7 rows in set (0.00 sec)

mysql> describe chat_messages;
+------------+--------------------------+------+-----+-------------------+-------------------+
| Field      | Type                     | Null | Key | Default           | Extra             |
+------------+--------------------------+------+-----+-------------------+-------------------+
| id         | int                      | NO   | PRI | NULL              | auto_increment    |
| user_id    | int                      | NO   | MUL | NULL              |                   |
| session_id | varchar(36)              | NO   |     | NULL              |                   |
| role       | enum('user','assistant') | NO   |     | NULL              |                   |
| content    | text                     | NO   |     | NULL              |                   |
| created_at | datetime                 | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+--------------------------+------+-----+-------------------+-------------------+
6 rows in set (0.03 sec)

mysql> describe chat_sessions;
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field      | Type         | Null | Key | Default           | Extra                                         |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id         | varchar(36)  | NO   | PRI | NULL              |                                               |
| user_id    | int          | NO   | MUL | NULL              |                                               |
| title      | varchar(255) | YES  |     | New Chat          |                                               |
| created_at | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
5 rows in set (0.00 sec)

mysql>