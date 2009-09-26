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

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_debug: %{expand: %%define build_debug 1}}
%{?_with_test: %{expand: %%define build_test 1}}
%{?_without_test: %global build_test 0}

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_libdir}/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%if %{build_debug}
%define build_debug 1
%endif

%if %{build_test}
%define build_test 1
%endif

%define _requires_exceptions perl(this)

%define major 16
%define libname %mklibname mysql %{major}
%define develname %mklibname -d mysql
%define staticdevelname %mklibname -d -s mysql

%define muser	mysql

# various version info
%define sphinx_version 0.9.8.1
%define pbxt_version 1.0.07
%define revision_version 0.1

Summary:	MySQL: a very fast and reliable SQL database engine
Name: 		mysql
Version:	5.1.39
Release:	%mkrel 2
Group:		System/Servers
License:	GPL
URL:		http://www.mysql.com
Source0:	http://mysql.dataphone.se/Downloads/MySQL-5.1/mysql-%{version}.tar.gz
Source1:	http://mysql.dataphone.se/Downloads/MySQL-5.1/mysql-%{version}.tar.gz.asc
Source2:	http://downloads.mysql.com/docs/refman-5.1-en.html-chapter.tar.gz
Source3:	mysqld.sysconfig
Source4:	mysqld-ndbd.init
Source5:	mysqld-ndb.sysconfig
Source6:	mysqld-ndb_cpcd.init
Source7:	mysqld-ndb_cpcd.sysconfig
Source8:	mysqld-ndb_mgmd.init
Source9:	mysqld-ndb_mgmd.sysconfig
Source10:	config.ini
Source11:	my.cnf
Patch1:		mysql-install_script_mysqld_safe.diff
Patch2:		mysql-lib64.diff
Patch3:		mysql-5.0.15-noproc.diff
Patch4:		mysql-mysqldumpslow_no_basedir.diff
Patch6:		mysql-errno.patch
Patch11:	mysql-logrotate.diff
Patch12:	mysql-initscript.diff
Patch13:	mysql-instance-manager.diff
Patch14:	mysql-5.1.30-use_-avoid-version_for_plugins.diff
# addons
Source99:	http://patg.net/downloads/convert_engine.pl
Source100:	http://www.sphinxsearch.com/downloads/sphinx-%{sphinx_version}.tar.gz
Patch100:	sphinx-plugindir_fix.diff
Patch101:	sphinx-0.9.8.1-no_-DENGINE_fix.diff
Source300:	http://www.primebase.org/download/pbxt-%{pbxt_version}-rc.tar.gz
Patch300:	pbxt-1.0.06-beta-avoid-version_fix.diff
Source400:	http://www.ddengine.org/dl/revision/files/revisionv01.tar.gz
Patch400:	revision-0.1-build_fix.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-common = %{version}-%{release}
Requires(preun): mysql-common = %{version}-%{release}
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires:	mysql-common = %{version}-%{release}
Requires:	mysql-client = %{version}-%{release}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	glibc-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtermcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	tetex
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	dos2unix
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	xfs-devel
BuildConflicts:	edit-devel
Provides:	msqlormysql MySQL-server mysqlserver MySQL = %{version}-%{release}
Obsoletes:	MySQL MySQL-devel <= 3.23.39
Conflicts:	MySQL-Max > 4.0.11
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
MySQL AB.

Please see the documentation and the manual for more information.

%package	max
Summary:	MySQL - server with extended functionality
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-common = %{version}-%{release}
Requires(preun): mysql-common = %{version}-%{release}
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires:	mysql-common = %{version}-%{release}
Requires:	mysql-client = %{version}-%{release}
Provides:	msqlormysql MySQL-server mysqlserver mysql MySQL-Max = %{version}-%{release}
Obsoletes:	MySQL-Max
Obsoletes:	MySQL-NDB
Conflicts:	MySQL > 4.0.11

%description	max 
Optional MySQL server binary that supports features like transactional tables
and more. You can use it as an alternate to MySQL basic server. The mysql-max
server is compiled with the following storage engines:

 - Ndbcluster Storage Engine interface
 - Archive Storage Engine
 - CSV Storage Engine
 - Federated Storage Engine
 - User Defined Functions (UDFs).
 - Blackhole Storage Engine
 - Partition Storage Engine

Addon storage engines (use with care):
 - Sphinx storage engine %{sphinx_version}
 - PBXT Storage Engine %{pbxt_version}
 - Revision Storage Engine %{revision_version}

%package	ndb-storage
Summary:	MySQL - ndbcluster storage engine
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Provides:	MySQL-ndb-storage = %{version}-%{release}
Obsoletes:	MySQL-ndb-storage

