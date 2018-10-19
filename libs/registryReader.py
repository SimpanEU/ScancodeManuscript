import re
import winreg
import platform
from time import sleep

def read_client_status(expectedValue):
    # Determine path to registry keys based upon whether the system is 64 or 32 bit.

    bit = platform.architecture()
    if "64" in bit[0]:
        bit = "\WOW6432Node"
    else:
         bit = ""
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE' + bit + '\CheckPoint\Endpoint Security\Full Disk Encryption\Status\Current Boot',0, winreg.KEY_READ)
    clientStatus, type = winreg.QueryValueEx(hkey, "clientStatus")
    winreg.CloseKey(hkey)
    isFound = False

    # Looks for expected key, if not found, sleeps for 60 secs before retrying.
    # If reaches last loop, returns a false assert.

    for x in range(0, 5):
        try:
            if int(clientStatus) == int(expectedValue):
                print('Found:', clientStatus, 'Expected:', expectedValue)
                isFound = True
                assert int(clientStatus) == int(expectedValue)
                break
        except AssertionError as str_error:
                print(str_error)
                assert False
        if not isFound:
            print('Found:', clientStatus, 'Expected:', expectedValue)
            if x == 4:
                assert False
            print('Trying again in 60s...')
            sleep(60)
        else:
            break

def read_encryption_state(part, algo):
    bit = platform.architecture()
    if "64" in bit[0]:
        bit = "\WOW6432Node"
    else:
        bit = ""

    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE'+bit+'\CheckPoint\Endpoint Security\Full Disk Encryption\Status\Current Boot', 0,winreg.KEY_READ)
    clientStatus, type = winreg.QueryValueEx(hkey, "clientStatus")
    winreg.CloseKey(hkey)
    isEncryptedStatus = False
    ciph = switch_cipher(algo)

    # Reads encryption state for each volume. Expects clientStatus to be 70(Encrypted).
    # Sleeps for 60 seconds if expected status is false.
    # If reaches last loop, returns a false assert.

    for x in range(0, 5):
        try:
            if int(clientStatus) == 70:
                isEncryptedStatus = True
                hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE'+bit+'\CheckPoint\Endpoint Security\Full Disk Encryption\Status\Current Boot',0, winreg.KEY_READ)
                targetProtection, type = winreg.QueryValueEx(hkey, "targetProtection")
                winreg.CloseKey(hkey)
                tP = re.split('[,]', targetProtection)
                p = int(part)
                for i in range(p):
                    print("Existing value:", int(tP[i]), "Input value:", ciph)
                    assert int(tP[i]) == ciph
                break
        except AssertionError as str_error:
            print(str_error)
            print("Given cipher is not matching with existing one.")
            assert False
        if not isEncryptedStatus:
            print("Client status still encrypting...")
            print('Trying again in 60s...')
            if x == 4:
                print('Found:', clientStatus, 'Expected:', '70')
                assert False
            sleep(60)
        else:
            break

def read_wol_status(arg1):
    bit = platform.architecture()
    if "64" in bit[0]:
        bit = "\WOW6432Node"
    else:
        bit = ""
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE'+bit+'\CheckPoint\Endpoint Security\Full Disk Encryption\Status\Current Boot', 0,winreg.KEY_READ)
    wolEnabled, type = winreg.QueryValueEx(hkey, "wolEnabled")
    winreg.CloseKey(hkey)

    print(wolEnabled)
    assert arg1 == str(wolEnabled)

def read_wil_status(arg1):
    bit = platform.architecture()
    if "64" in bit[0]:
        bit = "\WOW6432Node"
    else:
        bit = ""
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE'+bit+'\CheckPoint\Endpoint Security\Full Disk Encryption\Status\Current Boot', 0,winreg.KEY_READ)
    wilEnabled, type = winreg.QueryValueEx(hkey, "wilEnabled")
    winreg.CloseKey(hkey)

    print(wilEnabled)
    assert arg1 == str(wilEnabled)

def switch_cipher(argument):
    return {
        'None': 0,
        'Blowfish': 1,
        'CAST': 2,
        'AES-CBC': 3,
        '3DES': 4,
        'XTS-AES-256': 5,
        'XTS-AES-128': 6,
        '"None"': 0,
        '"Blowfish"': 1,
        '"CAST"': 2,
        '"AES-CBC"': 3,
        '"3DES"': 4,
        '"XTS-AES-256"': 5,
        '"XTS-AES-128"': 6,
    }.get(argument, "Invalid cipher")

def main():
    read_client_status(70)
if __name__ == "__main__":
    main()