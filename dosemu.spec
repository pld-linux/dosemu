# NOTE: if /dev/shm is mounted, it cannot be mounted with noexec
#
# Conditional build:
%bcond_with	static		# link statically
%bcond_with	AC
%bcond_without	htmldocs	# do not build documentation in HTML
%bcond_without	x		# X support
%bcond_with	samba		# samba support
#
%define		smarthogver	0.1.0
%define		smbrel		01

Summary:	A DOS emulator
Summary(de.UTF-8):	DOS-Emulator
Summary(es.UTF-8):	Emulador DOS
Summary(fr.UTF-8):	Emulateur DOS
Summary(pl.UTF-8):	Emulator DOS-a
Summary(pt_BR.UTF-8):	Emulador DOS
Summary(tr.UTF-8):	DOS öykünümcüsü
Name:		dosemu
Version:	1.4.0
Release:	4%{?with_samba:.smb%{smbrel}}
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/dosemu/%{name}-%{version}.tgz
# Source0-md5:	0bba530637266f99d404ba15e3f118d4
#Source2:	%{name}-sys.tar.gz
Source3:	%{name}-PRZECZYTAJ_TO
Source4:	%{name}-README.PLD
Source5:	%{name}.desktop
Source6:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
# Source6-md5:	7a8abf5c656e6b99bdd03a4783751895
Source7:	smarthog-%{smarthogver}.tgz
Patch0:		%{name}-man-pages.patch
Patch1:		%{name}-make-new.patch
Patch2:		%{name}-%{name}_conf.patch
Patch3:		%{name}-doSgmlTools.patch
Patch4:		%{name}-makehtml.patch
Patch5:		http://pascalek.pers.pl/files/projects/Samba4DosEmu/%{name}-1.4.0-samba-beta2.patch.gz
Patch6:		http://pascalek.pers.pl/files/projects/Samba4DosEmu/s4d-beta2-fix1.patch
Patch7:		%{name}-lpt4.patch
Patch8:		%{name}-Xquit.patch
Patch9:		%{name}-creat_mode.patch
URL:		http://www.dosemu.org/
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-style-dsssl
BuildRequires:	flex
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	gpm-devel
%{?with_samba:BuildRequires:	libcli_smb-devel}
BuildRequires:	libsndfile-devel
BuildRequires:	lynx
%{?with_htmldocs:BuildRequires:	openjade}
%{?with_htmldocs:BuildRequires:	perl-base}
%{?with_htmldocs:BuildRequires:	sgml-tools}
BuildRequires:	slang-devel
%{?with_static:BuildRequires:	slang-static}
BuildRequires:	unzip
BuildRequires:	util-linux
%if %{with x}
%if !%{with AC}
BuildRequires:	xorg-app-bdftopcf
BuildRequires:	xorg-app-mkfontdir
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
%if %{with static}
BuildRequires:	xorg-lib-libX11-static
BuildRequires:	xorg-lib-libXext-static
BuildRequires:	xorg-lib-libXxf86vm-static
%endif
%endif
%if %{with AC}
BuildRequires:	X11-devel
%{?with_static:BuildRequires:	X11-static}
%endif
%endif
Obsoletes:	xdosemu
Conflicts:	dosemu-freedos-minimal < 2.0.33
Conflicts:	kernel < 2.0.28
Conflicts:	mtools < 3.6
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_dosemudir	/var/lib/dosemu
%define		specflags	-fomit-frame-pointer

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos-* packages.

%description -l pl.UTF-8
Dosemu to Emulator systemu DOS. Po zainstalowaniu możesz go uruchomić
komendą "dos".

Jeśli korzystasz z dosowych programów i chciałbyś je uruchamiać na
twoim linuksowym systemie zainstaluj dosemu. Możesz też potrzebować
pakietów dosemu-freedos-*.

%description -l pt_BR.UTF-8
Essa é uma versão do emulador DOS que foi projetada para rodar em
sessões X Window. Oferece suporte para gráficos VGA bem como suporte
para mouse.

%package utils
Summary:	Utilities for dosemu
Summary(pl.UTF-8):	Programy pomocnicze do dosemu
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description utils
Utilities for dosemu: dexeconfig, hdinfo, mkhdimage, mkfatimage16.

%description utils -l pl.UTF-8
Programy pomocnicze dla dosemu: dexeconfig, hdinfo, mkhdimage,
mkfatimage16.

%package SDL
Summary:	SDL plugin for dosemu
Summary(pl.UTF-8):	Wtyczka SDL dla dosemu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description SDL
SDL plugin for dosemu.

%description SDL -l pl.UTF-8
Wtyczka SDL dla dosemu.

%package X
Summary:	X plugin for dosemu
Summary(pl.UTF-8):	Wtyczka X dla dosemu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description X
X plugin for dosemu.

%description X -l pl.UTF-8
Wtyczka X dla dosemu.

