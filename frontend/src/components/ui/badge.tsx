import * as React from "react";
import { cn } from "@/lib/utils";

function Badge({
  className,
  variant = "default",
  ...props
}: React.HTMLAttributes<HTMLDivElement> & {
  variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
}) {
  const variants = {
    default: "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]",
    secondary: "bg-[hsl(var(--secondary))] text-[hsl(var(--secondary-foreground))]",
    destructive: "bg-[hsl(var(--destructive))] text-[hsl(var(--destructive-foreground))]",
    outline: "border border-[hsl(var(--border))] text-[hsl(var(--foreground))]",
    success: "bg-green-500/10 text-green-600 dark:text-green-400 border border-green-500/20",
    warning: "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 border border-yellow-500/20",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}

export { Badge };
