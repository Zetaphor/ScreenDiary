// dateTimeUtils.js
export function parseDatetime(dateTimeStr) {
  // Split the string into date and time parts
  const [datePart, timePart] = dateTimeStr.split('_');
  const [year, month, day] = datePart.split('-').map(Number);
  const [hour, minute, second] = timePart.split('-').map(Number);

  // Create a new Date object
  const date = new Date(year, month - 1, day, hour, minute, second);

  // Format the date for display in 12-hour format
  return {
    date: date.toDateString(),
    time: ((date.getHours() % 12) || 12) + ':' +
      date.getMinutes().toString().padStart(2, '0') + ':' +
      date.getSeconds().toString().padStart(2, '0') + ' ' +
      (date.getHours() < 12 ? 'AM' : 'PM')
  };
}
