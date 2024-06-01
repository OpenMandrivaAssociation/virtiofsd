Name:           virtiofsd
Version:        1.10.1
Release:        1
Summary:        Virtio-fs vhost-user device daemon (Rust version)

License:        Apache-2.0 AND BSD-3-Clause
URL:            https://gitlab.com/virtio-fs/virtiofsd
Source:         %{crates_source}
Source1:	cargo-vendor.tar.xz

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging >= 21
BuildRequires:  pkgconfig(libcap-ng)
BuildRequires:  pkgconfig(libseccomp)
Requires:       qemu-common

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version_no_tilde} -p1 -a1
%cargo_prep

cat >>.cargo/config.toml <<'EOF'
[source.vendored-sources]
directory = "vendor"
EOF
sed -i -e 's,replace-with = "local-registry",replace-with = "vendored-sources",g' .cargo/config.toml

%build
%cargo_build

%install
mkdir -p %{buildroot}%{_libexecdir}
install -D -p -m 0755 target/release/virtiofsd %{buildroot}%{_libexecdir}/virtiofsd
install -D -p -m 0644 50-virtiofsd.json %{buildroot}%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%files
%license LICENSE-APACHE LICENSE-BSD-3-Clause
%doc README.md
%{_libexecdir}/virtiofsd
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json
