Summary: A DOS emulator.
Name: dosemu
Version: 0.99.10
Release: 4
Exclusivearch: i386
Copyright: distributable
Group: Applications/Emulators
Source0: ftp://dtp.dosemu.org/dosemu/dosemu-%{PACKAGE_VERSION}.tgz
Source1: http://www.freedos.org/files/fdbeta1.zip
# this kernel is generated from the freedos.144 floppy image coming with the
# above. Why they ship the kernel on the floppy image only ?!
Source2: dosemu-freedos-kernel.tar.gz
Patch0: dosemu-0.66.7-config.patch
Patch1: dosemu-0.66.7-glibc.patch
Patch2: dosemu-0.66.7-pushal.patch
Patch3: dosemu-0.98.1-security.patch
Patch4: dosemu-0.98.1-justroot.patch
Requires: kernel >= 2.0.28, mtools >= 3.6
Url: http://www.dosemu.org
Buildroot: /var/tmp/dosemu-root

%package -n xdosemu
Requires: dosemu = %{PACKAGE_VERSION}
Summary: A DOS emulator for the X Window System.
Group: Applications/Emulators

%package freedos
Requires: dosemu = %{PACKAGE_VERSION}
Summary: A FreeDOS hdimage for dosemu, a DOS emulator, to use.
Group: Applications/Emulators

%description
Dosemu is a DOS emulator.  Once you've installed dosemu, start the DOS
emulator by typing in the dos command.

You need to install dosemu if you use DOS programs and you want to be able
to run them on your Red Hat Linux system.  You may also need to install
the dosemu-freedos package.

%description -n xdosemu
Xdosemu is a version of the dosemu DOS emulator that runs with the X
]Window System.  Xdosemu provides VGA graphics and mouse support.

Install xdosemu if you need to run DOS programs on your system, and you'd
like to do so with the convenience of graphics support and mouse
capabilities.

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
%patch0 -p1 -b .lock
#%patch2 -p1 -b .pushal
%patch3 -p1 -b .security
%patch4 -p1 -b .justroot
unzip -L $RPM_SOURCE_DIR/fdbeta1.zip
rm -rf freedos
mkdir freedos
for i in orlando/{base,sys,util}/?/*.zip ; do
    unzip -d freedos -q $i
done
tar xzf $RPM_SOURCE_DIR/dosemu-freedos-kernel.tar.gz -C freedos

%build
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin
./default-configure
echo | make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
make install INSTROOT=$RPM_BUILD_ROOT
install -m 755 setup-hdimage $RPM_BUILD_ROOT/usr/bin
install -m 755 src/tools/periph/{dexeconfig,hdinfo,mkhdimage,mkfatimage16} $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/icons
install -m 644 etc/dosemu.xpm $RPM_BUILD_ROOT/usr/share/icons
install -m 644 etc/dosemu.users.secure $RPM_BUILD_ROOT/etc/dosemu.users
src/tools/periph/mkfatimage16 -p -k 8192 -l FreeDos \
	-b freedos/kernel/boot.bin \
	-f $RPM_BUILD_ROOT/var/lib/dosemu/hdimage.freedos \
	freedos/kernel/* 
FREEDOS=`/bin/mktemp /tmp/freedos.XXXXXX`
echo "drive n: file=\"$RPM_BUILD_ROOT/var/lib/dosemu/hdimage.freedos\" offset=8832" > $FREEDOS
MTOOLSRC=$FREEDOS
export MTOOLSRC
mcopy -o/ freedos/BIN freedos/DOC freedos/HELP n:
mmd n:/DOSEMU
mcopy -/ commands/* n:/DOSEMU
mcopy commands/exitemu* n:/
mdir -w n:
rm -f $FREEDOS
unset MTOOLSRC

install -m 644 etc/hdimage.dist $RPM_BUILD_ROOT/var/lib/dosemu/hdimage
# install dexe utils
install -m 755 dexe/{do_mtools,extract-dos,mkdexe,myxcopy} $RPM_BUILD_ROOT/usr/bin

cat <<EOF >$RPM_BUILD_ROOT/usr/bin/rundos
#!/bin/sh
BINDIR=/bin
export BINDIR 
# ignore errors if user does not have module installed
/usr/bin/dos
EOF
chmod 0755 $RPM_BUILD_ROOT/usr/bin/rundos

# Strip things
strip $RPM_BUILD_ROOT/usr/bin/* || :

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
[ -e /var/lib/dosemu/hdimage.first ] || \
    ln -s hdimage.freedos /var/lib/dosemu/hdimage.first

%postun freedos
if [ $1 = 0 ]; then
  if [ -e /var/lib/dosemu/hdimage.first ]; then
    rm -f /var/lib/dosemu/hdimage.first
  fi
fi
    
%files
%defattr(-,root,root)
%doc QuickStart doc/*
%dir /var/lib/dosemu
%config /etc/dosemu.conf
%config /etc/dosemu.users
%config /var/lib/dosemu/hdimage
%config /var/lib/dosemu/global.conf
/usr/bin/dos
/usr/bin/dosdebug
/usr/bin/dosexec
/usr/bin/dexeconfig
/usr/bin/hdinfo
/usr/bin/do_mtools
/usr/bin/extract-dos
/usr/bin/mkdexe
/usr/bin/myxcopy
/usr/bin/mkhdimage
/usr/bin/mkfatimage16
/usr/bin/rundos
/usr/bin/setup-hdimage
/usr/man/man1/dos.1
/usr/man/man1/dosdebug.1
/usr/man/man1/mkfatimage16.1
/usr/share/icons/dosemu.xpm

%files -n xdosemu
%defattr(-,root,root)
/usr/bin/xdos
/usr/bin/xtermdos
/usr/man/man1/xdos.1
/usr/man/man1/xtermdos.1
/usr/X11R6/lib/X11/fonts/misc/vga.pcf

%files freedos
%config /var/lib/dosemu/hdimage.freedos

%clean
rm -rf $RPM_BUILD_ROOT
rm -f dosemu.files
