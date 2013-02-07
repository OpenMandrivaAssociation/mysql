%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

%define _with_systemd 1
#(ie. use with rpm --rebuild):
#
#	--with debug	Compile with debugging code
# 
#  enable build with debugging code: will _not_ strip away any debugging code,
#  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
#  configure.

%define build_debug 0
%define build_test 0

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_libdir}/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%define _requires_exceptions perl(this)

%define major 18
%define services_major 0
%define services_minor 0.0
%define mysqld_major 0
%define mysqld_minor 0.1

%define libclient %mklibname mysqlclient %{major}
%define libservices %mklibname mysqlservices %{services_major}
%define libmysqld %mklibname mysqld %{mysqld_major}
%define develname %mklibname -d mysql
%define staticname %mklibname -d -s mysql

%define muser	mysql
Summary:	A very fast and reliable SQL database engine
Name: 		mysql
Version:	5.5.30
Release:	1
Group:		Databases
License:	GPL
URL:		http://www.mysql.com/
Source0:	ftp://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.5/mysql-%{version}.tar.gz
#Source1:	%{SOURCE0}.asc
Source2:	mysqld.sysconfig
Source3:	my.cnf
Source4:	libmysql.version
Source5:	mysqld.service
Source6:	mysqld-prepare-db-dir
Source7:	mysqld-wait-ready
# fedora patches
Patch0:		mysql-errno.patch
Patch1:		mysql-strmov.patch
Patch2:		mysql-install-test.patch
Patch3:		mysql-expired-certs.patch
Patch4:		mysql-stack-guard.patch
Patch5:		mysql-chain-certs.patch
Patch6:		mysql-versioning.patch
Patch7:		mysql-dubious-exports.patch
Patch8:		mysql-disable-test.patch
Patch10:	mysql-home.patch
Patch11:	mysqld_safe-nowatch.patch
# mandriva patches
Patch100:	mysql-mysqldumpslow_no_basedir.diff
Patch101:	mysql-logrotate.diff
Patch102:	mysql-initscript.diff
Patch103:	mysql_upgrade-exit-status.patch
Patch104:	mysql-5.1.31-shebang.patch
Patch105:	mysql-5.1.35-test-variables-big.patch
Patch106:	mysql-5.1.36-hotcopy.patch
Patch107:	mysql-install_db-quiet.patch
Patch108:	mysql-5.5.9-INSTALL_INCLUDEDIR_borkfix.diff
Patch109:	mysql-libify_libservices.patch

BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	glibc-devel
BuildRequires:	libaio-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	openssl-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	systemtap
BuildRequires:	xfsprogs-devel
BuildRequires:	zlib-devel
BuildRequires:  systemd-units
BuildConflicts:	edit-devel

Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
# This basically turns into a metapkg
Requires:	mysql-server >= %{version}-%{release}
Requires:	mysql-client >= %{version}-%{release}

Provides:	msqlormysql mysqlserver
Provides:	mysql-max = %{version}-%{release}
Obsoletes:	mysql-max < 5.1.43

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user, and
robust SQL (Structured Query Language) database server. MySQL Server is
intended for mission-critical, heavy-load production systems as well as for
embedding into mass-deployed software. MySQL is a trademark of MySQL AB.

The mysql server is compiled with the following storage engines:

 - InnoDB Storage Engine
 - Archive Storage Engine
 - CSV Storage Engine
 - Federated Storage Engine
 - User Defined Functions (UDFs).
 - Blackhole Storage Engine
 - Partition Storage Engine
 - Perfschema Storage Engine

%package	server
Summary:	Server mysqld binary
Group:		System/Servers
Conflicts:	mysql < 5.1.39-3
Conflicts:	mysql-max < 5.1.43
# all pkgs needed b/c of cleanup reorg
%rename %{name}-core
%rename %{name}-common-core
Requires:	mysql-common >= %{version}-%{release}
Requires:	mysql-plugin >= %{version}-%{release}
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Obsoletes:	mysql-common < 5.5.25a-1

%description  server
The  mysqld server binary. For a full MySQL database server, install
package 'mysql'.

%package	common
Summary:	Common files
Group:		System/Servers
BuildArch:	noarch
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.25a-1
Conflicts:	mysql-core < 5.5.25a-1
Obsoletes:	mysql-common-core < 5.5.25a-1

%description	common
Common files for the MySQL(TM) database server.

%package	plugin
Summary:	Mysql Plugins
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.25a-1

%description	plugin
This package contains the standard MySQL plugins.

%package	client
Summary:	Client
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql-core < 5.5.25a-1
Conflicts:	mysql-common < 5.5.25a-1
Conflicts:	mysql-common-core < 5.5.25a-1

%description	client
This package contains the standard MySQL clients.

%package	bench
Summary:	Benchmarks and test system
Group:		System/Servers
Requires:	mysql-client >= %{version}-%{release}

%description	bench
This package contains MySQL benchmark scripts and data.

%package -n	%{libclient}
Summary:	Shared libraries
Group:		System/Libraries
# mp3blaster is the last relic to require this
#Provides:	mysql-shared = %{version}-%{release}
%rename %{_lib}mysql18

%description -n	%{libclient}
This package contains the shared %{name}client library.

%package -n	%{libservices}
Summary:	Shared %{name}client library
Group:		System/Libraries
Conflicts:	%{mklibname mysql 16 } >= 5.5.8-1
Conflicts:	%{mklibname mysql 18 } <= 5.5.10-4

%description -n	%{libservices}
The libmysqlservices library provides access to the available services and
dynamic plugins now must be linked against this library 
(use the -lmysqlservices flag).

%package -n	%{libmysqld}
Summary:	Shared libraries
Group:		System/Libraries

%description -n	%{libmysqld}
This package contains the shared %{name}d library so the MySQL server that can
be embedded into a client application instead of running as a separate process.
The API is identical for the embedded MySQL version and the client/server
version.

%package -n	%{develname}
Summary:	Development header files and libraries
Group:		Development/Other
Requires:	%{libclient} = %{version}-%{release}
Requires:	%{libmysqld} = %{version}-%{release}
Requires:	%{libservices} = %{version}-%{release}
# https://qa.mandriva.com/show_bug.cgi?id=64668
Requires:	rpm-build
Provides:	mysql-devel = %{version}-%{release}
Conflicts:	%{mklibname mysql 12 -d}
Conflicts:	%{mklibname mysql 14 -d}
Conflicts:	%{mklibname mysql 15 -d}
Conflicts:	%{mklibname mysql 16 -d}

