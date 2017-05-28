import AppKit

def errorAlert(msgText, infoText):
    # Force NSApp initialisation.
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(0)
    alert = AppKit.NSAlert.alloc().init()
    alert.setMessageText_(msgText)
    alert.setInformativeText_(infoText)
    alert.setAlertStyle_(AppKit.NSCriticalAlertStyle)
    btn = alert.addButtonWithTitle_("OK")
    return alert.runModal()

