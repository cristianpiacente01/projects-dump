-- -----------------------------------------------------
-- Schema officina
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema officina
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `officina` DEFAULT CHARACTER SET utf8 ;
USE `officina` ;

-- -----------------------------------------------------
-- Table `officina`.`Stabilimento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `officina`.`Stabilimento` (
  `id_stabilimento` BIGINT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id_stabilimento`))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `officina`.`Stanza`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `officina`.`Stanza` (
  `id_stanza` BIGINT NOT NULL AUTO_INCREMENT,
  `id_stabilimento` BIGINT NOT NULL,
  `nome` VARCHAR(30) NOT NULL,
  `capienza_persone` INT NOT NULL,
  `piano` INT NOT NULL,
  PRIMARY KEY (`id_stanza`),
  CONSTRAINT `fk_Stanza_Stabilimento1`
    FOREIGN KEY (`id_stabilimento`)
    REFERENCES `officina`.`Stabilimento` (`id_stabilimento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `officina`.`Dipendente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `officina`.`Dipendente` (
  `id_dipendente` BIGINT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(30) NOT NULL,
  `cognome` VARCHAR(30) NOT NULL,
  `mansione` VARCHAR(30) NOT NULL,
  `supervisore` BIGINT NULL,
  PRIMARY KEY (`id_dipendente`),
  CONSTRAINT `fk_Dipendente_Dipendente1`
    FOREIGN KEY (`supervisore`)
    REFERENCES `officina`.`Dipendente` (`id_dipendente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `officina`.`Attrezzo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `officina`.`Attrezzo` (
  `id_attrezzo` BIGINT NOT NULL AUTO_INCREMENT,
  `modello` VARCHAR(30) NOT NULL,
  `marca` VARCHAR(30) NOT NULL,
  `id_stanza` BIGINT NOT NULL,
  `tipo` CHAR(1) NOT NULL,
  `potenza_watt` INT NOT NULL,
  `tipo_di_punta` VARCHAR(30) NULL,
  `catena_di_taglio` VARCHAR(30) NULL,
  PRIMARY KEY (`id_attrezzo`),
  CONSTRAINT `fk_Attrezzo_Stanza1`
    FOREIGN KEY (`id_stanza`)
    REFERENCES `officina`.`Stanza` (`id_stanza`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `officina`.`HaAccesso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `officina`.`HaAccesso` (
  `id_dipendente` BIGINT NOT NULL,
  `id_stanza` BIGINT NOT NULL,
  PRIMARY KEY (`id_dipendente`, `id_stanza`),
  CONSTRAINT `fk_Dipendente_has_Stanza_Dipendente1`
    FOREIGN KEY (`id_dipendente`)
    REFERENCES `officina`.`Dipendente` (`id_dipendente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Dipendente_has_Stanza_Stanza1`
    FOREIGN KEY (`id_stanza`)
    REFERENCES `officina`.`Stanza` (`id_stanza`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM;