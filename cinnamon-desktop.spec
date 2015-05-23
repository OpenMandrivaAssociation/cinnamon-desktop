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
Release: 1
License: GPLv2+ and LGPLv2+ add MIT
Group:   Graphical desktop/Other
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

Requires: pkgconfig(gtk+-3.0)
Requires: pkgconfig(glib-2.0)
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
