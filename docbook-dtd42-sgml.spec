%define name docbook-dtd42-sgml
%define version 1.0
%define release %mkrel 4
%define dtdver 4.2
%define mltyp sgml
%define sgmlbase %{_datadir}/sgml

Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:      Publishing
Summary:    SGML document type definition for DocBook %{dtdver}
License:    Artistic style
URL:        http://www.oasis-open.org/docbook/
Source:     http://www.oasis-open.org/docbook/sgml/4.2/docbook-4.2.tar.bz2
Patch:      docbook-dtd42-sgml-1.0.catalog.patch
Provides:   docbook-dtd-sgml
Requires:   sgml-common >= 0.6.3-2mdk
BuildArch:  noarch  
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is SGML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -q -c
%patch -p0

%build

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot}%{sgmlbase}/docbook/sgml-dtd-%{dtdver}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
mkdir -p %{buildroot}%{_sysconfdir}/sgml
touch %{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
touch %{buildroot}%{_sysconfdir}/sgml/catalog

%clean
rm -rf %{buildroot}

%post
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi


%postun
# Do not remove if upgrade
if [ "$1" = "0" -a -x %{_bindir}/xmlcatalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog


  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/openjade/catalog
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi
fi

%files
%defattr(-,root,root)
%doc README ChangeLog
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/catalog
%{sgmlbase}/docbook/sgml-dtd-%{dtdver}

 
