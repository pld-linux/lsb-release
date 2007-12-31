Summary:	LSB support for PLD Linux
Name:		lsb-release
Version:	2.0
Release:	0.1
License:	GPL v2 or later
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-make.patch
Group:		Base
URL:		http://www.linuxbase.org/
BuildRequires:	help2man
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux Standards Base (LSB) is an attempt to develop a set of
standards that will increase compatibility among Linux distributions.

%prep
%setup -q
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsb_release
%{_mandir}/man1/lsb_release.1*
