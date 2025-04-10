import React, { useEffect, useState } from 'react';
import { Habit } from '@/services/habit';
import { habitService } from '@/services/habit';
import { habitLogService } from '@/services/habitLog';
import HabitCard from './HabitCard';
import CompletionStat from './CompletionStat';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import HabitForm from './HabitForm';

export default function HabitList() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadHabits();
  }, []);

  const loadHabits = async () => {
    try {
      const habitsData = await habitService.getHabits();
      setHabits(habitsData);
    } catch (error) {
      console.error('Failed to load habits:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleCompletion = async (habitId: number) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      await habitLogService.logHabitCompletion(habitId, {
        log_date: today,
        status: true,
      });
      // Refresh habits to get updated completion status
      loadHabits();
    } catch (error) {
      console.error('Failed to toggle habit completion:', error);
    }
  };

  const handleCreateHabit = async (name: string, description?: string) => {
    try {
      await habitService.createHabit({ name, description });
      setShowForm(false);
      loadHabits();
    } catch (error) {
      console.error('Failed to create habit:', error);
    }
  };

  if (isLoading) {
    return <div>Loading habits...</div>;
  }

  const completedCount = habits.filter(habit => habit.completed_today).length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">My Habits</h2>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="w-4 h-4 mr-2" />
          New Habit
        </Button>
      </div>

      <CompletionStat completedCount={completedCount} totalCount={habits.length} />

      {showForm && <HabitForm onSubmit={handleCreateHabit} onCancel={() => setShowForm(false)} />}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {habits.map(habit => (
          <HabitCard
            key={habit.id}
            habit={habit}
            onToggleCompletion={() => handleToggleCompletion(habit.id)}
          />
        ))}
      </div>
    </div>
  );
}
