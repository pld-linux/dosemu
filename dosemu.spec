# Conditional build:
# --with static		- linked static 
#
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS öykünümcüsü
Name:		dosemu
Version:	1.1.3
Release:	1
License:	GPL v2
Group:		Applications/Emulators
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/dosemu/%{name}-%{version}.tgz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
Source2:	%{name}-sys.tar.gz
Source3:	%{name}-PRZECZYTAJ_TO
Source4:	%{name}-README.PLD
Source5:	%{name}.desktop
Patch0:		http://dosemu.sourceforge.net/testing/patch-1.1.3.1.gz
Patch1:		http://dosemu.sourceforge.net/testing/patch-1.1.3.2.gz
Patch11:	%{name}-1.0.2-man-pages.patch
Patch12:	%{name}-1.1-global.conf.patch
Patch20:	%{name}-mfs.patch
Patch21:	%{name}-escape.patch
Patch22:	%{name}-Oacute.patch
Patch30:	%{name}-doSgmlTools.patch
Patch31:	%{name}-dont_build_dvi.patch
URL:		http://www.dosemu.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	docbook-dtd-sgml
BuildRequires:	flex
BuildRequires:	lynx
BuildRequires:	openjade
BuildRequires:	perl
BuildRequires:	sgml-tools
BuildRequires:	slang-devel
BuildRequires:	unzip

#Requires:	dos
%{?_with_static:BuildRequires:	glibc-static}
%{?_with_static:BuildRequires:	XFree86-static}
%{?_with_static:BuildRequires:	slang-static}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28
Conflicts:	mtools < 3.6
Obsoletes:	xdosemu

%define		_xbindir	/usr/X11R6/bin
%define		_dosemudir	/var/lib/dosemu

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos-* packages.

%description -l es
Esta es una versión del emulador DOS que fue proyectada para
ejecutarse en secciones X Window. Ofrece soporte a gráficos VGA como
también soporte a ratón.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo¿esz go uruchomiæ
komend± "dos".

Je¶li korzystasz z dosowych programów i chcia³by¶ je uruchamiaæ na
twoim Linuksowym systemie zainstaluj dosemu. Mo¿esz te¿ potrzebowaæ
pakietów dosemu-freedos-*.

%description -l pt_BR
Essa é uma versão do emulador DOS que foi projetada para rodar em
sessões X Window. Oferece suporte para gráficos VGA bem como suporte
para mouse.

%package -n xdosemu
Summary:	A DOS emulator for the X Window System
Summary(de):	DOS-Emulator für X
Summary(es):	Emulador DOS que se ejecuta en X
Summary(fr):	Émulateur DOS conçu pou être lancé sous X
Summary(pt_BR):	Emulador DOS que roda no X
Summary(tr):	X altýnda çalýþan DOS öykünümcüsü
Group:		Applications/Emulators
Provides:	dosemu
Obsoletes:	dosemu
#Requires:	dos

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
Window System. Xdosemu provides VGA graphics and mouse support.

%description -n xdosemu -l de
Dies ist eine Version des DOS-Emulators für X-Windows-Sitzungen. Er
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
%setup -q -a1 -a2
%patch0 -p1
%patch1 -p1
%patch11 -p1
%patch12 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch30 -p1
%patch31 -p1

%build
OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"; export OPTFLAGS

./mkpluginhooks enable plugin_keyboard off plugin_kbd_unicode on \
plugin_extra_charset on plugin_term on plugin_translate on plugin_demo off 

cp -f base-configure.in configure.in
%{__autoconf}

# non-X version
%configure \
%{?_with_static:--enable-linkstatic} \
	--enable-new-intcode \
	--enable-aspi \
	--without-x

echo | %{__make}
mv -f bin/dosemu.bin bin/dos-nox

# X version
%configure \
%{?_with_static:--enable-linkstatic} \
	--enable-new-intcode \
	--enable-aspi
echo | %{__make}
mv -f bin/dosemu.bin bin/dos-x
mv -f bin/dos-nox bin/dosemu.bin

mv -f man/dosemu.bin.1 man/dos.1

# documentation
%{__make} docs
find src/doc -name "*.html" -exec cp -f '{}' doc/ ';' 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_xbindir},%{_sysconfdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/man1,%{_mandir}/pl/man1} \
	$RPM_BUILD_ROOT%{_dosemudir}/bootdir/{dosemu,freedos/doc/fdkernel}

install bin/dosemu.bin $RPM_BUILD_ROOT%{_bindir}/dos
install bin/dos-x $RPM_BUILD_ROOT%{_xbindir}/dos
ln -sf dos $RPM_BUILD_ROOT%{_xbindir}/xdos
ln -sf dos $RPM_BUILD_ROOT%{_xbindir}/dosexec
install bin/dosdebug $RPM_BUILD_ROOT%{_bindir}/dosdebug
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
ln -sf dos $RPM_BUILD_ROOT%{_bindir}/dosexec

install etc/dosemu.xpm $RPM_BUILD_ROOT%{_prefix}/X11R6/share/pixmaps
install etc/dosemu.users.secure $RPM_BUILD_ROOT%{_sysconfdir}/dosemu.users
install etc/global.conf $RPM_BUILD_ROOT%{_dosemudir}/global.conf
install etc/dosemu.conf $RPM_BUILD_ROOT%{_sysconfdir}/dosemu.conf

install man/{dos.1,dosdebug.1,xdos.1,mkfatimage16.1} $RPM_BUILD_ROOT%{_mandir}/man1
install pl/man1/{dos.1,dosdebug.1,xdos.1} $RPM_BUILD_ROOT%{_mandir}/pl/man1

install src/plugin/commands/*.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
install dosemu/*.sys $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
cp %{SOURCE3} PRZECZYTAJ_TO
cp %{SOURCE4} README.PLD
install %{SOURCE5} $RPM_BUILD_ROOT%{_applnkdir}/System/

#ln -sf dosemu/comcom.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/command.com

# Take out irritating ^H's from the documentation
#for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.\010//g' > doc/$i ; done

rm -f doc/{configuration,dosemu.lsm}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc QuickStart COPYING ChangeLog* doc/*.html PRZECZYTAJ_TO README.PLD
%dir %{_dosemudir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dos
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_bindir}/dosexec
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%{_dosemudir}/bootdir/dosemu/*
#%{_dosemudir}/bootdir/command.com
%{_mandir}/man1/[dm]*
%lang(pl) %{_mandir}/pl/man1/d*
%{_pixmapsdir}/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%doc QuickStart COPYING ChangeLog* doc/*.html PRZECZYTAJ_TO README.PLD
%dir %{_dosemudir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_xbindir}/*
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%{_dosemudir}/bootdir/dosemu/*
#%{_dosemudir}/bootdir/command.com
%{_mandir}/man1/[dm]*
%{_mandir}/man1/xdos.1*
%lang(pl) %{_mandir}/pl/man1/d*
%lang(pl) %{_mandir}/pl/man1/xdos.1*
%{_applnkdir}/System/*
%{_pixmapsdir}/dosemu.xpm

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
