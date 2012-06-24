%define         _kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null| cut -d'"' -f2)
#%define         _kernel_ver_str %(echo %{_kernel_ver} | sed s/-/_/g)
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(tr):	DOS �yk�n�mc�s�
Name:		dosemu
Version:	1.0.2
Release:	1
License:	distributable
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://ftp.dosemu.org/dosemu/%{name}-%{version}.tgz
Source1:	%{name}-pl-man-pages.tar.bz2
Source2:	dosemu-sys.tar.gz
Source3:	http://prdownloads.sourceforge.net/freedos/ke2025c16.zip
Source4:	autoexec2.bat
Source5:	config2.sys
Source6:	keybpl.exe
Source7:	egapl.exe
Source8:	shsucdx.exe
Patch0:		%{name}-dosemu_conf.patch
Patch1:		%{name}-1.0.2-man-pages.patch
URL:		http://www.dosemu.org/
BuildRequires:	bin86
BuildRequires:	unzip
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glibc-static
BuildRequires:	XFree86-static
BuildRequires:	slang-static
Conflicts:	mtools < 3.6
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos-* package.

%description -l es
Esta es una versi�n del emulador DOS que fue proyectada para
ejecutarse en secciones X Window. Ofrece soporte a gr�ficos VGA como
tambi�n soporte a rat�n.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo�esz go uruchomi�
komend� "dos".

Je�li korzystasz z dosowych program�w i chcia�by� je uruchamia�
na twoim Linuksowym systemie zainstaluj dosemu. Mo�esz te�
potrzebowa� pakiet�w dosemu-freedos-*.

%description -l pt_BR
Essa � uma vers�o do emulador DOS que foi projetada para rodar em
sess�es X Window. Oferece suporte para gr�ficos VGA bem como suporte
para mouse.

%package -n xdosemu
Summary:	A DOS emulator for the X Window System
Summary(de):	DOS-Emulator f�r X
Summary(fr):	�mulateur DOS con�u pou �tre lanc� sous X
Summary(tr):	X alt�nda �al��an DOS �yk�n�mc�s�
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Requires:	%{name} = %{version}

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
Window System. Xdosemu provides VGA graphics and mouse support.

Install xdosemu if you need to run DOS programs on your system, and
you'd like to do so with the convenience of graphics support and mouse
capabilities.

%description -l de -n xdosemu
Dies ist eine Version des DOS-Emulators f�r X-Windows-Sitzungen. Er
unterst�tzt VGA-Grafiken und Maus.

%description -l es -n xdosemu
Esta es la versi�n del emulador DOS dibujada para ejecutarse en una
ventana del X Window. Posee soporte para gr�ficos VGA y rat�n.

%description -l fr -n xdosemu
Version de l'�mulateur DOS con�ue pour tourner dans une session X.
Offre une gestion des graphismes VGA et de la souris.

%description -l pl -n xdosemu
Xdosemu jest wersj� emulatora dosemu dzia�aj�c� w X Window System.
Xdosemu ma wsparcie dla grafiki VGA i obs�ugi myszki.

%description -l pt_BR -n xdosemu
Esta � a vers�o do emulador DOS desenhada para rodar em uma janela do
X Window. Possui suporte a gr�ficos VGA e mouse.

%description -l tr -n xdosemu
Bu yaz�l�m, DOS �yk�n�mc�s�n�n X alt�nda �al��an bir s�r�m�d�r. VGA
grafikleri ve fare deste�i vard�r.

%package dosnet
Summary:	kernel module dosnet.o
Summary(pl):	Modu� dosnet.o do kernela
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Requires:	%{name} = %{version}
Prereq:		/sbin/depmod

%description dosnet
Kernel module for dosnet (vnet).  Dosnet lets you establish TCP/IP
connection beetween dosemu session and Linux kernel.  Read README
for dosemu for more information.

%description -l pl dosnet
Modu� dosnet.o dla kernela.  Modu� ten pozwala ��czy� si� programom
DOSowym wykorzystuj�cym TCP/IP z Linuksem.  Przydatny mi�dzy innymi
przy pisaniu program�w sieciowych dla DOSa.  Rzeteln� informacj� na
temat dosnet mo�esz znale�� w README do dosemu.   