%description	ndb-storage
This package contains the ndbcluster storage engine. It is necessary to have
this package installed on all computers that should store ndbcluster table
data. Note that this storage engine can only be used in conjunction with the
MySQL Max server.

%package	ndb-management
Summary:	MySQL - ndbcluster storage engine management
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(post): mysql-common = %{version}-%{release}
Requires(preun): mysql-common = %{version}-%{release}
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires:	mysql-common = %{version}-%{release}
Requires:	mysql-client = %{version}-%{release}
Provides:	MySQL-ndb-management = %{version}-%{release}
Obsoletes:	MySQL-ndb-management

%description	ndb-management
This package contains ndbcluster storage engine management. It is necessary to
have this package installed on at least one computer in the cluster.

%package	ndb-tools
Summary:	MySQL - ndbcluster storage engine basic tools
Group:		System/Servers
Provides:	MySQL-ndb-tools = %{version}-%{release}
Obsoletes:	MySQL-ndb-tools

%description	ndb-tools
This package contains ndbcluster storage engine basic tools.

%package	ndb-extra
Summary:	MySQL - ndbcluster storage engine extra tools
Group:		System/Servers
Provides:	MySQL-ndb-extra = %{version}-%{release}
Obsoletes:	MySQL-ndb-extra

%description	ndb-extra
This package contains some extra ndbcluster storage engine tools for the
advanced user. They should be used with caution.

%package	common
Summary:	MySQL - common files
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires(post): perl-DBD-mysql
Requires(preun): perl-DBD-mysql
Requires:	mysql-client = %{version}-%{release}
Requires:	perl-DBD-mysql
Provides:	MySQL-common = %{version}-%{release}
Obsoletes:      MySQL-common

%description	common
Common files for the MySQL(TM) database server.

%package	client
Summary:	MySQL - Client
Group:		System/Servers
Requires(post): %{libname} = %{version}-%{release}
Requires(preun): %{libname} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Provides:       MySQL-client = %{version}-%{release}
Obsoletes:      MySQL-client
# note to self: add a conflict here because files moved from -client (v4.0.x) to -common (v5.0.x) #19789
Conflicts:	MySQL-common < 5.0

%description	client
This package contains the standard MySQL clients.

%package	bench
Summary:	MySQL - Benchmarks and test system
Group:		System/Servers
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires:	mysql-client = %{version}-%{release}
Requires:	perl
Provides:       MySQL-bench = %{version}-%{release}
Obsoletes:      MySQL-bench

%description	bench
This package contains MySQL benchmark scripts and data.

%package -n	%{libname}
Summary:	MySQL - Shared libraries
Group:		System/Libraries
Obsoletes:	MySQL-shared-libs MySQL-shared
Provides:	MySQL-shared-libs = %{version}-%{release} mysql-shared-libs = %{version}-%{release}
Provides:	MySQL-shared = %{version}-%{release} mysql-shared = %{version}-%{release}

%description -n	%{libname}
This package contains the shared libraries (*.so*) which certain languages and
applications need to dynamically load and use MySQL.

%package -n	%{develname}
Summary:	MySQL - Development header files and libraries
Group:		Development/Other
Requires(post): %{libname} = %{version}-%{release}
Requires(preun): %{libname} = %{version}-%{release}
Requires(post): mysql-common = %{version}-%{release}
Requires(preun): mysql-common = %{version}-%{release}
Requires(post): mysql-client = %{version}-%{release}
Requires(preun): mysql-client = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	mysql-common = %{version}-%{release}
Requires:	mysql-client = %{version}-%{release}
Provides:	MySQL-devel = %{version}-%{release}
Provides:	mysql-devel = %{version}-%{release}
Obsoletes:	MySQL-devel
Obsoletes:	mysql-devel
Provides:	%{libname}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel
Conflicts:	%{mklibname mysql 12 -d}
Conflicts:	%{mklibname mysql 14 -d}
Conflicts:	%{mklibname mysql 15 -d}

%description -n	%{develname}
This package contains the development header files and libraries necessary to
develop MySQL client applications.

This package also contains the MySQL server as an embedded library.

The embedded MySQL server library makes it possible to run a full-featured
MySQL server inside the client application. The main benefits are increased
speed and more simple management for embedded applications.

The API is identical for the embedded MySQL version and the client/server
version.

%package -n	%{staticdevelname}
Summary:	MySQL - Static development libraries
Group:		Development/Other
Requires:	mysql-devel = %{version}-%{release}
Conflicts:	MySQL-devel < 5.0.16-5mdk
Provides:	MySQL-static-devel = %{version}-%{release}
Provides:	mysql-static-devel = %{version}-%{release}
Obsoletes:	mysql-static-devel
Provides:	%{libname}-static-devel = %{version}-%{release}
Obsoletes:	%{libname}-static-devel

