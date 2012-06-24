Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(tr):	DOS �yk�n�mc�s�
Name:		dosemu
Version:	1.0.1
Release:	5
License:	distributable
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
Source9:	%{name}-pl-man-pages.tar.bz2
Patch0:		%{name}-0.66.7-config.patch
Patch1:		%{name}-0.66.7-glibc.patch
Patch2:		%{name}-0.66.7-pushal.patch
Patch3:		%{name}-0.98.1-security.patch
Patch4:		%{name}-0.98.1-justroot.patch
Patch5:		%{name}-make-new.patch
Patch6:		%{name}m-1.0.0-glibc22.patch
Patch7:		%{name}-1.0.1-broken.patch
Patch8:		%{name}-time.patch
Patch9:		%{name}-man-pages.patch
URL:		http://www.dosemu.org/
BuildRequires:	bin86
BuildRequires:	mtools
BuildRequires:	unzip
BuildRequires:	bison
BuildRequires:	flex
Conflicts:	mtools < 3.6
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28

%description
Dosemu is a DOS emulator. Once you've installed dosemu, start the DOS
emulator by typing in the "dos" command.

You need to install dosemu if you use DOS programs and you want to be
able to run them on your GNU/Linux system. You may also need to
install the dosemu-freedos package.

%description -l pl
Dosemu to Emulator systemu DOS. Po zainstalowaniu mo�esz go uruchomi�
komend� "dos".

Powiniene� zainstalowa� dosemu, je�li korzystasz z dosowych program�w
i chcia�by� je uruchamia� na twoim Linuksowym systemie. Mo�esz te�
potrzebowa� pakiet dosemu-freedos.

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

%description -l pl -n xdosemu
Xdosemu jest wersj� emulatora dosemu dzia�aj�c� w X Window System.
Xdosemu ma wsparcie dla grafiki VGA i obs�ugi myszki.

%description -l tr -n xdosemu
Bu yaz�l�m, DOS �yk�n�mc�s�n�n X alt�nda �al��an bir s�r�m�d�r. VGA
grafikleri ve fare deste�i vard�r.

%package freedos
Summary:	A FreeDOS hdimage for dosemu, a DOS emulator, to use
Summary(pl):	Obraz FreeDOS-a do u�ywania z dosemu
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Requires:	%{name} = %{version}

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

%description -l pl freedos
Og�lnie rzecz bior�c dosemu wymaga posiadania b�d� jakiej� wersji
systemu DOS w systemie, b�d� partycji z zainstalowanym DOSem. Je�li
�aden z tych warunk�w nie jest spe�niony, to mo�esz w zast�pstwie u�y�
pakietu dosemu-freedos. Zawiera on obraz obraz dysku (kt�ry b�dzie
zainstalowany w katalogu /var/lib/dosemu) z zainstalowanym FreeDOSem.

Musisz wyedytowa� plik /etc/dosemu.conf aby doda� ten plik do listy
'drives' uzywanych przez dosemu.

Zainstaluj dosemu-freedos, je�li zainstalowa�e� pakiet dosemu, a nie
masz dost�pnej �adnej innej wersji DOSa.

%prep
%setup -q
%patch0 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

rm -rf freedos
mkdir freedos
mkdir freedos/kernel
mkdir freedos/tmp
mkdir freedos/vim

unzip -o -L -d freedos/kernel/ -j %{SOURCE4}
cp -f contrib/dosC/dist/* freedos/kernel
for i in %{SOURCE1} %{SOURCE3} %{SOURCE2} ; do
	unzip -o -L -d freedos/tmp $i
done
for i in freedos/tmp/*.zip ; do 
	unzip -o -L -o -d freedos $i
done
unzip -L -o -d freedos %{SOURCE6}
unzip -L -o -d freedos/vim-5.6 %{SOURCE5}

%build
./default-configure --without-x
echo | %{__make}
mv -f bin/dos bin/dos-nox
./default-configure
echo | %{__make}
mv -f bin/dos bin/dos-x
mv -f bin/dos-nox bin/dos

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1,%{_pixmapsdir},/var/lib/dosemu,%{_datadir}/fonts}

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
mcopy -o %{SOURCE7} %{SOURCE8} commands/exitemu* n:/
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

rm -f doc/{configuration,dosemu.lsm}

mv -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/fonts/misc \
	$RPM_BUILD_ROOT%{_fontsdir}

bzip2 -dc %{SOURCE9} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

gzip -9nf QuickStart COPYING ChangeLog* doc/* \
	$RPM_BUILD_ROOT%{_fontsdir}/misc/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%postun -n xdosemu
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%post freedos
[ -e /var/lib/dosemu/hdimage.first ] || \
	ln -sf hdimage.freedos /var/lib/dosemu/hdimage.first

%postun freedos
if [ "$1" = "0" ]; then
	if [ -e /var/lib/dosemu/hdimage.first ]; then
		rm -f /var/lib/dosemu/hdimage.first
	fi
fi
    
%files
%defattr(644,root,root,755)
%doc *.gz doc/*
%dir /var/lib/dosemu
%config(noreplace) %{_sysconfdir}/dosemu.conf
%config(noreplace) %{_sysconfdir}/dosemu.users
%config(noreplace) /var/lib/dosemu/hdimage
%config(noreplace) /var/lib/dosemu/global.conf
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
%{_mandir}/man1/dos*
%{_mandir}/man1/mkfatimage16.1*
%lang(pl) %{_mandir}/pl/man1/dos*
%{_pixmapsdir}/dosemu.xpm

%files -n xdosemu
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/xdos
# %attr(755,root,root) %{_bindir}/xtermdos
%{_mandir}/man1/xdos.1*
%lang(pl) %{_mandir}/pl/man1/xdos.1*
# %{_mandir}/man1/xtermdos.1*
%{_datadir}/fonts/misc/*

%files freedos
%defattr(644,root,root,755)
%config /var/lib/dosemu/hdimage.freedos
