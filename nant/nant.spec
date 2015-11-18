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
AutoReqProv: no
Requires: pkgconfig mono mono-devel libgdiplus0 libgdiplus-devel liberation-mono-fonts
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch mono mono-devel pkgconfig
BuildRoot: /tmp/buildroot
Source: %{NantGitTimestamp}.tar.gz
Patch1: nant-fixmono42_scripttask.patch

# In bootstrap mode, filter requires of the prebuilt DLLs. Some of these
# require older mono runtime, creating broken rpm deps.
%filter_requires_in %{_prefix}/lib/NAnt/
# Also filter provides of the prebuilt DLLs
%filter_provides_in %{_prefix}/lib/NAnt/
%filter_setup

%description
some development tools for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup  -q -n nant-%{NantGitTimestamp}
%patch1 -p1

#Fixes for Mono 4
sed -i "s#gmcs#mcs#g" Makefile
sed -i "s#TARGET=mono-2.0#TARGET=mono-4.0#g" Makefile
sed -i "s#mono/4.0#mono/4.5#g" src/NAnt.Console/App.config
sed -i "s#dmcs#mcs#g" src/NAnt.Console/App.config
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
# Configure and make source
make prefix=%{MonoPath}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install prefix=%{MonoPath}
sed -i 's#/bin/mono#/bin/mono --runtime=v4.0#g' %{buildroot}%{MonoPath}/bin/nant
chmod 555 %{buildroot}%{MonoPath}/bin
chmod 555 %{buildroot}%{MonoPath}/lib

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%post

%changelog
* Wed Nov 18 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- fix for Mono 4.2 for compiling ScriptTasks (see https://github.com/openpetra/openpetra/issues/109)
* Wed Feb 11 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build for Xamarin Mono packages
* Thu Jun 19 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- upgrade to latest version from Github Nant
* Thu Jul 11 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- using separate package mono-opt-libgdiplus
* Sat Jun 01 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build