%description -n	%{staticdevelname}
This package contains the static development libraries.

%package	doc
Summary:	Documentation for MySQL
Group:		Books/Other

%description	doc
This package contains the HTML documentation for MySQL.

%prep

%setup -q -n mysql-%{version} -a2

# HOWTO pull mysql-5.0.52
# bkf clone -rmysql-5.0.52 bk://mysql.bkbits.net/mysql-5.0 mysql-5.0.52
# libtoolize --automake --force; aclocal; autoheader; automake --force --add-missing; autoconf
# cd innobase; aclocal; autoheader; autoconf; automake
# cd bdb/dist; sh s_all

if [ -d BK ]; then
    rm -rf ndb/src/cw/cpcc-win32
    rm -rf ndb/src/cw/test
    rm -rf ndb/src/cw/util
    rm -rf VC++Files
fi

# put html docs in place
mv refman-5.1-en.html-chapter Docs/html

cp %{SOURCE99} convert_engine.pl

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0554 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
find . -type f -perm 0440 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v "\.gif" | grep -v "\.png" | grep -v "\.jpg" | xargs dos2unix -U

%patch1 -p0
%patch2 -p1
%patch3 -p0 -b .noproc
%patch4 -p0 -b .mysqldumpslow_no_basedir
%patch6 -p0 -b .errno_as_defines
%patch11 -p0 -b .logrotate
%patch12 -p0 -b .initscript
%patch13 -p0 -b .instance-manager

