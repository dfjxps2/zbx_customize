<?php
/*
** Zabbix
** Copyright (C) 2001-2018 Zabbix SIA
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
**/


require_once dirname(__FILE__).'/include/classes/user/CWebUser.php';
CWebUser::disableSessionCookie();

require_once dirname(__FILE__).'/include/config.inc.php';
require_once dirname(__FILE__).'/include/forms.inc.php';

// Load the settings from the central config file
require_once './config.php';
// Load the CAS lib
require_once './casclient/CAS-1.3.5/CAS.php';

// Enable debugging
phpCAS::setDebug();
// Enable verbose error messages. Disable in production!
phpCAS::setVerbose(true);

// Initialize phpCAS
phpCAS::client(CAS_VERSION_2_0, $cas_host, $cas_port, $cas_context);

// For production use set the CA certificate that is the issuer of the cert
// on the CAS server and uncomment the line below
phpCAS::setCasServerCACert($cas_server_ca_cert_path);

// For quick testing you can disable SSL validation of the CAS server.
// THIS SETTING IS NOT RECOMMENDED FOR PRODUCTION.
// VALIDATING THE CAS SERVER IS CRUCIAL TO THE SECURITY OF THE CAS PROTOCOL!
//phpCAS::setNoCasServerValidation();

// force CAS authentication
phpCAS::forceAuthentication();

// at this step, the user has been authenticated by the CAS server
// and the user's login name can be read with phpCAS::getUser().

// logout if desired
if (isset($_REQUEST['reconnect'])) {
    phpCAS::logout();
    phpCAS::handleLogoutRequests();
}

//----------------------------------------------------------------------------------------------------------------
$page['title'] = _('ZABBIX');
$page['file'] = 'index.php';

// VAR	TYPE	OPTIONAL	FLAGS	VALIDATION	EXCEPTION
$fields = [
	'name' =>		[T_ZBX_STR, O_NO,	null,	null,		'isset({enter})', _('Username')],
	'password' =>	[T_ZBX_STR, O_OPT, null,	null,			'isset({enter})'],
	'sessionid' =>	[T_ZBX_STR, O_OPT, null,	null,			null],
	'reconnect' =>	[T_ZBX_INT, O_OPT, P_SYS|P_ACT,	BETWEEN(0, 65535), null],
	'enter' =>		[T_ZBX_STR, O_OPT, P_SYS,	null,			null],
	'autologin' =>	[T_ZBX_INT, O_OPT, null,	null,			null],
	'request' =>	[T_ZBX_STR, O_OPT, null,	null,			null]
];
check_fields($fields);

// logout
/*if (isset($_REQUEST['reconnect'])) {
	CWebUser::logout();
	redirect('index.php');
}*/

$config = select_config();

if ($config['authentication_type'] == ZBX_AUTH_HTTP) {
	if (!empty($_SERVER['PHP_AUTH_USER'])) {
		$_REQUEST['enter'] = _('Sign in');
		$_REQUEST['name'] = $_SERVER['PHP_AUTH_USER'];
	}
	else {
		access_deny(ACCESS_DENY_PAGE);
	}
}

$local_url = $_SERVER['QUERY_STRING'];
// login via form
if (isset($_REQUEST['enter']) && $_REQUEST['enter'] == _('Sign in')) {
	// try to login
	$autoLogin = getRequest('autologin', 0);

	DBstart();
	$loginSuccess = CWebUser::login(getRequest('name', ''), getRequest('password', ''));
	DBend(true);

	if ($loginSuccess) {
		// save remember login preference
		if (CWebUser::$data['autologin'] != $。autoLogin) {
			API::User()->update([
				'userid' => CWebUser::$data['userid'],
				'autologin' => $autoLogin
			]);
		}

		$request = getRequest('request', '');

		if ($request) {
			preg_match('/^\/?(?<filename>[a-z0-9\_\.]+\.php)(?<request>\?.*)?$/i', $request, $test_request);

			$request = (array_key_exists('filename', $test_request) && file_exists('./'.$test_request['filename']))
				? $test_request['filename'].(array_key_exists('request', $test_request) ? $test_request['request'] : '')
				: '';
		}

		if (!zbx_empty($request)) {
			$url = $request;
		}
		elseif (!zbx_empty(CWebUser::$data['url'])) {
			$url = CWebUser::$data['url'];
		}
		else {
			$url = ZBX_DEFAULT_URL;
		}
		redirect($url);
		exit;
	}
	// login failed, fall back to a guest account
	else {

        CWebUser::checkAuthentication(null);
    }
}
else {
    //--------------------------------------------一以下为修改处----------------------------------------------------------

    // try to login
    //$autoLogin = getRequest('autologin', 0);
    phpCAS::setNoCasServerValidation();
    DBstart();
    $loginSuccess = CWebUser::login(Admin,zabbix);
    DBend(true);

    if ($loginSuccess) {
        // save remember login preference
        if (CWebUser::$data['autologin'] != $autoLogin) {
            API::User()->update([
                'userid' => CWebUser::$data['userid'],
                'autologin' => $autoLogin
            ]);
        }

        $request = Admin;

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
        redirect($url);
        exit;
    }
    //
    if($local_url){
        $session_id = explode('=', $local_url)[1];
        CWebUser::setSessionCookie($session_id);         # 将sessionid写在url里，然后从url中获取sessionid，然后再把sessionid写进去
        $url = "zabbix.php?action=dashboard.view";
        header("http:192.168.109.128:$url");                         # 302跳转
        exit;
    }
//    ------------------------------------------以上为修改处-----------------------------------------------------------
	// login the user from the session, if the session id is empty - login as a guest
	CWebUser::checkAuthentication(CWebUser::getSessionCookie());
/*}

// the user is not logged in, display the login form
if (!CWebUser::$data['alias'] || CWebUser::$data['alias'] == ZBX_GUEST_USER) {
	switch ($config['authentication_type']) {
		case ZBX_AUTH_HTTP:
			echo _('User name does not match with DB');
			break;
		case ZBX_AUTH_LDAP:
		case ZBX_AUTH_INTERNAL:
			if (isset($_REQUEST['enter'])) {
				$_REQUEST['autologin'] = getRequest('autologin', 0);
			}

			if ($messages = clear_messages()) {
				$messages = array_pop($messages);
				$_REQUEST['message'] = $messages['message'];
			}
			$loginForm = new CView('general.login');
			$loginForm->render();
	}
}
else {*/
	redirect(zbx_empty(CWebUser::$data['url']) ? ZBX_DEFAULT_URL : CWebUser::$data['url']);
}
