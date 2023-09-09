import {Lesson, LessonType} from "./cell"
const timetable_raw = '{"times": ["9:00", "10:00", "11:00"], "days": [{"name": "Понедельник", "subjects": [{"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 101", "periodicity": 2, "isEmpty": true}, {"name": "Science", "teacher": "Mr. Smith", "place": "Room 202", "periodicity": 0, "isEmpty": false}, {"name": "Science", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": true}, {"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 303", "periodicity": 0, "isEmpty": true}, {"name": "English", "teacher": "Mr. Smith", "place": "Room 101", "periodicity": 0, "isEmpty": false}, {"name": "English", "teacher": "Ms. Thompson", "place": "Room 202", "periodicity": 0, "isEmpty": false}, {"name": "English", "teacher": "Mr. Smith", "place": "Room 303", "periodicity": 1, "isEmpty": true}, {"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 303", "periodicity": 1, "isEmpty": false}, {"name": "English", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": false}, {"name": "Science", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": false}]}]}'
const timetable = JSON.parse(timetable_raw)
const times_navigator = timetable["times"].reduce((acc, value, index) => {
  acc[value] = index;
  return acc;
}, {});
console.log(times_navigator)
const table = document.querySelector(".time-table");
const rows = table.rows;
const DAYS_NAMES = []
const table_view = {}
rows[0].querySelectorAll("th").forEach(function (day, index) {
    if (index !== 0) {
        DAYS_NAMES.push(day.innerText);
    }
});

console.log(DAYS_NAMES)

const columns = [];

for (let columnIndex = 1; columnIndex < rows[0].cells.length; columnIndex++) {
    const column = [];

    // Iterate through each row and select the cell at the specific column index
  Array.from(rows).forEach(function(row) {
      const cell = row.cells[columnIndex].querySelector(".cell")
      column.push(cell)
  });

  table_view[DAYS_NAMES[columnIndex-1]] = column
  columns.push(column);
}
console.log(table_view)
//console.log(columns);

let t = new Lesson("kek", "214", "ivan", LessonType.LEC)
console.log(t)


