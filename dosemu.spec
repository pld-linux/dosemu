# Conditional build:
# --with static		- linked static 
#
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS �yk�n�mc�s�
Name:		dosemu
Version:	1.0.2
Release:	17
License:	GPL v2
Group:		Applications/Emulators
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/dosemu/%{name}-%{version}.tgz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
Source2:	%{name}-sys.tar.gz
Source3:	%{name}-PRZECZYTAJ_TO
Source4:	%{name}-README.PLD
Patch0:		ftp://ftp.dosemu.org/dosemu/fixes/patch-1.0.2.1.gz
Patch1:		%{name}-1.0.2-man-pages.patch
Patch2:		%{name}-0.98.1-security.patch
Patch3:		%{name}-make-new.patch
Patch4:		%{name}-Polish_keyboard.patch
Patch5:		%{name}-%{name}_conf.patch
Patch6:		%{name}-alt224.patch
Patch7:		pmstack.diff
Patch8:		%{name}-rawkeyboard-console.patch
Patch9:		%{name}-comcom.patch
Patch10:	%{name}-global.conf-xdos.patch
Patch11:	c_run_irqs.diff
URL:		http://www.dosemu.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	perl
BuildRequires:	slang-devel
BuildRequires:	unzip
Requires:	dos
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
Esta es una versi�n del emulador DOS que fue proyectada para
ejecutarse en secciones X Window. Ofrece soporte a gr�ficos VGA como
tambi�n soporte a rat�n.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo�esz go uruchomi�
komend� "dos".

Je�li korzystasz z dosowych program�w i chcia�by� je uruchamia� na
twoim Linuksowym systemie zainstaluj dosemu. Mo�esz te� potrzebowa�
pakiet�w dosemu-freedos-*.

%description -l pt_BR
Essa � uma vers�o do emulador DOS que foi projetada para rodar em
sess�es X Window. Oferece suporte para gr�ficos VGA bem como suporte
para mouse.

%package -n xdosemu
Summary:	A DOS emulator for the X Window System
Summary(de):	DOS-Emulator f�r X
Summary(es):	Emulador DOS que se ejecuta en X
Summary(fr):	�mulateur DOS con�u pou �tre lanc� sous X
Summary(pt_BR):	Emulador DOS que roda no X
Summary(tr):	X alt�nda �al��an DOS �yk�n�mc�s�
Group:		Applications/Emulators
Provides:	dosemu
Obsoletes:	dosemu
Requires:	dos

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
Window System. Xdosemu provides VGA graphics and mouse support.

%description -n xdosemu -l de
Dies ist eine Version des DOS-Emulators f�r X-Windows-Sitzungen. Er
unterst�tzt VGA-Grafiken und Maus.

%description -n xdosemu -l es
Esta es la versi�n del emulador DOS dibujada para ejecutarse en una
ventana del X Window. Posee soporte para gr�ficos VGA y rat�n.

%description -n xdosemu -l fr
Version de l'�mulateur DOS con�ue pour tourner dans une session X.
Offre une gestion des graphismes VGA et de la souris.

%description -n xdosemu -l pl
Xdosemu jest wersj� emulatora dosemu dzia�aj�c� w X Window System.
Xdosemu ma wsparcie dla grafiki VGA i obs�ugi myszki.

%description -n xdosemu -l pt_BR
Esta � a vers�o do emulador DOS desenhada para rodar em uma janela do
X Window. Possui suporte a gr�ficos VGA e mouse.

%description -n xdosemu -l tr
Bu yaz�l�m, DOS �yk�n�mc�s�n�n X alt�nda �al��an bir s�r�m�d�r. VGA
grafikleri ve fare deste�i vard�r.

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
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p0
%patch8 -p0
%patch9 -p1
%patch10 -p1
%patch11 -p0

%build
OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"; export OPTFLAGS

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

#ln -sf dosemu/comcom.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/command.com

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.\010//g' > doc/$i ; done

rm -f doc/{configuration,dosemu.lsm}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc QuickStart COPYING ChangeLog* doc/* PRZECZYTAJ_TO README.PLD
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
%doc QuickStart COPYING ChangeLog* doc/* PRZECZYTAJ_TO README.PLD
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
%{_pixmapsdir}/dosemu.xpm

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
