Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(fr):	Emulateur DOS
Summary(tr):	DOS �yk�n�mc�s�
Name:		dosemu
Version:	1.0.1
Release:	1
Copyright:	distributable
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://ftp.dosemu.org/dosemu/%{name}-%{version}.tgz
Source1:	http://www.freedos.org/files/distributions/base1.zip
Source2:	http://www.freedos.org/files/distributions/util1.zip
Source3:	http://www.freedos.org/files/distributions/edit1.zip
Source4:	ftp://ftp.gcfl.net/freedos/kernel/ker2019x.zip
Source5:	ftp://ftp.home.vim.org/pub/vim/pc/vim56d16.zip
Source6:	ftp://ftp.home.vim.org/pub/vim/pc/vim56rt.zip
Source7:	autoexec.bat
Source8:	config.sys
Patch0:		%{name}-0.66.7-config.patch
Patch1:		%{name}-0.66.7-glibc.patch
Patch2:		%{name}-0.66.7-pushal.patch
Patch3:		%{name}-0.98.1-security.patch
Patch4:		%{name}-0.98.1-justroot.patch
Patch5:		%{name}-make-new.patch
Patch6:		%{name}m-1.0.0-glibc22.patch
Patch7:		%{name}-1.0.1-broken.patch
BuildRequires:	bin86
BuildRequires:	mtools
Requires:	kernel >= 2.0.28, mtools >= 3.6
Url:		http://www.dosemu.org
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos package.

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

%description -l fr -n xdosemu
Version de l'�mulateur DOS con�ue pour tourner dans une session X.
Offre une gestion des graphismes VGA et de la souris.

%description -l tr -n xdosemu
Bu yaz�l�m, DOS �yk�n�mc�s�n�n X alt�nda �al��an bir s�r�m�d�r. VGA
grafikleri ve fare deste�i vard�r.

%package freedos
Requires:	%{name} = %{version}
Summary:	A FreeDOS hdimage for dosemu, a DOS emulator, to use.
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory

%description freedos
Generally, the dosemu DOS emulator requires either that your system
have some version of DOS available or that your system's partitions
were formatted and installed with DOS. If your system does not meet
either of the previous requirements, you can instead use the dosemu-
freedos package, which contains an hdimage file which will be
installed in the /var/lib/dosemu directory. The hdimage file is
already bootable with FreeDOS.

You will need to edit your /etc/dosemu.conf file to add the image to
the list of disk 'drives' used by dosemu.

Install dosemu-freedos if you are installing the dosemu package and
you don't have a version of DOS available on your system, and your
system's partitions were not formatted and installed with DOS.

%prep
%setup -q
%patch0 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

rm -rf freedos
mkdir freedos
mkdir freedos/kernel
mkdir freedos/tmp
mkdir freedos/vim

