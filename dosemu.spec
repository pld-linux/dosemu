#
# Conditional build:
%bcond_with	static		# linked statically
%bcond_without	x
#
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOS-a
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS öykünümcüsü
Name:		dosemu
Version:	1.3.3
Release:	1
License:	GPL v2
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/dosemu/%{name}-%{version}.tgz
# Source0-md5:	f3b27a9326e5c95e59093fcb79a61023
#Source2:	%{name}-sys.tar.gz
Source3:	%{name}-PRZECZYTAJ_TO
Source4:	%{name}-README.PLD
Source5:	%{name}.desktop
Source6:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
# Source6-md5:	7a8abf5c656e6b99bdd03a4783751895
Patch0:		%{name}-man-pages.patch
Patch1:		%{name}-make-new.patch
Patch2:		%{name}-%{name}_conf.patch
Patch3:		%{name}-doSgmlTools.patch
Patch4:		%{name}-makehtml.patch
URL:		http://www.dosemu.org/
%if %{with x}
BuildRequires:	XFree86-devel
%{?with_static:BuildRequires:	XFree86-static}
%endif
BuildRequires:	autoconf >= 2.57
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-style-dsssl
BuildRequires:	flex
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	lynx
BuildRequires:	openjade
BuildRequires:	perl
BuildRequires:	sgml-tools
BuildRequires:	slang-devel
%{?with_static:BuildRequires:	slang-static}
BuildRequires:	unzip
BuildRequires:	util-linux
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	dosemu-freedos-minimal < 2.0.33
Conflicts:	kernel < 2.0.28
Conflicts:	mtools < 3.6
Obsoletes:	xdosemu

%define		_dosemudir	/var/lib/dosemu
%define		specflags	-fomit-frame-pointer

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos-* packages.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo¿esz go uruchomiæ
komend± "dos".

Je¶li korzystasz z dosowych programów i chcia³by¶ je uruchamiaæ na
twoim linuksowym systemie zainstaluj dosemu. Mo¿esz te¿ potrzebowaæ
pakietów dosemu-freedos-*.

%description -l pt_BR
Essa é uma versão do emulador DOS que foi projetada para rodar em
sessões X Window. Oferece suporte para gráficos VGA bem como suporte
para mouse.

%if %{with x}
%package -n xdosemu
Summary:	A DOS emulator for the X Window System
Summary(de):	DOS-Emulator für X
Summary(es):	Emulador DOS que se ejecuta en X
Summary(fr):	Émulateur DOS conçu pou être lancé sous X
Summary(pl):	Emulator DOS-a dla Systemu X Window
Summary(pt_BR):	Emulador DOS que roda no X
Summary(tr):	X altýnda çalýþan DOS öykünümcüsü
Group:		Applications/Emulators
Provides:	dosemu = %{version}-%{release}
Obsoletes:	dosemu
Conflicts:	dosemu-freedos-minimal < 2.0.33

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
Window System. Xdosemu provides VGA graphics and mouse support.

%description -n xdosemu -l de
Dies ist eine Version des DOS-Emulators für X-Window-Sitzungen. Er
unterstützt VGA-Grafiken und Maus.

%description -n xdosemu -l es
Esta es la versión del emulador DOS dibujada para ejecutarse en una
ventana del X Window. Posee soporte para gráficos VGA y ratón.

%description -n xdosemu -l fr
Version de l'émulateur DOS conçue pour tourner dans une session X.
Offre une gestion des graphismes VGA et de la souris.

%description -n xdosemu -l pl
Xdosemu jest wersj± emulatora dosemu dzia³aj±c± w X Window System.
Xdosemu ma wsparcie dla grafiki VGA i obs³ugi myszki.

%description -n xdosemu -l pt_BR
Esta é a versão do emulador DOS desenhada para rodar em uma janela do
X Window. Possui suporte a gráficos VGA e mouse.

%description -n xdosemu -l tr
Bu yazýlým, DOS öykünümcüsünün X altýnda çalýþan bir sürümüdür. VGA
grafikleri ve fare desteði vardýr.
%endif

%package utils
Summary:	Utilities for dosemu
Summary(pl):	Programy pomocnicze do dosemu
Group:		Applications/Emulators
Requires:	dosemu

%description utils
Utilities for dosemu: dexeconfig, hdinfo, mkhdimage, mkfatimage16.

%description utils -l pl
Programy pomocnicze dla dosemu: dexeconfig, hdinfo, mkhdimage,
mkfatimage16.

%prep
%setup -q -a6
#sh tmp/do_patch
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
	--without-x

%{__make} WAIT=no
mv -f bin/dosemu.bin bin/dos-nox

%if %{with x}
# X version
%configure2_13 \
%{?with_static:--enable-linkstatic} \
	--enable-new-intcode \
	--enable-aspi
%{__make} WAIT=no
%endif

%{__make} -C man
mv -f man/dosemu.bin.1 man/dosemu.1
echo '.so dosemu.1' > man/dos.1
mv -f man/ru/dosemu.bin.1 man/ru/dosemu.1
echo '.so dosemu.1' > man/ru/dos.1

mv -f pl/man1/dos.1 pl/man1/dosemu.1
echo '.so dosemu.1' > pl/man1/dos.1
echo '.so dosemu.1' > pl/man1/xdosemu.1
echo '.so dosemu.1' > pl/man1/dosdebug.1

# documentation
%{__make} -C src/doc/DANG html
%{__make} -C src/doc/HOWTO html
%{__make} -C src/doc/README html

find src/doc -name "*.html" -exec cp -f '{}' doc/ ';'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_mandir}/{pl,ru}/man1} \
	$RPM_BUILD_ROOT%{_dosemudir}/bootdir/{dosemu,freedos/doc/fdkernel}

#%%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT

install bin/dos-nox $RPM_BUILD_ROOT%{_bindir}/dos
install bin/midid $RPM_BUILD_ROOT%{_bindir}/midid

%if %{with x}
install bin/dosemu.bin $RPM_BUILD_ROOT%{_bindir}/dosemu
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdosemu
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdosexec
ln -sf dosemu $RPM_BUILD_ROOT%{_bindir}/xdos
%endif

install bin/dosdebug $RPM_BUILD_ROOT%{_bindir}/dosdebug
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
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
%attr(755,root,root) %{_bindir}/dosexec
%attr(755,root,root) %{_bindir}/midid
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%{_dosemudir}/bootdir/dosemu/*
%{_mandir}/man1/d*
%lang(pl) %{_mandir}/pl/man1/d*
%lang(ru) %{_mandir}/ru/man1/d*
%{_pixmapsdir}/dosemu.xpm

%if %{with x}
%files -n xdosemu
%defattr(644,root,root,755)
%doc QuickStart COPYING ChangeLog* doc/* README.PLD
%lang(pl) %doc PRZECZYTAJ_TO
%dir %{_dosemudir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not md5 mtime size) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_bindir}/midid
%attr(755,root,root) %{_bindir}/dosemu
%attr(755,root,root) %{_bindir}/xdos*
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%{_dosemudir}/bootdir/dosemu/*
%{_mandir}/man1/d*
%{_mandir}/man1/xdosemu.1*
%lang(pl) %{_mandir}/pl/man1/d*
%lang(pl) %{_mandir}/pl/man1/xdosemu.1*
%lang(ru) %{_mandir}/ru/man1/d*
%lang(ru) %{_mandir}/ru/man1/xdosemu.1*
%{_desktopdir}/*
%{_pixmapsdir}/dosemu.xpm
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
%{_mandir}/man1/mkfatimage16.1*
%lang(ru) %{_mandir}/ru/man1/mkfatimage16.1*
