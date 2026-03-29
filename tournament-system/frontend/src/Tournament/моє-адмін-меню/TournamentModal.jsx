import React, { useState, useRef } from 'react';
import ReactQuill, { Quill } from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';

// Реєстрація розмірів у пікселях
const Size = Quill.import('attributors/style/size');
Size.whitelist = ['12px', '14px', '16px', '18px', '20px', '24px', '32px'];
Quill.register(Size, true);

const TournamentModal = ({ isOpen, onClose }) => {
    const [description, setDescription] = useState('');
    const [maxTeams, setMaxTeams] = useState(0);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const fileInputRef = useRef(null);

    const modules = {
        toolbar: { container: "#toolbar-bottom" }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-white w-full max-w-4xl rounded-3xl shadow-2xl overflow-hidden border border-gray-100 flex flex-col">
                
                <div className="px-10 py-6 border-b border-gray-100 flex justify-between items-center bg-white">
                    <h2 className="text-2xl font-black text-gray-900">Створення нового турніру</h2>
                    <button onClick={onClose} className="text-gray-300 hover:text-gray-500 text-3xl transition-colors">✕</button>
                </div>

                <div className="p-10 grid grid-cols-2 gap-x-12 gap-y-10">
                    <div className="space-y-8 flex flex-col">
                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-3 text-left">Назва турніру</label>
                            <input type="text" className="w-full px-5 py-3.5 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-400" placeholder="Введіть назву" />
                        </div>
                        
                        <div className="flex flex-col flex-1">
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-3 text-left">Опис</label>
                            <div className="border border-gray-200 rounded-xl bg-white shadow-sm flex flex-col overflow-visible-important">
                                <ReactQuill 
                                    theme="snow" 
                                    value={description} 
                                    onChange={setDescription} 
                                    modules={modules} 
                                    className="flex-1"
                                />
                                
                                <div id="toolbar-bottom">
                                    <span className="ql-formats">
                                        <select className="ql-size" defaultValue="14px">
                                            <option value="12px">12</option>
                                            <option value="14px">14</option>
                                            <option value="16px">16</option>
                                            <option value="18px">18</option>
                                            <option value="20px">20</option>
                                            <option value="24px">24</option>
                                            <option value="32px">32</option>
                                        </select>
                                    </span>

                                    <span className="ql-formats !border-l !border-gray-200 !pl-2">
                                        <button className="ql-bold"></button>
                                        <button className="ql-italic"></button>
                                        <button className="ql-underline"></button>
                                    </span>

                                    <span className="ql-formats !border-l !border-gray-200 !pl-2">
                                        <select className="ql-color"></select>
                                        <select className="ql-background"></select>
                                    </span>

                                    <span className="ql-formats !border-l !border-gray-200 !pl-2">
                                        <button className="ql-link"></button>
                                        <button type="button" onClick={() => fileInputRef.current.click()} className="p-1">
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"></path></svg>
                                        </button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-8 text-left">
                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-3">Дата старту турніру</label>
                            <input type="datetime-local" className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl outline-none shadow-sm focus:ring-2 focus:ring-blue-100" />
                        </div>

                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-3">Вікно реєстрації (Start/End)</label>
                            <div className="flex flex-col gap-3">
                                <input type="datetime-local" className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-xs outline-none shadow-sm focus:ring-1 focus:ring-blue-200" />
                                <input type="datetime-local" className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-xs outline-none shadow-sm focus:ring-1 focus:ring-blue-200" />
                            </div>
                        </div>

                        <div>
                            <label className={`block text-xs font-black uppercase tracking-widest mb-3 ${isSubmitted && maxTeams <= 0 ? 'text-red-500' : 'text-gray-400'}`}>
                                Макс. кількість команд
                            </label>
                            <input 
                                type="number" 
                                value={maxTeams}
                                onChange={(e) => setMaxTeams(e.target.value)}
                                className={`w-full px-5 py-3 border rounded-xl outline-none shadow-sm ${isSubmitted && maxTeams <= 0 ? 'border-red-300 bg-red-50 focus:ring-2 focus:ring-red-100 text-red-900' : 'border-gray-200 bg-gray-50 focus:ring-2 focus:ring-blue-100 text-gray-900'}`}
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-3 text-left">Статус</label>
                            <select className="w-full px-5 py-3 bg-gray-50 border border-gray-200 rounded-xl outline-none shadow-sm appearance-none">
                                <option>Чернетка</option>
                                <option>Опубліковано</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="px-10 py-6 border-t border-gray-100 flex justify-end gap-4 bg-gray-50">
                    <button onClick={onClose} className="px-8 py-3 bg-white border border-gray-300 rounded-xl text-gray-600 font-black hover:bg-gray-100 transition-all text-xs uppercase tracking-widest shadow-sm">
                        Скасувати
                    </button>
                    <button className="px-8 py-3 bg-blue-600 text-white rounded-xl font-black hover:bg-blue-700 transition-all shadow-md shadow-blue-200 text-xs uppercase tracking-widest">
                        Створити
                    </button>
                </div>
            </div>
            <input type="file" ref={fileInputRef} className="hidden" />
        </div>
    );
};

export default TournamentModal;