%prep
%setup -q -a1 -a2
%patch0 -p0
%patch1 -p1

rm -rf freedos
mkdir freedos
unzip -L -o %{SOURCE3} -d freedos

%build
cp base-configure.in configure.in
autoconf
%configure \
	--without-x \
	--enable-linkstatic \
	--enable-new-intcode \
	--enable-aspi
echo | %{__make}
mv -f bin/dosemu.bin bin/dos-nox
%configure \
	--enable-linkstatic \
	--enable-new-intcode \
	--enable-aspi
echo | %{__make}
make -C src/dosext/net/v-net
mv -f bin/dos-nox bin/dos

mv -f man/dosemu.bin.1 man/dos.1

%define _dosemudir /var/lib/dosemu

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_mandir}/man1,%{_mandir}/pl/man1,%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_dosemudir}/bootdir/{dosemu,freedos/doc/fdkernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net

install bin/dosemu.bin $RPM_BUILD_ROOT%{_bindir}/xdos
install bin/dos $RPM_BUILD_ROOT%{_bindir}/dos
install bin/dosdebug $RPM_BUILD_ROOT%{_bindir}/dosdebug
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
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
install src/dosext/net/v-net/dosnet.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net
install freedos/bin/kernel.sys $RPM_BUILD_ROOT%{_dosemudir}/bootdir
install freedos/doc/fdkernel/* $RPM_BUILD_ROOT%{_dosemudir}/bootdir/freedos/doc/fdkernel
ln -sf dosemu/comcom.com $RPM_BUILD_ROOT%{_dosemudir}/bootdir/command.com

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.//g' > doc/$i ; done

rm -f doc/{configuration,dosemu.lsm}

#mv -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/misc \
#	$RPM_BUILD_ROOT%{_fontsdir}


gzip -9nf QuickStart COPYING ChangeLog* doc/*

%clean
rm -rf $RPM_BUILD_ROOT


%post dosnet
depmod -a

%postun dosnet
depmod -a

    
%files
%defattr(644,root,root,755)
%doc *.gz doc/*
%dir %{_dosemudir}
%config(noreplace) %{_sysconfdir}/dosemu.conf
%config(noreplace) %{_sysconfdir}/dosemu.users
#%config(noreplace) %{_dosemudir}/hdimage
%config(noreplace) %{_dosemudir}/global.conf
%attr(755,root,root) %{_bindir}/dos
%attr(755,root,root) %{_bindir}/dosdebug
#%attr(755,root,root) %{_bindir}/dosexec
#%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
#%attr(755,root,root) %{_bindir}/do_mtools
#%attr(755,root,root) %{_bindir}/extract-dos
#%attr(755,root,root) %{_bindir}/mkdexe
#%attr(755,root,root) %{_bindir}/myxcopy
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
#%attr(755,root,root) %{_bindir}/rundos
%dir %{_dosemudir}/bootdir
%dir %{_dosemudir}/bootdir/dosemu
%dir %{_dosemudir}/bootdir/freedos
%{_dosemudir}/bootdir/dosemu/*
%{_dosemudir}/bootdir/kernel.sys
%config(noreplace) %{_dosemudir}/bootdir/autoexec.bat
%config(noreplace) %{_dosemudir}/bootdir/config.sys
%{_dosemudir}/bootdir/command.com
%{_dosemudir}/bootdir/*.exe
%{_dosemudir}/bootdir/freedos/*
%{_mandir}/man1/dos*
%{_mandir}/man1/mkfatimage16.1*
%lang(pl) %{_mandir}/pl/man1/dos*
%{_pixmapsdir}/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xdos
# %attr(755,root,root) %{_bindir}/xtermdos
%{_mandir}/man1/xdos.1*
%lang(pl) %{_mandir}/pl/man1/xdos.1*
# %{_mandir}/man1/xtermdos.1*
# %{_datadir}/fonts/misc/*

%files dosnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/net/dosnet.o
