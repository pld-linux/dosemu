# Conditional build:
# --with static		- links statically
# --without dist_kernel	- without distribution kernel
#
%define		_moddir		/lib/modules/%{_kernel_ver}/misc
%define		_moddirsmp	/lib/modules/%{_kernel_ver}smp/misc
%define _rel	14

Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS öykünümcüsü
Name:		dosemu
Version:	1.0.2
Release:	%{_rel}
License:	distributable
Group:		Applications/Emulators
Source0:	ftp://ftp.dosemu.org/dosemu/%{name}-%{version}.tgz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-pl-man-pages.tar.bz2
Source2:	%{name}-sys.tar.gz
Source3:	http://prdownloads.sourceforge.net/freedos/ke2026a16.zip
Source4:	autoexec2.bat
Source5:	config2.sys
Source6:	keybpl.exe
Source7:	egapl.exe
Source8:	shsucdx.exe
Patch0:		ftp://ftp.dosemu.org/dosemu/fixes/patch-1.0.2.1.gz
Patch1:		%{name}-1.0.2-man-pages.patch
Patch2:		%{name}-0.98.1-security.patch
Patch3:		%{name}-make-new.patch
Patch4:		%{name}-Polish_keyboard.patch
Patch5:		%{name}-%{name}_conf.patch
Patch6:		%{name}-alt224.patch
Patch7:		pmstack.diff
Patch8:		%{name}-rawkeyboard-console.patch
URL:		http://www.dosemu.org/
BuildRequires:	XFree86-devel
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	perl
BuildRequires:	slang-devel
BuildRequires:	unzip
%{?_with_static:BuildRequires:	glibc-static}
%{?_with_static:BuildRequires:	XFree86-static}
%{?_with_static:BuildRequires:	slang-static}
Exclusivearch:	%{ix86}
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
Requires:	%{name} = %{version}
Provides:	dosemu
Obsoletes:	dosemu

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

%package -n kernel-net-dosnet
Summary:	kernel module dosnet.o
Summary(pl):	Modu³ dosnet.o do kernela
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection beetween dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -n kernel-net-dosnet -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

%package -n kernel-smp-net-dosnet
Summary:	kernel-smp module dosnet.o
Summary(pl):	Modu³ dosnet.o do kernela SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-smp-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection beetween dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -n kernel-smp-net-dosnet -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

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

rm -rf freedos
mkdir freedos
unzip -q -L -o %{SOURCE3} -d freedos

%build
cp -f base-configure.in configure.in
autoconf
OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"; export OPTFLAGS

%{__cc} $OPTFLAGS -I%{_includedir} -D__KERNEL__ -D__KERNEL_SMP=1 \
	-Wall -Wstrict-prototypes \
	-fno-strength-reduce -I%{_kernelsrcdir}/include -Isrc/include \
	-DMODULE \
	-c -o src/dosext/net/v-net/dosnet.o src/dosext/net/v-net/dosnet.c
mkdir src/dosext/net/v-net/smp
mv -f src/dosext/net/v-net/dosnet.o src/dosext/net/v-net/smp/

%{__cc} $OPTFLAGS -I%{_includedir} -D__KERNEL__ \
	-Wall -Wstrict-prototypes \
	-fno-strength-reduce -I%{_kernelsrcdir}/include -Isrc/include \
	-DMODULE \
	-c -o src/dosext/net/v-net/dosnet.o src/dosext/net/v-net/dosnet.c

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

install %{SOURCE4} $RPM_BUILD_ROOT%{_dosemudir}/bootdir/autoexec.bat
install %{SOURCE5} $RPM_BUILD_ROOT%{_dosemudir}/bootdir/config.sys
install %{SOURCE6} $RPM_BUILD_ROOT%{_dosemudir}/bootdir/keybpl.exe
install %{SOURCE7} $RPM_BUILD_ROOT%{_dosemudir}/bootdir/egapl.exe
install %{SOURCE8} $RPM_BUILD_ROOT%{_dosemudir}/bootdir/shsucdx.exe
install src/plugin/commands/*.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
install dosemu/*.sys $RPM_BUILD_ROOT%{_dosemudir}/bootdir/dosemu
install freedos/bin/kernel.sys $RPM_BUILD_ROOT%{_dosemudir}/bootdir
install freedos/doc/fdkernel/* $RPM_BUILD_ROOT%{_dosemudir}/bootdir/freedos/doc/fdkernel
ln -sf dosemu/comcom.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/command.com

install -d $RPM_BUILD_ROOT{%{_moddir},%{_moddirsmp}}
install src/dosext/net/v-net/dosnet.o $RPM_BUILD_ROOT%{_moddir}
install src/dosext/net/v-net/smp/dosnet.o $RPM_BUILD_ROOT%{_moddirsmp}

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.\010//g' > doc/$i ; done

rm -f doc/{configuration,dosemu.lsm}

gzip -9nf QuickStart COPYING ChangeLog* doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-dosnet
/sbin/depmod -a

%postun	-n kernel-net-dosnet
/sbin/depmod -a

%post	-n kernel-smp-net-dosnet
/sbin/depmod -a

%postun	-n kernel-smp-net-dosnet
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz doc/*
%dir %{_dosemudir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dos
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_bindir}/dosexec
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%dir %{_dosemudir}/bootdir/freedos
%{_dosemudir}/bootdir/dosemu/*
%{_dosemudir}/bootdir/kernel.sys
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/bootdir/autoexec.bat
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/bootdir/config.sys
%{_dosemudir}/bootdir/command.com
%{_dosemudir}/bootdir/*.exe
%{_dosemudir}/bootdir/freedos/*
%{_mandir}/man1/[dm]*
%lang(pl) %{_mandir}/pl/man1/d*
%{_pixmapsdir}/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%doc *.gz doc/*
%dir %{_dosemudir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dosemu.users
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_xbindir}/*
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%dir %{_dosemudir}/bootdir/freedos
%{_dosemudir}/bootdir/dosemu/*
%{_dosemudir}/bootdir/kernel.sys
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/bootdir/autoexec.bat
%config(noreplace) %verify(not size mtime md5) %{_dosemudir}/bootdir/config.sys
%{_dosemudir}/bootdir/command.com
%{_dosemudir}/bootdir/*.exe
%{_dosemudir}/bootdir/freedos/*
%{_mandir}/man1/[dm]*
%{_mandir}/man1/xdos.1*
%lang(pl) %{_mandir}/pl/man1/d*
%lang(pl) %{_mandir}/pl/man1/xdos.1*
%{_pixmapsdir}/dosemu.xpm

%files -n kernel-net-dosnet
%defattr(644,root,root,755)
%{_moddir}/dosnet.o

%files -n kernel-smp-net-dosnet
%defattr(644,root,root,755)
%{_moddirsmp}/dosnet.o

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
