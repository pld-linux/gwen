Summary:	GWEN - GUI Without Extravagant Nonsense
Summary(pl.UTF-8):	GWEN - GUI bez ekstrawaganckiego nonsensu
Name:		gwen
Version:	0
%define	snap	20130723
Release:	0.%{snap}.1
License:	MIT
Group:		Libraries
Source0:	%{name}.tar.xz
# Source0-md5:	40fd5f76ab9083174a8f1715a7b3969a
Patch0:		%{name}-sfml2.patch
Patch1:		%{name}-allegro.patch
Patch2:		%{name}-bootil.patch
Patch3:		%{name}-shared.patch
URL:		https://github.com/garrynewman/GWEN
BuildRequires:	SFML-devel >= 2
BuildRequires:	allegro5-devel
BuildRequires:	allegro5-image-devel
BuildRequires:	allegro5-ttf-devel
BuildRequires:	bootil-devel
BuildRequires:	premake >= 4
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GWEN library - GUI Without Extravagant Nonsense.

%description -l pl.UTF-8
GWEN (GUI Without Extravagant Nonsense) to biblioteka GUI bez
ekstrawaganckiego nonsensu.

%package devel
Summary:	Header files for GWEN library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GWEN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GWEN library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GWEN.

%package static
Summary:	Static GWEN library
Summary(pl.UTF-8):	Statyczna biblioteka GWEN
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GWEN library.

%description static -l pl.UTF-8
Statyczna biblioteka GWEN.

%prep
%setup -q -n GWEN
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd gwen/Projects
premake4 gmake
LDFLAGS="%{rpmldflags}" \
%{__make} -C linux/gmake \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS='%{rpmcflags} %{rpmcppflags} $(CPPFLAGS) $(ARCH) -ffast-math -std=c++11' \
	verbose=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install gwen/lib/linux/gmake/lib*.so $RPM_BUILD_ROOT%{_libdir}
install gwen/lib/linux/gmake/libgwen_static.a $RPM_BUILD_ROOT%{_libdir}/libgwen.a
cp -pr gwen/include/Gwen $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md
%attr(755,root,root) %{_libdir}/libgwen.so
%attr(755,root,root) %{_libdir}/libGWEN-Renderer-Allegro.so
%attr(755,root,root) %{_libdir}/libGWEN-Renderer-OpenGL.so
%attr(755,root,root) %{_libdir}/libGWEN-Renderer-OpenGL_DebugFont.so
%attr(755,root,root) %{_libdir}/libGWEN-Renderer-SFML2.so
%attr(755,root,root) %{_libdir}/libGWEN-controlfactory.so
%attr(755,root,root) %{_libdir}/libGWEN-importexport.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/Gwen

%files static
%defattr(644,root,root,755)
%{_libdir}/libgwen.a
