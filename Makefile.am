
all: all-am
	find -name ".htaccess*" -exec rm {} \;

install: install-am
	mkdir -p $(DESTDIR)$(pkgdatadir)
	mkdir -p $(DESTDIR)/@HTTPD_CONF@
	mkdir -p $(DESTDIR)@sysconfdir@/cron.daily/
	mkdir -p $(DESTDIR)@sysconfdir@/sudoers.d/
	mkdir -p $(DESTDIR)@sysconfdir@/@PACKAGE@
	mkdir -p $(DESTDIR)@sbindir@
	cp -pr application/ html/ languages/ library/ $(DESTDIR)$(pkgdatadir)
	mkdir -p $(DESTDIR)$(pkgdatadir)/install
	cp -pr install/check_system_requirements.php install/MySql/ install/PostgreSql/ install/SqLite/ $(DESTDIR)$(pkgdatadir)/install/

	$(INSTALL) -m 0640 install/apache/webacula.conf  $(DESTDIR)@HTTPD_CONF@/webacula.conf

	$(INSTALL) -m 0440 install/sudoers.d/webacula-bconsole $(DESTDIR)@sysconfdir@/sudoers.d/

	mkdir -p $(DESTDIR)$(pkgdatadir)/data/cache

	mv $(DESTDIR)$(pkgdatadir)/application/config.ini  $(DESTDIR)@sysconfdir@/@PACKAGE@/config.ini
	ln -s @sysconfdir@/@PACKAGE@/config.ini  $(DESTDIR)$(pkgdatadir)/application/config.ini

	$(INSTALL_SCRIPT) install/webacula-config $(DESTDIR)@sbindir@
