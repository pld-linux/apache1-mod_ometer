%define		mod_name	ometer
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Web counter
Summary(pl):	Modu� do Apache: licznik odwiedzin
Name:		apache-mod_%{mod_name}
Version:	1.2.0
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.umich.edu/~umweb/downloads/mod_%{mod_name}-%{version}.tar.gz
Patch0:		%{name}-configure.patch
URL:		http://modometer.org/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
BuildRequires:	libjpeg-devel
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%description
mod_ometer is a Web counter implemented as an Apache C module. It uses
gd to generate its images. gd has some built-in fonts, but you can use
any TrueType font you want for the counter. In addition to allowing
font choice, mod_ometer has all sorts of options for customizing the
size, width, and color of your counter, as well as the ability to
output the counter as JPEG or PNG.

%description -l pl
mod_ometer jest licznikiem odwiedzin dzia�aj�cym jako modu� Apache'a
u�ywaj�cym biblioteki gd do generowania obrazk�w. gd posiada kilka
wbudowanych font�w, lecz w liczniku mo�na u�y� dowolnych font�w
TrueType. Poza mo�liwo�ci� wyboru kroju czcionki mod_ometer posiada
opcje umo�liwiaj�ce zmian� szeroko�ci, wysoko�ci i kolor�w licznika
oraz formatu obrazka: JPEG lub PNG.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
export LDFLAGS=" "
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
