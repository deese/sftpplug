# SFTP Plugin for Total Commander

**Version:** 1.0.0  
**License:** BSD-3-Clause (inherited from libssh2)

## Overview

This is a modernized **WFX (Filesystem) plugin** for Total Commander that provides SFTP/SCP connectivity using the libssh2 library with the **Windows CNG (Cryptography API: Next Generation)** backend.

### Key Changes from Legacy Version

- **Build system:** Migrated from Visual Studio 2005 (.vcproj) to Visual Studio 2022 (.vcxproj) + CMake.
- **CI/CD:** Automated builds via GitHub Actions for both Win32 and x64.
- **Dependencies:** Replaced OpenSSL (`libeay32.dll`) with **WinCNG** (native Windows crypto). Only requires `libssh2.dll` and `zlib1.dll` at runtime.
- **Unicode:** Implemented missing Unicode exports (`FsSetAttrW`, `FsStatusInfoW`, `FsDisconnectW`, `FsExtractCustomIconW`, `FsSetCryptCallbackW`).
- **libssh2:** Updated headers to version 1.11.1.
- **Windows 7 compatibility:** Target `_WIN32_WINNT=0x0601`.

## Directory Structure

```
.
├── .github/workflows/     # GitHub Actions CI/CD
├── src/                   # Source code, resources, and project files
│   ├── sftpplug.cpp       # WFX API implementation
│   ├── sftpfunc.cpp       # SFTP/SSH logic using libssh2
│   ├── sftpplug.vcxproj   # Visual Studio 2022 project
│   ├── sftpplug.rc        # Resources (dialogs, strings, VERSIONINFO)
│   └── ...
├── CMakeLists.txt         # CMake build configuration
├── vcpkg.json             # vcpkg manifest (dependencies)
└── AGENTS.md              # This file
```

## Dependencies

| Package | Backend | Purpose |
|---------|---------|---------|
| libssh2 1.11.x | WinCNG | SSH2/SFTP/SCP protocol implementation |
| zlib | - | Compression support for SSH channels |

**No OpenSSL required.** The WinCNG backend uses native Windows APIs (`bcrypt.dll`, `crypt32.dll`) available since Windows Vista.

## Building Locally

### Prerequisites

- Visual Studio 2022 (with C++ workload) **or** Visual Studio Build Tools 2022
- [vcpkg](https://vcpkg.io/) installed and integrated
- CMake 3.20+ (optional, for CMake builds)

### Build with Visual Studio (MSBuild)

1. Open `sftpplug.sln` in Visual Studio 2022.
2. Select **Release** and platform (**Win32** or **x64**).
3. Build solution (`Ctrl+Shift+B`).
4. Output: `wfx/sftpplug.wfx` (Win32) or `wfx/sftpplug.wfx64` (x64).

### Build with CMake

```powershell
# Configure
cmake -B build -S . -A Win32 -DCMAKE_TOOLCHAIN_FILE="$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"

# Build
cmake --build build --config Release

# Output: build/Release/sftpplug.wfx
```

For x64, replace `-A Win32` with `-A x64`.

## Runtime Requirements

Place the following files in the same directory as the plugin, in the Total Commander directory, or in a `64/` / `x64/` subdirectory for the x64 version:

- `sftpplug.wfx` (Win32) / `sftpplug.wfx64` (x64)
- `libssh2.dll`
- `zlib1.dll` (optional, only needed if compression is enabled)

## GitHub Actions CI

The repository includes a workflow (`.github/workflows/build.yml`) that:

1. Installs dependencies via vcpkg using `vcpkg.json`.
2. Builds the plugin for **Win32** and **x64** using both **CMake** and **MSBuild**.
3. Packages the plugin binaries and runtime DLLs as artifacts.

Trigger a build by pushing to `main` or via **Actions > Build SFTP Plugin > Run workflow**.

## Notes for Developers

### Dynamic Loading of libssh2

The plugin does **not** link statically against libssh2. At runtime, it loads `libssh2.dll` dynamically via `LoadLibrary()` and resolves function pointers through `GetProcAddress()`. This is handled in `src/sftpfunc.cpp` (`LoadSSHLib()`) and the generated function pointer table in `src/sshdynfunctions.h`.

### WinCNG vs OpenSSL

Using WinCNG instead of OpenSSL provides several advantages:
- **Zero external crypto DLLs:** Windows provides `bcrypt.dll` and `crypt32.dll` out of the box.
- **Windows 7 compatibility:** OpenSSL 3.x dropped Windows 7 support. WinCNG works on Windows 7 and later.
- **Smaller distribution:** No need to ship `libcrypto-*.dll` or `libeay32.dll`.

### Total Commander API

The plugin implements the WFX API v2.0 (`fsplugin.h`). It supports:
- Directory browsing (`FsFindFirstW`, `FsFindNextW`)
- File transfers (`FsGetFileW`, `FsPutFileW`)
- Background transfers (`FsGetBackgroundFlags`)
- Checksums (`FsServerSupportsChecksumsW`, etc.)
- Password encryption via TC master password (`FsSetCryptCallback`)

## License

This project uses code derived from libssh2 (BSD-3-Clause). See the libssh2 repository for full license details.
