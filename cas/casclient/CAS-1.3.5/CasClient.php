<?php

//Include 'CAS.php';
require_once dirname(__FILE__).'/CAS.php';
//请求ip
define ( 'CAS_SERVER_HOST', 'https://192.168.109.129' );
//请求端口
define ( 'CAS_SERVER_PORT', 8443 );
//请求路径
define ( 'CAS_SERVER_PATH', "/cas" );
//CAS证书路径
define ('CAS_SERVER_CA_CERT_PATH', '/local/CAS-1.3.5/zhengshu');

//include_once (dirname (_FILE_) . '/CAS.php');
// debug logfile name
phpCAS::setDebug ('./cas.log');

// initialize phpCAS
phpCAS::client ( CAS_VERSION_2_0, CAS_SERVER_HOST, CAS_SERVER_PORT, CAS_SERVER_PATH, CAS_SERVER_CA_CERT_PATH );

/**
 *no SSL validation for the CAS server
 * 关闭SSL的认证 这里不启用
 */
//phpCAS::setNoCasServerValidation ();
//phpCAS::handleLogoutRequests();

/**
 * 关闭url携带ticket参数，防止重复认证导致 ticket not recognized
 * 这里不启用
 */
//phpCAS::$_PHPCAS_CLIENT->setNoClearTicketsFromUrl ();

?>