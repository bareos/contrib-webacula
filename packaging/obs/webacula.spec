
Name:          webacula
Provides:      bareos-webacula
Provides:      bareos-console-web
Version:       5.5.2
Release:       0%{?dist}
Summary:       Web interface of a Bareos/Bacula backup system

Group:      Productivity/Archiving/Backup
License:    GPL-3.0+
URL:        http://webacula.sourceforge.net/
Source:     %{name}_%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-build
BuildArch:  noarch

BuildRequires: sudo

Requires: bareos-bconsole bareos-common
Requires: php >= 5.2.4
Requires: php-ZendFramework >= 1.8.3
Requires: php-ZendFramework-captcha
Requires: php-pdo
Requires: php-json
Requires: php-pcre
Requires: php-gd
Requires: php-xml
Requires: sudo

%if 0%{?suse_version}
BuildRequires: apache2
# /usr/sbin/apxs2
#BuildRequires: apache2-devel
#define _apache_conf_dir #(/usr/sbin/apxs2 -q SYSCONFDIR)
%define _apache_conf_dir /etc/apache2/conf.d/
%define daemon_user  wwwrun
%define daemon_group www
Requires:   apache
Requires:   cron
Requires:   mod_php_any
Recommends: php-pgsql php-mysql php-sqlite
Suggests:   postgresql-server mysql sqlite3
%else
#if 0#{?fedora} || 0#{?rhel_version} || 0#{?centos_version}
BuildRequires: httpd
%define _apache_conf_dir /etc/httpd/conf.d/
%define daemon_user  apache
%define daemon_group apache
Requires:   cronie
Requires:   httpd
Requires:   mod_php
Requires:   php-pgsql php-mysql
# not available?
#php-sqlite
%endif

#define serverroot #(/usr/sbin/apxs2 -q datadir 2>/dev/null || /usr/sbin/apxs2 -q PREFIX)/htdocs/

%description
Webacula - Web Bacula - web interface of a Bacula backup system.
Supports the run Job, restore all files or selected files,
restore the most recent backup for a client,
restore backup for a client before a specified time,
mount/umount Storages, show scheduled, running and terminated Jobs and more.
Supported languages: English, French, German, Italian,
Portuguese Brazil, Russian.

%description -l ru
Webacula - Web Bacula - веб интерфейс для Bacula backup system.
Поддерживает запуск Заданий, восстановление всех или выбранных файлов,
восстановление самого свежего бэкапа для клиента,
восстановление бэкапа для клиента сделанного перед указанным временем,
монтирование/размонтирование Хранилищ, показ запланированных,
выполняющихся и завершенных Заданий и прочее.
Поддерживаемые языки: английский, французский, немецкий, итальянский,
бразильский португальский, русский.



%prep
%setup -q
find -name ".htaccess*" -exec rm {} \;
#rm -f ./application/config.ini.*

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_apache_conf_dir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/usr/sbin/


#install -p -m 755 ./install/webacula_clean_tmp_files.sh \
#   $RPM_BUILD_ROOT#{_sysconfdir}/cron.daily/webacula_clean_tmp_files.sh
#rm -f ./install/webacula_clean_tmp_files.sh

cp -pr ./application $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./html        $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./languages   $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr ./library     $RPM_BUILD_ROOT%{_datadir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/install
cp -pr install/check_system_requirements.php install/MySql/ install/PostgreSql/ install/SqLite/ $RPM_BUILD_ROOT%{_datadir}/%{name}/install/

cp -p install/apache/webacula.conf  $RPM_BUILD_ROOT%{_apache_conf_dir}/webacula.conf

cp -a install/sudoers.d/webacula-bconsole $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/data/cache

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/application/config.ini  $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.ini
ln -s %{_sysconfdir}/%{name}/config.ini  $RPM_BUILD_ROOT%{_datadir}/%{name}/application/config.ini

cp -p install/webacula-config ${RPM_BUILD_ROOT}/usr/sbin/

%post
# if command a2enmod exists, 
# use it toenable Apache rewrite module
type -p a2enmod >/dev/null && a2enmod rewrite > /dev/null
LOG=/var/log/webacula-install.log
export WEBACULA_INTERACTIVE="no"
echo "`date`: BEGIN webacula-config init" >> $LOG
if /usr/sbin/webacula-config init >> $LOG 2>&1; then
    echo "SUCCESS: webacula-config init"
else
    echo "FAILED: webacula-config init, see $LOG"
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc 4CONTRIBUTORS.webacula AUTHORS COPYING README UPDATE ChangeLog
%doc docs/
%{_datadir}/%{name}/application
%{_datadir}/%{name}/html
%{_datadir}/%{name}/library
%{_datadir}/%{name}/install
%attr(-, %daemon_user, %daemon_group) %{_datadir}/%{name}/data
#{_sysconfdir}/cron.daily/webacula_clean_tmp_files.sh
%{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/languages
%config(noreplace) %{_apache_conf_dir}/webacula.conf
%config(noreplace) %{_sysconfdir}/%{name}/config.ini
/usr/sbin/webacula-config

# /etc/sudoers.d/ should not belong to this package,
# but is does currently not exist on most distributions
%dir /etc/sudoers.d/
# sudo requires permissions 440 and config files without any "."
%attr(440,root,root) %config(noreplace) /etc/sudoers.d/webacula-bconsole

%lang(de) %{_datadir}/%{name}/languages/de
%lang(en) %{_datadir}/%{name}/languages/en
%lang(fr) %{_datadir}/%{name}/languages/fr
%lang(pt) %{_datadir}/%{name}/languages/pt
%lang(ru) %{_datadir}/%{name}/languages/ru
%lang(it) %{_datadir}/%{name}/languages/it
%lang(es) %{_datadir}/%{name}/languages/es
%lang(cs) %{_datadir}/%{name}/languages/cs

%changelog
* Tue Nov 02 2013 Jörg Steffens <packager@dass-it.de> 5.5.2.x
- adapted to Bareos

* Tue Jan 18 2011 Philipp Storz <packager@dass-it.de> 5.0.2-1
- Port to opensuse build service

* Tue Aug 10 2010 Yuri Timofeev <tim4dev@gmail.com> 5.0.2-1
- Version 5.0.2

* Thu May 12 2010 Yuri Timofeev <tim4dev@gmail.com> 5.0.1-1
- Version 5.0.1

* Thu Feb 20 2010 Yuri Timofeev <tim4dev@gmail.com> 5.0-1
- Version 5.0

* Tue Feb 16 2010 Yuri Timofeev <tim4dev@gmail.com> 3.5-1
- Version 3.5

* Wed Dec 9 2009 Yuri Timofeev <tim4dev@gmail.com> 3.4.1-1
- Version 3.4.1

* Fri Oct 16 2009 Yuri Timofeev <tim4dev@gmail.com> 3.4-1
- Version 3.4

* Tue Oct 13 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-6
- Fix #526855.

* Tue Oct 13 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-5
- Fix #526855. Remove Zend Framework from source.

* Tue Oct 13 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-4
- Fix #526855

* Mon Oct 12 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-3
- Fix #526855

* Sat Oct 10 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-2
- Fix #526855 "Review Request"

* Thu Oct 08 2009 Yuri Timofeev <tim4dev@gmail.com> 3.3-1
- Initial Spec file creation for Fedora
