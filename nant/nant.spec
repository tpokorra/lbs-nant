%define name nant
%define version 0.92.999
%define MonoPath /usr/
%define NantGitTimestamp 7906a4d7e903b0ee26c466fefa58d7ba730f534c

Summary: some development tools for Mono
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development
Requires: pkgconfig mono libgdiplus libgdiplus-devel liberation-mono-fonts
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch mono pkgconfig
BuildRoot: /tmp/buildroot
Source: %{NantGitTimestamp}.tar.gz

%description
some development tools for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup  -q -n nant-%{NantGitTimestamp}

%build
# Configure and make source
make prefix=%{MonoPath}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install prefix=%{MonoPath}
sed -i 's#/bin/mono#/bin/mono --runtime=v4.0#g' %{buildroot}%{MonoPath}/bin/nant

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%post

%changelog
* Wed Feb 11 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build for Xamarin Mono packages
* Thu Jun 19 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- upgrade to latest version from Github Nant
* Thu Jul 11 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- using separate package mono-opt-libgdiplus
* Sat Jun 01 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build

