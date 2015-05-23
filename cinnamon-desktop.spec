%global _internal_version                 e02d319
%global gtk3_version                      3.3.6
%global glib2_version                     2.33.3
%global startup_notification_version      0.5
%global gtk_doc_version                   1.9
%global po_package                        cinnamon-desktop-3.0
%global date				  20141107

%define major   4
%define girmajor   1.0
%define libname %mklibname %{name} %{major}
%define libdev  %mklibname %{name} -d
%define girlib    %mklibname %{name}-gir %{girmajor}


Summary: Shared code among cinnamon-session, nemo, etc
Name:    cinnamon-desktop
Version: 2.4.2
Release: %mkrel 1
License: GPLv2+ and LGPLv2+ add MIT
Group:   Graphical desktop/Cinnamon
URL:     http://cinnamon.linuxmint.com

Source0: cinnamon-desktop-%{version}.tar.gz
#SourceGet0: https://github.com/linuxmint/cinnamon-desktop/archive/%{version}.tar.gz
#Source0: cinnamon-desktop-%{version}.git%{_internal_version}.tar.gz
##SourceGet0: https://github.com/linuxmint/cinnamon-desktop/tarball/%{_internal_version}

# Make sure that gnome-themes-standard gets pulled in for upgrades
Requires: gnome-themes-standard

BuildRequires: gnome-common
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: gobject-introspection-devel
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xkeyboard-config)
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: intltool
BuildRequires: itstool

%description

The cinnamon-desktop package contains an internal library
(libcinnamondesktop) used to implement some portions of the CINNAMON
desktop, and also some data files and other shared components of the
CINNAMON user environment.

#--------------------------------------------------------------------

%package -n %libname
Summary:  Libraries for %name
License:  LGPLv2+
Group:    System/Libraries

%description -n %libname
Libraries for %name

#--------------------------------------------------------------------

%package -n %{girlib}
Summary: GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libname} = %{version}-%{release}

%description -n %{girlib}
GObject introspection interface library for %{name}.

#--------------------------------------------------------------------

%package -n %libdev
Summary:  Libraries and headers for libcinnamon-desktop
License:  LGPLv2+
Group:    Development/C
Requires: %{libname} = %{version}-%{release}

Requires: gtk3-devel >= %{gtk3_version}
Requires: glib2-devel >= %{glib2_version}
Requires: startup-notification-devel >= %{startup_notification_version}

%description -n %libdev
Libraries and header files for the CINNAMON-internal private library
libcinnamondesktop.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --with-pnp-ids-path="%{_datadir}/misc/pnp.ids"
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make V=1 

%install
%{make_install}

# stuff we don't want
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%find_lang %{po_package} --all-name --with-gnome

%files -f %{po_package}.lang
%doc AUTHORS COPYING COPYING.LIB README
%{_datadir}/glib-2.0/schemas/org.cinnamon.*.xml
%{_libexecdir}/cinnamon-rr-debug
%{_bindir}/cinnamon-desktop-migrate-mediakeys

%files -n %libname
%{_libdir}/libcinnamon-desktop*.so.%{major}*

%files -n %{girlib}
%{_libdir}/girepository-1.0/C*-3.0.typelib

%files -n %libdev
%{_libdir}/libcinnamon-desktop.so
%{_libdir}/pkgconfig/cinnamon-desktop.pc
%{_includedir}/cinnamon-desktop/
%{_datadir}/gir-1.0/C*-3.0.gir


%changelog
* Thu Nov 27 2014 joequant <joequant> 2.4.2-1.mga5
+ Revision: 799543
- 2.4.2

* Sun Nov 23 2014 joequant <joequant> 2.4.1-1.mga5
+ Revision: 798406
- upgrade to 2.4

* Wed Oct 15 2014 umeabot <umeabot> 2.2.3-5.mga5
+ Revision: 745259
- Second Mageia 5 Mass Rebuild

* Sun Sep 28 2014 tv <tv> 2.2.3-4.mga5
+ Revision: 731111
- rebuild so that it picks typelib() requires

* Thu Sep 18 2014 umeabot <umeabot> 2.2.3-3.mga5
+ Revision: 693609
- Rebuild to fix library dependencies

* Tue Sep 16 2014 umeabot <umeabot> 2.2.3-2.mga5
+ Revision: 678397
- Mageia 5 Mass Rebuild

* Tue Jun 10 2014 joequant <joequant> 2.2.3-1.mga5
+ Revision: 635329
- upgrade to 2.2.3

* Thu May 15 2014 joequant <joequant> 2.2.2-1.mga5
+ Revision: 622879
- upgrade to 2.2.2

* Fri Apr 18 2014 joequant <joequant> 2.2.0-1.mga5
+ Revision: 616819
- upgrade to 2.2

* Wed Jan 08 2014 joequant <joequant> 2.0.4-3.mga4
+ Revision: 565561
- push to core/release

* Wed Jan 01 2014 joequant <joequant> 2.0.4-2.mga4
+ Revision: 563806
- upgrade to 2.0.4

* Tue Oct 22 2013 umeabot <umeabot> 2.0.1-2.mga4
+ Revision: 542039
- Mageia 4 Mass Rebuild

* Mon Oct 14 2013 joequant <joequant> 2.0.1-1.mga4
+ Revision: 496762
- update to 2.0.1

* Mon Oct 07 2013 joequant <joequant> 2.0.0-1.mga4
+ Revision: 492506
- packaged wrong source
- update to 2.0.0

* Tue Oct 01 2013 joequant <joequant> 1.9.1-1.mga4
+ Revision: 490048
- upgrade to 1.9.1

* Thu Sep 19 2013 joequant <joequant> 1.0.0-0.20130905git37ca83b.1.mga4
+ Revision: 481370
- sync with git

* Mon Sep 02 2013 neoclust <neoclust> 1.0.0-0.1.gitea72b22.1.mga4
+ Revision: 474292
- Libify

* Mon Sep 02 2013 joequant <joequant> 1.0.0-0.1.gitea72b22.mga4
+ Revision: 474250
- update to latest git version
- imported package cinnamon-desktop

