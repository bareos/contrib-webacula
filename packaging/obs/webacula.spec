
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
BuildRequires: apache2-devel
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
# apxs2
BuildRequires: httpd-devel
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


%build
#autoreconf -fvi
%configure
make


%install
# makeinstall macro does not work on RedHat
#makeinstall
make DESTDIR=%{buildroot} install


%post
# if command a2enmod exists, 
# use it to enable Apache rewrite module
LOG=/var/log/webacula-install.log
echo "`date`: BEGIN webacula-config init" >> $LOG
which a2enmod >/dev/null && a2enmod rewrite >> $LOG 2>&1
export WEBACULA_INTERACTIVE="no"
if /usr/sbin/webacula-config init >> $LOG 2>&1; then
    echo "SUCCESS: webacula-config init, see $LOG"
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
