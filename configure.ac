AC_INIT([webacula], [5.5.2])
AM_INIT_AUTOMAKE([foreign subdir-objects])

AC_PATH_PROG( [APXS], apxs2, [apxs2], [$PATH$PATH_SEPARATOR/usr/sbin$PATH_SEPARATOR/sbin])
AC_SUBST( [APACHE2_SYSCONFDIR], [`$APXS -q SYSCONFDIR`] )

AC_CONFIG_SRCDIR([configure.ac])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
