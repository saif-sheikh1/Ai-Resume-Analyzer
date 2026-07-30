import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Briefcase, Loader2, Target, CheckCircle2, XCircle, TrendingUp, Lightbulb } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import api from "@/lib/api";
import type { Resume, JobMatch } from "@/types";
import { toast } from "sonner";
import { getScoreColor } from "@/lib/utils";

export default function JobMatchPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResume, setSelectedResume] = useState<string>("");
  const [jobDescription, setJobDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<JobMatch | null>(null);

  useEffect(() => {
    api.get<Resume[]>("/resumes/").then(({ data }) => {
      setResumes(data);
      if (data.length > 0) setSelectedResume(data[0].id);
    });
  }, []);

  const handleMatch = async () => {
    if (!selectedResume || jobDescription.length < 50) {
      toast.error("Please select a resume and enter a job description (at least 50 characters)");
      return;
    }
    setLoading(true);
    try {
      const { data } = await api.post<JobMatch>("/job-match/", {
        resume_id: selectedResume,
        job_description: jobDescription,
        job_title: jobTitle || null,
        company_name: companyName || null,
      });
      setResult(data);
      toast.success("Job match analysis complete!");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Match analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Job Match</h1>
        <p className="text-[hsl(var(--muted-foreground))]">Compare your resume against a job description to see how well you match.</p>
      </div>

      {/* Input Form */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Select Resume</Label>
              <select
                className="flex h-10 w-full rounded-lg border border-[hsl(var(--input))] bg-[hsl(var(--background))] px-3 py-2 text-sm"
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
              >
                {resumes.map((r) => (
                  <option key={r.id} value={r.id}>{r.filename}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-2">
                <Label>Job Title (optional)</Label>
                <Input placeholder="Software Engineer" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label>Company (optional)</Label>
                <Input placeholder="Google" value={companyName} onChange={(e) => setCompanyName(e.target.value)} />
              </div>
            </div>
          </div>
          <div className="space-y-2">
            <Label>Job Description</Label>
            <Textarea placeholder="Paste the full job description here..." rows={8} value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} />
          </div>
          <Button onClick={handleMatch} disabled={loading || !selectedResume} className="w-full gap-2">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Briefcase className="h-4 w-4" />}
            Analyze Match
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          {/* Match Score */}
          <Card>
            <CardContent className="p-8 text-center">
              <div className="inline-flex flex-col items-center">
                <div className="relative h-32 w-32 mb-4">
                  <svg className="h-32 w-32 -rotate-90" viewBox="0 0 120 120">
                    <circle cx="60" cy="60" r="50" fill="none" stroke="hsl(var(--border))" strokeWidth="8" />
                    <circle cx="60" cy="60" r="50" fill="none" stroke={(result.match_percentage || 0) >= 80 ? "#22c55e" : (result.match_percentage || 0) >= 60 ? "#f59e0b" : "#ef4444"} strokeWidth="8" strokeDasharray={`${(result.match_percentage || 0) * 3.14} 314`} strokeLinecap="round" />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className={`text-3xl font-bold ${getScoreColor(result.match_percentage || 0)}`}>{result.match_percentage?.toFixed(0)}%</span>
                  </div>
                </div>
                <h2 className="text-xl font-semibold">Match Score</h2>
                <Badge variant={result.hiring_probability === "High" ? "success" : result.hiring_probability === "Medium" ? "warning" : "destructive"} className="mt-2">
                  {result.hiring_probability} Hiring Probability
                </Badge>
              </div>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Matching Skills */}
            {result.matching_skills && result.matching_skills.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-green-500" /> Matching Skills</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.matching_skills.map((s, i) => (
                      <Badge key={i} variant="success">{s}</Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Missing Skills */}
            {result.missing_skills && result.missing_skills.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><XCircle className="h-5 w-5 text-red-500" /> Missing Skills</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.missing_skills.map((s, i) => (
                      <Badge key={i} variant="destructive">{s}</Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Recommendations */}
          {result.recommendations && result.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Lightbulb className="h-5 w-5 text-yellow-500" /> Recommendations</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {result.recommendations.map((r, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-[hsl(var(--accent))]">
                    <span className="text-xs font-bold text-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.1)] rounded-full h-6 w-6 flex items-center justify-center flex-shrink-0">{i + 1}</span>
                    <span className="text-sm">{r}</span>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </motion.div>
      )}
    </div>
  );
}
