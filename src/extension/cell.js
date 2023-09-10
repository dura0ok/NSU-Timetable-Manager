export const LessonType = {
    LAB: "lab",
    PR: "pr",
    LEC: "lek",
    FAC_PR: "f_2"
};
export const Periodicity = {
    ODD: "нечетная",
    EVEN: "четная",
    ALWAYS: "всегда"
}

export function checkObjectValues(obj, v) {
    const values = Object.values(obj);
    //console.log(values, lessonType)
    for (let value of values) {
        if (value.toLowerCase() === v.toLowerCase()) {
            return value;
        }
    }
    return null; // Return null if the lesson type is not found
}

export function getByLessonType(lessonType) {
    return checkObjectValues(LessonType, lessonType)
}

export function getByPeriodicityType(periodicityType) {
    return checkObjectValues(Periodicity, periodicityType) ?? Periodicity.ALWAYS
}

export class Teacher {
    constructor(name, link) {
        this.name = name
        this.link = link
    }
}

export class Lesson {
    constructor(name, room, teacher, type, periodicity) {
        this.name = name
        this.room = room
        if (!teacher instanceof Teacher) {
            throw new Error("invalid Teacher type")
        }
        if (!Object.values(Periodicity).includes(periodicity)) {
            throw new Error("invalid periodicity type")
        }
        this.periodicity = periodicity
        this.teacher = teacher
        if (!Object.values(LessonType).includes(type)) {
            throw new Error("Invalid lessonType")
        }

        this.lesson_type = type
    }
}