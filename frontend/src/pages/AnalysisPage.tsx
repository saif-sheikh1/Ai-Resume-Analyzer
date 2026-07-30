import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { BarChart3, CheckCircle2, AlertTriangle, Lightbulb, Brain, Download, ArrowLeft, TrendingUp, Target, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import type { Analysis } from "@/types";
import { getScoreColor, getScoreLabel } from "@/lib/utils";

export default function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    const fetch = async () => {
      try {
        const { data } = await api.get<Analysis>(`/analysis/${id}`);
        setAnalysis(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, [id]);

  const handleDownloadPDF = async () => {
    if (!id) return;
    try {
      const response = await api.get(`/reports/${id}/pdf`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume_analysis_${id}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF download failed:", err);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-48 w-full" />
        <div className="grid md:grid-cols-2 gap-6">
          <Skeleton className="h-64 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    );
  }

  if (!analysis) {
    return <div className="text-center py-20">Analysis not found</div>;
  }

  const score = analysis.ats_score || 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/history">
            <Button variant="ghost" size="icon"><ArrowLeft className="h-5 w-5" /></Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Analysis Results</h1>
            <p className="text-[hsl(var(--muted-foreground))]">Comprehensive AI analysis of your resume</p>
          </div>
        </div>
        <Button onClick={handleDownloadPDF} variant="outline" className="gap-2">
          <Download className="h-4 w-4" /> Download PDF
        </Button>
      </div>

      {/* ATS Score */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardContent className="p-8 text-center">
            <div className="inline-flex flex-col items-center">
              <div className="relative h-32 w-32 mb-4">
                <svg className="h-32 w-32 -rotate-90" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="50" fill="none" stroke="hsl(var(--border))" strokeWidth="8" />
                  <circle cx="60" cy="60" r="50" fill="none" stroke={score >= 80 ? "#22c55e" : score >= 60 ? "#f59e0b" : "#ef4444"} strokeWidth="8" strokeDasharray={`${score * 3.14} 314`} strokeLinecap="round" className="transition-all duration-1000" />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className={`text-3xl font-bold ${getScoreColor(score)}`}>{score.toFixed(0)}</span>
                </div>
              </div>
              <h2 className="text-xl font-semibold">{getScoreLabel(score)}</h2>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">ATS Compatibility Score</p>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Section Scores */}
      {analysis.section_scores && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><BarChart3 className="h-5 w-5 text-[hsl(var(--primary))]" /> Section Scores</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {Object.entries(analysis.section_scores).map(([key, value]) => (
              <div key={key} className="space-y-1.5">
                <div className="flex justify-between text-sm">
                  <span className="capitalize font-medium">{key.replace(/_/g, " ")}</span>
                  <span className={getScoreColor(value as number)}>{(value as number).toFixed(0)}/100</span>
                </div>
                <Progress value={value as number} indicatorClassName={
                  (value as number) >= 80 ? "bg-green-500" : (value as number) >= 60 ? "bg-yellow-500" : "bg-red-500"
                } />
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* AI Summary */}
      {analysis.ai_summary && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Brain className="h-5 w-5 text-purple-500" /> AI Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">{analysis.ai_summary}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Strengths */}
        {analysis.strengths && analysis.strengths.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-green-500" /> Strengths</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {analysis.strengths.map((s, i) => (
                <div key={i} className="flex items-start gap-2 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>{s}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Weaknesses */}
        {analysis.weaknesses && analysis.weaknesses.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><AlertTriangle className="h-5 w-5 text-yellow-500" /> Areas to Improve</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {analysis.weaknesses.map((w, i) => (
                <div key={i} className="flex items-start gap-2 text-sm">
                  <AlertTriangle className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                  <span>{w}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </div>

      {/* Suggestions */}
      {analysis.suggestions && analysis.suggestions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Lightbulb className="h-5 w-5 text-yellow-500" /> Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {analysis.suggestions.map((s, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-[hsl(var(--accent))]">
                  <span className="text-xs font-bold text-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.1)] rounded-full h-6 w-6 flex items-center justify-center flex-shrink-0">{i + 1}</span>
                  <span className="text-sm">{s}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Missing Skills */}
      {analysis.missing_skills && analysis.missing_skills.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Target className="h-5 w-5 text-red-500" /> Missing Skills</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {analysis.missing_skills.map((s, i) => (
                <Badge key={i} variant="outline" className="text-sm">{s}</Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Improved Bullets */}
      {analysis.improved_bullets && analysis.improved_bullets.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Sparkles className="h-5 w-5 text-[hsl(var(--primary))]" /> Improved Bullet Points</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {analysis.improved_bullets.map((b, i) => (
              <div key={i} className="p-3 rounded-lg bg-[hsl(var(--accent))] text-sm">
                • {b}
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Career Advice */}
      {analysis.career_advice && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><TrendingUp className="h-5 w-5 text-green-500" /> Career Advice</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">{analysis.career_advice}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
