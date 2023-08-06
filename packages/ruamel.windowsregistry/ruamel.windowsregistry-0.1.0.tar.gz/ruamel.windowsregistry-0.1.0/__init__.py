# coding: utf-8

from typing import Dict, Any

_package_data: Dict[str, Any] = dict(
    full_package_name='ruamel.windowsregistry',
    version_info=(0, 1, 0),
    __version__='0.1.0',
    version_timestamp='2023-01-31 09:32:13',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='get and set values on windows registry',
    keywords='pypi statistics',
    # entry_points='windowsregistry=ruamel.windowsregistry.__main__:main',
    entry_points=None,
    license='Copyright Ruamel bvba 2007-2023',
    since=2023,
    # status='α|β|stable',  # the package status on PyPI
    # data_files="",
    # universal=True,  # py2 + py3
    # install_requires=['ruamel.std.pathlib', ],
    tox=dict(env='3',),  # *->all p->pypy
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


####
import weakref

import winreg as _winreg

date_time_format = '%Y-%m-%d %H:%M:%S'


class WindowsRegistry:
    """keeps registry open until the WindowsRegistry object is deleted.
       need to access including HKEY_LOCAL_MACHINE etc. prefix
    """

    def __init__(self, log=None, verbose=0):
        self._registries = {}
        self.log = log if log else self.nolog

    def get(self, fullpath, smart=True, readonly=False, default=None):
        """if key is not found, return default (i.e. None)
           smart -> convert loaded type smartly

           for the (Default) value of  key make sure it ends with a /
        """
        key, name = self._get_key(fullpath, readonly=readonly)
        try:
            val, type_id = _winreg.QueryValueEx(key, name)
            _winreg.CloseKey(key)
            if not smart:
                return val
            elif type_id == _winreg.REG_SZ:
                return val
            elif type_id == _winreg.REG_DWORD:
                return int(val)
            elif type_id == _winreg.REG_BINARY:
                if val:
                    return pickle.loads(bz2.decompress(val))
                return val
            elif type_id == _winreg.REG_MULTI_SZ:
                return val
        except WindowsError as e:
            self.log('WindowsError', e)
            self.log('fullpath', fullpath)
            return default
        except TypeError:
            return None

    def set(self, fullpath, value):
        key, name = self._get_key(fullpath)
        try:
            _winreg.SetValueEx(key, name, 0, _winreg.REG_SZ, value)
        except Exception as e:
            self.log(f'value not settable [{fullpath}] [{value}: {e}]')
            raise
        _winreg.CloseKey(key)

    def setint(self, fullpath, value):
        key, name = self._get_key(fullpath)
        try:
            _winreg.SetValueEx(key, name, 0, _winreg.REG_DWORD, value)
        except Exception as e:
            self.log(f'integer value not settable [{fullpath}] [{value}: {e}]')
            raise
        _winreg.CloseKey(key)

    def set_datetime(self, fullpath, dts=None):
        self.log('set_datetime')
        key, name = self._get_key(fullpath)
        try:
            if dts is None:
                import datetime

                dts = datetime.datetime.now()
            value = dts.strftime(date_time_format)
            _winreg.SetValueEx(key, name, 0, _winreg.REG_SZ, value)
        except Exception as e:
            self.log(f'datetime value not settable [{fullpath}] [{value}: {e}]')
            raise
        _winreg.CloseKey(key)

    def setbin(self, fullpath, value):
        key, name = self._get_key(fullpath)
        _winreg.SetValueEx(key, name, 0, _winreg.REG_BINARY, value)
        _winreg.CloseKey(key)

    def delete(self, fullpath):
        self.log(f'deleting {fullpath}')
        key, name = self._get_key(fullpath)
        self.log(f'del {key} {name}')
        _winreg.DeleteValue(key, name)

    def delete_key(self, full_path):
        self.log('deleting key {full_path}')
        parent_key, name = self._get_key(full_path)
        _winreg.DeleteKey(parent_key, name)

    def subkeys(self, fullpath):
        if fullpath[-1] == '/':
            fullpath = fullpath[:-1]
        regname, path = fullpath.replace('/', '\\').split('\\', 1)
        wreg = _winreg.__dict__[regname]
        h_key = _winreg.OpenKey(wreg, path)
        result = []
        try:
            count = -1
            while True:
                count += 1
                result.append(_winreg.EnumKey(h_key, count))
        except WindowsError as e:
            pass
        return result

    def _get_key(self, fullpath, readonly=False):
        # e.g. HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Control/
        access_method = _winreg.KEY_ALL_ACCESS if not readonly else _winreg.KEY_READ
        regname, path = fullpath.replace('/', '\\').split('\\', 1)
        wreg = _winreg.__dict__[regname]
        path, name = path.rsplit('\\', 1)
        reg = self._registries.setdefault(regname, _winreg.ConnectRegistry(None, wreg))
        try:
            key = _winreg.OpenKey(reg, path, 0, access_method)
        except WindowsError:
            if readonly:
                return None, None
            try:
                createkey = _winreg.CreateKey(reg, path)
                key = _winreg.OpenKey(reg, path, 0, access_method)
            except:
                am = 'R'
                if access_method == _winreg.KEY_ALL_ACCESS:
                    am = 'RW'
                self.log(f'Error creating registry path {fullpath} {am}')
                raise
        return key, name

    def close(self):
        if _winreg is not None:
            for k, v in self._registries.items():
                _winreg.CloseKey(v)
        self._registries.clear()

    def __del__(self):
        self.close()

    @classmethod
    def nolog(*args, **kw):
        pass


windows_registry = WindowsRegistry()
