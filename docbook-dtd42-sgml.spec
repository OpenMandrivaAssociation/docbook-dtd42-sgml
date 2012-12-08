%define name docbook-dtd42-sgml
%define version 1.0
%define release %mkrel 7
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

 


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-7mdv2011.0
+ Revision: 663823
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2011.0
+ Revision: 609147
- rebuild

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 1.0-5mdv2010.0
+ Revision: 428309
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.0-4mdv2009.0
+ Revision: 266571
- rebuild early 2009.0 package (before pixel changes)

* Sat May 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-3mdv2009.0
+ Revision: 210926
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue May 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-2mdv2008.0
+ Revision: 29882
- patch catalog for ignoring ISO entity sets, as version 4.1


* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.com> 1.0-12mdv2008.0
+ Revision: 18836
- rebuild for new era

  + Mandriva <devel@mandriva.com>


* Fri Sep 02 2005 Camille Begnis <camille@mandriva.com> 1.0-11mdk
- rebuild

* Mon Jul 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-10mdk
- Fix postun script

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-9mdk
- Fix uninstall when xmlcatalog is no longer present

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-8mdk
- Add some ghost/config files to package
- Fix upgrade

* Mon May 05 2003 <camille@ke.mandrakesoft.com> 1.0-7mdk
- Rebuild

* Tue Apr 02 2002 Camille Begnis <camille@mandrakesoft.com> 1.0-6mdk
- remove crappy %% {openjadever} (thanks gc)

* Thu Jan 24 2002 Camille Begnis <camille@mandrakesoft.com> 1.0-5mdk
- use xmlcatalog from libxml-utils instead of install-catalog

* Mon Jun 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0-4mdk
- Merge patches from Abel Cheung:
- Simplify %%files
- Source is not downloadable itself, it's just a re-compressed archive
- Removed useless variable
- Corrected file permissions
- More macros
- Rearrange BuildArch to bottom, no idea why source and patch refuses to be
  removed otherwise

* Tue Mar 13 2001 Camille Begnis <camille@mandrakesoft.com> 1.0-3mdk
- Redirect install-catalog output to /dev/null

* Thu Oct 19 2000 Camille Begnis <camille@mandrakesoft.com> 1.0-2mdk
- put DTD version in %%{dtdver}

* Wed Aug 23 2000 Camille Begnis <camille@mandrakesoft.com> 1.0-1mdk
- adapt spec from Eric Bischoff <ebisch@cybercable.tm.fr>
- Obsoletes docbook
- Pre-LSB compliance

