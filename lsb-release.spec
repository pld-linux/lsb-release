Summary:	Linux Standard Base tools
Summary(pl.UTF-8):	Narzędzia LSB (Linux Standard Base)
Name:		lsb-release
Version:	3.1
Release:	1
License:	GPL v2+
Group:		Base
#Source0:	http://dl.sourceforge.net/lsb/%{name}-2.0.tar.gz
Source0:	%{name}-2.0.tar.bz2
# Source0-md5:	cf40f5c02016bc61db03591cc3ea1ca2
Patch0:		%{name}-make.patch
URL:		http://www.linuxbase.org/
BuildRequires:	help2man
ExclusiveArch:	%{ix86} ia64 %{x8664} ppc ppc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define archname ia32
%endif
%ifarch ia64
%define archname ia64
%endif
%ifarch ppc
%define archname ppc32
%endif
%ifarch ppc64
%define archname ppc64
%endif
%ifarch s390
%define archname s390
%endif
%ifarch s390x
%define archname s390x
%endif
%ifarch %{x8664}
%define archname amd64
%endif

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
DISTRIB_RELEASE=3.0
DISTRIB_CODENAME=Th
DISTRIB_DESCRIPTION="PLD Linux"
EOF
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/core-%{version}-%{archname}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/core-%{version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/graphics-%{version}-%{archname}
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/graphics-%{version}-noarch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsb_release
%{_sysconfdir}/lsb-release
%{_sysconfdir}/%{name}.d
%{_mandir}/man1/lsb_release.1*
