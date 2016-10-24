CREATE TABLE `traffic_in` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`ip_dst` char(15) NOT NULL,
	`dst_port` int(2) NOT NULL,
	`ip_proto` char(6) NOT NULL,
	`packets` int NOT NULL,
	`bytes` bigint NOT NULL,
	`device_id` smallint NOT NULL,
	`stamp_inserted` DATETIME NOT NULL,
	`stamp_updated` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `traffic_out` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`ip_src` char(15) NOT NULL,
	`src_port` int(2) NOT NULL,
	`ip_proto` char(6) NOT NULL,
	`packets` int NOT NULL,
	`bytes` bigint NOT NULL,
	`device_id` smallint NOT NULL,
	`stamp_inserted` DATETIME NOT NULL,
	`stamp_updated` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `billing` (
	`billing_id` bigint NOT NULL,
	`rate_name` char(15) NOT NULL,
	`billable` bool NOT NULL,
	`cost_rate` FLOAT(10) NOT NULL,
	PRIMARY KEY (`billing_id`)
);

CREATE TABLE `devices` (
	`device_id` int NOT NULL AUTO_INCREMENT,
	`device_name` char(20) NOT NULL,
	`device_ip` char(15) NOT NULL,
	`billing_id` int NOT NULL,
	PRIMARY KEY (`device_id`)
);
