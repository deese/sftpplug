cmake_minimum_required(VERSION 3.20)
project(sftpplug VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Windows 7 compatibility
add_compile_definitions(_WIN32_WINNT=0x0601 WINVER=0x0601)

# Static runtime to avoid VC++ redist dependency
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")

# Source files
set(SOURCES
    src/sftpplug.cpp
    src/sftpfunc.cpp
    src/multiserver.cpp
    src/ftpdir.cpp
    src/utils.cpp
    src/cunicode.cpp
    src/CVTUTF.C
)

set(HEADERS
    src/fsplugin.h
    src/sftpfunc.h
    src/multiserver.h
    src/ftpdir.h
    src/utils.h
    src/cunicode.h
    src/CVTUTF.H
    src/libssh2.h
    src/libssh2_sftp.h
    src/sshdynfunctions.h
    src/sshdynload.h
    src/resource.h
    src/config.h
)

set(RESOURCES
    src/sftpplug.rc
)

# Create the DLL target
add_library(sftpplug SHARED ${SOURCES} ${HEADERS} ${RESOURCES})

# Set output names: .wfx for Win32, .wfx64 for x64
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set_target_properties(sftpplug PROPERTIES SUFFIX ".wfx64")
else()
    set_target_properties(sftpplug PROPERTIES SUFFIX ".wfx")
endif()

# Preprocessor definitions
target_compile_definitions(sftpplug PRIVATE
    WIN32
    NDEBUG
    _WINDOWS
    _USRDLL
    SFTPPLUG_EXPORTS
    HAVE_WINSOCK2_H
    LIBSSH2_WIN32
)

# Include directories
target_include_directories(sftpplug PRIVATE src)

# Link libraries
target_link_libraries(sftpplug PRIVATE
    ws2_32
)

# MSVC specific options
if(MSVC)
    target_compile_options(sftpplug PRIVATE
        /W3
        /O2
        /Gy
        /GF
    )
endif()

# Module definition file
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/sftpplug.def")
    target_sources(sftpplug PRIVATE src/sftpplug.def)
endif()
