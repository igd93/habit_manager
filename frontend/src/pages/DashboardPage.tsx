import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import HabitCard from '@/components/habits/HabitCard';
import CompletionStat from '@/components/habits/CompletionStat';

// Mock habit data type
interface Habit {
  id: number;
  name: string;
  description: string;
  created_at: string;
  completed_today: boolean;
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const [habits, setHabits] = useState<Habit[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  // Fetch habits (mock data for now)
  useEffect(() => {
    // In a real app, this would be an API call
    const fetchHabits = async () => {
      setIsLoading(true);
      try {
        // Mock API response
        const mockHabits: Habit[] = [
          {
            id: 1,
            name: 'Read for 20 minutes',
            description: 'Reading self-improvement books',
            created_at: '2023-06-01',
            completed_today: true,
          },
          {
            id: 2,
            name: 'Meditate',
            description: '10 minutes of mindfulness meditation',
            created_at: '2023-06-02',
            completed_today: false,
          },
          {
            id: 3,
            name: 'Exercise',
            description: '30 minutes of physical activity',
            created_at: '2023-06-03',
            completed_today: false,
          },
          {
            id: 4,
            name: 'Drink water',
            description: '8 glasses of water throughout the day',
            created_at: '2023-06-04',
            completed_today: true,
          },
        ];

        // Simulate API delay
        setTimeout(() => {
          setHabits(mockHabits);
          setIsLoading(false);
        }, 500);
      } catch (err) {
        setError('Failed to load habits');
        setIsLoading(false);
        console.error(err);
      }
    };

    fetchHabits();
  }, []);

  // Toggle habit completion status
  const toggleHabitCompletion = (habitId: number) => {
    setHabits(prevHabits =>
      prevHabits.map(habit =>
        habit.id === habitId ? { ...habit, completed_today: !habit.completed_today } : habit
      )
    );
  };

  // Calculate completion stats
  const completedCount = habits.filter(habit => habit.completed_today).length;
  const totalCount = habits.length;

  return (
    <MainLayout title="Dashboard | Habit Tracker">
      <div className="container max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-bold">Your Habits</h1>
            <p className="text-muted-foreground mt-1">Track and manage your daily habits</p>
          </div>
          <Button asChild>
            <Link to="/habits/new">Add New Habit</Link>
          </Button>
        </div>

        {/* Stats Overview */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Today's Progress</CardTitle>
            <CardDescription>Your habit completion status for today</CardDescription>
          </CardHeader>
          <CardContent>
            <CompletionStat completedCount={completedCount} totalCount={totalCount} />
          </CardContent>
        </Card>

        {/* Habits List */}
        {isLoading ? (
          <div className="py-12 text-center">
            <p className="text-muted-foreground">Loading habits...</p>
          </div>
        ) : error ? (
          <div className="py-12 text-center">
            <p className="text-destructive">{error}</p>
            <Button variant="outline" className="mt-4" onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </div>
        ) : habits.length === 0 ? (
          <div className="py-12 text-center">
            <p className="text-muted-foreground">You don't have any habits yet.</p>
            <Button asChild className="mt-4">
              <Link to="/habits/new">Create Your First Habit</Link>
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {habits.map(habit => (
              <HabitCard
                key={habit.id}
                habit={habit}
                onToggleCompletion={() => toggleHabitCompletion(habit.id)}
              />
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
}
