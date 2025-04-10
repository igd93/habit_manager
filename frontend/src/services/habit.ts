import api from './api';

export interface Habit {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  created_at: string;
  archived_at: string | null;
  completed_today?: boolean;
}

export interface HabitCreate {
  name: string;
  description?: string;
}

export interface HabitUpdate {
  name?: string;
  description?: string;
}

class HabitService {
  async createHabit(habit: HabitCreate): Promise<Habit> {
    const response = await api.post<Habit>('/habits', habit);
    return response.data;
  }

  async getHabits(): Promise<Habit[]> {
    const response = await api.get<Habit[]>('/habits');
    return response.data;
  }

  async getHabit(id: number): Promise<Habit> {
    const response = await api.get<Habit>(`/habits/${id}`);
    return response.data;
  }

  async updateHabit(id: number, habit: HabitUpdate): Promise<Habit> {
    const response = await api.put<Habit>(`/habits/${id}`, habit);
    return response.data;
  }

  async deleteHabit(id: number): Promise<Habit> {
    const response = await api.delete<Habit>(`/habits/${id}`);
    return response.data;
  }
}

export const habitService = new HabitService();
