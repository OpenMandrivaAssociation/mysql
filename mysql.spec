%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

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
Version:	5.5.19
Release:	1
Group:		Databases
License:	GPL
URL:		http://www.mysql.com/
Source0:	ftp://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.5/mysql-%{version}.tar.gz
Source1:	%{SOURCE0}.asc
Source2:	mysqld.sysconfig
Source3:	my.cnf
Source4:	libmysql.version
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
BuildRequires:	libtermcap-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	systemtap
BuildRequires:	tetex
BuildRequires:	texinfo
BuildRequires:	xfs-devel
BuildRequires:	zlib-devel
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
Conflicts:	mysql-common < 5.5.19-1
%rename %{name}-core
%rename %{name}-common-core
Requires:	mysql-common >= %{version}-%{release}
Requires:	mysql-plugin >= %{version}-%{release}
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description  server
The  mysqld server binary. For a full MySQL database server, install
package 'mysql'.

%package	common
Summary:	Common files
Group:		System/Servers
BuildArch:	noarch
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.19-1
Conflicts:	mysql-core < 5.5.19-1
Conflicts:	mysql-common-core < 5.5.19-1

%description	common
Common files for the MySQL(TM) database server.

%package	plugin
Summary:	Mysql Plugins
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.19-1

%description	plugin
This package contains the standard MySQL plugins.

%package	client
Summary:	Client
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql-core < 5.5.19-1
Conflicts:	mysql-common < 5.5.19-1
Conflicts:	mysql-common-core < 5.5.19-1

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
rm -rf %{buildroot}

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

%_post_service mysqld

%preun server
%_preun_service mysqld

%postun server
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld ]; then
        %{_initrddir}/mysqld restart > /dev/null 2>/dev/null || :
    fi
fi

%pre common
# enable plugins
if [ -f %{_sysconfdir}/my.cnf ]; then
    perl -pi -e "s|^#plugin-load|plugin-load|g" %{_sysconfdir}/my.cnf
    perl -pi -e "s|^#federated|federated|g" %{_sysconfdir}/my.cnf
fi

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
%attr(0755,root,root) %{_libdir}/libmysqlclient.so.%{major}*

%files -n %{libservices}
%attr(0755,root,root) %{_libdir}/libmysqlservices.so.%{services_major}*

%files -n %{libmysqld}
%attr(0755,root,root) %{_libdir}/libmysqld.so.%{mysqld_major}*

%files -n %{develname}
%doc INSTALL-SOURCE
%doc Docs/ChangeLog
%{multiarch_bindir}/mysql_config
%attr(0755,root,root) %{_bindir}/mysql_config
%attr(0755,root,root) %{_libdir}/libmysqlclient_r.so
%attr(0755,root,root) %{_libdir}/libmysqlclient.so
%attr(0755,root,root) %{_libdir}/libmysqlservices.so
%attr(0755,root,root) %{_libdir}/libmysqld.so
%dir %{_includedir}/mysql
%dir %{_includedir}/mysql/psi
%attr(0644,root,root) %{_includedir}/mysql/*.h
%attr(0644,root,root) %{_includedir}/mysql/psi/*.h
%{multiarch_includedir}/mysql/my_config.h
%attr(0644,root,root) %{_mandir}/man1/comp_err.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_config.1*
%attr(0644,root,root) %{_datadir}/aclocal/mysql.m4

%files -n %{staticname}
%attr(0644,root,root) %{_libdir}/*.a

