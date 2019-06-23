CREATE TABLE `fund_index`
(
    `id`         int(11) unsigned NOT NULL AUTO_INCREMENT,
    `index_code` varchar(255)     NOT NULL DEFAULT '',
    `con_code`   varchar(255)     NOT NULL DEFAULT '',
    `trade_date` date             NOT NULL,
    `weight`     decimal(12, 4)   NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;