
%define lsbver 3.1
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

Summary:	Linux Standard Base tools
Name:		lsb-release
Version:	3.1
Release:	0.3
License:	GPL v2+
#Source0:	http://dl.sourceforge.net/lsb/%{name}-2.0.tar.gz
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-make.patch
Group:		Base
URL:		http://www.linuxbase.org/
BuildRequires:	help2man
ExclusiveArch:	%{ix86} ia64 %{x8664} ppc ppc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LSB version query program

This program forms part of the required functionality of the LSB
(Linux Standard Base) specification.

The program queries the installed state of the distribution to display
certain properties such as the version of the LSB against which the
distribution claims compliance as well. It can also attempt to display
the name and release of the distribution along with an identifier of
who produces the distribution.

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
LSB_VERSION=lsb-%{lsbver}-%{arch_name}:lsb-%{lsbver}-noarch
DISTRIB_ID=PLD
DISTRIB_RELEASE=3.0
DISTRIB_CODENAME=Th
DISTRIB_DESCRIPTION="PLD"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsb_release
%{_sysconfdir}/lsb-release
%dir %{_sysconfdir}/%{name}.d
%{_mandir}/man1/lsb_release.1*