# Sphinx storage engine
tar -zxf %{SOURCE100}
pushd sphinx-%{sphinx_version}
%patch100 -p0
%patch101 -p0
# use a more unique name for the sphinx search daemon
perl -pi -e "s|searchd|sphinx-searchd|g" mysqlse/*
popd
cp -rp sphinx-%{sphinx_version}/mysqlse storage/sphinx

# pbxt storage engine
tar -zxf %{SOURCE300}
pushd pbxt-%{pbxt_version}*
%patch300 -p0
popd

# revision storage engine
mkdir -p revision-%{revision_version}
tar -zxf %{SOURCE400} -C revision-%{revision_version}
pushd revision-%{revision_version}
%patch400 -p0
cp -p src/* .
popd
cp -rp revision-%{revision_version} storage/revision

%patch14 -p1 -b .use_-avoid-version_for_plugins

# fix annoyances
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*
perl -pi -e "s|^MAX_C_OPTIMIZE.*|MAX_C_OPTIMIZE=\"\"|g" configure*
perl -pi -e "s|^MAX_CXX_OPTIMIZE.*|MAX_CXX_OPTIMIZE=\"\"|g" configure*

mkdir -p Mandriva
cp %{SOURCE3} Mandriva/mysqld.sysconfig
cp %{SOURCE4} Mandriva/mysqld-ndbd.init
cp %{SOURCE5} Mandriva/mysqld-ndb.sysconfig
cp %{SOURCE6} Mandriva/mysqld-ndb_cpcd.init
cp %{SOURCE7} Mandriva/mysqld-ndb_cpcd.sysconfig
cp %{SOURCE8} Mandriva/mysqld-ndb_mgmd.init
cp %{SOURCE9} Mandriva/mysqld-ndb_mgmd.sysconfig
cp %{SOURCE10} Mandriva/config.ini
cp %{SOURCE11} Mandriva/my.cnf

# lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" Mandriva/my.cnf

%build
# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
#autoreconf --install --force
#export WANT_AUTOCONF_2_5=1
libtoolize --automake --copy --force; aclocal -I config/ac-macros; autoheader; automake --foreign --add-missing --copy; autoconf

if [ -d BK ]; then
    pushd innobase
	libtoolize --automake --copy  --force; aclocal; autoheader; autoconf; automake
    popd
fi

%serverbuild
export CFLAGS="${CFLAGS:-%{optflags}}"
export CXXFLAGS="${CXXFLAGS:-%{optflags}}"
export FFLAGS="${FFLAGS:-%{optflags}}"

# (gb) We shall always have the fully versioned binary
# FIXME: Please, please, do tell why you need fully qualified version
GCC_VERSION=`gcc -dumpversion`
CFLAGS="$CFLAGS -fPIC"
%ifarch alpha x86_64
CXXFLAGS="$CXXFLAGS -fPIC"
%else
CXXFLAGS="$CXXFLAGS"
%endif

# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
export CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
# extra C++ flags as per recommendations in mysql's INSTALL-SOURCE doc
export CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"

export MYSQL_BUILD_CC="gcc-$GCC_VERSION"
export MYSQL_BUILD_CXX="g++-$GCC_VERSION"

export MYSQL_BUILD_CFLAGS="$CFLAGS"
export MYSQL_BUILD_CXXFLAGS="$CXXFLAGS"

%if %{build_debug}
CFLAGS="$CFLAGS -DUNIV_MUST_NOT_INLINE -DEXTRA_DEBUG -DFORCE_INIT_OF_VARS -DSAFEMALLOC -DPEDANTIC_SAFEMALLOC -DSAFE_MUTEX"
%endif

#
# Use MYSQL_BUILD_PATH so that we can use a dedicated version of gcc
#
export PATH=${MYSQL_BUILD_PATH:-/bin:/usr/bin}
export PS='/bin/ps'
export FIND_PROC='/bin/ps p $$PID'
export KILL='/bin/kill'
export CHECK_PID='/bin/kill -0 $$PID'

# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.
MYSQL_COMMON_CONFIGURE_LINE="--prefix=/ \
    --exec-prefix=%{_prefix} \
    --libexecdir=%{_sbindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --localstatedir=/var/lib/mysql \
    --infodir=%{_infodir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --with-pic \
    --with-extra-charsets=all \
    --enable-assembler \
    --enable-local-infile \
    --enable-largefile=yes \
    --without-readline \
    --without-libwrap \
    --with-ssl=%{_libdir} \
    --with-big-tables \
    --enable-thread-safe-client \
    --with-fast-mutexes \
%if %{build_debug}
    --with-debug=full \
%else
    --without-debug \
%endif
    --with-mysqld-user=%{muser} \
    --with-unix-socket-path=/var/lib/mysql/mysql.sock"

################################################################################
# make the plain mysqld server
%configure2_5x $MYSQL_COMMON_CONFIGURE_LINE \
    --disable-shared \
    --enable-static \
    --with-comment='Mandriva Linux - MySQL Standard Edition (GPL)' \
    --without-embedded-server \
    --with-plugin-archive \
    --with-plugin-innobase \
    --without-plugin-daemon_example \
    --without-plugin-example \
    --without-plugin-ftexample \
    --without-plugin-blackhole \
    --without-plugin-federated \
    --without-plugin-innodb_plugin \
    --without-plugin-ndbcluster \
    --without-plugin-partition \
    --without-plugin-revision \
    --without-plugin-sphinx

# benchdir does not fit in above model. Maybe a separate bench distribution
%make benchdir_root=%{buildroot}%{_datadir}

# tuck away various built files
make DESTDIR=`pwd`/STD benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test install

################################################################################
# cleanup
make clean

################################################################################
# make the mysqld-max server
%configure2_5x $MYSQL_COMMON_CONFIGURE_LINE \
    --enable-shared \
    --enable-static \
    --with-comment='Mandriva Linux - MySQL Max Edition (GPL)' \
    --with-embedded-server \
    --with-plugins=ndbcluster \
    --with-plugin-federated \
    --with-big-tables \
    --with-ndbcluster \
    --with-ndb-shm \
    --with-server-suffix="-Max"

%make benchdir_root=%{buildroot}%{_datadir}

# this one is built dynamically..., heh... 
pushd pbxt-%{pbxt_version}*
autoreconf -fis
%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-mysql=../ \
    --with-plugindir=%{_libdir}/mysql/plugin
%make
popd

################################################################################
# run the tests
%if %{build_test}
# disable failing tests
#echo "mysql_client_test : Unstable test case, bug#12258" >> mysql-test/t/disabled.def
#echo "openssl_1 : Unstable test case" >> mysql-test/t/disabled.def
#echo "rpl_openssl : Unstable test case" >> mysql-test/t/disabled.def
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
echo "type_enum : Unstable test case" >> mysql-test/t/disabled.def
echo "windows : For MS Windows only" >> mysql-test/t/disabled.def
echo "ndb_restore_different_endian_data : does not pass" >> mysql-test/t/disabled.def
# set some test env, should be free high random ports...
#export MYSQL_TEST_MANAGER_PORT=9305
#export MYSQL_TEST_MASTER_PORT=9306
#export MYSQL_TEST_SLAVE_PORT=9308
#export MYSQL_TEST_NDB_PORT=9350
make check
#make test
#%ifnarch s390x
#pushd mysql-test
#    ./mysql-test-run.pl \
#    --force \
#    --timer \
#    --master_port=$MYSQL_TEST_MASTER_PORT \
#    --slave_port=$MYSQL_TEST_SLAVE_PORT \
#    --ndbcluster_port=$MYSQL_TEST_NDB_PORT \
#    --testcase-timeout=60 \
#    --suite-timeout=120 || false
#popd
#%endif

pushd mysql-test
export LANG=C
export LC_ALL=C
export LANGUAGE=C
    perl ./mysql-test-run.pl \
    --timer \
    --testcase-timeout=60 \
    --suite-timeout=120 || false
popd

%endif

%install 
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%if %{build_debug}
export DONT_STRIP=1
%endif

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_var}/run/{mysqld,ndb_cpcd}
install -d %{buildroot}%{_var}/log/mysqld
install -d %{buildroot}/var/lib/mysql/{mysql,test}
install -d %{buildroot}/var/lib/mysql-cluster

%makeinstall_std benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test

pushd pbxt-%{pbxt_version}*
%makeinstall_std
popd

# antibork...
mv %{buildroot}%{_libdir}/mysql/ha_* %{buildroot}%{_libdir}/mysql/plugin/

# nuke one useless plugin
rm -f %{buildroot}%{_libdir}/mysql/plugin/ha_example*

mv %{buildroot}%{_sbindir}/mysqld %{buildroot}%{_sbindir}/mysqld-max
install -m0755 STD/usr/sbin/mysqld %{buildroot}%{_sbindir}/mysqld

# install init scripts
install -m0755 support-files/mysql.server %{buildroot}%{_initrddir}/mysqld
install -m0755 support-files/mysql.server %{buildroot}%{_initrddir}/mysqld-max
install -m0755 Mandriva/mysqld-ndbd.init %{buildroot}%{_initrddir}/mysqld-ndbd
install -m0755 Mandriva/mysqld-ndb_cpcd.init %{buildroot}%{_initrddir}/mysqld-ndb_cpcd
install -m0755 Mandriva/mysqld-ndb_mgmd.init %{buildroot}%{_initrddir}/mysqld-ndb_mgmd

# fix status and subsys
perl -pi -e 's/status mysqld\b/status mysqld-max/g;s,(/var/lock/subsys/mysqld\b),${1}-max,' %{buildroot}%{_initrddir}/mysqld-max

# mysqld-max needs special treatment running under the instance manager...
perl -pi -e "s|--default-mysqld-path=%{_sbindir}/mysqld|--default-mysqld-path=%{_sbindir}/mysqld-max|g"  %{buildroot}%{_initrddir}/mysqld-max

# install configuration files
install -m0644 Mandriva/mysqld.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld
install -m0644 Mandriva/mysqld-ndb.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndbd
install -m0644 Mandriva/mysqld-ndb_cpcd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndb_cpcd
install -m0644 Mandriva/mysqld-ndb_mgmd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndb_mgmd
install -m0644 Mandriva/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
install -m0644 Mandriva/config.ini %{buildroot}/var/lib/mysql-cluster/config.ini

# Install docs
install -m0644 Docs/mysql.info %{buildroot}%{_infodir}/mysql.info

# Fix libraries
mv %{buildroot}%{_libdir}/mysql/libmysqlclient.* %{buildroot}%{_libdir}/
mv %{buildroot}%{_libdir}/mysql/libmysqlclient_r.* %{buildroot}%{_libdir}/
mv %{buildroot}%{_libdir}/mysql/libndbclient.* %{buildroot}%{_libdir}/
perl -pi -e "s|%{_libdir}/mysql|%{_libdir}|" %{buildroot}%{_libdir}/*.la

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

# touch some files
touch %{buildroot}%{_sysconfdir}/mysqlmanager.passwd
echo "#" > %{buildroot}%{_sysconfdir}/ndb_cpcd.conf
echo "#" > %{buildroot}/var/lib/mysql/Ndb.cfg

install -m0755 convert_engine.pl %{buildroot}%{_bindir}/mysql_convert_engine

pushd pbxt-%{pbxt_version}*
    for i in ChangeLog TODO AUTHORS COPYING NEWS README; do
	cp $i ../${i}.pbxt
    done
popd

pushd revision-%{revision_version}
    for i in AUTHORS ChangeLog COPYING INSTALL README TODO; do
	cp $i ../${i}.revision
    done
popd

# nuke -Wl,--as-needed from the mysql_config file
perl -pi -e "s|^ldflags=.*|ldflags=\'-rdynamic\'|g" %{buildroot}%{_bindir}/mysql_config

# house cleaning
rm -f %{buildroot}%{_datadir}/info/dir
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_datadir}/mysql/*.spec
rm -f %{buildroot}%{_datadir}/mysql/postinstall
rm -f %{buildroot}%{_datadir}/mysql/preinstall
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate
rm -f %{buildroot}%{_datadir}/mysql/mysql.server
rm -f %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -f %{buildroot}%{_bindir}/client_test
#rm -f %{buildroot}%{_bindir}/mysql_client_test*
rm -f %{buildroot}%{_bindir}/mysqltest_embedded
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*
rm -f %{buildroot}%{_mandir}/man1/make_win_src_distribution.1*
rm -f %{buildroot}%{_datadir}/mysql/ChangeLog
rm -f %{buildroot}/mysql-test/lib/My/SafeProcess/my_safe_process

%multiarch_binaries %{buildroot}%{_bindir}/mysql_config
%multiarch_includes %{buildroot}%{_includedir}/mysql/my_config.h

cat > README.urpmi <<EOF

The initscript used to start mysql has been reverted to use the one shipped
by MySQL AB. This means the following changes:

 * The MYSQLD_OPTIONS="--skip-networking" option in the /etc/sysconfig/mysqld
   file has been removed, this is now set in the /etc/my.cnf file.

 * The MySQL Instance Manager is used by default, set use_mysqld_safe="1" in
   the /etc/sysconfig/mysqld file to use the old mysqld_safe script.

 * The generation of the initial system mysql database is now done when mysql
   is started from the initscript and only if the /var/lib/mysql/mysql
   directory is empty (mysql_install_db). Previousely this was quite hidden and
   silently done at (rpm) install time. As a consequence to this change you may
   have to perform some manual tasks to upgrade the mysql system database and
   such. So, doing something like this might help you:

   /etc/rc.d/init.d/mysqld stop
   TMPDIR=/var/tmp mysql_install_db
   mysql_upgrade

The extra MySQL-NDB server package has been merged into the MySQL-Max package 
and ndb related pieces has been split into different sub packages as done by
MySQL AB. The MySQL libraries and the MySQL-common sub package uses the
MySQL-Max build so that no functionality required by for example the NDB
parts are lost.

The MySQL-common package now ships with a default /etc/my.cnf file that is 
based on the my-medium.cnf file that comes with the source code.

To connect to the Instance Manager you need to pass the correct command line 
options like in the following examples:

  * mysql -u root --password=my_password --port=2273 --protocol=TCP
  * mysql -u root --password=my_password --socket=/var/lib/mysql/mysqlmanager.sock

Please note you also need to add a user in the /etc/mysqlmanager.passwd file and 
make sure the file is owned by the user under which the Instance Manager service 
is running under.

Starting from mysql-max-5.1.38-1 the storage engines is built as dynamically
loadable modules for the mysql-max version. You can either load the engines using
the  /etc/my.cnf file or at runtime. Please look at these lines in the /etc/my.cnf
file to enable additional engines or disable one or more of the default ones:

plugin_dir=%{_libdir}/mysql/plugin
plugin-load=ha_archive.so;ha_blackhole.so;ha_innodb.so;ha_revision.so;ha_sphinx.so;libpbxt.so

EOF

%pre common
# delete the mysql group if no mysql user is found, before adding the user
if [ -z "`getent passwd %{muser}`" ] && ! [ -z "`getent group %{muser}`" ]; then
    %{_sbindir}/groupdel %{muser} 2> /dev/null || :
fi

%_pre_useradd %{muser} /var/lib/mysql /bin/bash

%post common
%_install_info mysql.info
%create_ghostfile %{_sysconfdir}/mysqlmanager.passwd %{muser} %{muser} 0640

%preun common
%_remove_install_info mysql.info

%post
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld

%preun
if [ -x %{_sbindir}/mysqld-max -o -x %{_initrddir}/mysqld-max ]; then
    chkconfig --del mysqld-max
else
    %_preun_service mysqld
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld -o -f /var/lock/subsys/mysqlmanager ]; then
        %{_initrddir}/mysqld restart 1>&2
    fi
fi

%post max
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld-max

%preun max
if [ -x %{_sbindir}/mysqld -o -x %{_initrddir}/mysqld ]; then
    chkconfig --del mysqld
else
    %_preun_service mysqld-max
fi

%postun max
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld-max -o -f /var/lock/subsys/mysqlmanager ]; then
        %{_initrddir}/mysqld-max restart 1>&2
    fi
fi

%post ndb-storage
%_post_service mysqld-ndbd

%preun ndb-storage
%_preun_service mysqld-ndbd

%postun ndb-storage
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld-ndbd ]; then
        %{_initrddir}/mysqld-ndbd restart 1>&2
    fi
fi

%post ndb-management
%create_ghostfile %{_sysconfdir}/ndb_cpcd.conf root root 0644
%create_ghostfile /var/lib/mysql/Ndb.cfg root root 0644
%_post_service mysqld-ndb_cpcd
%_post_service mysqld-ndb_mgmd

%preun ndb-management
%_preun_service mysqld-ndb_cpcd
%_preun_service mysqld-ndb_mgmd

%postun ndb-management
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld-ndb_cpcd ]; then
        %{_initrddir}/mysqld-ndb_cpcd restart 1>&2
    fi
    if [ -f /var/lock/subsys/mysqld-ndb_mgmd ]; then
        %{_initrddir}/mysqld-ndb_mgmd restart 1>&2
    fi
fi

%triggerin -n %{name} -- MySQL < 4.1.10
if [ -f /var/lock/subsys/mysql ]; then
    pidname="/var/lib/mysql/`/bin/hostname`.pid"
    if [ -f ${pidname} ]; then
	kill `cat ${pidname}`
	%{_initrddir}/mysqld start
    fi
fi

%triggerin -n %{name}-max -- MySQL-Max < 4.1.10
if [ -f /var/lock/subsys/mysql-max ]; then
    pidname="/var/lib/mysql/`/bin/hostname`.pid"
    if [ -f ${pidname} ]; then
	kill `cat ${pidname}`
	%{_initrddir}/mysqld-max start
    fi
fi

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.urpmi
%attr(0755,root,root) %{_initrddir}/mysqld
%attr(0755,root,root) %{_sbindir}/mysqld
%dir %{_libdir}/mysql/plugin

%files max
%defattr(-,root,root)
%doc README.urpmi
%doc *.pbxt *.revision
%attr(0755,root,root) %{_initrddir}/mysqld-max
%attr(0755,root,root) %{_sbindir}/mysqld-max
%dir %{_libdir}/mysql/plugin
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_archive.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_blackhole.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_innodb_plugin.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_innodb.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_revision.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_sphinx.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/libpbxt.so
%attr(0755,root,root) %{_bindir}/xtstat

%files ndb-storage
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/mysqld-ndbd
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndbd
%attr(0755,root,root) %{_sbindir}/ndbd
%attr(0644,root,root) %{_mandir}/man8/ndbd.8*
%attr(0644,root,root) %{_mandir}/man8/ndbmtd.8*

%files ndb-management
%defattr(-,root,root)
%ghost %attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/ndb_cpcd.conf
%ghost %attr(0644,root,root) %config(noreplace,missingok) /var/lib/mysql/Ndb.cfg
%attr(0644,root,root) %config(noreplace,missingok) /var/lib/mysql-cluster/config.ini
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndb_cpcd
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndb_mgmd
%attr(0755,root,root) %{_initrddir}/mysqld-ndb_cpcd
%attr(0755,root,root) %{_initrddir}/mysqld-ndb_mgmd
%attr(0755,root,root) %{_sbindir}/ndb_mgmd
%attr(0755,root,root) %{_sbindir}/ndb_cpcd
%attr(0755,root,root) %{_bindir}/ndb_mgm
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/ndb_cpcd
%attr(0644,root,root) %{_mandir}/man1/ndb_cpcd.1*
%attr(0644,root,root) %{_mandir}/man8/ndb_mgmd.8*

%files ndb-tools
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ndb_print_schema_file
%attr(0755,root,root) %{_bindir}/ndb_print_sys_file
%attr(0755,root,root) %{_bindir}/ndb_config
%attr(0755,root,root) %{_bindir}/ndb_desc
%attr(0755,root,root) %{_bindir}/ndb_error_reporter
%attr(0755,root,root) %{_bindir}/ndb_mgm
%attr(0755,root,root) %{_bindir}/ndb_print_backup_file
%attr(0755,root,root) %{_bindir}/ndb_restore
%attr(0755,root,root) %{_bindir}/ndb_select_all
%attr(0755,root,root) %{_bindir}/ndb_select_count
%attr(0755,root,root) %{_bindir}/ndb_show_tables
%attr(0755,root,root) %{_bindir}/ndb_size.pl
%attr(0755,root,root) %{_bindir}/ndb_test_platform
%attr(0755,root,root) %{_bindir}/ndb_waiter
%attr(0644,root,root) %{_mandir}/man1/ndb_config.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_desc.1*
%attr(0644,root,root) %{_mandir}/man1/ndbd_redo_log_reader.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_error_reporter.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_mgm.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_print_backup_file.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_print_schema_file.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_print_sys_file.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_restore.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_select_all.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_select_count.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_show_tables.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_size.pl.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_waiter.1*

%files ndb-extra
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ndb_drop_index
%attr(0755,root,root) %{_bindir}/ndb_drop_table
%attr(0755,root,root) %{_bindir}/ndb_delete_all
%attr(0644,root,root) %{_mandir}/man1/ndb_delete_all.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_drop_index.1*
%attr(0644,root,root) %{_mandir}/man1/ndb_drop_table.1*

%files client
%defattr(-,root,root)
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

%files bench
%defattr(-,root,root)
%doc sql-bench/README
%attr(0755,root,root) %{_bindir}/mysql_client_test
%attr(0755,root,root) %{_bindir}/mysql_client_test_embedded
%{_datadir}/sql-bench
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%attr(0644,root,root) %{_mandir}/man1/mysql-stress-test.pl.1*
%attr(0644,root,root) %{_mandir}/man1/mysql-test-run.pl.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_client_test.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_client_test_embedded.1*
%attr(0644,root,root) %{_mandir}/man1/mysqltest.1*
%attr(0644,root,root) %{_mandir}/man1/mysqltest_embedded.1*

%files common
%defattr(-,root,root) 
%doc README COPYING support-files/*.cnf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/my.cnf
%ghost %attr(0640,%{muser},%{muser}) %config(noreplace,missingok) %{_sysconfdir}/mysqlmanager.passwd
%attr(0755,root,root) %{_bindir}/innochecksum
%attr(0755,root,root) %{_bindir}/myisamchk
%attr(0755,root,root) %{_bindir}/myisam_ftdump
%attr(0755,root,root) %{_bindir}/myisamlog
%attr(0755,root,root) %{_bindir}/myisampack
%attr(0755,root,root) %{_bindir}/my_print_defaults
%attr(0755,root,root) %{_bindir}/mysqlbug
%attr(0755,root,root) %{_bindir}/mysql_convert_engine
%attr(0755,root,root) %{_bindir}/mysql_convert_table_format
%attr(0755,root,root) %{_bindir}/mysqld_multi
%attr(0755,root,root) %{_bindir}/mysqld_safe
%attr(0755,root,root) %{_bindir}/mysql_fix_extensions 
%attr(0755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(0755,root,root) %{_bindir}/mysqlhotcopy
%attr(0755,root,root) %{_bindir}/mysql_install_db
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
%attr(0755,root,root) %{_sbindir}/mysqlmanager
%{_infodir}/mysql.info*
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql-cluster
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/test
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/mysqld
%attr(0755,%{muser},%{muser}) %dir %{_var}/log/mysqld
%dir %{_datadir}/mysql
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/charsets
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/*.ini
%{_datadir}/mysql/errmsg.txt
%{_datadir}/mysql/czech
%{_datadir}/mysql/danish
%{_datadir}/mysql/dutch
%{_datadir}/mysql/english
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
%attr(0644,root,root) %{_mandir}/man1/innochecksum.1*
%attr(0644,root,root) %{_mandir}/man1/myisamchk.1*
%attr(0644,root,root) %{_mandir}/man1/myisamlog.1*
%attr(0644,root,root) %{_mandir}/man1/myisampack.1*
%attr(0644,root,root) %{_mandir}/man1/my_print_defaults.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlbug.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_convert_table_format.1*
%attr(0644,root,root) %{_mandir}/man1/mysqld_multi.1*
%attr(0644,root,root) %{_mandir}/man1/mysqld_safe.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_fix_extensions.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_fix_privilege_tables.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlhotcopy.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_install_db.1*
%attr(0644,root,root) %{_mandir}/man1/mysqlman.1*
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
%attr(0644,root,root) %{_mandir}/man8/mysqlmanager.8*

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc INSTALL-SOURCE EXCEPTIONS-CLIENT
%multiarch %{multiarch_bindir}/mysql_config
%attr(0755,root,root) %{_bindir}/mysql_config
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/mysql/plugin/*.la
%attr(0755,root,root) %{_libdir}/*.so
%dir %{_includedir}/mysql
%dir %{_includedir}/mysql/storage/ndb
%dir %{_includedir}/mysql/storage/ndb/mgmapi
%dir %{_includedir}/mysql/storage/ndb/ndbapi
%attr(0644,root,root) %{_includedir}/mysql/*.h
%attr(0644,root,root) %{_includedir}/mysql/storage/ndb/*.h
%attr(0644,root,root) %{_includedir}/mysql/storage/ndb/mgmapi/*.h
%attr(0644,root,root) %{_includedir}/mysql/storage/ndb/ndbapi/*.h*
%multiarch %{multiarch_includedir}/mysql/my_config.h
%attr(0644,root,root) %{_mandir}/man1/comp_err.1*
%attr(0644,root,root) %{_mandir}/man1/mysql_config.1*
%attr(0644,root,root) %{_datadir}/aclocal/mysql.m4

%files -n %{staticdevelname}
%defattr(-,root,root)
%dir %{_libdir}/mysql
%attr(0644,root,root) %{_libdir}/mysql/libdbug.a
%attr(0644,root,root) %{_libdir}/mysql/libheap.a
%attr(0644,root,root) %{_libdir}/mysql/libmyisam.a
%attr(0644,root,root) %{_libdir}/mysql/libmyisammrg.a
%attr(0644,root,root) %{_libdir}/mysql/libmysqld.a
%attr(0644,root,root) %{_libdir}/mysql/libmystrings.a
%attr(0644,root,root) %{_libdir}/mysql/libmysys.a
%attr(0644,root,root) %{_libdir}/mysql/libvio.a
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/mysql/plugin/*.a

%files doc
%defattr(-,root,root)
%doc Docs/html/*
