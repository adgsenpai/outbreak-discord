"""Per-user install/uninstall and autostart for the companion (Windows and Linux).

Windows: double-clicking the released .exe copies it to %LOCALAPPDATA%\\OutbreakDiscord,
registers it under HKCU\\...\\Run so it starts at login, launches it in the background and
shows a confirmation dialog. Run it with --uninstall to remove it.

Linux: --install copies the binary (or points at this script when run from source) and
enables a systemd user service; without systemd it falls back to an XDG autostart entry.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

APP = 'OutbreakDiscord'
EXE_NAME = 'OutbreakDiscordCompanion.exe'
LINUX_BIN = Path.home() / '.local' / 'bin' / 'outbreak-discord-companion'
UNIT = Path.home() / '.config' / 'systemd' / 'user' / 'outbreak-discord.service'
AUTOSTART = Path.home() / '.config' / 'autostart' / 'outbreak-discord.desktop'
RUN_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'
EXTENSION_HINT = 'Next: install the "Outbreak Discord Rich Presence" Chrome extension, then play at outbreakweb.com.'

FROZEN = getattr(sys, 'frozen', False)
WINDOWS = os.name == 'nt'


def _win_dir():
    return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / APP


def setup_logging(config_dir):
    """A windowed (no-console) build has no stdout; send output to a log file instead."""
    if sys.stdout is None or (FROZEN and WINDOWS):
        config_dir.mkdir(parents=True, exist_ok=True)
        log = open(config_dir / 'companion.log', 'a', buffering=1, encoding='utf-8')
        sys.stdout = sys.stderr = log


def _message(text, error=False):
    if WINDOWS:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, text, 'Outbreak Discord Rich Presence', 0x10 if error else 0x40)
    else:
        print(text, flush=True)


def should_self_install():
    """Double-clicked Windows exe that isn't running from its install location."""
    if not (WINDOWS and FROZEN) or len(sys.argv) > 1:
        return False
    return Path(sys.executable).resolve().parent != _win_dir().resolve()


def install():
    try:
        (_install_windows if WINDOWS else _install_linux)()
    except Exception as exc:  # show the failure to someone who double-clicked
        _message(f'Install failed: {exc}', error=True)
        raise SystemExit(1)


def uninstall():
    try:
        (_uninstall_windows if WINDOWS else _uninstall_linux)()
    except Exception as exc:
        _message(f'Uninstall failed: {exc}', error=True)
        raise SystemExit(1)


# ---------------------------------------------------------------- Windows
def _install_windows():
    import winreg
    if not FROZEN:
        raise RuntimeError('Run the released OutbreakDiscordCompanion.exe to install on Windows.')
    target_dir = _win_dir()
    target = target_dir / EXE_NAME
    target_dir.mkdir(parents=True, exist_ok=True)
    if Path(sys.executable).resolve() != target.resolve():
        subprocess.run(['taskkill', '/F', '/IM', EXE_NAME], capture_output=True)  # replace an older running copy
        shutil.copy2(sys.executable, target)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, APP, 0, winreg.REG_SZ, f'"{target}"')
    flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    subprocess.Popen([str(target)], creationflags=flags, close_fds=True, cwd=str(target_dir))
    _message('Installed! The companion is running in the background and will start with Windows.\n\n'
             + EXTENSION_HINT + f'\n\nTo uninstall: run "{target}" --uninstall')


def _uninstall_windows():
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP)
    except FileNotFoundError:
        pass
    me = os.getpid()
    subprocess.run(['taskkill', '/F', '/IM', EXE_NAME, '/FI', f'PID ne {me}'], capture_output=True)
    target_dir = _win_dir()
    if target_dir.exists():
        # The running exe can't delete itself; remove the folder a moment after we exit.
        subprocess.Popen(f'cmd /c timeout /t 2 /nobreak >nul & rmdir /s /q "{target_dir}"',
                         shell=True, creationflags=0x08000000)  # CREATE_NO_WINDOW
    _message('Outbreak Discord Rich Presence was uninstalled.')


# ---------------------------------------------------------------- Linux
def _exec_command():
    if FROZEN:
        LINUX_BIN.parent.mkdir(parents=True, exist_ok=True)
        if Path(sys.executable).resolve() != LINUX_BIN.resolve():
            tmp = LINUX_BIN.with_suffix('.new')
            shutil.copy2(sys.executable, tmp)
            os.chmod(tmp, 0o755)
            os.replace(tmp, LINUX_BIN)
        return f'"{LINUX_BIN}"'
    return f'"{sys.executable}" "{Path(__file__).resolve().parent / "server.py"}"'


def _has_systemd():
    return shutil.which('systemctl') and subprocess.run(['systemctl', '--user', 'show-environment'], capture_output=True).returncode == 0


def _install_linux():
    cmd = _exec_command()
    if _has_systemd():
        UNIT.parent.mkdir(parents=True, exist_ok=True)
        UNIT.write_text(f"""[Unit]
Description=Outbreak Discord Rich Presence companion
After=graphical-session.target

[Service]
Type=simple
ExecStart={cmd}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
""")
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', '--user', 'enable', 'outbreak-discord.service'], check=True)
        subprocess.run(['systemctl', '--user', 'restart', 'outbreak-discord.service'], check=True)
        how = 'systemd user service "outbreak-discord" (logs: journalctl --user -u outbreak-discord -f)'
    else:
        AUTOSTART.parent.mkdir(parents=True, exist_ok=True)
        AUTOSTART.write_text(f'[Desktop Entry]\nType=Application\nName=Outbreak Discord Rich Presence\nExec={cmd}\nX-GNOME-Autostart-enabled=true\nNoDisplay=true\n')
        subprocess.Popen(cmd, shell=True, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        how = f'login autostart entry ({AUTOSTART})'
    print(f'Installed and running as a {how}.\n{EXTENSION_HINT}\nUninstall: {cmd} --uninstall', flush=True)


def _uninstall_linux():
    if UNIT.exists():
        subprocess.run(['systemctl', '--user', 'disable', '--now', 'outbreak-discord.service'], capture_output=True)
        UNIT.unlink()
        subprocess.run(['systemctl', '--user', 'daemon-reload'], capture_output=True)
    if AUTOSTART.exists():
        AUTOSTART.unlink()
        subprocess.run(['pkill', '-f', 'outbreak-discord-companion'], capture_output=True)
    if LINUX_BIN.exists():
        LINUX_BIN.unlink()
    print('Outbreak Discord Rich Presence was uninstalled.', flush=True)
