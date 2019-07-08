-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema basic_registration
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `basic_registration` ;

-- -----------------------------------------------------
-- Schema basic_registration
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `basic_registration` DEFAULT CHARACTER SET utf8 ;
USE `basic_registration` ;

-- -----------------------------------------------------
-- Table `basic_registration`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `basic_registration`.`user` ;

CREATE TABLE IF NOT EXISTS `basic_registration`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
