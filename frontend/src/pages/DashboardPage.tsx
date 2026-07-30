import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FileText, TrendingUp, Award, Clock, Upload, BarChart3, Briefcase, ArrowRight } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import type { DashboardStats } from "@/types";
import { formatDate, getScoreColor, getScoreLabel } from "@/lib/utils";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const { data } = await api.get<DashboardStats>("/analysis/dashboard/stats");
        setStats(data);
      } catch (err) {
        console.error("Failed to fetch dashboard stats:", err);
        setStats({
          total_resumes: 0, total_analyses: 0,
          average_ats_score: 0, highest_ats_score: 0,
          recent_analyses: [], score_history: []
        });
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const statCards = [
    { icon: FileText, label: "Total Resumes", value: stats?.total_resumes || 0, color: "text-blue-500", bg: "bg-blue-500/10" },
    { icon: TrendingUp, label: "Avg ATS Score", value: stats?.average_ats_score ? `${stats.average_ats_score.toFixed(1)}` : "—", color: "text-green-500", bg: "bg-green-500/10" },
    { icon: Award, label: "Highest Score", value: stats?.highest_ats_score ? `${stats.highest_ats_score.toFixed(1)}` : "—", color: "text-purple-500", bg: "bg-purple-500/10" },
    { icon: Clock, label: "Total Analyses", value: stats?.total_analyses || 0, color: "text-orange-500", bg: "bg-orange-500/10" },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-[hsl(var(--muted-foreground))]">Welcome back! Here's an overview of your resume analytics.</p>
        </div>
        <Link to="/upload">
          <Button className="gap-2">
            <Upload className="h-4 w-4" /> Upload Resume
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <Card>
              <CardContent className="p-6">
                {loading ? (
                  <div className="space-y-3">
                    <Skeleton className="h-10 w-10 rounded-xl" />
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-8 w-16" />
                  </div>
                ) : (
                  <>
                    <div className={`h-10 w-10 rounded-xl ${stat.bg} flex items-center justify-center mb-3`}>
                      <stat.icon className={`h-5 w-5 ${stat.color}`} />
                    </div>
                    <p className="text-sm text-[hsl(var(--muted-foreground))]">{stat.label}</p>
                    <p className="text-2xl font-bold mt-1">{stat.value}</p>
                  </>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Score Trend */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-[hsl(var(--primary))]" />
              ATS Score Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-64 w-full" />
            ) : stats?.score_history && stats.score_history.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={stats.score_history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="date" tick={{ fontSize: 12 }} tickFormatter={(v) => new Date(v).toLocaleDateString("en", { month: "short", day: "numeric" })} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                  <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid hsl(var(--border))", background: "hsl(var(--card))" }} />
                  <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ fill: "hsl(var(--primary))", r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-[hsl(var(--muted-foreground))]">
                <p>No analysis data yet. Upload and analyze a resume to see trends.</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Section Scores */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-[hsl(var(--primary))]" />
              Latest Section Scores
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-64 w-full" />
            ) : stats?.recent_analyses?.[0] ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={Object.entries(stats.recent_analyses[0] || {}).filter(([k]) => !["id", "resume_id", "ats_score", "ai_summary", "created_at", "resume_filename"].includes(k)).map(([k, v]) => ({ name: k.replace(/_/g, " "), score: typeof v === "number" ? v : 0 }))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-25} textAnchor="end" height={60} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                  <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid hsl(var(--border))", background: "hsl(var(--card))" }} />
                  <Bar dataKey="score" fill="hsl(var(--secondary))" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-[hsl(var(--muted-foreground))]">
                <p>No analysis data yet.</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity & Quick Actions */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-4">{[1,2,3].map(i => <Skeleton key={i} className="h-16 w-full" />)}</div>
            ) : stats?.recent_analyses && stats.recent_analyses.length > 0 ? (
              <div className="space-y-3">
                {stats.recent_analyses.map((analysis) => (
                  <Link key={analysis.id} to={`/analysis/${analysis.id}`}>
                    <div className="flex items-center justify-between p-3 rounded-lg hover:bg-[hsl(var(--accent))] transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-lg bg-[hsl(var(--primary)/0.1)] flex items-center justify-center">
                          <FileText className="h-5 w-5 text-[hsl(var(--primary))]" />
                        </div>
                        <div>
                          <p className="font-medium text-sm">{analysis.resume_filename || "Resume"}</p>
                          <p className="text-xs text-[hsl(var(--muted-foreground))]">{formatDate(analysis.created_at)}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`font-bold ${getScoreColor(analysis.ats_score || 0)}`}>
                          {analysis.ats_score?.toFixed(0) || "—"}
                        </p>
                        <p className="text-xs text-[hsl(var(--muted-foreground))]">{getScoreLabel(analysis.ats_score || 0)}</p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-[hsl(var(--muted-foreground))] text-sm">No recent activity. Start by uploading a resume!</p>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/upload">
              <Button variant="outline" className="w-full justify-start gap-3 h-12">
                <Upload className="h-5 w-5 text-[hsl(var(--primary))]" />
                Upload Resume
                <ArrowRight className="h-4 w-4 ml-auto" />
              </Button>
            </Link>
            <Link to="/job-match">
              <Button variant="outline" className="w-full justify-start gap-3 h-12">
                <Briefcase className="h-5 w-5 text-purple-500" />
                Job Match
                <ArrowRight className="h-4 w-4 ml-auto" />
              </Button>
            </Link>
            <Link to="/history">
              <Button variant="outline" className="w-full justify-start gap-3 h-12">
                <BarChart3 className="h-5 w-5 text-green-500" />
                View History
                <ArrowRight className="h-4 w-4 ml-auto" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
