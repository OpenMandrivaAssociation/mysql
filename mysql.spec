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
%define mysql_version 5.1.46
%define sphinx_version 0.9.9
%define pbxt_version 1.0.10
%define revision_version 0.1
%define pinba_version 0.0.5
%define spider_version 2.13

# various release info
%define mysql_release %mkrel 7
%define plugins_release %mkrel 14

Summary:	MySQL: a very fast and reliable SQL database engine
Name: 		mysql
Version:	%{mysql_version}
Release:	%{mysql_release}
Group:		Databases
License:	GPL
URL:		http://www.mysql.com/
Source0:	http://mysql.dataphone.se/Downloads/MySQL-5.1/mysql-%{mysql_version}.tar.gz
Source1:	http://mysql.dataphone.se/Downloads/MySQL-5.1/mysql-%{mysql_version}.tar.gz.asc
Source2:	mysqld.sysconfig
Source3:	my.cnf
Patch0:		mysql-lib64.diff
Patch1:		mysql-5.0.15-noproc.diff
Patch2:		mysql-mysqldumpslow_no_basedir.diff
Patch3:		mysql-errno.patch
Patch4:		mysql-logrotate.diff
Patch5:		mysql-initscript.diff
Patch6:		mysql-instance-manager.diff
Patch7:		mysql-5.1.30-federated-workaround.patch
Patch8:		mysql-enable-plugins.patch
Patch9:		mysql_upgrade-exit-status.patch
Patch11:	mysql-5.1.31-shebang.patch
Patch13:	mysql-5.1.33-scripts-paths.patch
Patch14:	mysql-5.1.35-test-variables-big.patch
Patch15:	mysql-5.1.36-bmove512.patch
Patch16:	mysql-5.1.36-hotcopy.patch
Patch17:	mysql-5.1.42-myslq-test.patch
Patch18:	mysql-install_db-quiet.patch
# addons
Source99:	http://patg.net/downloads/convert_engine.pl
Source100:	http://www.sphinxsearch.com/downloads/sphinx-%{sphinx_version}.tar.gz
Patch100:	sphinx-plugindir_fix.diff
Patch101:	sphinx-0.9.8.1-no_-DENGINE_fix.diff
Source300:	http://www.primebase.org/download/pbxt-%{pbxt_version}-rc.tar.gz
Patch300:	pbxt-1.0.06-beta-avoid-version_fix.diff
Source400:	http://www.ddengine.org/dl/revision/files/revisionv01.tar.gz
Patch400:	revision-0.1-build_fix.diff
Source600:	http://pinba.org/files/pinba_engine-%{pinba_version}.tar.gz
Source700:	http://launchpad.net/spiderformysql/spider-2.x/2.13-for-5.1.39/+download/spider-src-2.13-for-5.1.39.tgz
Patch700:	mysql-5.1.44-spider-2.13.diff
Patch1000:	mysql-5.1.30-use_-avoid-version_for_plugins.diff
Patch2000:	mysql-5.1.44-CVE-2008-7247.diff
Patch2001:	mysql-5.1.46-CVE-2010-1850.diff
Patch2002:	mysql-5.1.46-CVE-2010-1848.diff
Patch2003:	mysql-5.1.46-CVE-2010-1849.diff
Patch2004:	mysql-5.1.46-bug52512.diff
Patch2005:	mysql-5.1.46-bug52711.diff
Patch2006:	mysql-5.1.46-bug54007.diff
Patch2007:	mysql-5.1.46-bug54393.diff
Patch2008:	mysql-5.1.46-bug54477.diff
Patch2009:	mysql-5.1.46-bug54575.diff
Patch2010:	mysql-5.1.46-bug54044.diff
Patch2011:	mysql-5.1.46-CVE-2010-2008.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-common = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-common = %{mysql_version}-%{mysql_release}
Requires(post): mysql-client = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-client = %{mysql_version}-%{mysql_release}
Requires(postun): mysql-common = %{mysql_version}-%{mysql_release}
Requires(postun): mysql-client = %{mysql_version}-%{mysql_release}
Requires:	mysql-common = %{mysql_version}-%{mysql_release}
Requires:	mysql-core = %{mysql_version}-%{mysql_release}
Requires:	mysql-client = %{mysql_version}-%{mysql_release}
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
Provides:	msqlormysql MySQL-server mysqlserver MySQL = %{mysql_version}-%{mysql_release}
Provides:	mysql-max = %{mysql_version}-%{mysql_release}
Obsoletes:	MySQL MySQL-devel <= 3.23.39
Obsoletes:	mysql-max < 5.1.43
BuildRoot:	%{_tmppath}/%{name}-%{mysql_version}-%{mysql_release}-buildroot

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
MySQL AB.

