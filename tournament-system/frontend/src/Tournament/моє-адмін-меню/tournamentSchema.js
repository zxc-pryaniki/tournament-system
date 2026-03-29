import { z } from "zod";

export const tournamentSchema = z.object({
  name: z.string().min(5, "Назва повинна бути не менше 5 символів"),
  description: z.string().min(1, "Опис обов'язковий"),
  registrationStart: z.string().min(1, "Вкажіть дату"),
  registrationEnd: z.string().min(1, "Вкажіть дату"),
  startDate: z.string().min(1, "Вкажіть дату"),
  maxTeams: z.number({ invalid_type_error: "Введіть число" }).min(2, "Мінімум 2 команди"),
  status: z.enum(["draft", "open", "ongoing", "finished"]),
}).refine((data) => new Date(data.registrationEnd) > new Date(data.registrationStart), {
  message: "Кінець реєстрації має бути після початку",
  path: ["registrationEnd"],
}).refine((data) => new Date(data.startDate) >= new Date(data.registrationEnd), {
  message: "Старт турніру не може бути раніше дедлайну реєстрації",
  path: ["startDate"],
});
