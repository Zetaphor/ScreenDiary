console.info('Loaded');
const activeClient = workspace.activeClient
console.info('ACTIVE CLIENT!', workspace.activeClient.caption);
console.info("ACTIVECLIENT:::", "name:", activeClient.resourceName, "class:", activeClient.resourceClass, "caption:", activeClient.caption);
console.info("ACTIVECLIENT:::type:", activeClient.windowType, windowType(activeClient), (activeClient.normalWindow ? "" : "not ") + "normal", (activeClient.specialWindow ? "" : "not ") + "special");

callDBus(
  "com.screendiary.bridge",
  "/com/screendiary/bridge",
  "com.screendiary.bridge",
  "updateActiveWindow",
  activeClient.resourceName,
  activeClient.caption
);

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