# Conditional build:
# --with static	- links statically

%define         _kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null| cut -d'"' -f2)
%define         _kernel_ver_str %(echo %{_kernel_ver} | sed s/-/_/g)
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
%if %{_kernel24}
%define		_moddir		/lib/modules/%{_kernel_ver}/misc
%else
%define		_moddir		/lib/modules/%{_kernel_ver}/net
%endif

Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(tr):	DOS öykünümcüsü
Name:		dosemu
Version:	1.0.2
Release:	2
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
Patch2:		%{name}-0.98.1-justroot.patch
Patch3:		%{name}-0.98.1-security.patch
Patch4:		%{name}-make-new.patch
URL:		http://www.dosemu.org/
BuildRequires:	XFree86-devel
BuildRequires:	bin86
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	slang-devel
BuildRequires:	unzip
%{?_with_static:BuildRequires:	glibc-static}
%{?_with_static:BuildRequires:	XFree86-static}
%{?_with_static:BuildRequires:	slang-static}
Obsoletes:	xdosemu
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28
Conflicts:	mtools < 3.6

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos-* package.

%description -l es
Esta es una versión del emulador DOS que fue proyectada para
ejecutarse en secciones X Window. Ofrece soporte a gráficos VGA como
también soporte a ratón.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo¿esz go uruchomiæ
komend± "dos".

Je¶li korzystasz z dosowych programów i chcia³by¶ je uruchamiaæ
na twoim Linuksowym systemie zainstaluj dosemu. Mo¿esz te¿
potrzebowaæ pakietów dosemu-freedos-*.

%description -l pt_BR
Essa é uma versão do emulador DOS que foi projetada para rodar em
sessões X Window. Oferece suporte para gráficos VGA bem como suporte
para mouse.

%package -n kernel-net-dosnet
Summary:	kernel module dosnet.o
Summary(pl):	Modu³ dosnet.o do kernela
Release:	%{release}@%{_kernel_ver_str}
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Requires:	%{name} = %{version}
Obsoletes:	dosnet
Prereq:		/sbin/depmod

%description -n kernel-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection beetween dosemu session and Linux kernel. Read README
for dosemu for more information.

%description -n kernel-net-dosnet -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOSa. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.   

%prep
%setup -q -a1 -a2
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

rm -rf freedos
mkdir freedos
unzip -q -L -o %{SOURCE3} -d freedos

%build
cp -f base-configure.in configure.in
autoconf
OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"; export OPTFLAGS
%configure \
%{?_with_static:--enable-linkstatic} \
	--enable-new-intcode \
	--enable-aspi
echo | %{__make}

make -C src/dosext/net/v-net

mv -f man/dosemu.bin.1 man/dos.1

%define _dosemudir /var/lib/dosemu

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_mandir}/man1,%{_mandir}/pl/man1,%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_dosemudir}/bootdir/{dosemu,freedos/doc/fdkernel}

install bin/dosemu.bin $RPM_BUILD_ROOT%{_bindir}/dos
install bin/dosdebug $RPM_BUILD_ROOT%{_bindir}/dosdebug
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
ln -sf dos $RPM_BUILD_ROOT%{_bindir}/xdos

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

install -d $RPM_BUILD_ROOT%{_moddir}
install src/dosext/net/v-net/dosnet.o $RPM_BUILD_ROOT%{_moddir}

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.//g' > doc/$i ; done

rm -f doc/{configuration,dosemu.lsm}

gzip -9nf QuickStart COPYING ChangeLog* doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-dosnet
depmod -a

%postun	-n kernel-net-dosnet
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
%{_bindir}/xdos
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
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%{_pixmapsdir}/dosemu.xpm

%files -n kernel-net-dosnet
%defattr(644,root,root,755)
%{_moddir}/dosnet.o
