import React from 'react';

interface CompletionStatProps {
  completedCount: number;
  totalCount: number;
}

export default function CompletionStat({ completedCount, totalCount }: CompletionStatProps) {
  // Calculate percentage (safe division to avoid NaN)
  const percentage = totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100);

  // Determine color based on completion percentage
  const getColorClass = () => {
    if (percentage >= 75) return 'bg-green-500';
    if (percentage >= 50) return 'bg-blue-500';
    if (percentage >= 25) return 'bg-yellow-500';
    return 'bg-gray-500';
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium">
          {completedCount} of {totalCount} habits completed
        </span>
        <span className="text-sm font-medium">{percentage}%</span>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full ${getColorClass()}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      {/* Additional stats or messages */}
      <div className="pt-2 text-sm text-muted-foreground">
        {totalCount === 0 ? (
          <p>Add some habits to start tracking your progress!</p>
        ) : completedCount === totalCount ? (
          <p>Congratulations! You've completed all your habits today! 🎉</p>
        ) : completedCount === 0 ? (
          <p>You haven't completed any habits yet today. Let's get started!</p>
        ) : (
          <p>Keep going! You're making progress on your habits.</p>
        )}
      </div>
    </div>
  );
}
