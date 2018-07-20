
-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `realname` varchar(64) NOT NULL COMMENT '姓名',
  `account` varchar(64) NOT NULL COMMENT '登陆账号名',
  `passwd` varchar(40) NOT NULL COMMENT '密码',
  `ipaddr` text,
  `group` tinyint(2) NOT NULL DEFAULT '0' COMMENT '权限分组id',
  `ctime` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `flags` tinyint(2) NOT NULL DEFAULT '0',
  `modpwd` tinyint(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for admin_group
-- ----------------------------
DROP TABLE IF EXISTS `admin_group`;
CREATE TABLE `admin_group` (
  `gid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `group` varchar(64) NOT NULL COMMENT '分组名称',
  `permission` text NOT NULL COMMENT '权限列表',
  `flags` tinyint(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app_logs
-- ----------------------------
DROP TABLE IF EXISTS `app_logs`;
CREATE TABLE `app_logs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `order_no` bigint(20) unsigned NOT NULL COMMENT '订单号',
  `trade_no` varchar(48) DEFAULT NULL COMMENT '项目订单号',
  `content` text NOT NULL,
  `type` char(20) NOT NULL COMMENT '请求类型',
  `ip` char(20) DEFAULT NULL,
  `ctime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for app_order
-- ----------------------------
DROP TABLE IF EXISTS `app_order`;
CREATE TABLE `app_order` (
  `order_no` bigint(20) unsigned NOT NULL COMMENT '订单号',
  `trade_no` varchar(48) NOT NULL DEFAULT '' COMMENT '项目订单号',
  `app_type_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '项目id： 分配给内部项目的id号',
  `app_type` tinyint(3) NOT NULL DEFAULT '0' COMMENT '支付类型: 1 微信，2 支付宝，3盛付通',
  `trade_type` varchar(20) DEFAULT '' COMMENT '交易类型：NATIVE,JSAPI,APP等',
  `subject` varchar(100) NOT NULL DEFAULT '' COMMENT '支付主题',
  `body` varchar(200) NOT NULL DEFAULT '' COMMENT '支付内容描述',
  `goods_id` char(48) NOT NULL DEFAULT '' COMMENT '商品id',
  `attach` varchar(200) DEFAULT '' COMMENT '附加数据，在通知时原样返回',
  `money` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '支付金额',
  `notify_url` varchar(255) DEFAULT '' COMMENT '异步通知接口',
  `expired_time` int(11) DEFAULT '0' COMMENT '订单过期时间：单位分钟',
  `order_status` tinyint(2) NOT NULL DEFAULT '0' COMMENT '订单状态：0 未支付，1 已支付',
  `client_ip` char(20) NOT NULL DEFAULT '' COMMENT '客户端ip',
  `order_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '订单时间',
  `paid_time` datetime DEFAULT '0000-00-00 00:00:00' COMMENT '支付时间',
  `pay_total_price` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '用户真实支付金额',
  `pay_account` varchar(100) NOT NULL DEFAULT '' COMMENT '支付账号',
  `pay_trade_no` varchar(64) NOT NULL DEFAULT '' COMMENT '第三方支付机构交易号',
  `is_notify` tinyint(1) NOT NULL DEFAULT '0' COMMENT '支付成功是否已通知商户：0 否，1 是',
  `notify_time` datetime DEFAULT NULL COMMENT '支付成功通知商户时间',
  PRIMARY KEY (`order_no`),
  UNIQUE KEY `trade_no` (`trade_no`,`app_type_id`) USING BTREE,
  KEY `order_time` (`order_time`),
  KEY `order_status` (`order_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户充值表';

-- ----------------------------
-- Table structure for app_refund_order
-- ----------------------------
DROP TABLE IF EXISTS `app_refund_order`;
CREATE TABLE `app_refund_order` (
  `refund_order_no` bigint(20) unsigned NOT NULL COMMENT '退款订单号',
  `order_no` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '原订单号',
  `money` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '原订单金额',
  `refund_price` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '退款金额',
  `notify_url` varchar(255) DEFAULT '' COMMENT '异步通知接口',
  `refund_status` tinyint(2) NOT NULL DEFAULT '0' COMMENT '订单状态：0 未支付，1 已支付',
  `client_ip` char(20) NOT NULL DEFAULT '' COMMENT '客户端ip',
  `utime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '订单时间',
  `admin_note` varchar(255) DEFAULT NULL,
  `admin_name` varchar(50) DEFAULT NULL,
  `return_refund_price` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '用户真实支付金额',
  `return_refund_account` varchar(100) NOT NULL DEFAULT '' COMMENT '支付账号',
  `return_refund_trade_no` varchar(64) NOT NULL DEFAULT '' COMMENT '第三方支付机构交易号',
  PRIMARY KEY (`refund_order_no`),
  KEY `order_status` (`refund_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户充值表';

-- ----------------------------
-- Table structure for app_type
-- ----------------------------
DROP TABLE IF EXISTS `app_type`;
CREATE TABLE `app_type` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `type` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '类型：1,微信 2，支付宝 3,盛付通',
  `name` varchar(40) NOT NULL DEFAULT '' COMMENT '项目支付名称',
  `app_id` varchar(200) NOT NULL DEFAULT '' COMMENT '微信或支付宝app_id',
  `app_secret` varchar(200) NOT NULL DEFAULT '' COMMENT '微信或支付宝app_secret，微信jsapi使用',
  `app_key` varchar(50) DEFAULT '' COMMENT '微信支付签名key',
  `mchid` varchar(50) DEFAULT NULL COMMENT '微信商户id',
  `private_key` text COMMENT '私钥',
  `public_key` text COMMENT '公钥',
  `sslcert_path` varchar(255) DEFAULT '' COMMENT 'ssl证书',
  `sslkey_path` varchar(255) DEFAULT '' COMMENT 'ssl证书',
  `sign_key` varchar(255) NOT NULL DEFAULT '' COMMENT '内部项目签名使用',
  `ctime` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='app_id、支付密钥等';

-- ----------------------------
-- Table structure for generate_order_no
-- ----------------------------
DROP TABLE IF EXISTS `generate_order_no`;
CREATE TABLE `generate_order_no` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='生成支付订单号表';
