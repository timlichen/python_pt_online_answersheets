-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dojo_survey_validations
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dojo_survey_validations` ;

-- -----------------------------------------------------
-- Schema dojo_survey_validations
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dojo_survey_validations` DEFAULT CHARACTER SET utf8 ;
USE `dojo_survey_validations` ;

-- -----------------------------------------------------
-- Table `dojo_survey_validations`.`dojo_languages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dojo_survey_validations`.`dojo_languages` ;

CREATE TABLE IF NOT EXISTS `dojo_survey_validations`.`dojo_languages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `language` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dojo_survey_validations`.`dojo_locations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dojo_survey_validations`.`dojo_locations` ;

CREATE TABLE IF NOT EXISTS `dojo_survey_validations`.`dojo_locations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `location` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dojo_survey_validations`.`dojo_survey`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dojo_survey_validations`.`dojo_survey` ;

CREATE TABLE IF NOT EXISTS `dojo_survey_validations`.`dojo_survey` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `comment` VARCHAR(120) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `dojo_languages_id` INT NOT NULL,
  `dojo_locations_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_dojo_survey_languages_idx` (`dojo_languages_id` ASC) VISIBLE,
  INDEX `fk_dojo_survey_dojo_locations1_idx` (`dojo_locations_id` ASC) VISIBLE,
  CONSTRAINT `fk_dojo_survey_languages`
    FOREIGN KEY (`dojo_languages_id`)
    REFERENCES `dojo_survey_validations`.`dojo_languages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dojo_survey_dojo_locations1`
    FOREIGN KEY (`dojo_locations_id`)
    REFERENCES `dojo_survey_validations`.`dojo_locations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
