<?php

/**
 * This is an example of how a local.php could look like.
 * Simply copy the options you want to change from dokuwiki.php
 * to this file and change them.
 *
 * When using the installer, a correct local.php file be generated for
 * you automatically.
 */


$conf['title']       = 'HGV Support';        //what to show in the title

$conf['useacl']      = 1;                //Use Access Control Lists to restrict access?
$conf['superuser']   = '@administrator';
$conf['authtype'] = 'authldap';
$conf['plugin']['authldap']['server']      = 'ldap://ldap-db:1389'; #instead of the above two settings
$conf['plugin']['authldap']['usertree']    = 'ou=users, dc=hgvsupport, dc=ddns, dc=net';
$conf['plugin']['authldap']['grouptree']   = 'ou=roles, dc=hgvsupport, dc=ddns, dc=net';
$conf['plugin']['authldap']['userfilter']  = '(&(uid=%{user})(objectClass=posixAccount))';
$conf['plugin']['authldap']['groupfilter'] = '(&(objectClass=posixGroup)(memberUID=%{user}))';
$conf['plugin']['authldap']['attributes']  = array('cn', 'displayname', 'mail', 'givenname', 'objectclass', 'sn', 'uid', 'memberof');
$conf['plugin']['authldap']['version'] = 3;
$conf['savedir'] = '/app/dokuwiki/data';