The mysql server is compiled with the following storage engines:

 - InnoDB Storage Engine
 - Archive Storage Engine
 - CSV Storage Engine
 - Federated Storage Engine
 - User Defined Functions (UDFs).
 - Blackhole Storage Engine
 - Partition Storage Engine

Third party storage engines packaged separately:
 - Sphinx storage engine %{sphinx_version} (urpmi mysql-plugin_sphinx)
 - PBXT Storage Engine %{pbxt_version} (urpmi mysql-plugin_pbxt)
 - Revision Storage Engine %{revision_version} (urpmi mysql-plugin_revision)
 - Pinba Storage Engine %{pinba_version} (urpmi mysql-plugin_pinba)
 - Spider Storage Engine %{spider_version} (urpmi mysql-plugin_spider)

Please see the documentation and the manual for more information.

%package	plugin_sphinx
Summary:	MySQL - The Sphinx Storage Engine
Group:		Databases
Version:	%{sphinx_version}
Release:	%{plugins_release}
URL:		http://www.sphinxsearch.com/
Conflicts:	mysql < 5.1.44-2
Requires:	mysql = %{mysql_version}-%{mysql_release}
Suggests:	sphinx >= %{sphinx_version}

%description	plugin_sphinx
Sphinx is a full-text search engine. Generally, it's a standalone search
engine, meant to provide fast, size-efficient and relevant fulltext search
functions to other applications. Sphinx was specially designed to integrate
well with SQL databases and scripting languages. Currently built-in data
sources support fetching data either via direct connection to MySQL or
PostgreSQL, or using XML pipe mechanism (a pipe to indexer in special XML-based
format which Sphinx recognizes). 

This package provides the Sphinx Storage Engine %{sphinx_version}

%package	plugin_pbxt
Summary:	MySQL - The PBXT Storage Engine
Group:		Databases
Version:	%{pbxt_version}
Release:	%{plugins_release}
URL:		http://www.primebase.org/
Conflicts:	mysql < 5.1.44-2
Requires:	mysql = %{mysql_version}-%{mysql_release}

%description	plugin_pbxt
PrimeBase XT (PBXT) is a transactional storage engine for MySQL. As illustrated
below, a MySQL storage engine responsible for the caching, indexing and storage
management of MySQL table data.

On Creation of a table in MySQL, the storage engine may be specified. This
determines the basic characteristics of the table. For example, the default
storage engine is MyISAM, which can be used for non-transactional data that
requires fast read access. A table which uses the MEMORY storage engine is held
completely in RAM.

Tables that use the PBXT Storage engine have the following features:

 * MVCC: Multi-version concurrency control, enables reading without locking.
 * Transactional: support for BEGIN, COMMIT and ROLLBACK and recovery on startup.
 * ACID compliant: Atomic, Consistent, Isolated, Durable (once committed changes cannot be lost).
 * Row-level locking: updates use row-level locking allowing for maximum concurrency.
 * Deadlock detection: immediate notification if client processes are deadlocked.
 * Referential Integrity: foreign key support.
 * Write-once: PBXT avoids double-writes by using a log-based architecture.
 * BLOB streaming: In combination with the BLOB Streaming engine.

