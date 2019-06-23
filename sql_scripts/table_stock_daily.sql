CREATE TABLE `stock_daily`
(
    `id`         int(11) unsigned NOT NULL AUTO_INCREMENT,
    `ts_code`    varchar(255)     NOT NULL DEFAULT '',
    `trade_date` date             NOT NULL,
    `open`       decimal(12, 4)   NOT NULL,
    `high`       decimal(12, 4)   NOT NULL,
    `low`        decimal(12, 4)   NOT NULL,
    `close`      decimal(12, 4)   NOT NULL,
    `pre_close`  decimal(12, 4)   NOT NULL,
    `vol`        decimal(12, 4)   NOT NULL,
    `amount`     decimal(12, 4)   NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;