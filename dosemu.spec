Summary:	A DOS emulator.
Name:		dosemu
Version:	0.99.13
Release:	2
Copyright:	distributable
Group:		Applications/Emulators
Source0:	ftp://ftp.dosemu.org/dosemu/dosemu-%{version}.tgz
Source1:	http://www.freedos.org/files/distributions/base1.zip
Source2:	http://www.freedos.org/files/distributions/util1.zip
Source3:	http://www.freedos.org/files/distributions/edit1.zip
Source4:	ftp://ftp.gcfl.net/freedos/kernel/latestbin.zip
Source5:	ftp://ftp.simtel.net/pub/simtelnet/msdos/editor/vim53d16.zip
Source6:	ftp://ftp.simtel.net/pub/simtelnet/msdos/editor/vim53rt.zip
Source7:	autoexec.bat
Source8:	config.sys
Patch0:		dosemu-0.66.7-config.patch
Patch1:		dosemu-0.66.7-glibc.patch
Patch2:		dosemu-0.66.7-pushal.patch
Patch3:		dosemu-0.98.1-security.patch
Patch4:		dosemu-0.98.1-justroot.patch
Patch5:		dosemu-make.patch
BuildRequires:	mtools
Requires:	kernel >= 2.0.28, mtools >= 3.6
Url:		http://www.dosemu.org
Exclusivearch:	%{ix86}
Buildroot:	/tmp/%{name}-%{version}-root

%description
Dosemu is a DOS emulator.  Once you've installed dosemu, start the DOS
emulator by typing in the dos command.

You need to install dosemu if you use DOS programs and you want to be able
to run them on your Red Hat Linux system.  You may also need to install
the dosemu-freedos package.

%package -n xdosemu
Requires:	%{name} = %{version}
Summary:	A DOS emulator for the X Window System.
Group:		Applications/Emulators

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
]Window System.  Xdosemu provides VGA graphics and mouse support.

Install xdosemu if you need to run DOS programs on your system, and you'd
like to do so with the convenience of graphics support and mouse
capabilities.

%package freedos
Requires:	%{name} = %{version}
Summary	:	A FreeDOS hdimage for dosemu, a DOS emulator, to use.
Group:		Applications/Emulators

%description freedos
Generally, the dosemu DOS emulator requires either that your system
have some version of DOS available or that your system's partitions
were formatted and installed with DOS. If your system does not meet
either of the previous requirements, you can instead use the dosemu-
freedos package, which contains an hdimage file which will be
installed in teh /var/lib/dosemu directory. The hdimage file is
already bootable with FreeDOS.

You will need to edit your /etc/dosemu.conf file to add the
image to the list of disk 'drives' used by dosemu.

Install dosemu-freedos if you are installing the dosemu package
and you don't have a version of DOS available on your system,
and your system's partitions were not formatted and installed
with DOS.

%prep
%setup -q
%patch0 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

rm -rf freedos
mkdir freedos
mkdir freedos/kernel
mkdir freedos/tmp
mkdir freedos/vim

unzip -L -d freedos/kernel/ -j $RPM_SOURCE_DIR/latestbin.zip
cp -f contrib/dosC/dist/* freedos/kernel
for i in $RPM_SOURCE_DIR/{base1.zip,edit1.zip,util1.zip}; do
	unzip -L -d freedos/tmp $i
done
for i in freedos/tmp/*.zip ; do 
	unzip -L -o -d freedos $i
done
unzip -L -o -d freedos $RPM_SOURCE_DIR/vim53rt.zip
unzip -L -o -d freedos/vim-5.3 $RPM_SOURCE_DIR/vim53d16.zip

%build
./default-configure --without-x
echo | make
mv bin/dos bin/dos-nox
./default-configure
echo | make
mv bin/dos bin/dos-x
mv bin/dos-nox bin/dos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc,%{_mandir}/man1,%{_datadir}/icons,/var/state/dosemu}

make install INSTROOT=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_bindir}/xdos

install bin/dos-x $RPM_BUILD_ROOT%{_bindir}/xdos
install setup-hdimage $RPM_BUILD_ROOT%{_bindir}
install src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT%{_bindir}
install etc/dosemu.xpm $RPM_BUILD_ROOT%{_datadir}/icons
install etc/dosemu.users.secure $RPM_BUILD_ROOT/etc/dosemu.users
src/tools/periph/mkfatimage16 -p -k 16192 -l FreeDos \
	-b freedos/kernel/boot.bin \
	-f $RPM_BUILD_ROOT/var/state/dosemu/hdimage.freedos \
	freedos/kernel/* 
FREEDOS=`/bin/mktemp /tmp/freedos.XXXXXX`
echo "drive n: file=\"$RPM_BUILD_ROOT/var/state/dosemu/hdimage.freedos\" offset=8832" > $FREEDOS
MTOOLSRC=$FREEDOS
export MTOOLSRC
mcopy -o/ freedos/vim-5.3 freedos/bin freedos/doc freedos/help freedos/emacs n:
mmd n:/DOSEMU
mcopy -/ commands/* n:/DOSEMU
mcopy -o $RPM_SOURCE_DIR/autoexec.bat $RPM_SOURCE_DIR/config.sys commands/exitemu* n:/
mdir -w n:
rm -f $FREEDOS
unset MTOOLSRC

install -m 644 etc/hdimage.dist $RPM_BUILD_ROOT/var/state/dosemu/hdimage
# install dexe utils
install -m 755 dexe/{do_mtools,extract-dos,mkdexe,myxcopy} $RPM_BUILD_ROOT%{_bindir}

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/rundos
#!/bin/sh
BINDIR=/bin
export BINDIR 
# ignore errors if user does not have module installed
%{_bindir}/dos
EOF

# Strip things
strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/* || :

# Take out irritating ^H's from the documentation
for i in `ls --color=no doc/` ; do cat doc/$i > $i ; cat $i | perl -p -e 's/.//g' > doc/$i ; done

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/* \
	QuickStart doc/*

%clean
rm -rf $RPM_BUILD_ROOT
rm -f dosemu.files

%post -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/X11R6/lib/X11/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 || :

%postun -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/X11R6/lib/X11/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 || :

%post freedos
[ -e /var/state/dosemu/hdimage.first ] || \
    ln -s hdimage.freedos /var/state/dosemu/hdimage.first

%postun freedos
if [ $1 = 0 ]; then
	if [ -e /var/state/dosemu/hdimage.first ]; then
		rm -f /var/state/dosemu/hdimage.first
	fi
fi
    
%files
%defattr(644,root,root,755)
%doc QuickStart.gz doc/*
%dir /var/state/dosemu
%config /etc/dosemu.conf
%config /etc/dosemu.users
%config /var/state/dosemu/hdimage
%config /var/state/dosemu/global.conf
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
%{_mandir}/man1/dos.1.gz
%{_mandir}/man1/dosdebug.1.gz
%{_mandir}/man1/mkfatimage16.1.gz
%{_datadir}/icons/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/xdos
%attr(755,root,root) %{_bindir}/xtermdos
%{_mandir}/man1/xdos.1.gz
%{_mandir}/man1/xtermdos.1.gz
/usr/X11R6/lib/X11/fonts/misc/vga.pcf

%files freedos
%config /var/state/dosemu/hdimage.freedos