This package provides the PBXT Storage Engine %{pbxt_version}

%package	plugin_revision
Summary:	MySQL - The Revision Storage Engine
Group:		Databases
Version:	%{revision_version}
Release:	%{plugins_release}
URL:		http://www.ddengine.org/
Conflicts:	mysql < 5.1.44-2
Requires:	mysql = %{mysql_version}-%{mysql_release}

%description	plugin_revision
This package provides the Revision Storage Engine %{revision_version}

%package	plugin_pinba
Summary:	MySQL - The Pinba Storage Engine
Group:		Databases
Version:	%{pinba_version}
Release:	%{plugins_release}
URL:		http://pinba.org/
Conflicts:	mysql < 5.1.44-2
Requires:	mysql = %{mysql_version}-%{mysql_release}
BuildRequires:	judy-devel
BuildRequires:	libevent-devel
BuildRequires:	protobuf-devel

%description	plugin_pinba
Pinba is a statistics server for PHP using MySQL as a read-only interface.

This package provides the Pinba Storage Engine %{pinba_version}

%package	plugin_spider
Summary:	MySQL - The Spider Storage Engine
Group:		Databases
Version:	%{spider_version}
Release:	%{plugins_release}
URL:		http://launchpad.net/spiderformysql/
Conflicts:	mysql < 5.1.44-2
Requires:	mysql = %{mysql_version}-%{mysql_release}

%description	plugin_spider
The spider storage engine enables tables of different MySQL instances to be
treated like a table of a same instance. Because xa transaction and
partitioning is supported, it can do decentralized arrangement to two or more
servers of data of same table.

This package provides the Spider Storage Engine %{spider_version}

%package	core
Summary:	MySQL - server core binary
Group:		System/Servers
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Conflicts:	mysql < 5.1.39-3
Conflicts:	mysql-max < 5.1.43
Requires:	mysql-common-core = %{mysql_version}-%{mysql_release}

%description	core
Core mysqld server binary. For a full MySQL database server, install
package 'mysql'.

%package	common-core
Summary:	MySQL - common files required by core binary
Group:		System/Servers
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Conflicts:	mysql-common < 5.1.43-1

%description	common-core
Common files minimally required by mysqld server binary.

%package	common
Summary:	MySQL - common files
Group:		System/Servers
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-client = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-client = %{mysql_version}-%{mysql_release}
Requires:	mysql-client = %{mysql_version}-%{mysql_release}
Requires:	mysql-common-core = %{mysql_version}-%{mysql_release}
Provides:	MySQL-common = %{mysql_version}-%{mysql_release}
Obsoletes:      MySQL-common

%description	common
Common files for the MySQL(TM) database server.

%package	client
Summary:	MySQL - Client
Group:		Databases
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Requires(post): %{libname} = %{mysql_version}-%{mysql_release}
Requires(preun): %{libname} = %{mysql_version}-%{mysql_release}
Requires:	%{libname} = %{mysql_version}-%{mysql_release}
Provides:       MySQL-client = %{mysql_version}-%{mysql_release}
Obsoletes:      MySQL-client
# note to self: add a conflict here because files moved from -client (v4.0.x) to -common (v5.0.x) #19789
Conflicts:	MySQL-common < 5.0

%description	client
This package contains the standard MySQL clients.

%package	bench
Summary:	MySQL - Benchmarks and test system
Group:		System/Servers
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Requires(post): mysql-client = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-client = %{mysql_version}-%{mysql_release}
Requires:	mysql-client = %{mysql_version}-%{mysql_release}
Requires:	perl
Provides:       MySQL-bench = %{mysql_version}-%{mysql_release}
Obsoletes:      MySQL-bench

%description	bench
This package contains MySQL benchmark scripts and data.

