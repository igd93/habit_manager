import React from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Habit type definition
interface Habit {
  id: number;
  name: string;
  description: string;
  created_at: string;
  completed_today: boolean;
}

interface HabitCardProps {
  habit: Habit;
  onToggleCompletion: () => void;
}

export default function HabitCard({
  habit,
  onToggleCompletion,
}: HabitCardProps) {
  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-start justify-between gap-2">
          <span className="truncate">{habit.name}</span>
          {habit.completed_today && (
            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full flex-shrink-0">
              Completed
            </span>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-grow">
        <p className="text-muted-foreground text-sm">
          {habit.description || "No description provided"}
        </p>
      </CardContent>
      <CardFooter className="pt-4 border-t flex justify-between items-center">
        <Button
          variant={habit.completed_today ? "outline" : "default"}
          onClick={onToggleCompletion}
          className="w-full"
        >
          {habit.completed_today ? "Undo Completion" : "Mark As Done"}
        </Button>
      </CardFooter>
    </Card>
  );
}
