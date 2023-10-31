import {getValueByDotNotation} from "./helper";

export const subjectSelectors = [
    {selector: ".subject", property: "textContent", dataKey: "name.shortName", placeholder: "Имя предмета"},
    {selector: ".room a", property: "textContent", dataKey: "room.name", placeholder: "Имя комнаты"},
    {selector: ".type", property: "textContent", dataKey: "type.shortName", placeholder: "Тип предмета"},
    {selector: ".tutor", property: "textContent", dataKey: "tutor.name", placeholder: "Имя препода"},
    {selector: ".tutor", property: "href", dataKey: "tutor.href"},
];

export const renderData = (apiData) => {
    const tds = document.querySelectorAll(
        '.time-table tr:not(:first-child) td:not(:first-child)'
    )

    const renderSubject = (el, subjectData) => {
        subjectSelectors.forEach(({selector, property, dataKey}) => {
            const element = el.querySelector(selector);
            if (element) {
                const value = getValueByDotNotation(subjectData, dataKey);
                if (value !== null) {
                    element[property] = value;
                }
            }
        });
    };

    const renderCell = (cell, cellIndex) => {
        const subjectsDataInCell = apiData[cellIndex]['subjects']
        subjectsDataInCell.forEach((subjectData, subjectIndex) => {
            renderSubject(cell, subjectData)
        })
    };

    tds.forEach((td, dataID) => {
        td.setAttribute('data-id', dataID.toString());
        const cells = td.querySelectorAll('.cell');
        cells.forEach((cell) => {
            renderCell(cell, dataID)
        })
    })
}