%package -n	%{libname}
Summary:	MySQL - Shared libraries
Group:		System/Libraries
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Obsoletes:	MySQL-shared-libs MySQL-shared
Provides:	MySQL-shared-libs = %{mysql_version}-%{mysql_release} mysql-shared-libs = %{mysql_version}-%{mysql_release}
Provides:	MySQL-shared = %{mysql_version}-%{mysql_release} mysql-shared = %{mysql_version}-%{mysql_release}

%description -n	%{libname}
This package contains the shared libraries (*.so*) which certain languages and
applications need to dynamically load and use MySQL.

%package -n	%{develname}
Summary:	MySQL - Development header files and libraries
Group:		Development/Other
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Requires(post): %{libname} = %{mysql_version}-%{mysql_release}
Requires(preun): %{libname} = %{mysql_version}-%{mysql_release}
Requires(post): mysql-common = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-common = %{mysql_version}-%{mysql_release}
Requires(post): mysql-client = %{mysql_version}-%{mysql_release}
Requires(preun): mysql-client = %{mysql_version}-%{mysql_release}
Requires:	%{libname} = %{mysql_version}-%{mysql_release}
Requires:	mysql-common = %{mysql_version}-%{mysql_release}
Requires:	mysql-client = %{mysql_version}-%{mysql_release}
Provides:	MySQL-devel = %{mysql_version}-%{mysql_release}
Provides:	mysql-devel = %{mysql_version}-%{mysql_release}
Obsoletes:	MySQL-devel
Obsoletes:	mysql-devel
Provides:	%{libname}-devel = %{mysql_version}-%{mysql_release}
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
Version:	%{mysql_version}
Release:	%{mysql_release}
URL:		http://www.mysql.com/
Requires:	mysql-devel = %{mysql_version}-%{mysql_release}
Conflicts:	MySQL-devel < 5.0.16-5mdk
Provides:	MySQL-static-devel = %{mysql_version}-%{mysql_release}
Provides:	mysql-static-devel = %{mysql_version}-%{mysql_release}
Obsoletes:	mysql-static-devel
Provides:	%{libname}-static-devel = %{mysql_version}-%{mysql_release}
Obsoletes:	%{libname}-static-devel

%description -n	%{staticdevelname}
This package contains the static development libraries.

%prep

%setup -q -n mysql-%{mysql_version}

cp %{SOURCE99} convert_engine.pl

%patch0 -p1 -b .lib64
%patch1 -p0 -b .noproc
%patch2 -p0 -b .mysqldumpslow_no_basedir
%patch3 -p0 -b .errno_as_defines
%patch4 -p0 -b .logrotate
%patch5 -p0 -b .initscript
%patch6 -p0 -b .instance-manager
%patch7 -p0 -b .federated
%patch8 -p1 -b .enable-plugins
%patch9 -p0 -b .mysql_upgrade-exit-status
%patch11 -p1 -b .shebang
%patch13 -p0 -b .scripts-paths
%patch14 -p0 -b .test-variables-big
%patch15 -p0 -b .bmove512
%patch16 -p0 -b .hotcopy
%patch17 -p0 -b .myslq-test
%patch18 -p0 -b .install_db-quiet

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

# pinba storage engine
tar -zxf %{SOURCE600}

# spider storage engine
tar -zxf %{SOURCE700}
%patch700 -p1
mv spider storage/

%patch1000 -p1 -b .use_-avoid-version_for_plugins

%patch2000 -p0 -b .CVE-2008-7247
%patch2001 -p0 -b .CVE-2010-1850
%patch2002 -p1 -b .CVE-2010-1848
%patch2003 -p1 -b .CVE-2010-1849
%patch2004 -p1 -b .bug52512
%patch2005 -p1 -b .bug52711
%patch2006 -p1 -b .bug54007
%patch2007 -p1 -b .bug54393
%patch2008 -p1 -b .bug54477
%patch2009 -p1 -b .bug54575
%patch2010 -p1 -b .bug54044
%patch2011 -p1 -b .CVE-2010-2008

