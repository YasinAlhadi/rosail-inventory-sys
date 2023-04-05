-- prepare database for project

CREATE DATABASE IF NOT EXISTS rms_db;
CREATE USER IF NOT EXISTS 'rms_admin'@'localhost' IDENTIFIED BY 'rms1516';
GRANT ALL PRIVILEGES ON rms_db.* TO 'rms_admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'rms_admin'@'localhost';
FLUSH PRIVILEGES;