%description -n	%{develname}
This package contains the development header files and libraries necessary to
develop MySQL client applications.

%package -n	%{staticname}
Summary:	Static development libraries
Group:		Development/Other
Requires:	%{develname} >= %{version}-%{release}
Provides:	mysql-static-devel = %{version}-%{release}

%description -n	%{staticname}
This package contains the static development libraries.

%prep
%setup -q

# fedora patches
%patch0 -p1 -b .errno
%patch1 -p1 -b .strmov
%patch2 -p1 -b .install-test
%patch3 -p1 -b .expired-certs
%patch4 -p1 -b .stack-guard
%patch5 -p1 -b .chain-certs
%patch6 -p1 -b .versioning
%patch7 -p1 -b .dubious-exports
%patch8 -p0 -b .disable-test
%patch10 -p0 -b .home
%patch11 -p1 -b .nowatch

# mandriva patches
%patch100 -p0 -b .mysqldumpslow_no_basedir
%patch101 -p0 -b .logrotate
%patch102 -p0 -b .initscript
%patch103 -p1 -b .mysql_upgrade-exit-status
%patch104 -p1 -b .shebang
%patch105 -p0 -b .test-variables-big
%patch106 -p0 -b .hotcopy
%patch107 -p0 -b .install_db-quiet
%patch108 -p0 -b .INSTALL_INCLUDEDIR_borkfix
%patch109 -p0 -b .libify_libservices

mkdir -p Mandriva
cp %{SOURCE2} Mandriva/mysqld.sysconfig
cp %{SOURCE3} Mandriva/my.cnf

# lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" Mandriva/my.cnf

