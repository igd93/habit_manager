import React from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Habit } from "@/services/habit";

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
          <span className="text-xs text-muted-foreground">
            Created {new Date(habit.created_at).toLocaleDateString()}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-grow">
        <p className="text-muted-foreground text-sm">
          {habit.description || "No description provided"}
        </p>
      </CardContent>
      <CardFooter className="pt-4 border-t flex justify-between items-center">
        <Button
          variant="default"
          onClick={onToggleCompletion}
          className="w-full"
        >
          Mark As Done
        </Button>
      </CardFooter>
    </Card>
  );
}