unzip -o -L -d freedos/kernel/ -j $RPM_SOURCE_DIR/ker2019x.zip
cp -f contrib/dosC/dist/* freedos/kernel
for i in $RPM_SOURCE_DIR/{base1.zip,edit1.zip,util1.zip}; do
	unzip -o -L -d freedos/tmp $i
done
for i in freedos/tmp/*.zip ; do 
	unzip -o -L -o -d freedos $i
done
unzip -L -o -d freedos $RPM_SOURCE_DIR/vim56rt.zip
unzip -L -o -d freedos/vim-5.6 $RPM_SOURCE_DIR/vim56d16.zip

%build
./default-configure --without-x
echo | make
mv -f bin/dos bin/dos-nox
./default-configure
echo | make
mv -f bin/dos bin/dos-x
mv -f bin/dos-nox bin/dos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1,%{_prefix}/X11R6/share/pixmaps,/var/lib/dosemu}

%{__make} install INSTROOT=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_bindir}/xdos

install bin/dos-x $RPM_BUILD_ROOT%{_bindir}/xdos
install setup-hdimage $RPM_BUILD_ROOT%{_bindir}
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
install etc/dosemu.xpm $RPM_BUILD_ROOT%{_prefix}/X11R6/share/pixmaps
install etc/dosemu.users.secure $RPM_BUILD_ROOT%{_sysconfdir}/dosemu.users
	src/tools/periph/mkfatimage16 -p -k 16192 -l FreeDos \
	-b freedos/kernel/boot.bin \
	-f $RPM_BUILD_ROOT/var/lib/dosemu/hdimage.freedos \
	freedos/kernel/* 
FREEDOS=`/bin/mktemp /tmp/freedos.XXXXXX`
echo "drive n: file=\"$RPM_BUILD_ROOT/var/lib/dosemu/hdimage.freedos\" offset=8832" > $FREEDOS
MTOOLSRC=$FREEDOS
export MTOOLSRC
mcopy -o/ freedos/vim-5.6 freedos/bin freedos/doc freedos/help freedos/emacs n:
mmd n:/DOSEMU
mcopy -/ commands/* n:/DOSEMU
mcopy -o $RPM_SOURCE_DIR/autoexec.bat $RPM_SOURCE_DIR/config.sys commands/exitemu* n:/
mdir -w n:
rm -f $FREEDOS
unset MTOOLSRC

install etc/hdimage.dist $RPM_BUILD_ROOT/var/lib/dosemu/hdimage
# install dexe utils
install dexe/{do_mtools,extract-dos,mkdexe,myxcopy} $RPM_BUILD_ROOT%{_bindir}

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/rundos
#!/bin/sh
BINDIR=/bin
export BINDIR 
# ignore errors if user does not have module installed
%attr(755,root,root) %{_bindir}/dos
EOF

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.//g' > doc/$i ; done

gzip -9nf QuickStart doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/X11R6/lib/X11/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%postun -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/X11R6/lib/X11/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%post freedos
[ -e /var/lib/dosemu/hdimage.first ] || \
    ln -s hdimage.freedos /var/lib/dosemu/hdimage.first

%postun freedos
if [ "$1" =" 0" ]; then
	if [ -e /var/lib/dosemu/hdimage.first ]; then
		rm -f /var/lib/dosemu/hdimage.first
	fi
fi
    
%files
%defattr(644,root,root,755)
%doc QuickStart.gz doc/*
%dir /var/lib/dosemu
%config %{_sysconfdir}/dosemu.conf
%config %{_sysconfdir}/dosemu.users
%config /var/lib/dosemu/hdimage
%config /var/lib/dosemu/global.conf
%attr(4755,root,root) %{_bindir}/dos
%attr(755,root,root) %{_bindir}/dosdebug
%attr(755,root,root) %{_bindir}/dosexec
%attr(755,root,root) %{_bindir}/dexeconfig
%attr(755,root,root) %{_bindir}/hdinfo
%attr(755,root,root) %{_bindir}/do_mtools
%attr(755,root,root) %{_bindir}/extract-dos
%attr(755,root,root) %{_bindir}/mkdexe
%attr(755,root,root) %{_bindir}/myxcopy
%attr(755,root,root) %{_bindir}/mkhdimage
%attr(755,root,root) %{_bindir}/mkfatimage16
%attr(755,root,root) %{_bindir}/rundos
%attr(755,root,root) %{_bindir}/setup-hdimage
%{_mandir}/man1/dos.1*
%{_mandir}/man1/dosdebug.1*
%{_mandir}/man1/mkfatimage16.1*
%{_prefix}/X11R6/share/pixmaps/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/xdos
# %attr(755,root,root) %{_bindir}/xtermdos
%{_mandir}/man1/xdos.1*
# %{_mandir}/man1/xtermdos.1*
%{_prefix}/X11R6/lib/X11/fonts/misc/vga.pcf

%files freedos
%defattr(644,root,root,755)
%config /var/lib/dosemu/hdimage.freedos