%prep
%setup -q -a6 -a7

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{?with_samba:%patch5 -p1}
%{?with_samba:%patch6 -p1}
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
OPTFLAGS="%{rpmcflags}"; export OPTFLAGS

./mkpluginhooks enable plugin_keyboard off plugin_kbd_unicode on \
plugin_extra_charset on plugin_term on plugin_translate on plugin_demo off

%{__autoconf}
# configure2_13 must be used though because of ./default-configure

# non-X version
%configure2_13 \
	%{?with_static:--enable-linkstatic} \
	--enable-new-intcode \
	--enable-aspi \
	%{!?with_x:--without-x}

%{__make} \
	WAIT=no

%{__make} -C man
mv -f man/dosemu.bin.1 man/dosemu.1
echo '.so dosemu.1' > man/dos.1
mv -f man/ru/dosemu.bin.1 man/ru/dosemu.1
echo '.so dosemu.1' > man/ru/dos.1

mv -f pl/man1/dos.1 pl/man1/dosemu.1
echo '.so dosemu.1' > pl/man1/dos.1
echo '.so dosemu.1' > pl/man1/xdosemu.1
echo '.so dosemu.1' > pl/man1/dosdebug.1

%if %{with htmldocs}
# documentation
%{__make} -C src/doc/DANG html
%{__make} -C src/doc/HOWTO html
%{__make} -C src/doc/README html

find src/doc -name "*.html" -exec cp -f '{}' doc/ ';'
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_mandir}/{pl,ru}/man1} \
	$RPM_BUILD_ROOT%{_dosemudir}/bootdir/{dosemu,freedos/doc/fdkernel} \
	$RPM_BUILD_ROOT%{_libdir}/dosemu

#%%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT

install bin/midid $RPM_BUILD_ROOT%{_bindir}/midid
install bin/dosemu.bin $RPM_BUILD_ROOT%{_bindir}/dosemu
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/dos
%if %{with x}
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdos
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdosemu
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdosexec
%endif

install bin/libplugin*.so  $RPM_BUILD_ROOT%{_libdir}/dosemu

install bin/{dosdebug,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage} $RPM_BUILD_ROOT%{_bindir}
ln -sf dos $RPM_BUILD_ROOT%{_bindir}/dosexec

install etc/dosemu.xpm $RPM_BUILD_ROOT%{_pixmapsdir}
install etc/dosemu.users.example $RPM_BUILD_ROOT%{_sysconfdir}/dosemu.users
install etc/global.conf $RPM_BUILD_ROOT%{_dosemudir}/global.conf
install etc/dosemu.conf $RPM_BUILD_ROOT%{_sysconfdir}/dosemu.conf

install man/{dosemu.1,dosdebug.1,xdosemu.1,dos.1,mkfatimage16.1} $RPM_BUILD_ROOT%{_mandir}/man1
install pl/man1/{dosemu.1,dosdebug.1,xdosemu.1,dos.1} $RPM_BUILD_ROOT%{_mandir}/pl/man1
install man/ru/{dosemu.1,dosdebug.1,xdosemu.1,dos.1,mkfatimage16.1} $RPM_BUILD_ROOT%{_mandir}/ru/man1

install commands/*.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
install commands/*.sys $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
install smarthog-%{smarthogver}/*.exe	$RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
cp %{SOURCE3} PRZECZYTAJ_TO
cp %{SOURCE4} README.PLD
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}

rm -f doc/{configuration,dosemu.lsm}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc QuickStart COPYING ChangeLog* doc/* README.PLD
%lang(pl) %doc PRZECZYTAJ_TO
%dir %{_dosemudir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not md5 mtime size) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dos
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_bindir}/dosemu
%attr(755,root,root) %{_bindir}/dosexec
%attr(755,root,root) %{_bindir}/midid
%dir %{_libdir}/dosemu
%{_libdir}/dosemu/libplugin_alsa.so
%{_libdir}/dosemu/libplugin_gpm.so
%{_libdir}/dosemu/libplugin_sndfile.so
%{_libdir}/dosemu/libplugin_term.so
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%{_dosemudir}/bootdir/dosemu/*
%{_mandir}/man1/d*
%lang(pl) %{_mandir}/pl/man1/d*
%lang(ru) %{_mandir}/ru/man1/d*
%{_pixmapsdir}/dosemu.xpm
%if %{with x}
%attr(755,root,root) %{_bindir}/xdos*
%{_mandir}/man1/xdosemu.1*
%lang(pl) %{_mandir}/pl/man1/xdosemu.1*
%lang(ru) %{_mandir}/ru/man1/xdosemu.1*
%{_desktopdir}/dosemu.desktop
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
%{_mandir}/man1/mkfatimage16.1*
%lang(ru) %{_mandir}/ru/man1/mkfatimage16.1*

%files SDL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dosemu/libplugin_sdl.so

%if %{with x}
%files X
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dosemu/libplugin_X.so
%endif
