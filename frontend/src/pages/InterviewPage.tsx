import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { MessageSquare, Loader2, ChevronDown, ChevronUp, Upload, Sparkles, Lightbulb } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import api from "@/lib/api";
import type { Resume, InterviewPrepResponse, InterviewQuestion } from "@/types";
import { toast } from "sonner";

function QuestionCard({ q, index }: { q: InterviewQuestion; index: number }) {
  const [open, setOpen] = useState(index === 1); // Expand first item by default
  const difficultyVariant = q.difficulty === "Easy" ? "success" : q.difficulty === "Hard" ? "destructive" : "warning";

  return (
    <div className="border border-[hsl(var(--border))] rounded-xl overflow-hidden bg-[hsl(var(--card))] transition-shadow hover:shadow-sm">
      <button
        className="w-full p-4 text-left flex items-center justify-between hover:bg-[hsl(var(--accent)/0.5)] transition-colors cursor-pointer"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-3 pr-4">
          <span className="text-xs font-bold text-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.1)] rounded-full h-7 w-7 flex items-center justify-center flex-shrink-0">
            {index}
          </span>
          <span className="font-semibold text-sm sm:text-base">{q.question}</span>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <Badge variant={difficultyVariant}>{q.difficulty}</Badge>
          {open ? <ChevronUp className="h-4 w-4 text-[hsl(var(--muted-foreground))]" /> : <ChevronDown className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />}
        </div>
      </button>

      {open && (
        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} transition={{ duration: 0.2 }} className="px-4 pb-4">
          <div className="p-4 rounded-lg bg-[hsl(var(--accent))] border border-[hsl(var(--border)/0.5)] text-sm leading-relaxed space-y-1">
            <p className="text-xs font-bold uppercase tracking-wider text-[hsl(var(--primary))] mb-1">Recommended Sample Answer:</p>
            <p className="text-[hsl(var(--foreground))] whitespace-pre-wrap">{q.sample_answer}</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default function InterviewPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetchingResumes, setFetchingResumes] = useState(true);
  const [result, setResult] = useState<InterviewPrepResponse | null>(null);

  useEffect(() => {
    api.get<Resume[]>("/resumes/")
      .then(({ data }) => {
        setResumes(data);
        if (data.length > 0) setSelectedResume(data[0].id);
      })
      .catch((err) => {
        console.error("Failed to fetch resumes:", err);
      })
      .finally(() => setFetchingResumes(false));
  }, []);

  const handleGenerate = async () => {
    if (!selectedResume) {
      toast.error("Please select a resume");
      return;
    }

    setLoading(true);
    try {
      const { data } = await api.post<InterviewPrepResponse>("/job-match/interview-prep", {
        resume_id: selectedResume,
        job_description: jobDescription.trim() || null,
        job_title: jobTitle.trim() || null,
      });
      setResult(data);
      toast.success("Interview prep generated successfully!");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Generation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const categories = result ? [
    { title: "HR & General Questions", icon: "💼", questions: result.hr_questions || [] },
    { title: "Technical Questions", icon: "⚙️", questions: result.technical_questions || [] },
    { title: "Behavioral Questions (STAR Method)", icon: "🧠", questions: result.behavioral_questions || [] },
    { title: "Coding & Problem Solving", icon: "💻", questions: result.coding_questions || [] },
  ] : [];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Interview Preparation</h1>
        <p className="text-[hsl(var(--muted-foreground))]">Generate customized interview questions and expert answers based on your background.</p>
      </div>

      {!fetchingResumes && resumes.length === 0 && (
        <Card className="border-yellow-500/40 bg-yellow-500/5">
          <CardContent className="p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h3 className="font-semibold text-yellow-600 dark:text-yellow-400">No Resumes Found</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">Please upload your resume first to generate personalized interview questions.</p>
            </div>
            <Link to="/upload">
              <Button className="gap-2">
                <Upload className="h-4 w-4" /> Upload Resume
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="p-6 space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="resumeSelect">Select Resume</Label>
              <select
                id="resumeSelect"
                className="flex h-10 w-full rounded-lg border border-[hsl(var(--input))] bg-[hsl(var(--background))] px-3 py-2 text-sm"
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
                disabled={resumes.length === 0}
              >
                {resumes.length === 0 ? (
                  <option value="">No resumes available</option>
                ) : (
                  resumes.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.filename}
                    </option>
                  ))
                )}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="jobTitle">Target Job Title (optional)</Label>
              <Input
                id="jobTitle"
                placeholder="e.g. Senior Software Engineer"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="jdText">Job Description (optional - for targeted questions)</Label>
            <Textarea
              id="jdText"
              placeholder="Paste job description to tailor interview questions specifically to the role requirements..."
              rows={4}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <Button
            onClick={handleGenerate}
            disabled={loading || resumes.length === 0}
            className="w-full gap-2 text-base h-11"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" /> Generating Questions & Answers...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" /> Generate Interview Prep Q&A
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          {categories.map(
            (cat) =>
              cat.questions.length > 0 && (
                <Card key={cat.title}>
                  <CardHeader>
                    <CardTitle className="text-xl flex items-center gap-2">
                      <span>{cat.icon}</span> {cat.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {cat.questions.map((q, i) => (
                      <QuestionCard key={i} q={q} index={i + 1} />
                    ))}
                  </CardContent>
                </Card>
              )
          )}

          {result.improvement_suggestions && result.improvement_suggestions.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" /> Interview Strategy & Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {result.improvement_suggestions.map((s, i) => (
                  <div key={i} className="p-3.5 rounded-lg bg-[hsl(var(--accent))] text-sm flex items-start gap-3">
                    <span className="font-bold text-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.1)] rounded-full h-5 w-5 flex items-center justify-center text-xs flex-shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span>{s}</span>
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
