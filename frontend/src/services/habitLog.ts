import api from './api';

export interface HabitLog {
  id: number;
  habit_id: number;
  log_date: string;
  status: boolean;
  created_at: string;
}

export interface HabitLogCreate {
  log_date: string;
  status: boolean;
}

class HabitLogService {
  async logHabitCompletion(habitId: number, log: HabitLogCreate): Promise<HabitLog> {
    const response = await api.post<HabitLog>(`/habits/${habitId}/log`, log);
    return response.data;
  }

  async getHabitLogs(habitId: number, startDate: string, endDate: string): Promise<HabitLog[]> {
    const response = await api.get<HabitLog[]>(`/habits/${habitId}/log`, {
      params: {
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response.data;
  }
}

export const habitLogService = new HabitLogService();
