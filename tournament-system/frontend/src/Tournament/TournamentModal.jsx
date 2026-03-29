import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { X, Calendar, ChevronDown } from 'lucide-react';
import { tournamentSchema } from "./tournamentSchema";

const TournamentModal = ({ isOpen, onClose, onSuccess }) => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(tournamentSchema),
    defaultValues: { status: 'draft', maxTeams: 0 }
  });

  const handleInternalSubmit = async (data) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/tournaments/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        alert("Турнір успішно збережено!");
        if (onSuccess) onSuccess();
        onClose();
      } else {
        const errorData = await response.json();
        alert(`Помилка: ${JSON.stringify(errorData)}`);
      }
    } catch (error) {
      console.error("Помилка:", error);
      alert("Перевір з'єднання з Django!");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white w-full max-w-[850px] rounded-2xl shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-8 py-5 border-b border-gray-100">
          <h2 className="text-xl font-bold text-slate-800">Створення нового турніру</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
            <X size={22} />
          </button>
        </div>

        <form onSubmit={handleSubmit(handleInternalSubmit)} className="p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
            <div className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Назва турніру</label>
                <input {...register('name')} className={`w-full px-4 py-2 border rounded-lg outline-none ${errors.name ? 'border-red-500' : 'border-gray-200'}`} />
                {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Опис (Markdown)</label>
                <textarea {...register('description')} rows={10} className="w-full px-4 py-3 border border-gray-200 rounded-lg outline-none resize-none text-sm font-mono" />
              </div>
            </div>

            <div className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Дата старту</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-2.5 text-gray-400" size={18} />
                  <input type="datetime-local" {...register('startDate')} className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Вікно реєстрації</label>
                <div className="flex gap-2">
                  <input type="datetime-local" {...register('registrationStart')} className="w-1/2 px-2 py-2 border border-gray-200 rounded-lg" />
                  <input type="datetime-local" {...register('registrationEnd')} className="w-1/2 px-2 py-2 border border-gray-200 rounded-lg" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Макс. команд</label>
                <input type="number" {...register('maxTeams', { valueAsNumber: true })} className="w-full px-4 py-2 border border-gray-200 rounded-lg" />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Статус</label>
                <select {...register('status')} className="w-full px-4 py-2 border border-gray-200 rounded-lg bg-white">
                  <option value="draft">Чернетка</option>
                  <option value="open">Опубліковано</option>
                </select>
              </div>
            </div>
          </div>

          <div className="mt-8 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="px-6 py-2 text-slate-600 font-medium">Скасувати</button>
            <button type="submit" disabled={isSubmitting} className="px-8 py-2 bg-blue-600 text-white font-bold rounded-lg shadow-lg">
              {isSubmitting ? 'Завантаження...' : 'Створити'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TournamentModal;
