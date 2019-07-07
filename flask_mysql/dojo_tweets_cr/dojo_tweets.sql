-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dojo_tweets
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dojo_tweets` ;

-- -----------------------------------------------------
-- Schema dojo_tweets
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dojo_tweets` DEFAULT CHARACTER SET utf8 ;
USE `dojo_tweets` ;

-- -----------------------------------------------------
-- Table `dojo_tweets`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dojo_tweets`.`users` ;

CREATE TABLE IF NOT EXISTS `dojo_tweets`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dojo_tweets`.`tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dojo_tweets`.`tweets` ;

CREATE TABLE IF NOT EXISTS `dojo_tweets`.`tweets` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tweets_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_tweets_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `dojo_tweets`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
