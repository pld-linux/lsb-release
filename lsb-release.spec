
# Define this to link to which library version  eg. /lib64/ld-lsb-x86-64.so.3
%define lsbsover 3

%ifarch %{ix86}
%define archname ia32
%define ldso ld-linux.so.2
%define lsbldso ld-lsb.so
%endif
%ifarch ia64
%define archname ia64
%define ldso ld-linux-ia64.so.2
%define lsbldso ld-lsb-ia64.so
%endif
%ifarch ppc
%define archname ppc32
%define ldso ld.so.1
%define lsbldso ld-lsb-ppc32.so
%endif
%ifarch ppc64
%define archname ppc64
%define ldso ld64.so.1
%define lsbldso ld-lsb-ppc64.so
%endif
%ifarch s390
%define archname s390
%define ldso ld.so.1
%define lsbldso ld-lsb-s390.so
%endif
%ifarch s390x
%define archname s390x
%define ldso ld64.so.1
%define lsbldso ld-lsb-s390x.so
%endif
%ifarch %{x8664}
%define archname amd64
%define ldso ld-linux-x86-64.so.2
%define lsbldso ld-lsb-x86-64.so
%endif

%ifarch x32
%define archname x32
%define ldso ld-linux-x32.so.2
%define lsbldso ld-lsb-x32.so
%endif

%ifarch ia64 ppc64 s390x x86_64
%define qual ()(64bit)
%else
%ifarch x32
%define qual ()(x32bit)
%else
%define qual %{nil}
%endif
%endif

Summary:	LSB base libraries support for PLD Linux
Summary(pl.UTF-8):	Narzędzia LSB (Linux Standard Base)
Name:		lsb-release
Version:	4.0
Release:	1
License:	GPL v2+
Group:		Base
#Source0:	http://dl.sourceforge.net/lsb/%{name}-2.0.tar.gz
Source0:	%{name}-2.0.tar.bz2
# Source0-md5:	cf40f5c02016bc61db03591cc3ea1ca2
Patch0:		%{name}-make.patch
URL:		http://www.linuxbase.org/
BuildRequires:	help2man
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	util-linux
Requires:	coreutils
Requires:	glibc
Requires:	util-linux
ExclusiveArch:	%{ix86} ia64 %{x8664} x32 ppc ppc64 s390 s390x
# dependency for primary LSB application for v1.3
Provides:	lsb = %{version}
# dependency for primary LSB application for v2.0 and v3.0
Provides:	lsb-core-%{archname} = %{version}
Provides:	lsb-core-noarch = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# no payload
%define		_enable_debug_packages	0

%description
LSB version query program. This program forms part of the required
functionality of the LSB (Linux Standard Base) specification.

The program queries the installed state of the distribution to display
certain properties such as the version of the LSB against which the
distribution claims compliance as well. It can also attempt to display
the name and release of the distribution along with an identifier of
who produces the distribution.

%description -l pl.UTF-8
Program do sprawdzania wersji LSB. Stanowi część wymaganej
funkcjonalności specyfikacji LSB (Linux Standard Base).

Program sprawdza stan instalacji dystrybucji, wyświetlając określone
właściwości, takie jak wersja LSB z którą zgodna ma być dystrybucja.
Może także próbować wyświetlić nazwę i wersję dystrybucji wraz z
identyfikatorem producenta.

%package graphics
Summary:	LSB graphics libraries support for PLD Linux
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	lsb-graphics-%{archname} = %{version}
Provides:	lsb-graphics-noarch = %{version}

%description graphics
The Linux Standard Base (LSB) Graphics Specifications define
components that are required to be present on an LSB conforming
system.

%package printing
Summary:	LSB printing libraries support for PLD Linux
Group:		Base
Provides:	lsb-printing-%{archname} = %{version}
Provides:	lsb-printing-noarch = %{version}

%description printing
The Linux Standard Base (LSB) Printing Specifications define
components that are required to be present on an LSB conforming
system.

%prep
%setup -q -n %{name}-2.0
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release << 'EOF'
LSB_VERSION=lsb-%{version}-%{archname}:lsb-%{version}-noarch
DISTRIB_ID=PLD
DISTRIB_DESCRIPTION="PLD Linux"
%if "%{pld_release}" == "ac"
DISTRIB_RELEASE=2.0
DISTRIB_CODENAME=Ac
%endif
%if "%{pld_release}" == "th"
DISTRIB_RELEASE=3.0
DISTRIB_CODENAME=Th
%endif
EOF
%if "%{pld_release}" == "ti"
exit 1
%endif
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/core-%{version}-%{archname}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/core-%{version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/graphics-%{version}-%{archname}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/graphics-%{version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/printing-%{version}-%{archname}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/printing-%{version}-noarch

install -d $RPM_BUILD_ROOT/%{_lib}
ln -s %{ldso} $RPM_BUILD_ROOT/%{_lib}/%{lsbldso}.%{lsbsover}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/%{lsbldso}.%{lsbsover}
%attr(755,root,root) %{_bindir}/lsb_release
%{_mandir}/man1/lsb_release.1*
%{_sysconfdir}/lsb-release
%dir %{_sysconfdir}/%{name}.d
# These files are needed because they shows which LSB we're supporting now,
# for example, if core-3.1-noarch exists, it means we are supporting LSB3.1 now
%{_sysconfdir}/%{name}.d/core*

%files graphics
%defattr(644,root,root,755)
%{_sysconfdir}/%{name}.d/graphics*

%files printing
%defattr(644,root,root,755)
%{_sysconfdir}/%{name}.d/printing*
