import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MainLayout from '@/components/layout/MainLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

export default function AddHabitPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim()) {
      toast.error('Habit name is required');
      return;
    }

    setIsLoading(true);

    try {
      // In a real app, make API call to POST /habits
      // const response = await fetch("/api/habits", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     "Authorization": `Bearer ${localStorage.getItem("token")}`
      //   },
      //   body: JSON.stringify(formData),
      // });

      // Mock successful response
      const mockResponse = {
        ok: true,
        json: async () => ({ id: Date.now(), ...formData }),
      };

      if (mockResponse.ok) {
        toast.success('Habit created successfully');
        navigate('/dashboard');
      } else {
        toast.error('Failed to create habit');
      }
    } catch (err) {
      console.error(err);
      toast.error('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <MainLayout title="Add New Habit | Habit Tracker">
      <div className="container max-w-2xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Add New Habit</h1>
          <p className="text-muted-foreground mt-1">Create a new habit to track daily</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Habit Details</CardTitle>
            <CardDescription>Enter the details of the habit you want to track</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-medium leading-none">
                  Habit Name*
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  placeholder="e.g., Read for 20 minutes"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  value={formData.name}
                  onChange={handleChange}
                />
                <p className="text-xs text-muted-foreground">A short, clear name for your habit</p>
              </div>

              <div className="space-y-2">
                <label htmlFor="description" className="text-sm font-medium leading-none">
                  Description (Optional)
                </label>
                <textarea
                  id="description"
                  name="description"
                  placeholder="Additional details about this habit"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 min-h-24 resize-y"
                  value={formData.description}
                  onChange={handleChange}
                />
                <p className="text-xs text-muted-foreground">
                  Provide any additional information about your habit
                </p>
              </div>

              <div className="flex gap-3 pt-2">
                <Button type="button" variant="outline" onClick={() => navigate('/dashboard')}>
                  Cancel
                </Button>
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? 'Creating...' : 'Create Habit'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
