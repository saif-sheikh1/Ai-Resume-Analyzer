import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FileText, Loader2, Copy, Upload, Sparkles, Check } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/lib/api";
import type { Resume } from "@/types";
import { toast } from "sonner";

export default function CoverLetterPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [position, setPosition] = useState("");
  const [tone, setTone] = useState("professional");
  const [loading, setLoading] = useState(false);
  const [fetchingResumes, setFetchingResumes] = useState(true);
  const [coverLetter, setCoverLetter] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.get<Resume[]>("/resumes/")
      .then(({ data }) => {
        setResumes(data);
        if (data.length > 0) {
          setSelectedResume(data[0].id);
        }
      })
      .catch((err) => {
        console.error("Failed to load resumes:", err);
      })
      .finally(() => {
        setFetchingResumes(false);
      });
  }, []);

  const handleGenerate = async () => {
    if (!selectedResume) {
      toast.error("Please select a resume first");
      return;
    }
    if (!jobDescription.trim() || !companyName.trim() || !position.trim()) {
      toast.error("Please fill in Position, Company Name, and Job Description");
      return;
    }

    setLoading(true);
    try {
      const { data } = await api.post("/job-match/cover-letter", {
        resume_id: selectedResume,
        job_description: jobDescription,
        company_name: companyName,
        position,
        tone,
      });
      setCoverLetter(data.cover_letter);
      toast.success("Cover letter generated successfully!");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Generation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(coverLetter);
    setCopied(true);
    toast.success("Copied to clipboard!");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Cover Letter Generator</h1>
        <p className="text-[hsl(var(--muted-foreground))]">Generate a tailored, professional AI cover letter in seconds.</p>
      </div>

      {!fetchingResumes && resumes.length === 0 && (
        <Card className="border-yellow-500/40 bg-yellow-500/5">
          <CardContent className="p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h3 className="font-semibold text-yellow-600 dark:text-yellow-400">No Resumes Found</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">Please upload your resume first to generate a personalized cover letter.</p>
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
              <Label htmlFor="toneSelect">Tone</Label>
              <select
                id="toneSelect"
                className="flex h-10 w-full rounded-lg border border-[hsl(var(--input))] bg-[hsl(var(--background))] px-3 py-2 text-sm"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              >
                <option value="professional">Professional & Formal</option>
                <option value="creative">Creative & Engaging</option>
                <option value="technical">Technical & Detail-Oriented</option>
              </select>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="position">Position / Job Title</Label>
              <Input
                id="position"
                placeholder="e.g. Senior Software Engineer"
                value={position}
                onChange={(e) => setPosition(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="companyName">Company Name</Label>
              <Input
                id="companyName"
                placeholder="e.g. Google"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="jobDesc">Job Description</Label>
            <Textarea
              id="jobDesc"
              placeholder="Paste the job description here..."
              rows={6}
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
                <Loader2 className="h-5 w-5 animate-spin" /> Generating Cover Letter...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" /> Generate Cover Letter
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {coverLetter && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-[hsl(var(--primary))]" /> Your AI Cover Letter
              </CardTitle>
              <Button variant="outline" size="sm" onClick={handleCopy} className="gap-2">
                {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
                {copied ? "Copied!" : "Copy to Clipboard"}
              </Button>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="whitespace-pre-wrap bg-[hsl(var(--accent))] rounded-lg p-6 text-sm leading-relaxed border border-[hsl(var(--border))] font-sans">
                {coverLetter}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
