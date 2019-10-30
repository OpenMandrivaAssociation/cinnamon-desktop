%global _internal_version                 e02d319
%global gtk3_version                      3.3.6
%global glib2_version                     2.33.3
%global startup_notification_version      0.5
%global gtk_doc_version                   1.9
%global po_package                        cinnamon-desktop-3.0
%global date				  20141107

%define major   4
%define cvcmaj  0
%define girmajor   1.0
%define libname %mklibname %{name} %{major}
%define libcvcname %mklibname cvc %{cvcmaj}

%define libdev  %mklibname %{name} -d
%define girlib    %mklibname %{name}-gir %{girmajor}


Summary: Shared code among cinnamon-session, nemo, etc
Name:    cinnamon-desktop
Version: 4.2.0
Release: 1
License: GPLv2+ and LGPLv2+ add MIT
Group:   Graphical desktop/Other
URL:     http://cinnamon.linuxmint.com

Source0: cinnamon-desktop-%{version}.tar.gz

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
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libpulse-mainloop-glib)
BuildRequires: meson

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

%package -n %libcvcname
Summary:  Libraries for %name
License:  LGPLv2+
Group:    System/Libraries

%description -n %libcvcname
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
Requires: %{libcvcname} = %{version}-%{release}

Requires: pkgconfig(gtk+-3.0)
Requires: pkgconfig(glib-2.0)
Requires: startup-notification-devel >= %{startup_notification_version}

%description -n %libdev
Libraries and header files for the CINNAMON-internal private library
libcinnamondesktop.

%prep
%setup -q

%build
%meson -Dpnp_ids="%{_datadir}/misc/pnp.ids"
%meson_build

%install
%{meson_install}

# stuff we don't want
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%find_lang %{po_package} --all-name --with-gnome

%files -f %{po_package}.lang
%doc AUTHORS COPYING COPYING.LIB README
%{_datadir}/glib-2.0/schemas/org.cinnamon.*.xml

%files -n %libname
%{_libdir}/libcinnamon-desktop*.so.%{major}*

%files -n %libcvcname
%{_libdir}/libcvc.so.%{cvcmaj}*

%files -n %{girlib}
%{_libdir}/girepository-1.0/C*-*.0.typelib

%files -n %libdev
%{_libdir}/libcinnamon-desktop.so
%{_libdir}/libcvc.so
%{_libdir}/pkgconfig/cinnamon-desktop.pc
%{_libdir}/pkgconfig/cvc.pc
%{_includedir}/cinnamon-desktop/
%{_datadir}/gir-1.0/C*-*.0.gir


