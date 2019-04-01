Name:               greenboot
Version:            0.7
Release:            1%{?dist}
Summary:            Generic Health Check Framework for systemd
License:            LGPLv2+

%global repo_owner  LorbusChris
%global repo_name   %{name}
%global repo_tag    v%{version}

URL:                https://github.com/%{repo_owner}/%{repo_name}
Source0:            https://github.com/%{repo_owner}/%{repo_name}/archive/%{repo_tag}.tar.gz

BuildArch:          noarch
BuildRequires:      systemd-rpm-macros
%{?systemd_requires}
Requires:           systemd

%description
%{summary}.

%package auto-update-fallback
Summary:            Automatic updates and failure fallback for rpm-ostree-based system 
Requires:           %{name} = %{version}-%{release}
Requires:           %{name}-reboot = %{version}-%{release}
Requires:           %{name}-rpm-ostree-grub2 = %{version}-%{release}

%description auto-update-fallback
%{summary}.

%package status
Summary:            Message of the Day updater for greenboot
Requires:           %{name} = %{version}-%{release}
# PAM is required to programatically read motd messages from /etc/motd.d/*
Requires:           pam >= 1.3.1-15
# While not strictly necessary to generate the motd, the main use-case of this package is to display it on SSH login
Recommends:         openssh

%description status
%{summary}.

%package rpm-ostree-grub2
Summary:            Scripts for greenboot on rpm-ostree-based systems using the Grub2 bootloader
Requires:           %{name} = %{version}-%{release}
Requires:           %{name}-grub2 = %{version}-%{release}

%description rpm-ostree-grub2
%{summary}.

%package grub2
Summary:            Grub2 specific scripts for greenboot
Requires:           %{name} = %{version}-%{release}

%description grub2
%{summary}.

%package reboot
Summary:            Reboot on red status for greenboot
Requires:           %{name} = %{version}-%{release}

%description reboot
%{summary}.

%prep
%setup

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/check/required.d
mkdir    %{buildroot}%{_sysconfdir}/%{name}/check/wanted.d
mkdir    %{buildroot}%{_sysconfdir}/%{name}/green.d
mkdir    %{buildroot}%{_sysconfdir}/%{name}/red.d
mkdir -p %{buildroot}%{_unitdir}
install -DpZm 0755 usr/libexec/greenboot/greenboot %{buildroot}%{_libexecdir}/%{name}/%{name}
install -DpZm 0755 usr/libexec/greenboot/greenboot-grub2-set-counter %{buildroot}%{_libexecdir}/%{name}/greenboot-grub2-set-counter
install -DpZm 0755 usr/libexec/greenboot/greenboot-rpm-ostree-grub2-check-fallback %{buildroot}%{_libexecdir}/%{name}/greenboot-rpm-ostree-grub2-check-fallback
install -DpZm 0755 usr/libexec/greenboot/greenboot-status %{buildroot}%{_libexecdir}/%{name}/greenboot-status
install -DpZm 0644 usr/lib/motd.d/boot-status %{buildroot}%{_exec_prefix}/lib/motd.d/boot-status
install -DpZm 0644 usr/lib/systemd/system/* %{buildroot}%{_unitdir}
install -DpZm 0644 usr/lib/tmpfiles.d/greenboot-status-motd.conf %{buildroot}%{_tmpfilesdir}/greenboot-status-motd.conf
install -DpZm 0755 etc/greenboot/check/required.d/* %{buildroot}%{_sysconfdir}/%{name}/check/required.d
install -DpZm 0755 etc/greenboot/check/wanted.d/* %{buildroot}%{_sysconfdir}/%{name}/check/wanted.d

%post
%systemd_post greenboot-healthcheck.service
%systemd_post greenboot.service
%systemd_post redboot.service
%systemd_post redboot.target

%post grub2
%systemd_post greenboot-grub2-set-counter.service
%systemd_post greenboot-grub2-set-success.service

%post reboot
%systemd_post redboot-auto-reboot.service

%post rpm-ostree-grub2
%systemd_post greenboot-rpm-ostree-grub2-check-fallback.service

%post status
%systemd_post greenboot-status.service

%preun
%systemd_preun greenboot-healthcheck.service
%systemd_preun greenboot.service
%systemd_preun redboot.service
%systemd_preun redboot.target

%preun grub2
%systemd_preun greenboot-grub2-set-counter.service
%systemd_preun greenboot-grub2-set-success.service

%preun rpm-ostree-grub2
%systemd_preun greenboot-rpm-ostree-grub2-check-fallback.service

%preun status
%systemd_preun greenboot-status.service

%postun
%systemd_postun greenboot-healthcheck.service
%systemd_postun greenboot.service
%systemd_postun redboot.service
%systemd_postun redboot.target

%postun grub2
%systemd_postun greenboot-grub2-set-counter.service
%systemd_postun greenboot-grub2-set-success.service

%postun rpm-ostree-grub2
%systemd_postun greenboot-rpm-ostree-grub2-check-fallback.service

%postun status
%systemd_postun greenboot-status.service

%files
%doc README.md
%license LICENSE
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/%{name}
%{_unitdir}/greenboot-healthcheck.service
%{_unitdir}/greenboot.service
%{_unitdir}/redboot.service
%{_unitdir}/redboot.target
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/check
%dir %{_sysconfdir}/%{name}/check/required.d
%{_sysconfdir}/%{name}/check/required.d/00_required_scripts_start.sh
%dir %{_sysconfdir}/%{name}/check/wanted.d
%{_sysconfdir}/%{name}/check/wanted.d/00_wanted_scripts_start.sh
%dir %{_sysconfdir}/%{name}/green.d
%dir %{_sysconfdir}/%{name}/red.d

%files status
%{_exec_prefix}/lib/motd.d/boot-status
%{_libexecdir}/%{name}/greenboot-status
%{_tmpfilesdir}/greenboot-status-motd.conf
%{_unitdir}/greenboot-status.service

%files rpm-ostree-grub2
%{_libexecdir}/%{name}/greenboot-rpm-ostree-grub2-check-fallback
%{_unitdir}/greenboot-rpm-ostree-grub2-check-fallback.service

%files grub2
%{_libexecdir}/%{name}/greenboot-grub2-set-counter
%{_unitdir}/greenboot-grub2-set-success.service
%{_unitdir}/greenboot-grub2-set-counter.service

%files reboot
%{_unitdir}/redboot-auto-reboot.service

%changelog
* Mon Apr 01 2019 Christian Glombek <lorbus@fedoraproject.org> - 0.7-1
- Update to v0.7
- Rename ostree-grub2 subpackage to  rpm-ostree-grub2 to be more explicit
- Add auto-update-fallback meta subpackage

* Wed Feb 13 2019 Christian Glombek <lorbus@fedoraproject.org> - 0.6-1
- Update to v0.6
- Integrate with systemd's boot-complete.target
- Rewrite motd sub-package and rename to status

* Fri Oct 19 2018 Christian Glombek <lorbus@fedoraproject.org> - 0.5-1
- Update to v0.5

* Tue Oct 02 2018 Christian Glombek <lorbus@fedoraproject.org> - 0.4-2
- Spec Review

* Thu Jun 14 2018 Christian Glombek <lorbus@fedoraproject.org> - 0.4-1
- Initial Package
