export const LessonType = {
  LAB: "Laboratory",
  PR: "Practice",
  LEC: "Lecture"
};

export class Lesson{
    constructor(name, room, teacher, type) {
      this.name = name
      this.room = room
      this.teacher = teacher
       if (!Object.values(LessonType).includes(type)) {
         throw new Error("Invalid lessonType")
       }
       this.lesson_type = type
    }
}