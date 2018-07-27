<?php
/**
 * Created by PhpStorm.
 * User: xiaoy
 * Date: 7/27/2018
 * Time: 11:22 PM
 */

// Load the settings from the central config file
require_once 'config.php';
// Load the CAS lib
//require_once $phpcas_path . '/CAS.php';
require_once 'CAS.php';

// Enable debugging
phpCAS::setDebug();
// Enable verbose error messages. Disable in production!
phpCAS::setVerbose(true);

// Initialize phpCAS
phpCAS::client(CAS_VERSION_2_0, $cas_host, $cas_port, $cas_context);

// For production use set the CA certificate that is the issuer of the cert
// on the CAS server and uncomment the line below
// phpCAS::setCasServerCACert($cas_server_ca_cert_path);

// For quick testing you can disable SSL validation of the CAS server.
// THIS SETTING IS NOT RECOMMENDED FOR PRODUCTION.
// VALIDATING THE CAS SERVER IS CRUCIAL TO THE SECURITY OF THE CAS PROTOCOL!
phpCAS::setNoCasServerValidation();

// force CAS authentication
phpCAS::forceAuthentication();

require_once dirname(__FILE__) . '/include/classes/user/CWebUser.php';
CWebUser::disableSessionCookie();

require_once dirname(__FILE__) . '/include/config.inc.php';
require_once dirname(__FILE__) . '/include/forms.inc.php';

$page['title'] = _('ZABBIX');
$page['file'] = 'index.php';

// VAR	TYPE	OPTIONAL	FLAGS	VALIDATION	EXCEPTION
$fields = [
    'name' => [T_ZBX_STR, O_NO, null, null, 'isset({enter})', _('Username')],
    'password' => [T_ZBX_STR, O_OPT, null, null, 'isset({enter})'],
    'sessionid' => [T_ZBX_STR, O_OPT, null, null, null],
    'reconnect' => [T_ZBX_INT, O_OPT, P_SYS | P_ACT, BETWEEN(0, 65535), null],
    'enter' => [T_ZBX_STR, O_OPT, P_SYS, null, null],
    'autologin' => [T_ZBX_INT, O_OPT, null, null, null],
    'request' => [T_ZBX_STR, O_OPT, null, null, null]
];
check_fields($fields);

// logout
if (isset($_REQUEST['reconnect'])) {
    CWebUser::logout();
    $urlElements = parse_url($_SERVER['REQUEST_URI']);
    phpCAS::logoutWithRedirectService("http://" . $_SERVER['SERVER_NAME'] . ":" . $_SERVER['SERVER_PORT'] . $urlElements['path']);
//    redirect('index.php');
}

$config = select_config();

if ($config['authentication_type'] == ZBX_AUTH_HTTP) {
    if (!empty($_SERVER['PHP_AUTH_USER'])) {
        $_REQUEST['enter'] = _('Sign in');
        $_REQUEST['name'] = $_SERVER['PHP_AUTH_USER'];
    } else {
        access_deny(ACCESS_DENY_PAGE);
    }
}

$autoLogin = getRequest('autologin', 0);

$userName = phpCAS::getUser();
if ($userName == "admin")
    $userName = "Admin";

DBstart();
$loginSuccess = CWebUser::login($userName, "");
DBend(true);

if ($loginSuccess) {
    // save remember login preference
    if (CWebUser::$data['autologin'] != $autoLogin) {
        API::User()->update([
            'userid' => CWebUser::$data['userid'],
            'autologin' => $autoLogin
        ]);
    }

    $request = getRequest('request', '');

    if ($request) {
        preg_match('/^\/?(?<filename>[a-z0-9\_\.]+\.php)(?<request>\?.*)?$/i', $request, $test_request);

        $request = (array_key_exists('filename', $test_request) && file_exists('./' . $test_request['filename']))
            ? $test_request['filename'] . (array_key_exists('request', $test_request) ? $test_request['request'] : '')
            : '';
    }

    if (!zbx_empty($request)) {
        $url = $request;
    } elseif (!zbx_empty(CWebUser::$data['url'])) {
        $url = CWebUser::$data['url'];
    } else {
        $url = ZBX_DEFAULT_URL;
    }
} else {
    // login the user from the session, if the session id is empty - login as a guest
    CWebUser::checkAuthentication(CWebUser::getSessionCookie());
}

redirect($url);