# antiborker
perl -pi -e "s|\@bindir\@|%{_bindir}|g" support-files/* scripts/*
perl -pi -e "s|\@sbindir\@|%{_sbindir}|g" support-files/* scripts/*
perl -pi -e "s|\@libexecdir\@|%{_sbindir}|g" support-files/* scripts/*
perl -pi -e "s|\@localstatedir\@|/var/lib/mysql|g" support-files/* scripts/*
perl -pi -e "s|^basedir=.*|basedir=%{_prefix}|g" support-files/* scripts/mysql_install_db*

# this may be part of the problems with mysql-test
# http://bugs.mysql.com/bug.php?id=52223
#perl -pi -e "s|basedir/lib\b|basedir/%{_lib}\b|g" mysql-test/mysql-test-run.pl
#perl -pi -e "s|basedir/lib/|basedir/%{_lib}/|g" mysql-test/mysql-test-run.pl

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
cp %{SOURCE4} libmysql/libmysql.version

%build
%serverbuild

# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`

CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
export CFLAGS CXXFLAGS

%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_SBINDIR=sbin \
    -DMYSQL_DATADIR=/var/lib/mysql \
    -DSYSCONFDIR=%{_sysconfdir} \
    -DINSTALL_PLUGINDIR=%{_lib}/mysql/plugin \
    -DINSTALL_MANDIR=share/man \
    -DINSTALL_SHAREDIR=share/mysql \
    -DINSTALL_LIBDIR=%{_lib} \
    -DINSTALL_INCLUDEDIR=include/mysql \
    -DINSTALL_INFODIR=share/info \
    -DINSTALL_MYSQLDATADIR=/var/lib/mysql \
    -DINSTALL_MYSQLTESTDIR=share/mysql/mysql-test \
    -DINSTALL_SQLBENCHDIR=share/mysql \
    -DINSTALL_SUPPORTFILESDIR=share/mysql \
    -DINSTALL_MYSQLSHAREDIR=share/mysql \
    -DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
    -DWITH_READLINE=0 \
    -DWITH_LIBEDIT=0 \
    -DWITH_LIBWRAP=1 \
    -DWITH_SSL=system \
    -DWITH_ZLIB=system \
    -DWITH_PIC=1 \
    -DMYSQL_TCP_PORT=3306 \
    -DEXTRA_CHARSETS=all \
    -DENABLED_LOCAL_INFILE=1 \
    -DENABLE_DTRACE=0 \
    -DWITH_EMBEDDED_SERVER=1 \
    -DMYSQL_USER=%{muser} \
%if %{build_debug}
    -DWITH_DEBUG=1 \
%else
    -DWITH_DEBUG=0 \
%endif
    -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
    -DWITHOUT_NDBCLUSTER_STORAGE_ENGINE=1 \
    -DWITHOUT_DAEMON_EXAMPLE=1 \
    -DFEATURE_SET="community" \
    -DCOMPILATION_COMMENT="Mandriva Linux - MySQL Community Edition (GPL)" \
    -DLIBSERVICES_SOVERSION="%{services_major}" \
    -DLIBSERVICES_VERSION="%{services_major}.%{services_minor}"

cp ../libmysql/libmysql.version libmysql/libmysql.version

%make
# regular build will make libmysqld.a but not libmysqld.so :-(
mkdir libmysqld/work
cd libmysqld/work
ar -x ../libmysqld.a
# these result in missing dependencies: (filed upstream as bug 59104)
rm -f sql_binlog.cc.o rpl_utility.cc.o
gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.%{mysqld_major} -o libmysqld.so.%{mysqld_major}.%{mysqld_minor} \
	*.o \
	-lpthread -laio -lcrypt -lssl -lcrypto -lz -lrt -lstdc++ -ldl -lm -lc

%install 
# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%if %{build_debug}
export DONT_STRIP=1
%endif

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_var}/run/mysqld
install -d %{buildroot}%{_var}/log/mysqld
install -d %{buildroot}/var/lib/mysql/{mysql,test}

%makeinstall_std -C build

# install init scripts
install -m0755 build/support-files/mysql.server %{buildroot}%{_initrddir}/mysqld

# install configuration files
install -m0644 Mandriva/mysqld.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld
install -m0644 Mandriva/my.cnf %{buildroot}%{_sysconfdir}/my.cnf

# bork
mv %{buildroot}%{_bindir}/mysqlaccess.conf %{buildroot}%{_sysconfdir}/
chmod 644 %{buildroot}%{_sysconfdir}/mysqlaccess.conf
mv %{buildroot}%{_prefix}/scripts/mysql_install_db %{buildroot}%{_bindir}/
mv %{buildroot}%{_datadir}/mysql/aclocal %{buildroot}%{_datadir}/aclocal

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

# nuke -Wl,--as-needed from the mysql_config file
perl -pi -e "s|^ldflags=.*|ldflags=\'-rdynamic\'|g" %{buildroot}%{_bindir}/mysql_config

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	%{buildroot}%{_bindir}/mysql_config >mysql_config.tmp
cp -f mysql_config.tmp %{buildroot}%{_bindir}/mysql_config
chmod 755 %{buildroot}%{_bindir}/mysql_config

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f %{buildroot}%{_libdir}/libmysqlclient_r.so*
ln -s libmysqlclient.so %{buildroot}%{_libdir}/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv %{buildroot}%{_datadir}/mysql/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir}
ln -s %{_bindir}/my_safe_process %{buildroot}%{_datadir}/mysql/mysql-test/lib/My/SafeProcess/my_safe_process

# Remove libmysqld.a, install libmysqld.so
rm -f %{buildroot}%{_libdir}/libmysqld.a
install -m 0755 build/libmysqld/work/libmysqld.so.%{mysqld_major}.%{mysqld_minor} %{buildroot}%{_libdir}/libmysqld.so.%{mysqld_major}.%{mysqld_minor}
ln -s libmysqld.so.%{mysqld_major}.%{mysqld_minor} %{buildroot}%{_libdir}/libmysqld.so.%{mysqld_major}
ln -s libmysqld.so.%{mysqld_major} %{buildroot}%{_libdir}/libmysqld.so

# house cleaning
rm -rf %{buildroot}%{_datadir}/info
rm -f %{buildroot}%{_bindir}/client_test
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_datadir}/mysql/config.huge.ini
rm -f %{buildroot}%{_datadir}/mysql/config.medium.ini
rm -f %{buildroot}%{_datadir}/mysql/config.small.ini
rm -f %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate
rm -f %{buildroot}%{_datadir}/mysql/mysql.server
rm -f %{buildroot}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*
rm -f %{buildroot}%{_mandir}/man1/make_win_src_distribution.1*
rm -f %{buildroot}%{_datadir}/mysql/magic
rm -f %{buildroot}%{_libdir}/mysql/plugin/daemon_example.ini
rm -f %{buildroot}%{_bindir}/mysql_embedded

# no idea how to fix this
rm -rf %{buildroot}%{_prefix}/data
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}%{_prefix}/scripts
rm -f %{buildroot}%{_prefix}/COPYING
rm -f %{buildroot}%{_prefix}/INSTALL-BINARY
rm -f %{buildroot}%{_prefix}/README

%multiarch_binaries %{buildroot}%{_bindir}/mysql_config

%multiarch_includes %{buildroot}%{_includedir}/mysql/my_config.h

%if %{_with_systemd}
	# systemd
	mkdir -p %{buildroot}/lib/systemd/system
	install -m644 %{SOURCE5} %{buildroot}%{_systemunitdir}
	install -m 755 %{SOURCE6} %{buildroot}%{_bindir}/
	install -m 755 %{SOURCE7} %{buildroot}%{_bindir}/
%endif
cat > README.urpmi <<EOF

The initscript used to start mysql has been reverted to use the one shipped
by MySQL AB. This means the following changes:

 * The generation of the initial system mysql database is now done when mysql
   is started from the initscript and only if the /var/lib/mysql/mysql
   directory is empty (mysql_install_db). Previousely this was quite hidden and
   silently done at (rpm) install time. As a consequence to this change you may
   have to perform some manual tasks to upgrade the mysql system database and
   such. So, doing something like this might help you:

   /etc/rc.d/init.d/mysqld stop
   TMPDIR=/var/tmp mysql_install_db
   mysql_upgrade

The cluster functionalities (ndb) has been deactivated and will be removed in
future mysql versions. A new product named mysql-cluster has been added (in
contrib) that replaces the cluster functionalities.

The mysql-common-core package ships with a default /etc/my.cnf file that is 
based on the my-medium.cnf file that comes with the source code.

Starting from mysql-5.1.43-2 the storage engines is built as dynamically
loadable modules. You can either load the engines using the /etc/my.cnf file or
at runtime. Please look at these lines in the /etc/my.cnf file to enable
additional engines or disable one or more of the default ones:

plugin_dir=%{_libdir}/mysql/plugin
plugin-load=ha_archive.so;ha_blackhole.so;ha_federated.so

Starting from mysql-5.1.44-3 the html documentation and the mysql.info is not
shipped with the Mandriva packages due to strict licensing.

EOF

################################################################################
# run the tests
%if %{build_test}
# disable failing tests
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
echo "type_enum : Unstable test case" >> mysql-test/t/disabled.def
echo "windows : For MS Windows only" >> mysql-test/t/disabled.def
pushd build/mysql-test
export LANG=C
export LC_ALL=C
export LANGUAGE=C
    perl ./mysql-test-run.pl \
    --mtr-build-thread="$((${RANDOM} % 100))" \
    --skip-ndb \
    --timer \
    --retry=0 \
    --ssl \
    --mysqld=--binlog-format=mixed \
    --testcase-timeout=60 \
    --suite-timeout=120 || false
popd
%endif

%pre server
# delete the mysql group if no mysql user is found, before adding the user
if [ -z "`getent passwd %{muser}`" ] && ! [ -z "`getent group %{muser}`" ]; then
    %{_sbindir}/groupdel %{muser} 2> /dev/null || :
fi

%_pre_useradd %{muser} /var/lib/mysql /bin/bash

%post server
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld mysqld.service

%preun server
%_preun_service mysqld mysqld.service

%postun server
%_postun_unit mysqld.service

%pre common
# enable plugins
if [ -f %{_sysconfdir}/my.cnf ]; then
    perl -pi -e "s|^#plugin-load|plugin-load|g" %{_sysconfdir}/my.cnf
    perl -pi -e "s|^#federated|federated|g" %{_sysconfdir}/my.cnf
fi

%triggerun -- %{name} < 5.5.24-1
%_systemd_migrate_service_pre %{name} %{name}d.service

%triggerpostun -- %{name} < 5.5.24-1
%_systemd_migrate_service_post %{name} %{name}d.service

%files
# metapkg

%files plugin
%dir %{_libdir}/mysql/plugin
%attr(0755,root,root) %{_libdir}/mysql/plugin/adt_null.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/auth.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/auth_socket.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/auth_test_plugin.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_archive.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_blackhole.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_federated.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/mypluglib.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/qa_auth_client.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/qa_auth_interface.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/qa_auth_server.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/semisync_master.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/semisync_slave.so

%files client
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mysqlaccess.conf
%attr(0755,root,root) %{_bindir}/msql2mysql
%attr(0755,root,root) %{_bindir}/mysql
%attr(0755,root,root) %{_bindir}/mysqlaccess
%attr(0755,root,root) %{_bindir}/mysqladmin
%attr(0755,root,root) %{_bindir}/mysqlanalyze
%attr(0755,root,root) %{_bindir}/mysqlbinlog
%attr(0755,root,root) %{_bindir}/mysqlcheck
%attr(0755,root,root) %{_bindir}/mysqldump
%attr(0755,root,root) %{_bindir}/mysqldumpslow
%attr(0755,root,root) %{_bindir}/mysql_find_rows
%attr(0755,root,root) %{_bindir}/mysqlimport
%attr(0755,root,root) %{_bindir}/mysqloptimize
%attr(0755,root,root) %{_bindir}/mysqlrepair
%attr(0755,root,root) %{_bindir}/mysqlshow
%attr(0755,root,root) %{_bindir}/mysqlslap
%attr(0755,root,root) %{_bindir}/mysql_waitpid
%attr(0755,root,root) %{_bindir}/my_print_defaults
%attr(0644,root,root) %{_mandir}/man1/msql2mysql.1*
%attr(0644,root,root) %{_mandir}/man1/myisam_ftdump.1*
%attr(0644,root,root) %{_mandir}/man1/mysql.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlaccess.1*
%attr(0644,root,root) %{_mandir}/man1/mysqladmin.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlbinlog.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlcheck.1*
%attr(0644,root,root) %{_mandir}/man1/mysqldump.1*
%attr(0644,root,root) %{_mandir}/man1/mysqldumpslow.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_find_rows.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlimport.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlshow.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_waitpid.1*
%attr(0644,root,root) %{_mandir}/man1/my_print_defaults.1*

%files bench
%doc build/sql-bench/README
%attr(0755,root,root) %{_bindir}/my_safe_process
%attr(0755,root,root) %{_bindir}/mysql_client_test
%attr(0755,root,root) %{_bindir}/mysql_client_test_embedded
%attr(0755,root,root) %{_bindir}/mysqltest_embedded
%{_datadir}/mysql/sql-bench
%attr(-,mysql,mysql) %{_datadir}/mysql/mysql-test
%attr(0644,root,root) %{_mandir}/man1/mysql-stress-test.pl.1*
%attr(0644,root,root) %{_mandir}/man1/mysql-test-run.pl.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_client_test.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_client_test_embedded.1*
%attr(0644,root,root) %{_mandir}/man1/mysqltest.1*
%attr(0644,root,root) %{_mandir}/man1/mysqltest_embedded.1*

%files server
%doc README.urpmi
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%attr(0755,root,root) %{_initrddir}/mysqld
%attr(0755,root,root) %{_bindir}/innochecksum
%attr(0755,root,root) %{_bindir}/myisamchk
%attr(0755,root,root) %{_bindir}/myisam_ftdump
%attr(0755,root,root) %{_bindir}/myisamlog
%attr(0755,root,root) %{_bindir}/myisampack
%attr(0755,root,root) %{_bindir}/mysql_convert_table_format
%attr(0755,root,root) %{_bindir}/mysql_fix_extensions 
%attr(0755,root,root) %{_bindir}/mysqlbug
%attr(0755,root,root) %{_bindir}/mysqld_multi
%attr(0755,root,root) %{_bindir}/mysqld_safe
%attr(0755,root,root) %{_bindir}/mysqlhotcopy
%attr(0755,root,root) %{_bindir}/mysql_install_db
%attr(0755,root,root) %{_bindir}/mysql_plugin
%attr(0755,root,root) %{_bindir}/mysql_secure_installation
%attr(0755,root,root) %{_bindir}/mysql_setpermission
%attr(0755,root,root) %{_bindir}/mysqltest
%attr(0755,root,root) %{_bindir}/mysql_tzinfo_to_sql
%attr(0755,root,root) %{_bindir}/mysql_upgrade
%attr(0755,root,root) %{_bindir}/mysql_zap
%attr(0755,root,root) %{_bindir}/perror
%attr(0755,root,root) %{_bindir}/replace
%attr(0755,root,root) %{_bindir}/resolveip
%attr(0755,root,root) %{_bindir}/resolve_stack_dump
%attr(0755,root,root) %{_sbindir}/mysqld
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/test
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/mysqld
%attr(0755,%{muser},%{muser}) %dir %{_var}/log/mysqld
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/errmsg-utf8.txt
%attr(0644,root,root) %{_mandir}/man1/innochecksum.1*
%attr(0644,root,root) %{_mandir}/man1/myisamchk.1*
%attr(0644,root,root) %{_mandir}/man1/myisamlog.1*
%attr(0644,root,root) %{_mandir}/man1/myisampack.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlbug.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_convert_table_format.1*
%attr(0644,root,root) %{_mandir}/man1/mysqld_multi.1*
%attr(0644,root,root) %{_mandir}/man1/mysqld_safe.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_fix_extensions.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlhotcopy.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_install_db.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlman.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_plugin.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_secure_installation.1*
%attr(0644,root,root) %{_mandir}/man1/mysql.server.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_setpermission.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlslap.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_upgrade.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_zap.1*
%attr(0644,root,root) %{_mandir}/man1/perror.1*
%attr(0644,root,root) %{_mandir}/man1/replace.1*
%attr(0644,root,root) %{_mandir}/man1/resolveip.1*
%attr(0644,root,root) %{_mandir}/man1/resolve_stack_dump.1*
%attr(0644,root,root) %{_mandir}/man8/mysqld.8*

%{_systemunitdir}/mysqld.service
%{_bindir}/mysqld-prepare-db-dir
%{_bindir}/mysqld-wait-ready

%files common
%doc README COPYING
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%{_datadir}/mysql/charsets
%{_datadir}/mysql/czech
%{_datadir}/mysql/danish
%{_datadir}/mysql/dutch
%{_datadir}/mysql/estonian
%{_datadir}/mysql/french
%{_datadir}/mysql/german
%{_datadir}/mysql/greek
%{_datadir}/mysql/hungarian
%{_datadir}/mysql/italian
%{_datadir}/mysql/japanese
%{_datadir}/mysql/korean
%{_datadir}/mysql/norwegian
%{_datadir}/mysql/norwegian-ny
%{_datadir}/mysql/polish
%{_datadir}/mysql/portuguese
%{_datadir}/mysql/romanian
%{_datadir}/mysql/russian
%{_datadir}/mysql/serbian
%{_datadir}/mysql/slovak
%{_datadir}/mysql/spanish
%{_datadir}/mysql/swedish
%{_datadir}/mysql/ukrainian

%files -n %{libclient}
%{_libdir}/libmysqlclient.so.%{major}*

%files -n %{libservices}
%{_libdir}/libmysqlservices.so.%{services_major}*

%files -n %{libmysqld}
%{_libdir}/libmysqld.so.%{mysqld_major}*

%files -n %{develname}
%doc INSTALL-SOURCE
%doc Docs/ChangeLog
%{multiarch_bindir}/mysql_config
%{_bindir}/mysql_config
%{_libdir}/libmysqlclient_r.so
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlservices.so
%{_libdir}/libmysqld.so
%dir %{_includedir}/mysql
%dir %{_includedir}/mysql/psi
%attr(0644,root,root) %{_includedir}/mysql/*.h
%attr(0644,root,root) %{_includedir}/mysql/psi/*.h
%{multiarch_includedir}/mysql/my_config.h
%attr(0644,root,root) %{_mandir}/man1/comp_err.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_config.1*
%attr(0644,root,root) %{_datadir}/aclocal/mysql.m4

%files -n %{staticname}
%{_libdir}/*.a



%changelog
* Fri Jul 13 2012 Oden Eriksson <oeriksson@mandriva.com> 5.5.25a-1
+ Revision: 809176
- 5.5.25a

* Tue Jun 19 2012 Oden Eriksson <oeriksson@mandriva.com> 5.5.25-1
+ Revision: 806237
- 5.5.25

* Sat Jun 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.5.24-5
+ Revision: 803861
- fix check for if database has been prepared or not, otherwise mysql will fail
  to start if no database and systemd will make it keep try again every other
  second without giving up, while hogging tons of resources

* Mon May 21 2012 Guilherme Moro <guilherme@mandriva.com> 5.5.24-4
+ Revision: 799957
+ rebuild (emptylog)

* Sat May 19 2012 Guilherme Moro <guilherme@mandriva.com> 5.5.24-3
+ Revision: 799679
+ rebuild (emptylog)

* Sat May 19 2012 Guilherme Moro <guilherme@mandriva.com> 5.5.24-2
+ Revision: 799588
- Add systemd unit
  drop tetex BR

* Sun May 13 2012 Matthew Dawkins <mattydaw@mandriva.org> 5.5.24-1
+ Revision: 798576
- new version 5.5.24

* Mon Apr 23 2012 Oden Eriksson <oeriksson@mandriva.com> 5.5.23-1
+ Revision: 792790
- 5.5.23

* Fri Mar 23 2012 Oden Eriksson <oeriksson@mandriva.com> 5.5.22-1
+ Revision: 786478
- disable rpmlint
- fix deps
- 5.5.22

* Wed Feb 22 2012 Oden Eriksson <oeriksson@mandriva.com> 5.5.21-1
+ Revision: 779205
- 5.5.21

* Sat Jan 14 2012 Matthew Dawkins <mattydaw@mandriva.org> 5.5.20-1
+ Revision: 760834
- new version 5.5.20

  + Oden Eriksson <oeriksson@mandriva.com>
    - nuke one redundant dep

* Thu Dec 15 2011 Matthew Dawkins <mattydaw@mandriva.org> 5.5.19-1
+ Revision: 741689
- fix BR libtermcap-devel to termcap-devel
- added new source and checksum
- new version 5.5.19
- major major spec clean up
- only one common pkg now
- common pkg is noarch like it should be
- made a plugins pkg for obvious plugin
- moved bins to either client or server pkgs
- core (server) is now called server
- removed unneeded mysqld_embedded bin for libmysqld pkg
- renamed client lib to proper name
- did anyone know that the bins mysql are statically built
- no needed no manually link libs
- devel pkg now only needs libs, not any of the bin pkgs
- made mysql pkg a generic metapkg to install all bin pkgs
- removed pre 200900 scriplets
- cleaned several summaries and descriptions
- need to fix mp3blaster for manual req/provides mysql-shared

* Tue Nov 22 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.18-1
+ Revision: 732369
- mysql can't be built with -fPIC (thanks pcpa)
- sync slightly with fedora
- 5.5.18

* Thu Nov 03 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.17-1
+ Revision: 716038
- fix built
- 5.5.17
- fix #64668 (mysql_config (required by Ruby MySQL gem) doesn't work without rpm-build)
- fix #62925 (Unnecessary conflict with libmysql16-5.1.53)
- fix #62158 (mysql is compiled with DTRACE enabled which breaks the Amarok build (and possibly other stuff))

* Fri Sep 16 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.16-1
+ Revision: 699999
- 5.5.16

* Fri Jul 29 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.15-1
+ Revision: 692248
- 5.5.15

* Sat Jul 16 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.14-1
+ Revision: 690097
- 5.5.14 (singlehandedly)

* Wed Jun 01 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.13-1
+ Revision: 682252
- 5.5.13

* Sat May 14 2011 Guillaume Rousse <guillomovitch@mandriva.org> 5.5.12-2
+ Revision: 674627
- add is_prefix symbol to the list of exported symbols, needed by perl DBD driver (# 62653)

* Wed May 11 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.12-1
+ Revision: 673463
- 5.5.12

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.11-4
+ Revision: 661986
- stupid macros
- multiarch fixes

* Mon Apr 18 2011 Guillaume Rousse <guillomovitch@mandriva.org> 5.5.11-3
+ Revision: 655851
- export scramble function, needed by hydra

* Thu Apr 07 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.11-2
+ Revision: 651710
- fix a silly typo spotted by Jani V?\195?\164limaa

* Thu Apr 07 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.11-1
+ Revision: 651591
- 5.5.11

* Fri Mar 25 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.10-5
+ Revision: 648543
- fix #62276 (With the latest MySQL, Amarok constantly reports "amarok: [MySqlStorage] Tried to perform
  query on uninitialized MySQL " and won't display trees in Jamendo/Magnatune)

* Fri Mar 18 2011 Mikael Andersson <mikson@mandriva.org> 5.5.10-4
+ Revision: 646493
- P109: fix version numbering in libmysqlservices.so filename

  + Oden Eriksson <oeriksson@mandriva.com>
    - prepare for cmake guru interventions...
    - fix a typo
    - "fix" the libmysqlservices.so bork

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.10-2
+ Revision: 645993
- add the my_make_scrambled_password symbol (make_scrambled_password) for pure-ftpd

* Wed Mar 16 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.10-1
+ Revision: 645650
- 5.5.10
- note, the major was bumped from 16 to 18, so..., a major rebuild has
  to be done of all the packages linking to the mysqlclient libraries.
- sync with fedora

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 5.5.9-2
+ Revision: 640305
- rebuild to obsolete old packages

* Wed Feb 09 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.9-1
+ Revision: 637011
- fix bork
- 5.5.9

* Wed Jan 19 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-5
+ Revision: 631701
- sync with mysql-5.5.8-5.fc15.src.rpm
- P9: fix #62016 (Amarok doesn't start due to embedded mysql database)
- fix better mysql id check

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-4mdv2011.0
+ Revision: 627085
- rebuild
- some symbols were missing

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-3mdv2011.0
+ Revision: 626985
- rebuild
- really fix mysql_install_db (duh!)

* Fri Dec 31 2010 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-2mdv2011.0
+ Revision: 626889
- sync some changes with mysql-5.5.8-2.fc15.src.rpm
- added more futile attempts to make the tests work...
- fix upstream bug #58350
- added hints for mysql-test

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-1mdv2011.0
+ Revision: 626096
- disable the tests, they are borked!
- run the test suite
- nuke one useless file
- added some safety...
- added better logic to determine the mysql version id

* Mon Dec 27 2010 Oden Eriksson <oeriksson@mandriva.com> 5.5.8-0mdv2011.0
+ Revision: 625387
- 5.5.8
- rediff/drop patches
- fix deps
- drop 3rd party storage engines for now

* Sat Dec 25 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.54-1mdv2011.0
+ Revision: 624854
- 5.1.54
- fix #61973 (MySQL is built without partitioning)

* Fri Nov 26 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.53-1mdv2011.0
+ Revision: 601564
- 5.1.53

* Tue Nov 02 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.52-1mdv2011.0
+ Revision: 591927
- 5.1.52

* Tue Sep 28 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.51-1mdv2011.0
+ Revision: 581852
- 5.1.51

* Fri Sep 24 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.50-1mdv2011.0
+ Revision: 580887
- 5.1.50
- pbxt-1.0.11-6-pre-ga
- drop upstream added patches
- the spider storage engine has been removed because upstream do not care making it build with and since mysql-5.1.47

* Sat Aug 21 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.46-7mdv2011.0
+ Revision: 571701
- P2004: security fix for upstream bug52512 (fixed in 5.1.49)
- P2005: security fix for upstream bug52711 (fixed in 5.1.49)
- P2006: security fix for upstream bug54007 (fixed in 5.1.49)
- P2007: security fix for upstream bug54393 (fixed in 5.1.49)
- P2008: security fix for upstream bug54477 (fixed in 5.1.49)
- P2009: security fix for upstream bug54575 (fixed in 5.1.49)
- P2010: security fix for upstream bug54044 (fixed in 5.1.49)
- P2011: security fix for CVE-2010-2008 (fixed in 5.1.48)

* Wed Jul 21 2010 Jérôme Quelin <jquelin@mandriva.org> 5.1.46-6mdv2011.0
+ Revision: 556383
- perl-DBD-mysql is no more used in %%pre and %%postun

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - revert last commit, such changes must be discussed with the maintainer first
      and should never happen so late in the release cycle

  + Raphaël Gertz <rapsys@mandriva.org>
    - Add ccp config merge

* Tue May 25 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.46-4mdv2010.1
+ Revision: 545987
- P2001: security fix for CVE-2010-1850
- P2002: security fix for CVE-2010-1848
- P2003: security fix for CVE-2010-1849

* Tue May 04 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.46-3mdv2010.1
+ Revision: 542042
- better fix for #58843 by Nicolas Rueff

* Mon May 03 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.46-2mdv2010.1
+ Revision: 541788
- fix #58843 (MysqlD init script exits too quickly)
- fix #58844 (Typo in init script)

* Mon Apr 26 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.46-1mdv2010.1
+ Revision: 538914
- 5.1.46
- drop P19, a different akonadi fix was added

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 5.1.45-2mdv2010.1
+ Revision: 531716
- rebuild for new openssl

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.45-1mdv2010.1
+ Revision: 523692
- fix release (duh!)
- 5.1.45
- drop 2 upstream added patches

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-7mdv2010.1
+ Revision: 511593
- rebuilt against openssl-0.9.8m

* Thu Feb 25 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-6mdv2010.1
+ Revision: 510952
- more fixes in the initscript
- revert to r510729

* Wed Feb 24 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-5mdv2010.1
+ Revision: 510787
- added measures for determistic stuff
- replace deprecated skip-locking with skip-external-locking

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-4mdv2010.1
+ Revision: 509560
- fix versioning

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-3mdv2010.1
+ Revision: 509521
- remove some useless cruft
- added info about the html documention and the mysql.info file
  in the README.urpmi file
- only list non third party storage engines in README.urpmi
- really don't package the mysql.info file
- remove the html manual and don't package mysql.info because
  of licensing issues
- P19: Revert broken upstream fix for their bug 45058 (from fedora)
- added the pinba and spider storage engines
- broke out the third party storage engines into sub
  packages to reduce dependancies a bit
- don't set utf-8 as default collation
- don't load the third party storage engines per default
- added the spider and pinba storage engines

* Fri Feb 19 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-2mdv2010.1
+ Revision: 508125
- sync some patches by Michal Hru?\195?\133?\194?\161eck?\195?\131?\197?\147 from openSUSE

* Fri Feb 19 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.44-1mdv2010.1
+ Revision: 507980
- 5.1.44
- new html manual

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.43-2mdv2010.1
+ Revision: 506830
- more fixes
- make akonadi happier
- bump release
- no more mysql-max, meaning the old plain mysql version now has
  all the features from mysql-max
- update the readme a bit
- fix the postun scripts
- pbxt-1.0.09-rc
- really make it work
- remove ndb remains
- use the mysqld_safe script per default because the instance manager was
  badly designed and will be removed in future releases
- remove the old triggerin triggers
- remove the cluster features as it will be removed upstream in future
  releases, please use the mysql-cluster packages (in contrib) instead
- bitkeeper isn't used anymore

* Mon Feb 01 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.43-1mdv2010.1
+ Revision: 499064
- 5.1.43

* Sun Jan 17 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.42-3mdv2010.1
+ Revision: 492846
- commit the "symbolic-links=0" change as well...
- use symbolic-links=0 in /etc/my.cnf to mitigate CVE-2008-7247 (fedora)
- 5.1.42 fixed CVE-2009-4030
- 5.1.41 fixed CVE-2009-4028, CVE-2009-4019
- no more bitkeeper, look at: http://dev.mysql.com/doc/refman/5.1/en/installing-source-tree.html

* Wed Jan 06 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.42-2mdv2010.1
+ Revision: 486780
- rebuilt due to unknown build system problems
- 5.1.42

* Fri Dec 11 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.41-2mdv2010.1
+ Revision: 476477
- sphinx-0.9.9
- rediffed some patches

* Fri Nov 20 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.41-1mdv2010.1
+ Revision: 467715
- 5.1.41
- new html manual
- pbxt-1.0.09
- rediffed one patch

* Fri Oct 23 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.40-1mdv2010.0
+ Revision: 459012
- 5.1.40
- new html manual

* Tue Oct 06 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.39-5mdv2010.0
+ Revision: 454626
- fix #51787 (MySQL not listed as database by Software management)

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.39-4mdv2010.0
+ Revision: 451828
- attempt to fix #54166 (%%postun script accesses just removed files,
 leading to errors on removal of mysql package)

* Tue Sep 29 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.39-3mdv2010.0
+ Revision: 450923
- fix #53457 (akonadi requires full mysql, while it only needs the basic executable)
- increase max_allowed_packet to 32MB
- fix #54102 (MySQL don't work)

* Sat Sep 26 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.39-2mdv2010.0
+ Revision: 449483
- the federated storage engine has to be statically built in for
  now due to "undefined symbol: dynstr_append_mem" problems.
  http://bugs.mysql.com/bug.php?id=40942

* Mon Sep 21 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.39-1mdv2010.0
+ Revision: 446797
- 5.1.39
- new html manual (S2)

* Sat Sep 12 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.38-2mdv2010.0
+ Revision: 438552
- fix deps (xfs-devel)

* Tue Sep 08 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.38-1mdv2010.0
+ Revision: 433451
- 5.1.38
- new html manual
- drop the federatedx engine
- rediffed P12,P14
- enable loadable engines for the max version and note this
  change in the README.urpmi file (read this file!)
- don't build the ndb development docs anymore and re-enable
  parallel build again (borked doxigen stuff...)

* Thu Aug 20 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.37-2mdv2010.0
+ Revision: 418521
- bump release
- try parallel build again
- use some of the fedora optimizations to try and fix #52936 (Qt4 mysql prepared statement corruption)
- minor cleanup

* Mon Aug 03 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.37-1mdv2010.0
+ Revision: 408404
- 5.1.37

* Wed Jul 01 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.36-1mdv2010.0
+ Revision: 391313
- 5.1.36
- new html manual
- drop P1000, the CVE-2008-4456 fix is finally in there...

* Tue Jun 09 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.35-1mdv2010.0
+ Revision: 384346
- 5.1.35
- new html manual

* Wed Apr 22 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.34-2mdv2009.1
+ Revision: 368671
- P1000: security fix for CVE-2008-4456

* Mon Apr 20 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.34-1mdv2009.1
+ Revision: 368419
- 5.1.34
- new html manual

* Tue Apr 07 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.33-1mdv2009.1
+ Revision: 364828
- 5.1.33
- new manual (S2)
- comment one line in P400 to fix build

* Thu Mar 05 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.32-1mdv2009.1
+ Revision: 348751
- 5.1.32 (fixes CVE-2009-0819)

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.31-2mdv2009.1
+ Revision: 344698
- rebuilt against new readline

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.31-1mdv2009.1
+ Revision: 341464
- 5.1.31
- new html manual
- rediffed some patches
- pbxt-1.0.07-rc
- provide the my.cnf as S11 instead of making it from the spec file
- don't provide the /var/lib/mysql/.tmp anymore, use /var/tmp
- don't tag language files like %%{_datadir}/mysql/swedish as %%lang(sv)
  because it only works if the locales has been installed first

* Tue Feb 10 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1.30-5mdv2009.1
+ Revision: 339216
- no need to workaround #38398 anymore

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1.30-4mdv2009.1
+ Revision: 315515
- disable -Werror=format-security, too complex to fix...

* Fri Dec 12 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1.30-3mdv2009.1
+ Revision: 313615
- rediff some patches to meet the nofuzz criteria

* Thu Dec 04 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1.30-2mdv2009.1
+ Revision: 309983
- added a bunch of storage engines...
- mention a possible upgrade scenario in the README.urpmi file
- fix one "typo"

* Fri Nov 28 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1.30-1mdv2009.1
+ Revision: 307471
- fix the mysqld-max init script
- 5.1.30
- rediff patches, drop redundant ones
- sphinx-0.9.8.1
- nuke -Wl,--as-needed from the mysql_config file

* Mon Sep 29 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.67-3mdv2009.0
+ Revision: 289293
- added P300 (fixes CVE-2008-2079 in myisam)

* Sat Sep 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 5.0.67-2mdv2009.0
+ Revision: 281837
- make initscript provides mysqld, not mysql (bug #40845)

* Sat Aug 09 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.67-1mdv2009.0
+ Revision: 270052
- 5.0.67
- drop P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P200,P201,P202,P203,
  P300,P301, it's fixed with this version
- rediffed P2,P12
- new S2

* Sat Jul 26 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51b-5mdv2009.0
+ Revision: 250242
- sphinx-0.9.8 (final)

* Sat Jul 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 5.0.51b-4mdv2009.0
+ Revision: 238810
- fix init script dependency: don't wait for nscd to start

* Wed Jul 16 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51b-3mdv2009.0
+ Revision: 236348
- P301: fixes CVE-2008-2079 (patch from opensuse)
- fix buildroot

  + Thierry Vignaud <tv@mandriva.org>
    - description is neither licence nor url field

* Fri Jun 13 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51b-2mdv2009.0
+ Revision: 218851
- bump release
- use _disable_ld_no_undefined to try and fix the build
- hardcode %%{_localstatedir}
- fix error: Missing %%files for subpackage mysql-test

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed May 07 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51b-1mdv2009.0
+ Revision: 202771
- 5.0.51b
- new html manual

* Fri Apr 18 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.0.51a-8mdv2009.0
+ Revision: 195721
- pass -p0 to patch40 (fixes build with rpm 5.1)

  + Oden Eriksson <oeriksson@mandriva.com>
    - sphinx-0.9.8-rc2
    - revert the "conform to the 2008 specs (don't start the services per
      default)" changes and let this be handled some other way...
    - fix #36235, #34904 (remove stale pid files)
    - added P26 that fixes upstream bug 32202 (coling)

* Tue Apr 01 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-7mdv2008.1
+ Revision: 191448
- bump release
- revert back the TMP env fix
- fix the logic in P12

* Tue Apr 01 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-6mdv2008.1
+ Revision: 191376
- rebuilt due to packet loss

* Mon Mar 31 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-5mdv2008.1
+ Revision: 191196
- another approach at fixing #39356 with P4 instead
- another approach at fixing #38398 by making the initial mysql
  database from the initscript instead and document that change
  in READE.urpmi

* Tue Mar 25 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-4mdv2008.1
+ Revision: 189905
- fix #38398 (mysql seems to have default root password after 2008.1 rc1 install)
- fix #39356 (mysqldumpslow cannot determine basedir)
- sphinx-0.9.8-rc1

* Wed Feb 13 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-3mdv2008.1
+ Revision: 167181
- added upstream fixes for:
 - P22 - bug33201
 - P23 - bug26489
 - P24 - bug27427
 - P25 - bug28908
- rebuild
- remove borked hunk in mysql-install_script_mysqld_safe.diff

* Thu Jan 31 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-2mdv2008.1
+ Revision: 160895
- use the latest sphinx-0.9.8-svn-r1112 release
- drop P101, it's implemented upstream
- adjust P102

* Wed Jan 30 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51a-1mdv2008.1
+ Revision: 160261
- 5.0.51a (fixes CVE-2008-0226, CVE-2008-0227, bug29908, bug29801)
- dropped upstream fixes for:
 - P14  - bug32458
 - P301 - CVE-2007-6303
 - P302 - CVE-2007-6304
- Added upstream fixes:
 - P16 - bug31669
 - P17 - bug37300
 - P18 - bug30069
 - P19 - bug5731
 - P20 - bug29419
 - P21 - bug29446
- make it use UTF-8 per default in /etc/my.cnf (Raphael Gertz)

* Wed Jan 23 2008 Oden Eriksson <oeriksson@mandriva.com> 5.0.51-3mdv2008.1
+ Revision: 157233
- added P102 to make it recognize sphinx at "make test"
- enable running the test suite
- disable the ndb_restore_different_endian_data test for now
- added P27 (fedora)
- added upstream fixes:
 - P14  - bug32458
 - P15  - bug31761
 - P200 - bug26817 (debian)
 - P201 - bug31799 (debian)
 - P202 - bug33292 (debian)
 - P203 - bug33623 (debian)
 - P204 - bug16574 (debian)
- renumbered the sec fix patches:
 - P300: security fix for CVE-2007-5925
 - P301: security fix for CVE-2007-6303
 - P302: security fix for CVE-2007-6304
- fix #32313 (under cron.daily reports failure rotating mysqld.log and mysqlmanager.log access denied)
- P27: security fix for CVE-2007-5925
- P28: security fix for CVE-2007-6303
- P29: security fix for CVE-2007-6304

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - remove URLs from description

* Fri Dec 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.51-2mdv2008.1
+ Revision: 116182
- broke out the html documentation into the mysql-doc sub package

* Thu Dec 06 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.51-1mdv2008.1
+ Revision: 116012
- 5.0.51
- drop P14, #29451 is fixed for real

* Wed Oct 31 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-8mdv2008.1
+ Revision: 104220
- added the experimental sphinx storage backend (http://www.sphinxsearch.com/)

* Fri Sep 28 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-7mdv2008.0
+ Revision: 93555
- fix #29321 (MySQL Daemon started, "DrakeConf Services" say stopped)
- fix #31919 (problems in 5.0.45-1mdv2008.0)

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 5.0.45-6mdv2008.0
+ Revision: 90004
- rebuild

* Mon Jul 23 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-5mdv2008.0
+ Revision: 54645
- fix #30226, #32020

* Thu Jul 19 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-4mdv2008.0
+ Revision: 53549
- fix #29451, #30051

* Tue Jul 17 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-3mdv2008.0
+ Revision: 52949
- delete the mysql group if no mysql user is found, before adding the user

* Mon Jul 16 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-2mdv2008.0
+ Revision: 52562
- bump release
- fix deps
- fix #28930, #30505

* Thu Jul 12 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.45-1mdv2008.0
+ Revision: 51628
- 5.0.45
- renamed from MySQL to mysql and fix deps accordingly
- dropped the upstream implemented CVE-2007-2691 fix
- rediffed P2,P12
- conform to the latest specs, don't start it per default and devel naming
- rename it from MySQL to mysql (to preserve history)

* Sat Jul 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.41-3mdv2008.0
+ Revision: 49579
- P100: security fix for CVE-2007-2691

* Thu Jun 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.41-2mdv2008.0
+ Revision: 36816
- use distro conditional -fstack-protector

* Fri May 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.41-1mdv2008.0
+ Revision: 26228
- 5.0.41
- drop opsolete/upstream patches; P14,P20,P21,P27,P28
- rediffed patches; P1

* Tue May 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0.37-3mdv2008.0
+ Revision: 25069
- rebuild

