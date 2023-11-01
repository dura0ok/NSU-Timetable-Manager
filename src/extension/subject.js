export const subjectSelectors = [
    {selector: ".subject", property: "textContent", dataKey: "name.shortName", placeholder: "Имя предмета"},
    {selector: ".room a", property: "textContent", dataKey: "room.name", placeholder: "Имя комнаты"},
    {selector: ".room a", property: "renderMap()", dataKey: "room.location"},
    {
        selector: ".type",
        property: "textContent",
        dataKey: "type.shortName",
        formRender: "renderTypeSelect()",
        placeholder: "Тип предмета"
    },
    {selector: ".type", property: "renderType()", dataKey: "type"},
    {selector: ".tutor", property: "textContent", dataKey: "tutor.name", placeholder: "Имя препода"},
    {selector: ".tutor", property: "href", dataKey: "tutor.href"},
];

export const subjectType = new Map(Object.entries({
    "лаб": "lab",
    "пр": "pr",
    "лек": "lek",
    "ф, пр": "f_2"
}))