# fix annoyances
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*
perl -pi -e "s|^MAX_C_OPTIMIZE.*|MAX_C_OPTIMIZE=\"\"|g" configure*
perl -pi -e "s|^MAX_CXX_OPTIMIZE.*|MAX_CXX_OPTIMIZE=\"\"|g" configure*

mkdir -p Mandriva
cp %{SOURCE2} Mandriva/mysqld.sysconfig
cp %{SOURCE3} Mandriva/my.cnf

# lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" Mandriva/my.cnf

%build
# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
#autoreconf --install --force
#export WANT_AUTOCONF_2_5=1
libtoolize --automake --copy --force; aclocal -I config/ac-macros; autoheader; automake --foreign --add-missing --copy; autoconf

%serverbuild
export CFLAGS="${CFLAGS:-%{optflags}}"
export CXXFLAGS="${CXXFLAGS:-%{optflags}}"
export FFLAGS="${FFLAGS:-%{optflags}}"

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
export MYSQL_BUILD_CFLAGS="$CFLAGS"
export MYSQL_BUILD_CXXFLAGS="$CXXFLAGS"

%if %{build_debug}
CFLAGS="$CFLAGS -DUNIV_MUST_NOT_INLINE -DEXTRA_DEBUG -DFORCE_INIT_OF_VARS -DSAFEMALLOC -DPEDANTIC_SAFEMALLOC -DSAFE_MUTEX"
%endif

export PS='/bin/ps'
export FIND_PROC='/bin/ps p $$PID'
export KILL='/bin/kill'
export CHECK_PID='/bin/kill -0 $$PID'

# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.
%configure2_5x \
    --prefix=/ \
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
    --with-unix-socket-path=/var/lib/mysql/mysql.sock \
    --enable-shared \
    --enable-static \
    --with-comment='Mandriva Linux - MySQL Community Edition (GPL)' \
    --with-embedded-server \
    --with-big-tables \
    --without-plugin-ndbcluster

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

pushd pinba_engine-%{pinba_version}*
# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
autoreconf -fis
%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-mysql=../ \
    --with-protobuf=%{_prefix} \
    --with-event=%{_prefix} \
    --with-judy=%{_prefix}
%make
popd

################################################################################
# run the tests
%if %{build_test}
%check
# disable failing tests
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
echo "type_enum : Unstable test case" >> mysql-test/t/disabled.def
echo "windows : For MS Windows only" >> mysql-test/t/disabled.def
pushd mysql-test
export LANG=C
export LC_ALL=C
export LANGUAGE=C
    perl ./mysql-test-run.pl \
    --mtr-build-thread="$((${RANDOM} % 100))" \
    --skip-ndb \
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
install -d %{buildroot}%{_var}/run/mysqld
install -d %{buildroot}%{_var}/log/mysqld
install -d %{buildroot}/var/lib/mysql/{mysql,test}

%makeinstall_std benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test

pushd pbxt-%{pbxt_version}*
%makeinstall_std
popd

pushd pinba_engine-%{pinba_version}*
%makeinstall_std libdir=%{_libdir}/mysql/plugin
popd

# antibork...
mv %{buildroot}%{_libdir}/mysql/ha_* %{buildroot}%{_libdir}/mysql/plugin/

# nuke one useless plugin
rm -f %{buildroot}%{_libdir}/mysql/plugin/ha_example*

# install init scripts
install -m0755 support-files/mysql.server %{buildroot}%{_initrddir}/mysqld

# install configuration files
install -m0644 Mandriva/mysqld.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld
install -m0644 Mandriva/my.cnf %{buildroot}%{_sysconfdir}/my.cnf

