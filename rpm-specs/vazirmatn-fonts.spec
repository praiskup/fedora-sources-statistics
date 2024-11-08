Version: 33.003
Release: %autorelease
URL:     https://rastikerdar.github.io/vazirmatn

%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          AUTHORS.txt *.md
%global fontdocsex        %{fontlicenses}

%global common_description %{expand:
Vazirmatn (formerly known as Vazir), is a Persian/Arabic typeface family with
a simple and smooth form usable in most contexts. For Latin glyphs, Vazirmatn
is combined with Roboto font, however there is also a version without Latin
glyphs (Non-Latin).
}

# Declaration for the subpackage containing the main font family. Also used as
# source rpm info.
%global fontfamily0       Vazirmatn
%global fontsummary0      A simple and legible Persian/Arabic typeface
%global fontpkgheader0    %{expand:
}
%global fonts0            fonts/ttf/*.ttf
%global fontconfs0        %{SOURCE10}
%global fontdescription0  %{expand: %{common_description}
}

# Declaration for the subpackage containing the NL font family.
%global fontfamily1       Vazirmatn NL
%global fontsummary1      Non-Latin Vazirmatn font
%global fontpkgheader1    %{expand:
}
%global fonts1            misc/Non-Latin/fonts/ttf/*.ttf
%global fontconfs1        %{SOURCE11}
%global fontdescription1  %{expand: %{common_description}

This is the version of the font without Latin glyphs.
}

# Declaration for the subpackage containing the UI font family.
%global fontfamily2       Vazirmatn UI
%global fontsummary2      Vazirmatn UI font
%global fontpkgheader2    %{expand:
}
%global fonts2            misc/UI/fonts/ttf/*.ttf
%global fontconfs2        %{SOURCE12}
%global fontdescription2  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI.
}

# Declaration for the subpackage containing the UI NL font family.
%global fontfamily3       Vazirmatn UI NL
%global fontsummary3      Non-Latin Vazirmatn UI font
%global fontpkgheader3    %{expand:
}
%global fonts3            misc/UI-Non-Latin/fonts/ttf/*.ttf
%global fontconfs3        %{SOURCE13}
%global fontdescription3  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI and without Latin glyphs.
}

# Declaration for the subpackage containing the RD font family.
%global fontfamily4       Vazirmatn RD
%global fontsummary4      A variant of Vazirmatn using round dots instead of cubic ones
%global fontpkgheader4    %{expand:
}
%global fonts4            Round-Dots/fonts/ttf/*.ttf
%global fontconfs4        %{SOURCE14}
%global fontdescription4  %{expand: %{common_description}

This variant uses round dots including the dots used over or under letters
rather than cubic dots used in original variant.
}

# Declaration for the subpackage containing the RD NL font family.
%global fontfamily5       Vazirmatn RD NL
%global fontsummary5      Non-Latin Vazirmatn RD font
%global fontpkgheader5    %{expand:
}
%global fonts5            Round-Dots/misc/Non-Latin/fonts/*/*.ttf
%global fontconfs5        %{SOURCE15}
%global fontdescription5  %{expand: %{common_description}

This variant uses round dots including the dots used over or under letters
rather than cubic dots used in original variant. It also comes without Latin
glyphs.
}

# Declaration for the subpackage containing the RD UI font family.
%global fontfamily6       Vazirmatn RD UI
%global fontsummary6      Vazirmatn RD UI font
%global fontpkgheader6    %{expand:
}
%global fonts6            Round-Dots/misc/UI/fonts/*/*.ttf
%global fontconfs6        %{SOURCE16}
%global fontdescription6  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI.
}

# Declaration for the subpackage containing the RD UI NL font family.
%global fontfamily7       Vazirmatn RD UI NL
%global fontsummary7      Non-Latin Vazirmatn RD UI font
%global fontpkgheader7    %{expand:
}
%global fonts7            Round-Dots/misc/UI-Non-Latin/fonts/*/*.ttf
%global fontconfs7        %{SOURCE17}
%global fontdescription7  %{expand: %{common_description}

This version of the font provides generally smaller height to be more suitable
for UI and without Latin glyphs.
}

# Declaration for the subpackages of the variable versions
%global fontfamily8       %{fontfamily0} VF
%global fontsummary8      %{fontsummary0} (variable version)
%global fontpkgheader8    %{fontpkgheader0}
%global fonts8            fonts/variable/*.ttf
%global fontconfs8        %{fontconfs0}
%global fontdescription8  %{expand:
%{fontdescription0}
This is the variable version of this font.
}

%global fontfamily9       %{fontfamily1} VF
%global fontsummary9      %{fontsummary1} (variable version)
%global fontpkgheader9    %{fontpkgheader1}
%global fonts9            misc/Non-Latin/fonts/variable/*.ttf
%global fontconfs9        %{fontconfs1}
%global fontdescription9  %{expand:
%{fontdescription1}
This is the variable version of this font.
}

%global fontfamily10       %{fontfamily4} VF
%global fontsummary10      %{fontsummary4} (variable version)
%global fontpkgheader10    %{fontpkgheader4}
%global fonts10            Round-Dots/fonts/variable/*.ttf
%global fontconfs10        %{fontconfs4}
%global fontdescription10  %{expand:
%{fontdescription4}
This is the variable version of this font.
}

%global fontfamily11       %{fontfamily5} VF
%global fontsummary11      %{fontsummary5} (variable version)
%global fontpkgheader11    %{fontpkgheader5}
%global fonts11            Round-Dots/misc/Non-Latin/fonts/variable/*.ttf
%global fontconfs11        %{fontconfs5}
%global fontdescription11  %{expand:
%{fontdescription5}
This is the variable version of this font.
}

Source0:  https://github.com/rastikerdar/vazirmatn/releases/download/v%{version}/vazirmatn-v%{version}.zip
Source10: 55-%{fontpkgname0}.conf
Source11: 55-%{fontpkgname1}.conf
Source12: 62-%{fontpkgname2}.conf
Source13: 62-%{fontpkgname3}.conf
Source14: 55-%{fontpkgname4}.conf
Source15: 55-%{fontpkgname5}.conf
Source16: 62-%{fontpkgname6}.conf
Source17: 62-%{fontpkgname7}.conf

# Generate the font subpackage headers
%fontpkg -a

# Generate a font meta(sub)package header for all the font subpackages generated in this spec.
%fontmetapkg

%prep
%setup -q -c
%linuxtext *.txt

%build
%fontbuild -a
sed -i 's/VF/(Variable)/' org*.xml

%install
%{lua:
for i = 0, 7 do
    print(rpm.expand('%fontinstall -z ' .. i))
end}
# Remove shared symlinks to prevent errors during fontinstall
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/55-*
%{lua:
for i = 8, 11 do
    print(rpm.expand('%fontinstall -z ' .. i))
end}

%check
%fontcheck -a

%fontfiles -a

%changelog
%autochangelog
