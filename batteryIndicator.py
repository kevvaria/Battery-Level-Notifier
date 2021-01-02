import ctypes
import time
from ctypes import wintypes
from win10toast import ToastNotifier    # External lib download(C:\Python27\): python -m pip install win10toast

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ExternalPower', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD)
    ]


def getPercent():
    """
    :rtype: bool
    """
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    toaster = ToastNotifier()
    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
        return False

    print 'current time: ', time.ctime(time.time())
    print 'current battery level: ', status.BatteryLifePercent

    # case 1: completely charged
    if status.ExternalPower == True and status.BatteryLifePercent == 100:
        return True

    # case 2: charging, but not completed
    elif status.ExternalPower == True and status.BatteryLifePercent < 100:

        # sub case #1: battery almost completely charged
        if status.BatteryLifePercent > 95:

            toaster.show_toast("Battery Level: " + str(status.BatteryLifePercent) + "%",
                               "Battery ALMOST FULL!",
                               duration=60)
            time.sleep(30)

        # sub case #2: battery still has a lot to charge up before reaching completion
        else:

            toaster.show_toast("Battery Level: " + str(status.BatteryLifePercent) + "%",
                               "Battery Charging, nothing critical",
                               duration=60)

            time.sleep(30)

        return False

    # case #3: charger not connected
    elif status.ExternalPower == False:

        #sub case #1: battery life critical and requires charging urgently
        if status.BatteryLifePercent > 5 and status.BatteryLifePercent < 20:

            toaster.show_toast("Battery Level: " + str(status.BatteryLifePercent) + "%",
                               "Battery Low! Please plug in charger",
                               duration=60)
            time.sleep(10)

        #sub case #2: machine running on battery life, not charging
        else:

            toaster.show_toast("Battery Level: " + str(status.BatteryLifePercent) + "%",
                               "Running on Battery Power!",
                               duration=60)
            time.sleep(300)

        return False

    # case #4: failed to retrieve battery info
    else:

        toaster.show_toast("No battery information found",
                           "Battery Percent and Status unknown")
        return False


def getConnectionStatus():
    """
    :rtype: bool
    """
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    toaster = ToastNotifier()
    status = SYSTEM_POWER_STATUS()

    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
        return False

    if status.ExternalPower == True:
        return True

    else:
        return False


def main():

    while not getPercent():
        print '\n\n'

    while (getPercent() and getConnectionStatus()):
        toasterPass = ToastNotifier()
        toasterPass.show_toast("Battery Level: 100%",
                               "BATTERY FULL! Please Unplug Charger!",
                               duration=10)
        time.sleep(30)

main()