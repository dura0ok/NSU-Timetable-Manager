import {Lesson, LessonType, getByLessonType, Teacher, Periodicity, getByPeriodicityType} from "./cell"

function getTimeTableData() {
    const timetable_raw = '{"times": ["9:00", "10:00", "11:00"], "days": [{"name": "Понедельник", "subjects": [{"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 101", "periodicity": 2, "isEmpty": true}, {"name": "Science", "teacher": "Mr. Smith", "place": "Room 202", "periodicity": 0, "isEmpty": false}, {"name": "Science", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": true}, {"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 303", "periodicity": 0, "isEmpty": true}, {"name": "English", "teacher": "Mr. Smith", "place": "Room 101", "periodicity": 0, "isEmpty": false}, {"name": "English", "teacher": "Ms. Thompson", "place": "Room 202", "periodicity": 0, "isEmpty": false}, {"name": "English", "teacher": "Mr. Smith", "place": "Room 303", "periodicity": 1, "isEmpty": true}, {"name": "Math", "teacher": "Mrs. Johnson", "place": "Room 303", "periodicity": 1, "isEmpty": false}, {"name": "English", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": false}, {"name": "Science", "teacher": "Ms. Thompson", "place": "Room 101", "periodicity": 0, "isEmpty": false}]}]}'
    return JSON.parse(timetable_raw);
}


function generateHelpTimesArray() {
    return timetable["times"].reduce((acc, value, index) => {
        acc[value] = index;
        return acc;
    }, {});
}


function parseDaysNames(row) {
    const DAYS_NAMES = []

    row.querySelectorAll("th").forEach(function (day, index) {
        if (index !== 0) {
            DAYS_NAMES.push(day.innerText);
        }
    });
    return DAYS_NAMES;
}

function fillDays(table) {
    const tableView = {}
    for (let i = 1; i < table.rows[0].cells.length; i++) {
        const column = [];
        // Iterate through each row in the column
        for (let j = 0; j < table.rows.length; j++) {
            const columnElement = table.rows[j].cells[i];
            const columnElementCells = columnElement.querySelectorAll(".cell")
            const variants = []
            columnElementCells.forEach(function (cell) {
                const subject_type = cell.querySelector(".type")
                const subject_name = cell.querySelector(".subject")
                const room = cell.querySelector(".room")
                const tutor = cell.querySelector(".tutor")
                const periodicity = cell.querySelector(".week")
                const elements = [subject_type, subject_name, room, tutor, periodicity]
                elements.forEach(element => {
                    if(element == null){
                        return
                    }
                    element.onclick = () => {
                        const inputText = prompt("Enter new text");
                        if (inputText !== null) {
                            element.innerText = inputText;
                        }
                    };
                })
                let lesson = new Lesson(
                    subject_name.innerText,
                    room.innerText,
                    tutor == null ? null : new Teacher(tutor.innerText, tutor.href),
                    getByLessonType(subject_type.classList[1]),
                    getByPeriodicityType(periodicity ? periodicity.innerText : '')
                )
                variants.push({"data": lesson, "element": cell})
            })
            column.push(variants)
        }
        console.log(column)
        tableView[DAYS_NAMES[i - 1]] = column
    }

    return tableView
}

const timetable = getTimeTableData();
const times_navigator = generateHelpTimesArray();
const table = document.querySelector(".time-table");
const DAYS_NAMES = parseDaysNames(table.rows[0]);
const tableView = fillDays(table);
console.log(tableView)
// let t = new Lesson("kek", "214", "ivan", LessonType.LEC)



