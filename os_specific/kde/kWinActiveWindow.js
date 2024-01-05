const activeClient = workspace.activeClient
// console.info('ScreenDiary Debug | Name: ', activeClient.resourceName, ' | Class:', activeClient.resourceClass, ' | Type:', windowType(activeClient), ' | Text:', activeClient.caption);

if (windowType(activeClient) == "normalWindow") {
  callDBus(
    "com.screendiary.bridge",
    "/com/screendiary/bridge",
    "com.screendiary.bridge",
    "updateActiveWindow",
    activeClient.resourceName,
    activeClient.resourceClass,
    activeClient.caption
  );
}

function windowType(win) {
  var windowTypes = [
    "normalWindow", // 0
    "desktopWindow", // 1
    "dock", // 2
    "dialog", // 5
    "utility", // 8
    "splash", // 9
    "notification", // 13
    "onScreenDisplay", // 16
    "dropdownMenu",
    "popupMenu",
    "criticalNotification",
    "tooltip",
    "toolbar",
    "menu",
    "comboBox",
    "dndIcon"
  ];
  return windowTypes.map(type => (win[type] ? type : "")).join("");
}