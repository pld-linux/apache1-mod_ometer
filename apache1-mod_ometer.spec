%define		mod_name	ometer
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Web counter
Summary(pl):	Modu³ do Apache: licznik odwiedzin
Name:		apache-mod_%{mod_name}
Version:	1.2.0
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.umich.edu/~umweb/downloads/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	50b7b641409abd5d1a57077422fd444e
Source1:	%{name}.conf
Source2:	http://www.umich.edu/~umweb/how-to/cgi-scripts/counter.html
# Source2-md5:	6d6f56cec95c5fa2a28caf0ecb86b034
Patch0:		%{name}-configure.patch
Patch1:		%{name}-symbols.patch
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
mod_ometer jest licznikiem odwiedzin dzia³aj±cym jako modu³ Apache'a
u¿ywaj±cym biblioteki gd do generowania obrazków. gd posiada kilka
wbudowanych fontów, lecz w liczniku mo¿na u¿yæ dowolnych fontów
TrueType. Poza mo¿liwo¶ci± wyboru kroju czcionki mod_ometer posiada
opcje umo¿liwiaj±ce zmianê szeroko¶ci, wysoko¶ci i kolorów licznika
oraz formatu obrazka: JPEG lub PNG.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1
cp %SOURCE2 .

%build
export LDFLAGS=" "
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*mod_ometer.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/mod_ometer.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
	grep -v "^Include.*mod_ometer.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mod_ometer.conf
%attr(755,root,root) %{_pkglibdir}/*
