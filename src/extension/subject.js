export const subjectSelectors = [
    {selector: ".subject", property: "textContent", dataKey: "name.short_name", placeholder: "Имя предмета"},
    {selector: ".room a", property: "textContent", dataKey: "room.name", placeholder: "Имя комнаты"},
    {selector: ".room a", property: "renderMap()", dataKey: "room"},
    {
        selector: ".type",
        property: "textContent",
        dataKey: "type",
        formRender: "renderTypeSelect()",
        placeholder: "Тип предмета"
    },
    {selector: ".type", property: "renderType()", dataKey: "type"},
    {selector: ".tutor", property: "textContent", dataKey: "tutor.name", placeholder: "Имя препода"},
    {selector: ".tutor", property: "href", dataKey: "tutor.href"},
    {
        selector: ".week",
        property: "renderWeek()",
        dataKey: "periodicity",
        placeholder: "Четность",
        formRender: "renderWeekSelect()"
    },
];


export const weekType = new Map(Object.entries({
    0: "По чётным",
    1: "По нечётным",
    2: "Всегда",
}))

export const subjectType = new Map(Object.entries({
    0: "noType",
    3: "lab",
    2: "pr",
    1: "lek",
    4: "f_2",
    5: "f_2",
    6: "f_2",
}))

export const subjectTypeNames = new Map(Object.entries({
    0: "—",
    3: "лаб",
    2: "пр",
    1: "лек",
    4: "ф.пр",
    5: "ф.лек",
    6: "ф.лаб",
}))

export const getWeekNum = (searchValue) => {
    for (const [key, value] of weekType.entries()) {
        if (value === searchValue) {
            return key;
        }
    }
    return null;
}


const cellHtml = `
<div class="cell">
  <span class="type" data-toggle="tooltip" data-placement="right" title="" data-original-title=""></span>
  <div class="subject" data-toggle="tooltip" data-placement="top" title="" data-original-title=""></div>
  <div class="room">
    <a href="#" onclick=""></a>
  </div>
  <a class="tutor" href=""></a>
  <div class="week"></div>
</div>
`

export const insertCells = (tdElement, n) => {
    for (let i = 0; i < n; i++) {
        tdElement.insertAdjacentHTML("beforeend", cellHtml);
    }


}