%undefine	_enable_debug_packages

Name:		gpu-viv-bin-mx6q
Version:	1.0.0
Release:	4
Summary:	GPU driver for imx6
License:	Proprietary
Group:		System/Libraries
Url:		http://www.freescale.com/lgfiles/NMG/MAD/YOCTO/
ExclusiveArch:	armv7hl armv7hnl

Source0:	%{name}-3.10.17-%{version}.tar.gz
Source1:	egl.pc
Source2:	egl_x11.pc
Source3:	glesv1_cm.pc
Source4:	glesv1_cm_x11.pc
Source5:	glesv2.pc
Source6:	glesv2_x11.pc
Source7:	vg.pc
Source8:	vg_x11.pc
Patch0:		0001-change-header-path-to-HAL.patch
Patch1:		fix-conflicting-TLS-definition.patch
Patch2:		gc_hal_eglplatform-remove-xlib-undefs.patch
ExclusiveArch:	armv7hl armv7hnl

%description
%{summary}.

%define	libname	%{mklibname %{name}}
%package -n	%{libname}
Summary:	Libraries for imx6 GPU driver
Group:		System/Libraries
Requires:	wandboard-support-vpu-firmware
# XXX: soname is libGL.so.1.2 rather than libGL.so.1...
Provides:	libGL.so.1
Conflicts:	%{mklibname egl 1}
Provides:	libgl1 = 10.4.0-0.20141106.1:2015.0
Conflicts:	%{mklibname glesv2 2}


%description -n	%{libname}
Libraries for imx6 GPU driver.

%define	devname	%{mklibname -d %{name}}
%package -n	%{devname}
Summary:	Header files & development libraries for imx6 GPU driver
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	opencl-devel
Conflicts:	libopencl-devel
#Requires:	pkgconfig(gl)
%define	__noautoreq	'devel\\(libGAL\\)'
Conflicts:	%{mklibname -d egl}
Conflicts:	%{mklibname -d glesv2}


%description -n	%{devname}
Header files for imx6 GPU driver.

%define	dri_pkg	%{mklibname dri-drivers-vivante}
%package -n	%{dri_pkg}
Summary:	DRI drivers for Vivante chipsets
Group:		System/Libraries

%description -n	%{dri_pkg}
DRI drivers for Vivante chipsets.

%define	dfb_pkg	%{mklibname directfb1.6-gal}
%package -n	%{dfb_pkg}
Summary:	GAL gfx driver for DirectFB
Group:		System/Libraries

%description -n	%{dfb_pkg}
GAL gfx driver for DirectFB.

%prep
%setup -q -n %{name}-3.10.17-%{version}
%autopatch -p1

%build

%install
%makeinstall_std FLOAT_ABI=hardfp USE_DIRECTFB=y
mv %{buildroot}%{_libdir}/libEGL-fb.so %{buildroot}%{_libdir}/libEGL.so.1.0
rm %{buildroot}%{_libdir}/libEGL-wl.so
mv %{buildroot}%{_libdir}/libGLESv2-fb.so %{buildroot}%{_libdir}/libGLESv2.so.2.0.0
ln -sf libGLESv2.so.2 %{buildroot}%{_libdir}/libGLESv2.so
rm %{buildroot}%{_libdir}/libGLESv2-wl.so

mv %{buildroot}%{_libdir}/libGAL-fb.so %{buildroot}%{_libdir}/libGAL.so
rm %{buildroot}%{_libdir}/libGAL-wl.so

mv %{buildroot}%{_libdir}/libVIVANTE-fb.so %{buildroot}%{_libdir}/libVIVANTE.so
rm %{buildroot}%{_libdir}/libVIVANTE-wl.so

mv %{buildroot}%{_libdir}/libOpenVG_3D.so %{buildroot}%{_libdir}/libOpenVG.so
rm %{buildroot}%{_libdir}/libOpenVG_355.so

rm %{buildroot}%{_libdir}/libGL.so
rm %{buildroot}%{_libdir}/{pkgconfig/,}*wayland*
rm -r %{buildroot}/opt

%files -n	%{libname}
%{_libdir}/lib*.so.*
%{_libdir}/libCLC.so
%{_libdir}/libGAL.so
%{_libdir}/libGLES_CL.so
%{_libdir}/libGLES_CM.so
%{_libdir}/libGLSLC.so
%{_libdir}/libOpenCL.so
%{_libdir}/libOpenVG.so
%{_libdir}/libVDK.so
%{_libdir}/libVIVANTE.so


%files -n %{devname}
%{_includedir}/*
%{_libdir}/libEGL.so
%{_libdir}/libGLESv1_CL.so
%{_libdir}/libGLESv1_CM.so
%{_libdir}/libGLESv2.so

#%{_libdir}/libGL.so
%{_libdir}/pkgconfig/*.pc

%files -n %{dri_pkg}
%{_libdir}/dri/vivante_dri.so

%files -n %{dfb_pkg}
%config(noreplace) %{_sysconfdir}/directfbrc
%{_libdir}/directfb-*