# Fix libraries
mv %{buildroot}%{_libdir}/mysql/libmysqlclient.* %{buildroot}%{_libdir}/
mv %{buildroot}%{_libdir}/mysql/libmysqlclient_r.* %{buildroot}%{_libdir}/
perl -pi -e "s|%{_libdir}/mysql|%{_libdir}|" %{buildroot}%{_libdir}/*.la

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

# touch some files
touch %{buildroot}%{_sysconfdir}/mysqlmanager.passwd

install -m0755 convert_engine.pl %{buildroot}%{_bindir}/mysql_convert_engine

# nuke -Wl,--as-needed from the mysql_config file
perl -pi -e "s|^ldflags=.*|ldflags=\'-rdynamic\'|g" %{buildroot}%{_bindir}/mysql_config

# house cleaning
rm -rf %{buildroot}%{_datadir}/info
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
plugin-load=ha_archive.so;ha_blackhole.so;ha_innodb.so;ha_federated.so

Starting from mysql-5.1.44-3 the html documentation and the mysql.info is not
shipped with the Mandriva packages due to strict licensing.

EOF

%pre
# enable plugins
if [ -f %{_sysconfdir}/my.cnf ]; then
    perl -pi -e "s|^#plugin-load|plugin-load|g" %{_sysconfdir}/my.cnf
    perl -pi -e "s|^#federated|federated|g" %{_sysconfdir}/my.cnf
fi

%pre common
# delete the mysql group if no mysql user is found, before adding the user
if [ -z "`getent passwd %{muser}`" ] && ! [ -z "`getent group %{muser}`" ]; then
    %{_sbindir}/groupdel %{muser} 2> /dev/null || :
fi

%_pre_useradd %{muser} /var/lib/mysql /bin/bash

%post common
%create_ghostfile %{_sysconfdir}/mysqlmanager.passwd %{muser} %{muser} 0640

%post
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld

%preun
%_preun_service mysqld

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld ]; then
        %{_initrddir}/mysqld restart > /dev/null 2>/dev/null || :
    fi
fi

%pre common-core
# enable plugins
if [ -f %{_sysconfdir}/my.cnf ]; then
    perl -pi -e "s|^#plugin-load|plugin-load|g" %{_sysconfdir}/my.cnf
    perl -pi -e "s|^#federated|federated|g" %{_sysconfdir}/my.cnf
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
%dir %{_libdir}/mysql/plugin
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_archive.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_blackhole.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_federated.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_innodb_plugin.so

%files plugin_sphinx
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_sphinx.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/sphinx.so

%files plugin_pbxt
%defattr(-,root,root)
%doc pbxt-%{pbxt_version}*/ChangeLog
%doc pbxt-%{pbxt_version}*/TODO
%doc pbxt-%{pbxt_version}*/AUTHORS
%doc pbxt-%{pbxt_version}*/NEWS
%doc pbxt-%{pbxt_version}*/README
%attr(0755,root,root) %{_libdir}/mysql/plugin/libpbxt.so
%attr(0755,root,root) %{_bindir}/xtstat

%files plugin_revision
%defattr(-,root,root)
%doc revision-%{revision_version}/AUTHORS
%doc revision-%{revision_version}/ChangeLog
%doc revision-%{revision_version}/README
%doc revision-%{revision_version}/TODO
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_revision.so

%files plugin_pinba
%defattr(-,root,root)
%doc pinba_engine-%{pinba_version}/NEWS
%doc pinba_engine-%{pinba_version}/README
%doc pinba_engine-%{pinba_version}/TODO
%doc pinba_engine-%{pinba_version}/default_tables.sql
%attr(0755,root,root) %{_libdir}/mysql/plugin/libpinba_engine.so

%files plugin_spider
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_spider.so

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

%files core
%defattr(-,root,root) 
%attr(0755,root,root) %{_sbindir}/mysqld
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_innodb.so

%files common-core
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%{_datadir}/mysql/charsets

%files common
%defattr(-,root,root) 
%doc README COPYING support-files/*.cnf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mysqld
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
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/test
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/mysqld
%attr(0755,%{muser},%{muser}) %dir %{_var}/log/mysqld
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/*.cnf
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
%attr(0644,root,root) %{_includedir}/mysql/*.h
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
